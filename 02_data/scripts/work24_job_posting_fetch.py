#!/usr/bin/env python3
"""Fetch or parse Work24 job postings into review-ready CSV files.

Network access is opt-in. Without --fetch, the script only prints planned API
requests. For offline verification, pass --input-xml with a saved Work24 XML
response or the bundled fixture.
"""

from __future__ import annotations

import argparse
import csv
import os
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[2]
API_ENDPOINT = "https://www.work24.go.kr/cm/openApi/call/wk/callOpenApiSvcInfo210L01.do"
DEFAULT_USER_AGENT = "GraduationResearchBot/0.1"
MIN_INTERVAL_SECONDS = 5.0

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


@dataclass(frozen=True)
class Work24Posting:
    wanted_auth_no: str
    company: str
    industry: str
    title: str
    salary_type: str
    salary: str
    min_salary: str
    max_salary: str
    region: str
    education_min: str
    education_max: str
    career: str
    reg_date: str
    close_date: str
    info_url: str
    employment_type_code: str
    jobs_code: str


def repo_path(value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return REPO_ROOT / path


def text(element: ET.Element, tag: str) -> str:
    found = element.find(tag)
    return "" if found is None or found.text is None else found.text.strip()


def parse_work24_xml(xml_text: str) -> list[Work24Posting]:
    root = ET.fromstring(xml_text)
    postings: list[Work24Posting] = []
    for wanted in root.findall(".//wanted"):
        postings.append(
            Work24Posting(
                wanted_auth_no=text(wanted, "wantedAuthNo"),
                company=text(wanted, "company"),
                industry=text(wanted, "indTpNm"),
                title=text(wanted, "title"),
                salary_type=text(wanted, "salTpNm"),
                salary=text(wanted, "sal"),
                min_salary=text(wanted, "minSal"),
                max_salary=text(wanted, "maxSal"),
                region=text(wanted, "region") or text(wanted, "basicAddr"),
                education_min=text(wanted, "minEdubg"),
                education_max=text(wanted, "maxEdubg"),
                career=text(wanted, "career"),
                reg_date=text(wanted, "regDt"),
                close_date=text(wanted, "closeDt"),
                info_url=text(wanted, "wantedInfoUrl"),
                employment_type_code=text(wanted, "empTpCd"),
                jobs_code=text(wanted, "jobsCd"),
            )
        )
    return postings


def normalize_role(title: str) -> str:
    lower_title = title.lower()
    if any(term in lower_title for term in ("mlops", "platform", "플랫폼", "인프라")):
        return "mlops_platform_engineer"
    if any(term in lower_title for term in ("llm", "rag", "생성형", "챗봇", "agent", "에이전트")):
        return "applied_ai_developer"
    if any(term in lower_title for term in ("research", "researcher", "리서처", "연구")):
        return "ai_researcher"
    if any(term in lower_title for term in ("deep", "딥러닝", "vision", "nlp", "비전", "자연어")):
        return "ai_deep_learning_engineer"
    if any(term in lower_title for term in ("machine learning", "ml ", "머신러닝")):
        return "ml_engineer"
    if any(term in lower_title for term in ("data scientist", "데이터 사이언티스트")):
        return "data_scientist"
    if any(term in lower_title for term in ("prompt", "프롬프트", "operator", "오퍼레이터")):
        return "prompt_ai_operator"
    if any(term in lower_title for term in ("ai", "인공지능")):
        return "applied_ai_developer"
    return ""


def education_label(posting: Work24Posting) -> str:
    if posting.education_min and posting.education_max and posting.education_min != posting.education_max:
        return f"{posting.education_min}~{posting.education_max}"
    return posting.education_min or posting.education_max


def compensation_label(posting: Work24Posting) -> str:
    parts = [part for part in (posting.salary_type, posting.salary) if part]
    if parts:
        return " ".join(parts)
    range_parts = [part for part in (posting.min_salary, posting.max_salary) if part]
    return "~".join(range_parts)


def query_url(auth_key: str, keyword: str, page: int, display: int) -> str:
    params = {
        "authKey": auth_key,
        "callTp": "L",
        "returnType": "XML",
        "startPage": str(page),
        "display": str(display),
        "keyword": keyword,
    }
    return f"{API_ENDPOINT}?{urllib.parse.urlencode(params)}"


def masked_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    masked_query = [("authKey", "[AUTH_KEY]") if key == "authKey" else (key, value) for key, value in query]
    return urllib.parse.urlunparse(parsed._replace(query=urllib.parse.urlencode(masked_query, safe="[]")))


def fetch_xml(url: str, user_agent: str, timeout: float) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": user_agent})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def read_xml_files(paths: Iterable[str]) -> list[tuple[str, str]]:
    payloads: list[tuple[str, str]] = []
    for path_value in paths:
        path = repo_path(path_value)
        payloads.append((str(path.relative_to(REPO_ROOT)), path.read_text(encoding="utf-8")))
    return payloads


def make_sample_rows(
    postings: list[Work24Posting],
    keyword: str,
    source_log_id: str,
    collected_at: str,
    raw_file: str,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for posting in postings:
        rows.append(
            {
                "sample_id": "",
                "collected_at": collected_at,
                "posting_date": posting.reg_date,
                "collection_method": "auto",
                "robots_terms_checked": "yes",
                "source_log_id": source_log_id,
                "search_keyword": keyword,
                "platform": "Work24",
                "company": posting.company,
                "industry": posting.industry,
                "job_title": posting.title,
                "normalized_role": normalize_role(posting.title),
                "experience_level": posting.career,
                "min_experience_years": "",
                "education_level": education_label(posting),
                "employment_type": posting.employment_type_code,
                "required_skills": "",
                "skill_tags": "",
                "domain_requirement": "",
                "compensation": compensation_label(posting),
                "location": posting.region,
                "url": posting.info_url,
                "raw_file": raw_file,
                "manual_reviewed": "no",
                "notes": (
                    f"wantedAuthNo={posting.wanted_auth_no}; jobsCd={posting.jobs_code}; "
                    f"closeDt={posting.close_date}; requires_manual_review"
                ),
            }
        )
    return rows


def make_review_rows(sample_rows: list[dict[str, str]], candidate_prefix: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, sample in enumerate(sample_rows, start=1):
        rows.append(
            {
                "candidate_id": f"{candidate_prefix}-{index:03d}",
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
        )
    return rows


def write_csv(path: Path, header: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=header, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def require_fetch_safety(args: argparse.Namespace, auth_key: str) -> None:
    if not args.fetch:
        return
    if not auth_key or auth_key in {"[AUTH_KEY]", "AUTH_KEY", "YOUR_AUTH_KEY"}:
        raise SystemExit("Set --auth-key or WORK24_OPENAPI_AUTH_KEY before --fetch.")
    if args.request_interval < MIN_INTERVAL_SECONDS:
        raise SystemExit(f"--request-interval must be at least {MIN_INTERVAL_SECONDS:g} seconds.")
    if args.display < 1 or args.display > 100:
        raise SystemExit("--display must be between 1 and 100.")
    if args.max_pages < 1 or args.max_pages > 1000:
        raise SystemExit("--max-pages must be between 1 and 1000.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Prepare Work24 Open API job-posting candidates. Default mode plans "
            "requests only; --fetch is required for network access."
        )
    )
    parser.add_argument("--auth-key", default=os.environ.get("WORK24_OPENAPI_AUTH_KEY", ""))
    parser.add_argument("--keyword", action="append", default=None, help="Search keyword. Repeatable.")
    parser.add_argument("--display", type=int, default=10, help="Rows per API page, max 100.")
    parser.add_argument("--start-page", type=int, default=1)
    parser.add_argument("--max-pages", type=int, default=1)
    parser.add_argument("--request-interval", type=float, default=10.0)
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--user-agent", default=DEFAULT_USER_AGENT)
    parser.add_argument("--source-log-id", default="LOG-101")
    parser.add_argument("--candidate-prefix", default="CAND-W24")
    parser.add_argument(
        "--input-xml",
        action="append",
        default=[],
        help="Saved Work24 XML response to parse offline. Repeatable.",
    )
    parser.add_argument("--fetch", action="store_true", help="Make Work24 API requests.")
    parser.add_argument("--write", action="store_true", help="Write output CSV files.")
    parser.add_argument(
        "--sample-out",
        default="02_data/raw/work24_job_posting_candidates.csv",
        help="Sample-compatible candidate CSV output.",
    )
    parser.add_argument(
        "--review-out",
        default="02_data/job_posting_manual_review.work24.csv",
        help="Manual-review queue CSV output.",
    )
    parser.add_argument(
        "--raw-xml-dir",
        default="01_research/raw/Work24",
        help="Directory for fetched XML copies when --fetch and --write are used.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    auth_key = args.auth_key.strip()
    args.keyword = args.keyword or ["AI"]
    require_fetch_safety(args, auth_key)

    collected_at = date.today().isoformat()
    payloads: list[tuple[str, str, str]] = []

    if args.input_xml:
        for raw_file, xml_text in read_xml_files(args.input_xml):
            keyword = args.keyword[0] if args.keyword else ""
            payloads.append((keyword, raw_file, xml_text))

    if args.fetch:
        raw_dir = repo_path(args.raw_xml_dir)
        for keyword in args.keyword:
            for page_offset in range(args.max_pages):
                page = args.start_page + page_offset
                url = query_url(auth_key, keyword, page, args.display)
                print(f"fetch: {masked_url(url)}")
                xml_text = fetch_xml(url, args.user_agent, args.timeout)
                raw_name = f"work24_{collected_at}_{keyword}_p{page}.xml".replace("/", "_")
                raw_file = str((raw_dir / raw_name).relative_to(REPO_ROOT))
                payloads.append((keyword, raw_file, xml_text))
                if args.write:
                    raw_dir.mkdir(parents=True, exist_ok=True)
                    (raw_dir / raw_name).write_text(xml_text, encoding="utf-8")
                if page_offset < args.max_pages - 1:
                    time.sleep(args.request_interval)

    if not payloads:
        planned_key = auth_key or "[AUTH_KEY]"
        print("plan_only: no network requests made")
        for keyword in args.keyword:
            for page_offset in range(args.max_pages):
                page = args.start_page + page_offset
                print(masked_url(query_url(planned_key, keyword, page, args.display)))
        print("pass --fetch with WORK24_OPENAPI_AUTH_KEY to request the API")
        print("or pass --input-xml to parse a saved XML response offline")
        return 0

    sample_rows: list[dict[str, str]] = []
    for keyword, raw_file, xml_text in payloads:
        postings = parse_work24_xml(xml_text)
        sample_rows.extend(
            make_sample_rows(postings, keyword, args.source_log_id, collected_at, raw_file)
        )
        print(f"parsed {len(postings)} postings from {raw_file}")

    review_rows = make_review_rows(sample_rows, args.candidate_prefix)
    print(f"sample_rows: {len(sample_rows)}")
    print(f"review_rows: {len(review_rows)}")

    if args.write:
        sample_out = repo_path(args.sample_out)
        review_out = repo_path(args.review_out)
        write_csv(sample_out, SAMPLE_HEADER, sample_rows)
        write_csv(review_out, REVIEW_HEADER, review_rows)
        print(f"wrote: {sample_out.relative_to(REPO_ROOT)}")
        print(f"wrote: {review_out.relative_to(REPO_ROOT)}")
    else:
        print("dry_run_only: pass --write to write output CSV files")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
