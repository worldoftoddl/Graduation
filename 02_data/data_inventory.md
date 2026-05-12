# 데이터 인벤토리

## 목적

3장 정량 분석과 2장 산업 구조 설명에 사용할 CSV·노트북·차트의 출처, 조회 조건, 한계를 추적한다.

## 예정 데이터셋

| dataset_id | 파일 경로 | 원자료 | 목적 | 상태 |
|---|---|---|---|---|
| DATA-001 | `02_data/raw/ai_industry_spri_2024.csv` / `02_data/processed/ai_industry_spri_2024.csv` | IND-001 | AI 기업 매출·인력·투자 현황 | 예정 |
| DATA-002 | `02_data/raw/kosis_labor_macro.csv` / `02_data/processed/kosis_labor_macro_long.csv` | LAB-002 | 거시 고용 배경 | 예정 |
| DATA-003 | `02_data/raw/eaps_employment_by_industry_occupation.csv` / `02_data/processed/eaps_ai_related_employment.csv` | LAB-002 | AI 관련 후보 산업·직업군 고용 | 예정 |
| DATA-004 | `02_data/raw/regional_employment_ai_related.csv` / `02_data/processed/regional_ai_labor_distribution.csv` | LAB-003 | 지역·산업·직업 분포 | 예정 |
| DATA-005 | `02_data/raw/wage_job_portal_ai_occupations.csv` / `02_data/processed/ai_occupation_wage_outlook.csv` | LAB-004, LAB-005 | 직무·직급별 보상 기준선 | 예정 |
| DATA-006 | `02_data/raw/job_posting_sample.csv` / `02_data/processed/job_posting_sample_coded.csv` | 자동 수집 + 기준 기반 검수 표본 | 요구 스킬셋·직무명 분석 | 표본 50건 작성 |
| DATA-007 | `02_data/raw/sw_industry_spri_2024.csv` / `02_data/processed/sw_industry_spri_2024.csv` | LAB-007 | SW 산업 인력과 AI 비교 | 예정 |
| DATA-008 | `02_data/job_posting_collection_targets_template.csv` | 수집 대상 후보 URL·검색 조건 | 자동 수집 전 허용 조건 확인 | 템플릿 |
| DATA-009 | `02_data/job_posting_manual_review_template.csv` | 자동 수집 후보 공고 | 최종 표본 편입 전 수동 검수 | 템플릿 |
| DATA-010 | `02_data/raw/work24_job_posting_candidates.csv` / `02_data/job_posting_manual_review.work24.csv` | Work24 채용정보 Open API | Work24 채용공고 수동 검수 후보 | 보류 |
| DATA-011 | `02_data/raw/public_ats_job_posting_candidates.csv` / `02_data/job_posting_manual_review.public_ats.csv` | Ashby·Lever·Greenhouse 공개 채용 보드 API | 공개 ATS 기반 채용공고 검수 후보 | 후보 55건 수집 |
| DATA-012 | `02_data/processed/public_ats_reviewed_candidates.csv` | DATA-011 | 공개 ATS 후보 자동 검수 결과 | include 50건, hold 5건 |

## 공통 메타데이터 필드

| 필드 | 설명 |
|---|---|
| dataset_id | `DATA-001` 형식 |
| source_code | `sources.md`의 자료코드 |
| downloaded_at | 다운로드 또는 수동 입력일 |
| source_url | 원자료 URL |
| query_condition | 통계 조회 조건 또는 표본 수집 조건 |
| collection_method | 수동 다운로드, 자동 수집, 수동 검수 등 |
| unit | 명, 건, 원, %, 개 등 |
| time_range | 분석 기간 |
| limitations | 표본·분류·시점 한계 |

## 주요 CSV 스키마

### DATA-002. KOSIS 거시 노동시장 지표

| 컬럼 | 설명 |
|---|---|
| year | 기준연도 |
| month | 월간 자료일 경우 기준월 |
| indicator | 고용률, 실업률, 취업자 수 등 |
| value | 수치 |
| unit | %, 천명 등 |
| sex | 전체/남/여 |
| age_group | 전체/15-29세 등 |
| source_table | 통계표명 |
| download_date | 다운로드일 |

### DATA-003. 산업·직업별 고용

| 컬럼 | 설명 |
|---|---|
| year | 기준연도 |
| industry_code | 산업분류 코드 |
| industry_name | 산업명 |
| occupation_code | 직업분류 코드 |
| occupation_name | 직업명 |
| employment_count | 취업자 수 |
| ai_related_flag | AI 관련 후보 산업·직업 여부 |
| ai_related_reason | 포함 사유 |
| source_table | 통계표명 |
| download_date | 다운로드일 |

### DATA-006. 채용공고 자동 수집 + 기준 기반 검수 표본

2026-05-12 기준 공개 ATS 후보 중 include 50건을 `JOB-001`~`JOB-050`으로 반영했다. `manual_reviewed=auto_reviewed`는 사람이 개별 URL을 모두 수동 확인했다는 뜻이 아니라, 공개 ATS 원본 JSON과 자동 검수 기준을 통과했다는 뜻이다.

| 컬럼 | 설명 |
|---|---|
| sample_id | `JOB-001` 형식 |
| collected_at | 수집일 |
| collection_method | `auto` 또는 `manual` |
| robots_terms_checked | robots.txt·약관 확인 여부 |
| source_log_id | 출처 로그 ID |
| search_keyword | 사용 검색어 |
| platform | 공고 확인 플랫폼 |
| company | 회사명 |
| industry | 산업 |
| job_title | 원문 직무명 |
| normalized_role | 7개 직군 중 하나 |
| experience_level | 신입/경력/연차 |
| required_skills | 원문 요구 기술 |
| skill_tags | 정규화한 스킬 태그 |
| domain_requirement | 도메인 지식 요건 |
| compensation | 공개 보상 정보 |
| url | 원문 URL |
| raw_file | PDF/스크린샷 경로 |
| notes | 분류·중복 판단 메모 |

