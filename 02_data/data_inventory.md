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
| DATA-006 | `02_data/raw/job_posting_sample.csv` / `02_data/processed/job_posting_sample_coded.csv` | 자동 수집 + 수동 검수 표본 | 요구 스킬셋·직무명 분석 | 예정 |
| DATA-007 | `02_data/raw/sw_industry_spri_2024.csv` / `02_data/processed/sw_industry_spri_2024.csv` | LAB-007 | SW 산업 인력과 AI 비교 | 예정 |

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

### DATA-006. 채용공고 자동 수집 + 수동 검수 표본

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

## 차트 후보

| chart_id | 제목 | 데이터셋 | 권장 유형 | 비고 |
|---|---|---|---|---|
| FIG-001 | 한국 AI 산업 매출·인력 구조 | DATA-001 | 막대/누적 막대 | PDF 표 확인 후 생성 |
| FIG-002 | 정보통신/SW 관련 고용 추이 | DATA-002 | 선 그래프 | AI 직접 지표 아님 표시 |
| FIG-003 | 지역별 AI 관련 직무 배경 지표 | DATA-003 | 지도 또는 막대 | 표본오차 주의 |
| FIG-004 | 직무군별 임금 기준선 | DATA-004 | 박스/막대 | 총보상 아님 표시 |
| FIG-005 | 채용공고 표본의 요구 스킬 빈도 | DATA-006 | 가로 막대 | 자동 수집 + 수동 검수 표본이며 대표통계 아님 표시 |
| FIG-006 | 직무군별 도메인 요건 비중 | DATA-006 | 100% 누적 막대 | 수동 태깅 기준 명시 |
