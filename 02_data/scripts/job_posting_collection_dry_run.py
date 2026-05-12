#!/usr/bin/env python3
"""Prepare a gated job-posting collection dry run.

This script intentionally does not fetch web pages. It checks a target-list CSV
before any crawler runs, keeps network access off by default, and emits CSV rows
compatible with the project's source-log, sample, and manual-review schemas.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[2]

TARGET_HEADER = [
    "target_id",
    "platform",
    "source_name",
    "url",
    "search_keyword",
    "period_covered",
    "collection_method",
    "robots_url",
    "terms_url",
    "robots_terms_checked",
    "allowed_basis",
    "requires_login",
    "has_captcha",
    "has_paywall",
    "request_interval_seconds",
    "crawler_user_agent",
    "source_log_id",
    "limitations",
    "notes",
]

SAMPLE_HEADER = [
    "sample_id",
    "collected_at",
    "posting_date",
    "collection_method",
    "robots_terms_checked",
    "source_log_id",
    "search_keyword",
    "platform",
    "company",
    "industry",
    "job_title",
    "normalized_role",
    "experience_level",
    "min_experience_years",
    "education_level",
    "employment_type",
    "required_skills",
    "skill_tags",
    "domain_requirement",
    "compensation",
    "location",
    "url",
    "raw_file",
    "manual_reviewed",
    "notes",
]

SOURCE_LOG_HEADER = [
    "source_log_id",
    "dataset_file",
    "source_name",
    "source_table_or_page",
    "query_condition",
    "period_covered",
    "download_or_access_date",
    "collection_method",
    "robots_terms_checked",
    "request_interval_seconds",
    "crawler_user_agent",
    "url",
    "limitations",
    "notes",
]

REVIEW_HEADER = [
    "candidate_id",
    "sample_id",
    "source_log_id",
    "reviewed_at",
    "reviewer",
    "include_decision",
    "exclude_reason",
    "duplicate_of",
    "company",
    "job_title",
    "normalized_role",
    "experience_level",
    "required_skills",
    "skill_tags",
    "domain_requirement",
    "url",
    "raw_file",
    "review_notes",
]


@dataclass(frozen=True)
class GateResult:
    ok: bool
    reasons: list[str]


def repo_path(value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return REPO_ROOT / path


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        header = reader.fieldnames or []
        rows = [{key: (value or "").strip() for key, value in row.items()} for row in reader]
    return header, rows


def read_header(path: Path) -> list[str]:
    with path.open(newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        return next(reader, [])


def require_columns(actual: Iterable[str], expected: Iterable[str], label: str) -> None:
    missing = [column for column in expected if column not in set(actual)]
    if missing:
        raise SystemExit(f"{label} is missing required columns: {', '.join(missing)}")


def is_yes(value: str) -> bool:
    return value.strip().lower() in {"yes", "y", "true", "1", "checked"}


def is_no_or_blank(value: str) -> bool:
    return value.strip().lower() in {"", "no", "n", "false", "0"}


def parse_interval(value: str) -> float | None:
    if not value.strip():
        return None
    try:
        return float(value)
    except ValueError:
        return None


def gate_target(row: dict[str, str], min_interval: float) -> GateResult:
    reasons: list[str] = []
    method = row.get("collection_method", "").lower()

    if method != "auto":
        reasons.append("collection_method is not auto")
    if not row.get("target_id"):
        reasons.append("target_id is blank")
    if not row.get("url"):
        reasons.append("url is blank")
    if not row.get("source_log_id"):
        reasons.append("source_log_id is blank")
    if not row.get("allowed_basis"):
        reasons.append("allowed_basis is blank")
    if not is_yes(row.get("robots_terms_checked", "")):
        reasons.append("robots_terms_checked is not yes")
    if not is_no_or_blank(row.get("requires_login", "")):
        reasons.append("requires_login is not no")
    if not is_no_or_blank(row.get("has_captcha", "")):
        reasons.append("has_captcha is not no")
    if not is_no_or_blank(row.get("has_paywall", "")):
        reasons.append("has_paywall is not no")

    interval = parse_interval(row.get("request_interval_seconds", ""))
    if interval is None:
        reasons.append("request_interval_seconds is blank or invalid")
    elif interval < min_interval:
        reasons.append(f"request_interval_seconds is below {min_interval:g}")

    if not row.get("crawler_user_agent"):
        reasons.append("crawler_user_agent is blank")

    return GateResult(ok=not reasons, reasons=reasons)


def make_source_log_row(row: dict[str, str], today: str) -> dict[str, str]:
    return {
        "source_log_id": row.get("source_log_id", ""),
        "dataset_file": "02_data/raw/job_posting_sample.csv",
        "source_name": row.get("source_name") or row.get("platform", ""),
        "source_table_or_page": row.get("source_name", ""),
        "query_condition": row.get("search_keyword", ""),
        "period_covered": row.get("period_covered", ""),
        "download_or_access_date": today,
        "collection_method": "auto",
        "robots_terms_checked": row.get("robots_terms_checked", ""),
        "request_interval_seconds": row.get("request_interval_seconds", ""),
        "crawler_user_agent": row.get("crawler_user_agent", ""),
        "url": row.get("url", ""),
        "limitations": row.get("limitations", ""),
        "notes": row.get("notes", ""),
    }


def make_sample_row(row: dict[str, str], today: str) -> dict[str, str]:
    values = {column: "" for column in SAMPLE_HEADER}
    values.update(
        {
            "collected_at": today,
            "collection_method": "auto",
            "robots_terms_checked": row.get("robots_terms_checked", ""),
            "source_log_id": row.get("source_log_id", ""),
            "search_keyword": row.get("search_keyword", ""),
            "platform": row.get("platform", ""),
            "url": row.get("url", ""),
            "manual_reviewed": "no",
            "notes": "dry-run placeholder; assign sample_id only after manual review",
        }
    )
    return values


def make_review_row(row: dict[str, str], index: int) -> dict[str, str]:
    values = {column: "" for column in REVIEW_HEADER}
    values.update(
        {
            "candidate_id": f"CAND-{index:03d}",
            "source_log_id": row.get("source_log_id", ""),
            "include_decision": "hold",
            "url": row.get("url", ""),
            "review_notes": f"dry-run candidate from {row.get('target_id', '')}",
        }
    )
    return values


def write_csv(path: Path, header: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=header, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Validate job-posting collection targets and prepare dry-run CSV rows. "
            "No network requests are made."
        )
    )
    parser.add_argument(
        "--targets",
        default="02_data/job_posting_collection_targets_template.csv",
        help="Target-list CSV path.",
    )
    parser.add_argument(
        "--sample-template",
        default="02_data/job_posting_sample_template.csv",
        help="Existing sample CSV header to validate against.",
    )
    parser.add_argument(
        "--source-log",
        default="02_data/source_log.csv",
        help="Existing source-log CSV header to validate against.",
    )
    parser.add_argument(
        "--review-template",
        default="02_data/job_posting_manual_review_template.csv",
        help="Existing manual-review CSV header to validate against.",
    )
    parser.add_argument(
        "--sample-out",
        default="02_data/job_posting_sample.dry_run.csv",
        help="Dry-run sample-compatible output path.",
    )
    parser.add_argument(
        "--source-log-out",
        default="02_data/source_log.dry_run.csv",
        help="Dry-run source-log-compatible output path.",
    )
    parser.add_argument(
        "--review-out",
        default="02_data/job_posting_manual_review.dry_run.csv",
        help="Dry-run manual-review output path.",
    )
    parser.add_argument(
        "--min-interval",
        type=float,
        default=5.0,
        help="Minimum allowed request interval in seconds for auto collection.",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write dry-run output CSV files. Without this flag, only report results.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    targets_path = repo_path(args.targets)
    target_header, targets = read_csv_rows(targets_path)
    require_columns(target_header, TARGET_HEADER, str(targets_path))

    sample_header = read_header(repo_path(args.sample_template))
    source_log_header = read_header(repo_path(args.source_log))
    review_header = read_header(repo_path(args.review_template))
    if sample_header != SAMPLE_HEADER:
        raise SystemExit("sample template header is not compatible with expected schema")
    if source_log_header != SOURCE_LOG_HEADER:
        raise SystemExit("source log header is not compatible with expected schema")
    if review_header != REVIEW_HEADER:
        raise SystemExit("manual review template header is not compatible with expected schema")

    today = date.today().isoformat()
    eligible: list[dict[str, str]] = []
    skipped: list[tuple[str, list[str]]] = []
    for row in targets:
        result = gate_target(row, args.min_interval)
        if result.ok:
            eligible.append(row)
        else:
            skipped.append((row.get("target_id") or "(blank target_id)", result.reasons))

    source_rows = [make_source_log_row(row, today) for row in eligible]
    sample_rows = [make_sample_row(row, today) for row in eligible]
    review_rows = [make_review_row(row, index + 1) for index, row in enumerate(eligible)]

    print(f"targets: {targets_path.relative_to(REPO_ROOT)}")
    print(f"total_rows: {len(targets)}")
    print(f"eligible_rows: {len(eligible)}")
    print(f"skipped_rows: {len(skipped)}")
    for target_id, reasons in skipped:
        print(f"- skipped {target_id}: {'; '.join(reasons)}")

    if args.write:
        write_csv(repo_path(args.source_log_out), SOURCE_LOG_HEADER, source_rows)
        write_csv(repo_path(args.sample_out), SAMPLE_HEADER, sample_rows)
        write_csv(repo_path(args.review_out), REVIEW_HEADER, review_rows)
        print(f"wrote: {repo_path(args.source_log_out).relative_to(REPO_ROOT)}")
        print(f"wrote: {repo_path(args.sample_out).relative_to(REPO_ROOT)}")
        print(f"wrote: {repo_path(args.review_out).relative_to(REPO_ROOT)}")
    else:
        print("dry_run_only: pass --write to create output CSV files")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