### DATA-008. 채용공고 수집 대상 후보

| 컬럼 | 설명 |
|---|---|
| target_id | `TGT-001` 형식 |
| platform | 채용 플랫폼 또는 회사 채용페이지 |
| source_name | 원자료명 또는 검색 결과 페이지명 |
| url | 수집 대상 URL |
| search_keyword | 검색어 |
| period_covered | 공고 게시 기간 또는 검색 기간 |
| collection_method | `auto` 또는 `manual` |
| robots_url | 확인한 robots.txt URL |
| terms_url | 확인한 약관 또는 API 문서 URL |
| robots_terms_checked | 자동 수집 허용 조건 확인 여부 |
| allowed_basis | 허용 판단 근거 |
| requires_login | 로그인 필요 여부 |
| has_captcha | 캡차 존재 여부 |
| has_paywall | 유료벽 존재 여부 |
| request_interval_seconds | 요청 간격 |
| crawler_user_agent | 사용할 User-Agent |
| source_log_id | `02_data/source_log.csv`의 로그 ID |
| limitations | 플랫폼·검색어·기간 편향 |
| notes | 제외 사유 또는 추가 확인 사항 |

### DATA-009. 채용공고 수동 검수 큐

| 컬럼 | 설명 |
|---|---|
| candidate_id | 자동 수집 후보 ID |
| sample_id | 최종 표본 편입 시 부여할 `JOB-001` 형식 ID |
| source_log_id | 출처 로그 ID |
| reviewed_at | 수동 검수일 |
| reviewer | 검수자 |
| include_decision | `include`, `exclude`, `hold` |
| exclude_reason | 제외 사유 |
| duplicate_of | 중복인 경우 기준 후보 ID |
| normalized_role | 코딩북의 7개 직군 |
| skill_tags | 코딩북의 정규화 스킬 태그 |
| review_notes | 판단 근거 |

### DATA-010. Work24 채용공고 후보

`02_data/scripts/work24_job_posting_fetch.py`로 생성한다. Work24 API 목록 응답의 `wanted` 항목을 표본 후보 CSV와 수동 검수 큐로 변환한다.

주의:

- 개인회원 신청으로는 채용정보목록·채용정보상세 API를 사용할 수 없으므로 현 단계에서는 실제 호출을 보류한다.
- 채용정보목록·상세 API 권한이 있는 인증키가 없으면 계획 모드 또는 저장 XML fixture만 사용한다.
- `02_data/raw/work24_job_posting_candidates.csv`는 최종 표본이 아니라 수동 검수 전 후보 파일이다.
- `required_skills`, `skill_tags`, `domain_requirement`는 목록 API만으로 충분하지 않을 수 있으므로 상세 페이지/API 확인 후 수동 보강한다.
- 최종 표본 편입 시에만 `sample_id`를 부여하고 `02_data/raw/job_posting_sample.csv`로 옮긴다.

### DATA-011. 공개 ATS 채용공고 후보

`02_data/scripts/public_ats_job_board_fetch.py`로 생성한다. Ashby, Lever, Greenhouse의 공개 채용 보드 API를 사용해 현재 게시 중인 공고를 가져오고, 한국 위치 필드와 AI/ML 직무 근거가 있는 후보만 남긴다.

주의:

- `02_data/raw/public_ats_job_posting_candidates.csv`는 최종 표본이 아니라 수동 검수 전 후보 파일이다.
- 원본 JSON은 `01_research/raw/public_ats/`에 저장한다.
- 수집 범위는 회사 공식 채용 보드 13개이므로 대표통계가 아니라 탐색적 보조 표본이다.
- 최종 표본 편입 시 중복·비기술 직무·해외 직무를 수동으로 제외하고 `sample_id`를 부여한다.

### DATA-012. 공개 ATS 후보 자동 검수 결과

`02_data/scripts/review_public_ats_candidates.py`로 생성한다. DATA-011 후보를 `include`, `exclude`, `hold`로 1차 판정하고, 포함 후보에 `recommended_sample_id`를 제안한다. 2026-05-12 실행 결과는 include 50건, hold 5건, exclude 0건이다.

주의:

- 자동 판정은 최종 검수가 아니라 검수 보조 결과다.
- `hold` 후보는 원문 공고를 확인한 뒤 최종 포함 여부를 결정한다.
- 최종 표본은 `02_data/raw/job_posting_sample.csv`에 별도 반영한다.

## 차트 후보

| chart_id | 제목 | 데이터셋 | 권장 유형 | 비고 |
|---|---|---|---|---|
| FIG-001 | 한국 AI 산업 매출·인력 구조 | DATA-001 | 막대/누적 막대 | PDF 표 확인 후 생성 |
| FIG-002 | 정보통신/SW 관련 고용 추이 | DATA-002 | 선 그래프 | AI 직접 지표 아님 표시 |
| FIG-003 | 지역별 AI 관련 직무 배경 지표 | DATA-003 | 지도 또는 막대 | 표본오차 주의 |
| FIG-004 | 직무군별 임금 기준선 | DATA-004 | 박스/막대 | 총보상 아님 표시 |
| FIG-005 | 채용공고 표본의 요구 스킬 빈도 | DATA-006 | 가로 막대 | 자동 수집 + 수동 검수 표본이며 대표통계 아님 표시 |
| FIG-006 | 직무군별 도메인 요건 비중 | DATA-006 | 100% 누적 막대 | 수동 태깅 기준 명시 |
