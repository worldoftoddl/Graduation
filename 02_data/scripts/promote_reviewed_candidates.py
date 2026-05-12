#!/usr/bin/env python3
"""Promote reviewed public ATS candidates into the final job sample CSV."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SAMPLE_COLUMNS = [
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


def repo_path(value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return REPO_ROOT / path


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as file:
        return [dict(row) for row in csv.DictReader(file)]


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=SAMPLE_COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def promote(rows: list[dict[str, str]], include_hold: bool) -> list[dict[str, str]]:
    allowed = {"include"}
    if include_hold:
        allowed.add("hold")

    promoted: list[dict[str, str]] = []
    next_id = 1
    for row in rows:
        if row.get("review_decision") not in allowed:
            continue
        sample = {column: row.get(column, "") for column in SAMPLE_COLUMNS}
        sample["sample_id"] = f"JOB-{next_id:03d}"
        sample["manual_reviewed"] = "auto_reviewed" if row.get("review_decision") == "include" else "hold"
        sample["notes"] = sample.get("notes", "").replace("requires_manual_review", "auto_reviewed_include")
        review_note = (
            f"review_decision={row.get('review_decision')}; "
            f"review_reason={row.get('review_reason')}; "
            f"dedupe_key={row.get('dedupe_key')}"
        )
        sample["notes"] = "; ".join(part for part in [sample.get("notes", ""), review_note] if part)
        promoted.append(sample)
        next_id += 1
    return promoted


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Promote reviewed candidates to final sample CSV.")
    parser.add_argument("--input", default="02_data/processed/public_ats_reviewed_candidates.csv")
    parser.add_argument("--output", default="02_data/raw/job_posting_sample.csv")
    parser.add_argument("--include-hold", action="store_true", help="Also promote hold rows as manual_reviewed=hold.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    reviewed = read_rows(repo_path(args.input))
    promoted = promote(reviewed, args.include_hold)
    write_rows(repo_path(args.output), promoted)
    print(f"input_rows: {len(reviewed)}")
    print(f"promoted_rows: {len(promoted)}")
    print(f"wrote: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
