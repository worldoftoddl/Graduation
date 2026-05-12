#!/usr/bin/env python3
"""Review public ATS job-posting candidates.

The output is a review aid, not the final sample. Include decisions still need
human confirmation before rows move into 02_data/raw/job_posting_sample.csv.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]

ADDED_COLUMNS = [
    "review_decision",
    "review_reason",
    "review_flags",
    "dedupe_key",
    "recommended_sample_id",
]

NON_TECH_TERMS = (
    "sales",
    "business development",
    "marketing",
    "customer success",
    "recruit",
    "people",
    "hr",
    "finance",
    "legal",
    "counsel",
    "operations",
    "assistant",
    "strategist",
    "deployment strategist",
    "영업",
    "마케팅",
    "인사",
    "법무",
)

HOLD_TITLE_TERMS = (
    "solution architect",
    "field application",
    "technical program manager",
    "engineering manager",
    "application engineer",
    "infrastructure engineer",
    "deployment",
    "architect",
)

STRONG_AI_TITLE_TERMS = (
    "ai engineer",
    "ai research",
    "research engineer",
    "research scientist",
    "machine learning",
    "ml engineer",
    "data scientist",
    "deep learning",
    "computer vision",
    "nlp",
    "llm",
    "rag",
    "recommendation",
    "recommender",
    "quantization",
    "npu",
    "gpu",
    "ai scientist",
    "applied ai",
    "머신러닝",
    "딥러닝",
    "인공지능",
    "데이터 사이언티스트",
)

TECH_ROLE_TERMS = (
    "engineer",
    "scientist",
    "research",
    "developer",
    "software",
    "data",
    "platform",
    "architect",
    "엔지니어",
    "개발",
    "연구",
)

AI_EVIDENCE_TERMS = (
    "ai",
    "machine learning",
    "ml",
    "llm",
    "rag",
    "nlp",
    "computer vision",
    "vision",
    "recommendation",
    "recommender",
    "model",
    "inference",
    "quantization",
    "npu",
    "gpu",
    "pytorch",
    "tensorflow",
    "python",
    "mlops",
    "agent",
    "data scientist",
    "머신러닝",
    "딥러닝",
    "생성형",
)

KOREA_TERMS = (
    "seoul",
    "south korea",
    "korea",
    "kr",
    "서울",
    "판교",
    "성남",
)


def repo_path(value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return REPO_ROOT / path


def contains_any(text: str, terms: tuple[str, ...]) -> list[str]:
    lower = text.lower()
    return [term for term in terms if term in lower]


def normalize_role(row: dict[str, str]) -> str:
    text = " ".join(
        [
            row.get("job_title", ""),
            row.get("search_keyword", ""),
            row.get("skill_tags", ""),
            row.get("notes", ""),
        ]
    ).lower()
    if any(term in text for term in ("mlops", "platform", "infrastructure", "model serving", "gpu kernel")):
        return "mlops_platform_engineer"
    if any(term in text for term in ("ai research", "research scientist", "research engineer")):
        return "ai_researcher"
    if any(term in text for term in ("deep learning", "computer vision", "nlp", "quantization", "npu")):
        return "ai_deep_learning_engineer"
    if any(term in text for term in ("machine learning", "ml engineer", "머신러닝")):
        return "ml_engineer"
    if "data scientist" in text:
        return "data_scientist"
    if any(term in text for term in ("llm", "rag", "agent", "applied ai", "ai application")):
        return "applied_ai_developer"
    return row.get("normalized_role", "")


def skill_tags(row: dict[str, str]) -> str:
    existing = [tag for tag in row.get("skill_tags", "").split(";") if tag]
    text = " ".join([row.get("job_title", ""), row.get("search_keyword", ""), row.get("notes", "")]).lower()
    checks = {
        "python": ("python",),
        "pytorch": ("pytorch",),
        "tensorflow": ("tensorflow",),
        "sql": ("sql",),
        "cloud": ("cloud", "aws", "gcp", "azure"),
        "docker_k8s": ("docker", "kubernetes", "k8s"),
        "mlops": ("mlops", "model serving", "kubeflow", "mlflow"),
        "llm": ("llm", "large language"),
        "rag": ("rag", "retrieval"),
        "nlp": ("nlp", "natural language"),
        "cv": ("computer vision", "vision", "cv"),
        "recommender": ("recommendation", "recommender"),
    }
    merged = list(dict.fromkeys(existing))
    for tag, terms in checks.items():
        if tag not in merged and any(term in text for term in terms):
            merged.append(tag)
    return ";".join(merged)


def dedupe_key(row: dict[str, str]) -> str:
    company = row.get("company", "").strip().lower()
    title = " ".join(row.get("job_title", "").strip().lower().split())
    location = " ".join(row.get("location", "").strip().lower().split())
    return f"{company}|{title}|{location}"


def review_row(row: dict[str, str], seen_keys: set[str]) -> tuple[str, str, list[str], str]:
    title = row.get("job_title", "")
    location = row.get("location", "")
    search_note = row.get("search_keyword", "")
    notes = row.get("notes", "")
    tags = row.get("skill_tags", "")
    combined = " ".join([title, location, search_note, notes, tags])

    flags: list[str] = []
    key = dedupe_key(row)
    if key in seen_keys:
        flags.append("duplicate_key")

    korea_hits = contains_any(location, KOREA_TERMS)
    strong_hits = contains_any(title, STRONG_AI_TITLE_TERMS)
    non_tech_hits = contains_any(title, NON_TECH_TERMS)
    hold_hits = contains_any(title, HOLD_TITLE_TERMS)
    tech_hits = contains_any(title, TECH_ROLE_TERMS)
    evidence_hits = contains_any(combined, AI_EVIDENCE_TERMS)

    if not row.get("url"):
        return "exclude", "missing_url", flags + ["missing_url"], key
    if not korea_hits:
        return "exclude", "no_korea_location_evidence", flags + ["no_korea_location"], key
    if "duplicate_key" in flags:
        return "exclude", "duplicate_company_title_location", flags, key
    if non_tech_hits and not strong_hits:
        return "exclude", f"non_technical_title:{';'.join(non_tech_hits)}", flags + ["non_technical_title"], key
    if strong_hits:
        return "include", f"strong_ai_title:{';'.join(strong_hits)}", flags + ["strong_ai_title"], key
    if tech_hits and len(evidence_hits) >= 2 and not hold_hits:
        return "include", f"technical_role_with_ai_evidence:{';'.join(evidence_hits[:5])}", flags + ["technical_ai_role"], key
    if tech_hits and evidence_hits:
        return "hold", f"borderline_technical_ai_role:{';'.join(evidence_hits[:5])}", flags + ["borderline_ai_role"], key
    return "exclude", "weak_ai_technical_evidence", flags + ["weak_ai_evidence"], key


def read_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return reader.fieldnames or [], [dict(row) for row in reader]


def write_rows(path: Path, header: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=header, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_summary(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    decision_counts = Counter(row["review_decision"] for row in rows)
    include_by_company = Counter(row["company"] for row in rows if row["review_decision"] == "include")
    reason_counts = Counter(row["review_reason"].split(":")[0] for row in rows)
    hold_rows = [row for row in rows if row["review_decision"] == "hold"]

    lines = [
        "# 공개 ATS 후보 자동 검수 요약",
        "",
        "## 전체 결과",
        "",
        f"- 총 후보: {len(rows)}건",
        f"- include: {decision_counts.get('include', 0)}건",
        f"- hold: {decision_counts.get('hold', 0)}건",
        f"- exclude: {decision_counts.get('exclude', 0)}건",
        "",
        "## 회사별 include",
        "",
    ]
    for company, count in include_by_company.most_common():
        lines.append(f"- {company}: {count}건")
    lines.extend(["", "## 주요 판정 사유", ""])
    for reason, count in reason_counts.most_common():
        lines.append(f"- {reason}: {count}건")
    lines.extend(["", "## hold 후보", ""])
    if hold_rows:
        for row in hold_rows:
            lines.append(f"- {row['company']} / {row['job_title']}: {row['review_reason']}")
    else:
        lines.append("- 없음")
    lines.extend(
        [
            "",
            "## 다음 액션",
            "",
            "1. include 후보를 원문 URL 기준으로 빠르게 확인한다.",
            "2. hold 후보는 직무 설명을 보고 포함 또는 제외로 확정한다.",
            "3. 확정 include 후보만 `02_data/raw/job_posting_sample.csv`로 옮긴다.",
            "4. 최종 표본이 50건 미만이면 공개 ATS 보드 대상을 추가 수집한다.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Auto-review public ATS candidates.")
    parser.add_argument("--input", default="02_data/raw/public_ats_job_posting_candidates.csv")
    parser.add_argument("--output", default="02_data/processed/public_ats_reviewed_candidates.csv")
    parser.add_argument("--summary", default="02_data/processed/public_ats_review_summary.md")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    header, rows = read_rows(repo_path(args.input))
    output_header = header + [column for column in ADDED_COLUMNS if column not in header]

    seen_keys: set[str] = set()
    reviewed_rows: list[dict[str, str]] = []
    next_sample_id = 1
    for row in rows:
        row = dict(row)
        row["normalized_role"] = normalize_role(row)
        row["skill_tags"] = skill_tags(row)
        decision, reason, flags, key = review_row(row, seen_keys)
        seen_keys.add(key)
        row["review_decision"] = decision
        row["review_reason"] = reason
        row["review_flags"] = ";".join(flags)
        row["dedupe_key"] = key
        if decision == "include":
            row["recommended_sample_id"] = f"JOB-{next_sample_id:03d}"
            next_sample_id += 1
        else:
            row["recommended_sample_id"] = ""
        reviewed_rows.append(row)

    write_rows(repo_path(args.output), output_header, reviewed_rows)
    write_summary(repo_path(args.summary), reviewed_rows)

    counts = Counter(row["review_decision"] for row in reviewed_rows)
    print(f"total_rows: {len(reviewed_rows)}")
    print(f"include: {counts.get('include', 0)}")
    print(f"hold: {counts.get('hold', 0)}")
    print(f"exclude: {counts.get('exclude', 0)}")
    print(f"wrote: {args.output}")
    print(f"wrote: {args.summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
