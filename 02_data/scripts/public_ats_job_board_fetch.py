#!/usr/bin/env python3
"""Collect public ATS job board postings into review-ready CSV files.

Supported providers:
- Ashby public Job Postings API
- Lever public Postings API
- Greenhouse public Job Board API

The script performs GET requests only against documented public job-board
endpoints. It never submits applications, follows private APIs, or uses cookies.
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import re
import time
import urllib.request
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Iterable


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_USER_AGENT = "GraduationResearchBot/0.1"
MIN_INTERVAL_SECONDS = 5.0

STRONG_TITLE_TERMS = (
    "ai engineer",
    "applied ai",
    "machine learning",
    "ml engineer",
    "ml software",
    "data scientist",
    "ai scientist",
    "research scientist",
    "ai research",
    "deep learning",
    "computer vision",
    "nlp",
    "llm",
    "rag",
    "mlops",
    "modeling",
    "inference",
    "recommendation",
    "recommender",
    "npu",
    "gpu",
    "quantization",
    "인공지능",
    "머신러닝",
    "딥러닝",
    "데이터 사이언티스트",
    "자연어",
    "추천",
    "생성형",
)

TECHNICAL_ROLE_TERMS = (
    "engineer",
    "scientist",
    "research",
    "developer",
    "architect",
    "software",
    "data",
    "platform",
    "solution architect",
    "solutions architect",
    "엔지니어",
    "개발",
    "연구",
    "아키텍트",
)

AI_EVIDENCE_TERMS = (
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "ai model",
    "ai platform",
    "advancements in ai",
    "cutting-edge ai",
    "ml model",
    "model training",
    "model serving",
    "inference",
    "llm",
    "large language",
    "rag",
    "retrieval",
    "vector database",
    "pytorch",
    "tensorflow",
    "scikit",
    "mlflow",
    "kubeflow",
    "computer vision",
    "natural language",
    "nlp",
    "recommendation",
    "recommender",
    "quantization",
    "npu",
    "gpu",
    "ai agent",
    "생성형",
    "머신러닝",
    "딥러닝",
    "자연어",
    "추천",
)

NON_TECH_TITLE_TERMS = (
    "sales",
    "account executive",
    "business development",
    "marketing",
    "revenue",
    "recruit",
    "people",
    "hr",
    "finance",
    "legal",
    "designer",
    "assistant",
    "strategist",
    "deployment strategist",
    "customer success",
    "operations",
    "office",
    "영업",
    "마케팅",
    "디자이너",
    "채용",
    "인사",
)

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

TARGET_HEADER = [
    "target_id",
    "provider",
    "board_token",
    "company",
    "job_board_url",
    "api_url",
    "keywords",
    "location_terms",
    "source_log_id",
    "robots_terms_checked",
    "allowed_basis",
    "request_interval_seconds",
    "crawler_user_agent",
    "limitations",
    "notes",
]


@dataclass(frozen=True)
class Target:
    target_id: str
    provider: str
    board_token: str
    company: str
    job_board_url: str
    api_url: str
    keywords: list[str]
    location_terms: list[str]
    source_log_id: str
    robots_terms_checked: str
    allowed_basis: str
    request_interval_seconds: float
    crawler_user_agent: str
    limitations: str
    notes: str


@dataclass(frozen=True)
class Posting:
    provider: str
    target_id: str
    source_log_id: str
    company: str
    title: str
    location: str
    department: str
    employment_type: str
    published_at: str
    url: str
    description: str
    compensation: str
    raw_id: str


def repo_path(value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return REPO_ROOT / path


def split_terms(value: str) -> list[str]:
    return [term.strip() for term in value.split(";") if term.strip()]


def strip_html(value: str) -> str:
    text = re.sub(r"<br\s*/?>", "\n", value or "", flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def read_targets(path: Path) -> list[Target]:
    with path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        missing = [column for column in TARGET_HEADER if column not in (reader.fieldnames or [])]
        if missing:
            raise SystemExit(f"{path} is missing columns: {', '.join(missing)}")
        targets = []
        for row in reader:
            if row["robots_terms_checked"].strip().lower() != "yes":
                continue
            try:
                interval = float(row["request_interval_seconds"])
            except ValueError as exc:
                raise SystemExit(f"invalid request interval for {row['target_id']}") from exc
            if interval < MIN_INTERVAL_SECONDS:
                raise SystemExit(f"{row['target_id']} request interval below {MIN_INTERVAL_SECONDS:g}s")
            targets.append(
                Target(
                    target_id=row["target_id"].strip(),
                    provider=row["provider"].strip().lower(),
                    board_token=row["board_token"].strip(),
                    company=row["company"].strip(),
                    job_board_url=row["job_board_url"].strip(),
                    api_url=row["api_url"].strip(),
                    keywords=split_terms(row["keywords"]),
                    location_terms=split_terms(row["location_terms"]),
                    source_log_id=row["source_log_id"].strip(),
                    robots_terms_checked=row["robots_terms_checked"].strip(),
                    allowed_basis=row["allowed_basis"].strip(),
                    request_interval_seconds=interval,
                    crawler_user_agent=row["crawler_user_agent"].strip() or DEFAULT_USER_AGENT,
                    limitations=row["limitations"].strip(),
                    notes=row["notes"].strip(),
                )
            )
    return targets


def fetch_json(url: str, user_agent: str, timeout: float) -> Any:
    request = urllib.request.Request(url, headers={"User-Agent": user_agent, "Accept": "application/json"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return json.loads(response.read().decode(charset, errors="replace"))


def ashby_postings(target: Target, payload: dict[str, Any]) -> list[Posting]:
    postings = []
    for job in payload.get("jobs", []):
        if job.get("isListed") is False:
            continue
        description = job.get("descriptionPlain") or strip_html(job.get("descriptionHtml", ""))
        compensation = ""
        comp = job.get("compensation") or {}
        if isinstance(comp, dict):
            compensation = comp.get("scrapeableCompensationSalarySummary") or comp.get("compensationTierSummary") or ""
        postings.append(
            Posting(
                provider="ashby",
                target_id=target.target_id,
                source_log_id=target.source_log_id,
                company=target.company,
                title=str(job.get("title", "")),
                location=str(job.get("location", "")),
                department=str(job.get("department") or job.get("team") or ""),
                employment_type=str(job.get("employmentType", "")),
                published_at=str(job.get("publishedAt", ""))[:10],
                url=str(job.get("jobUrl") or job.get("applyUrl") or target.job_board_url),
                description=description,
                compensation=compensation,
                raw_id=str(job.get("id") or job.get("externalLink") or ""),
            )
        )
    return postings


def lever_postings(target: Target, payload: list[dict[str, Any]]) -> list[Posting]:
    postings = []
    for job in payload:
        categories = job.get("categories") or {}
        all_locations = categories.get("allLocations") or []
        location_parts = [str(categories.get("location", ""))]
        if isinstance(all_locations, list):
            location_parts.extend(str(location) for location in all_locations)
        lists = job.get("lists") or []
        description_parts = [job.get("descriptionPlain") or strip_html(job.get("description", ""))]
        for section in lists:
            description_parts.append(strip_html(section.get("text", "")))
            for content in section.get("content", []) or []:
                description_parts.append(strip_html(content))
        postings.append(
            Posting(
                provider="lever",
                target_id=target.target_id,
                source_log_id=target.source_log_id,
                company=target.company,
                title=str(job.get("text", "")),
                location="; ".join(dict.fromkeys(part for part in location_parts if part)),
                department=str(categories.get("team") or categories.get("department") or ""),
                employment_type=str(categories.get("commitment", "")),
                published_at="",
                url=str(job.get("hostedUrl") or job.get("applyUrl") or target.job_board_url),
                description=" ".join(part for part in description_parts if part),
                compensation="",
                raw_id=str(job.get("id", "")),
            )
        )
    return postings


def greenhouse_postings(target: Target, payload: dict[str, Any]) -> list[Posting]:
    postings = []
    for job in payload.get("jobs", []):
        offices = ", ".join(office.get("name", "") for office in job.get("offices", []) if office.get("name"))
        departments = ", ".join(dept.get("name", "") for dept in job.get("departments", []) if dept.get("name"))
        postings.append(
            Posting(
                provider="greenhouse",
                target_id=target.target_id,
                source_log_id=target.source_log_id,
                company=target.company,
                title=str(job.get("title", "")),
                location=str(job.get("location", {}).get("name") or offices),
                department=departments,
                employment_type="",
                published_at=str(job.get("updated_at", ""))[:10],
                url=str(job.get("absolute_url") or target.job_board_url),
                description=strip_html(job.get("content", "")),
                compensation="",
                raw_id=str(job.get("id", "")),
            )
        )
    return postings


def parse_payload(target: Target, payload: Any) -> list[Posting]:
    if target.provider == "ashby":
        if not isinstance(payload, dict):
            raise SystemExit(f"{target.target_id} Ashby response is not an object")
        return ashby_postings(target, payload)
    if target.provider == "lever":
        if not isinstance(payload, list):
            raise SystemExit(f"{target.target_id} Lever response is not a list")
        return lever_postings(target, payload)
    if target.provider == "greenhouse":
        if not isinstance(payload, dict):
            raise SystemExit(f"{target.target_id} Greenhouse response is not an object")
        return greenhouse_postings(target, payload)
    raise SystemExit(f"unsupported provider: {target.provider}")


def matches_terms(posting: Posting, keywords: list[str], location_terms: list[str]) -> tuple[bool, str]:
    title_dept = " ".join([posting.title, posting.department]).lower()
    description = posting.description.lower()
    haystack = " ".join([title_dept, description])
    location = posting.location.lower()
    matched_keywords = [term for term in keywords if term.lower() in haystack]
    matched_locations = [term for term in location_terms if term.lower() in location]
    if location_terms and not matched_locations:
        return False, "no_location_match"

    strong_title = [term for term in STRONG_TITLE_TERMS if term in title_dept]
    technical_role = [term for term in TECHNICAL_ROLE_TERMS if term in title_dept]
    ai_evidence = [term for term in AI_EVIDENCE_TERMS if term in description or term in title_dept]
    non_tech = [term for term in NON_TECH_TITLE_TERMS if term in title_dept]

    if non_tech and not strong_title:
        return False, f"non_tech_title={';'.join(non_tech)}"
    if strong_title:
        return True, (
            f"strong_title={';'.join(strong_title)} "
            f"keywords={';'.join(matched_keywords)} locations={';'.join(matched_locations)}"
        )
    if technical_role and len(ai_evidence) >= 2:
        return True, (
            f"technical_role={';'.join(technical_role)} "
            f"ai_evidence={';'.join(ai_evidence[:5])} "
            f"locations={';'.join(matched_locations)}"
        )
    return False, "weak_ai_job_evidence"


def normalize_role(posting: Posting) -> str:
    text = " ".join([posting.title, posting.department, posting.description[:1000]]).lower()
    if any(term in text for term in ("mlops", "platform engineer", "infrastructure", "인프라")):
        return "mlops_platform_engineer"
    if any(term in text for term in ("llm", "rag", "agent", "generative", "생성형", "에이전트", "챗봇")):
        return "applied_ai_developer"
    if any(term in text for term in ("research scientist", "researcher", "ai scientist", "리서처", "연구")):
        return "ai_researcher"
    if any(term in text for term in ("deep learning", "computer vision", "nlp", "딥러닝", "비전", "자연어")):
        return "ai_deep_learning_engineer"
    if any(term in text for term in ("machine learning", "ml engineer", "머신러닝")):
        return "ml_engineer"
    if any(term in text for term in ("data scientist", "데이터 사이언티스트")):
        return "data_scientist"
    if any(term in text for term in ("prompt", "프롬프트", "operator", "오퍼레이터")):
        return "prompt_ai_operator"
    if any(term in text for term in ("ai", "artificial intelligence", "인공지능")):
        return "applied_ai_developer"
    return ""


def skill_tags(posting: Posting) -> str:
    text = " ".join([posting.title, posting.description]).lower()
    tags = []
    checks = {
        "python": ("python", "파이썬"),
        "pytorch": ("pytorch",),
        "tensorflow": ("tensorflow",),
        "sql": ("sql",),
        "cloud": ("aws", "gcp", "azure", "cloud", "kubernetes"),
        "docker_k8s": ("docker", "kubernetes", "k8s"),
        "llm": ("llm", "large language", "gpt", "claude", "생성형"),
        "rag": ("rag", "retrieval", "vector database", "vector db"),
        "nlp": ("nlp", "natural language", "자연어"),
        "cv": ("computer vision", "vision", "비전"),
        "recommender": ("recommendation", "recommender", "추천"),
        "mlops": ("mlops", "mlflow", "kubeflow", "model serving"),
    }
    for tag, terms in checks.items():
        if any(term in text for term in terms):
            tags.append(tag)
    return ";".join(tags)


def sample_row(posting: Posting, collected_at: str, raw_file: str, match_note: str) -> dict[str, str]:
    return {
        "sample_id": "",
        "collected_at": collected_at,
        "posting_date": posting.published_at,
        "collection_method": "auto",
        "robots_terms_checked": "yes",
        "source_log_id": posting.source_log_id,
        "search_keyword": match_note,
        "platform": posting.provider,
        "company": posting.company,
        "industry": "",
        "job_title": posting.title,
        "normalized_role": normalize_role(posting),
        "experience_level": "",
        "min_experience_years": "",
        "education_level": "",
        "employment_type": posting.employment_type,
        "required_skills": "",
        "skill_tags": skill_tags(posting),
        "domain_requirement": "",
        "compensation": posting.compensation,
        "location": posting.location,
        "url": posting.url,
        "raw_file": raw_file,
        "manual_reviewed": "no",
        "notes": (
            f"target_id={posting.target_id}; provider={posting.provider}; raw_id={posting.raw_id}; "
            "public_ats_api; requires_manual_review"
        ),
    }


def review_row(sample: dict[str, str], index: int) -> dict[str, str]:
    return {
        "candidate_id": f"CAND-ATS-{index:03d}",
        "sample_id": "",
        "source_log_id": sample["source_log_id"],
        "reviewed_at": "",
        "reviewer": "",
        "include_decision": "hold",
        "exclude_reason": "",
        "duplicate_of": "",
        "company": sample["company"],
        "job_title": sample["job_title"],
        "normalized_role": sample["normalized_role"],
        "experience_level": sample["experience_level"],
        "required_skills": sample["required_skills"],
        "skill_tags": sample["skill_tags"],
        "domain_requirement": sample["domain_requirement"],
        "url": sample["url"],
        "raw_file": sample["raw_file"],
        "review_notes": sample["notes"],
    }


def source_log_row(target: Target, collected_at: str, dataset_file: str) -> dict[str, str]:
    return {
        "source_log_id": target.source_log_id,
        "dataset_file": dataset_file,
        "source_name": f"{target.company} public {target.provider} job board",
        "source_table_or_page": target.job_board_url,
        "query_condition": f"keywords={';'.join(target.keywords)}; locations={';'.join(target.location_terms)}",
        "period_covered": "currently published postings",
        "download_or_access_date": collected_at,
        "collection_method": "auto",
        "robots_terms_checked": target.robots_terms_checked,
        "request_interval_seconds": str(int(target.request_interval_seconds)),
        "crawler_user_agent": target.crawler_user_agent,
        "url": target.api_url,
        "limitations": target.limitations,
        "notes": f"{target.allowed_basis}; {target.notes}",
    }


def write_csv(path: Path, header: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=header, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch public ATS job-board postings.")
    parser.add_argument("--targets", default="02_data/public_ats_targets.csv")
    parser.add_argument("--fetch", action="store_true", help="Make public ATS API requests.")
    parser.add_argument("--write", action="store_true", help="Write output CSV/JSON files.")
    parser.add_argument("--include-unmatched", action="store_true", help="Keep non-matching postings for review.")
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--sample-out", default="02_data/raw/public_ats_job_posting_candidates.csv")
    parser.add_argument("--review-out", default="02_data/job_posting_manual_review.public_ats.csv")
    parser.add_argument("--source-log-out", default="02_data/source_log.public_ats.csv")
    parser.add_argument("--raw-dir", default="01_research/raw/public_ats")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    targets = read_targets(repo_path(args.targets))
    print(f"eligible_targets: {len(targets)}")
    for target in targets:
        print(f"- {target.target_id} {target.provider} {target.company}: {target.api_url}")

    if not args.fetch:
        print("plan_only: pass --fetch to request documented public job-board APIs")
        return 0

    collected_at = date.today().isoformat()
    raw_dir = repo_path(args.raw_dir)
    sample_rows: list[dict[str, str]] = []
    review_rows: list[dict[str, str]] = []
    source_rows: list[dict[str, str]] = []
    skipped = 0

    for target_index, target in enumerate(targets):
        print(f"fetch: {target.target_id} {target.company}")
        payload = fetch_json(target.api_url, target.crawler_user_agent, args.timeout)
        raw_name = f"{target.target_id}_{target.provider}_{target.board_token}_{collected_at}.json"
        raw_path = raw_dir / raw_name
        if args.write:
            raw_path.parent.mkdir(parents=True, exist_ok=True)
            raw_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

        postings = parse_payload(target, payload)
        matched = 0
        for posting in postings:
            ok, note = matches_terms(posting, target.keywords, target.location_terms)
            if not ok and not args.include_unmatched:
                skipped += 1
                continue
            matched += 1
            row = sample_row(posting, collected_at, str(raw_path.relative_to(REPO_ROOT)), note)
            sample_rows.append(row)
            review_rows.append(review_row(row, len(review_rows) + 1))
        source_rows.append(source_log_row(target, collected_at, args.sample_out))
        print(f"  postings={len(postings)} matched={matched}")

        if target_index < len(targets) - 1:
            time.sleep(target.request_interval_seconds)

    if args.write:
        write_csv(repo_path(args.sample_out), SAMPLE_HEADER, sample_rows)
        write_csv(repo_path(args.review_out), REVIEW_HEADER, review_rows)
        write_csv(repo_path(args.source_log_out), SOURCE_LOG_HEADER, source_rows)
        print(f"wrote: {args.sample_out}")
        print(f"wrote: {args.review_out}")
        print(f"wrote: {args.source_log_out}")

    print(f"sample_rows: {len(sample_rows)}")
    print(f"review_rows: {len(review_rows)}")
    print(f"skipped_unmatched: {skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
