# 원자료 저장 매니페스트

## 목적

`01_research/sources.md`에 등록한 자료를 본문에서 사용하기 전에 원문 파일, 웹 스냅샷, 통계 조회 조건을 남겨 재현 가능성을 확보한다.

## 저장 규칙

- PDF·첨부파일: `01_research/raw/{기관분류}/{자료코드}_{발행연도}_{기관}_{slug}.pdf`
- 웹페이지 스냅샷: `01_research/raw/{기관분류}/{자료코드}_{slug}_snapshot.html` 또는 `.pdf`
- 통계표 CSV/XLSX: `02_data/raw/{dataset_slug}.csv` 또는 `.xlsx`
- 자료별 요약 노트: `01_research/notes/{자료코드}_{slug}.md`
- 조회형 자료는 `기준시점`, `분류`, `산업`, `직업`, `지역`, `단위`, `다운로드일`을 별도 메타로 남긴다.

## 우선순위 高

| 코드 | 구분 | 보존 대상 | 권고 저장 경로 | 본문 인용 전 확인 |
|---|---|---|---|---|
| IND-001 | SPRi | 원문 PDF | `01_research/raw/SPRi/IND-001_2025_MSICT-SPRi_2024_AI_industry_survey.pdf` | AI 기업 수, 매출, 수출, 투자, 인력 현황 표. 조사 기준연도와 모집단 정의 |
| IND-002 | SPRi | 원문 PDF | `01_research/raw/SPRi/IND-002_2024_SPRi_AI_startup_business_analysis.pdf` | AI 창업기업 정의, 사업모델 분류, 성장 제약, 정책 수요 |
| IND-003 | NIPA | 공고문 PDF/첨부, HTML 스냅샷 | `01_research/raw/NIPA/IND-003_2024_NIPA_AI_voucher_notice.pdf` | 지원 목적, 지원 규모, 수요·공급기업 요건, 예산 |
| IND-004 | NIPA | 공고문 PDF/첨부, HTML 스냅샷 | `01_research/raw/NIPA/IND-004_2025_NIPA_AI_voucher_semiconductor_notice.pdf` | AI 반도체 컨소시엄 구조, 참여 요건, 지원 규모 |
| IND-005 | KISDI | 원문 PDF | `01_research/raw/public_reports/IND-005_2025_KISDI_AI_adoption_business_reports.pdf` | 사업보고서 텍스트 분석 방법론, AI 도입 식별 기준 |
| IND-006 | KIET | 원문 PDF | `01_research/raw/public_reports/IND-006_2025_KIET_global_AI_industry.pdf` | 글로벌 AI 시장 구분, 성장 요인, 원자료 출처 |
| IND-009 | 법령 | 현행 조문 PDF/HTML 스냅샷 | `01_research/raw/law/IND-009_2026_AI_basic_act_lawgo_snapshot.pdf` | 목적, 정의, 고영향 AI, 신뢰성·안전성, 시행일 조문 |
| IND-010 | 기업 PDF | NAVER 통합보고서 PDF | `01_research/raw/corporate_pdf/IND-010_2025_NAVER_integrated_report_2024_KOR.pdf` | HyperCLOVA X, AI 사업, 연구개발, 리스크 관련 페이지 |
| LAB-001 | 통계청 | 고시문·분류표 첨부 | `01_research/raw/KOSTAT/LAB-001_2024_KSCO_8th_revision_notice.pdf` | KSCO 제8차 개정 시행일, 정보통신·데이터·AI 관련 직업 코드 |
| LAB-002 | KOSIS/통계청 | 통계표 CSV/XLSX, 조회조건 캡처 | `01_research/raw/KOSIS/LAB-002_YYYYMM_economically_active_population.xlsx` | 전체 취업자, 산업별·직업별 취업자 표, 기준월 |
| LAB-003 | KOSIS/통계청 | 통계표 CSV/XLSX, 조회조건 캡처 | `01_research/raw/KOSIS/LAB-003_YYYYH_area_employment_survey.xlsx` | 지역×산업×직업 교차표, 공표 한계 |
| LAB-004 | 공공 임금통계 | 조회 결과 CSV/XLSX, 조건 캡처 | `01_research/raw/MOEL/LAB-004_2024_wagework_job_grade_wage.xlsx` | 직군·직급·사업체 규모·산업 조건과 임금 단위 |
| LAB-006 | KEIS | 직업분류 PDF/표 | `01_research/raw/KEIS/LAB-006_2025_KECO_classification.pdf` | KECO 코드표, KSCO와 매핑 가능한 직업군 |
| LAB-007 | SPRi | 원문 PDF | `01_research/raw/SPRi/LAB-007_2025_MSICT-SPRi_2024_SW_industry_survey.pdf` | SW 산업 인력, AI·빅데이터·클라우드 인력 부족 표 |
| LAB-008 | KLI | 노동리뷰 PDF | `01_research/raw/KLI/LAB-008_2026_KLI_labor_review_AI_transition.pdf` | AI 전환, 개발자 노동, 핵심 숙련, 노사관계 쟁점 |
| DOM-004 | DART | 사업보고서 원문 PDF/HTML, 접수번호 메타 | `01_research/raw/DART/DOM-004_2025_KakaoBank_business_report_2024_rcp20250318000824.pdf` | 사업 개요, 리스크 관리, 신용평가·CSS 언급 여부 |
| THEORY-007 | KCI | 논문 PDF, KCI 상세 HTML | `01_research/raw/KCI/THEORY-007_2015_Kim_digital_creative_labor.pdf` | pp.71-110 중 창의노동·주체성·노동윤리 논의 |
| THEORY-008 | KCI | 논문 PDF, KCI 상세 HTML | `01_research/raw/KCI/THEORY-008_2025_Park_AI_data_labor_discourse.pdf` | pp.73-108 중 자료·방법론, 1,757건 언론보도, 분석 결과 |

## 우선순위 中

| 코드 | 구분 | 보존 대상 | 권고 저장 경로 |
|---|---|---|---|
| IND-007 | NIA | 백서 PDF | `01_research/raw/public_reports/IND-007_2025_NIA_2024_national_informatization_whitepaper.pdf` |
| IND-008 | 정부 정책 | 보도자료 HTML, 안건 PDF/첨부 | `01_research/raw/policy/IND-008_2023_MSIT_AI_daily_life_industry_plan.pdf` |
| IND-011 | 기업 웹 | 보도자료 HTML/PDF 스냅샷 | `01_research/raw/corporate_web/IND-011_2024_Upstage_Solar_Pro_AWS_snapshot.pdf` |
| LAB-005 | WorkNet | 직업별 상세 페이지 PDF/HTML | `01_research/raw/KEIS/LAB-005_worknet_AI_data_job_info_snapshot.pdf` |
| LAB-009 | BLS | 웹페이지 PDF/HTML, 표 캡처 | `01_research/raw/global/LAB-009_2025_BLS_OOH_data_scientists_snapshot.pdf` |
| LAB-010 | OECD | 보고서 PDF/HTML | `01_research/raw/global/LAB-010_2023_OECD_employment_outlook_AI_labour_market.pdf` |
| LAB-011 | WEF | 보고서 PDF | `01_research/raw/global/LAB-011_2025_WEF_future_of_jobs_report.pdf` |
| DOM-001 | 금융위 | 보도자료 HTML/PDF, 첨부 | `01_research/raw/finance_policy/DOM-001_2024_FSC_financial_sector_AI_support.pdf` |
| DOM-002 | 금융위 | 보도자료 HTML/PDF, 첨부 | `01_research/raw/finance_policy/DOM-002_2024_FSC_generative_AI_financial_services.pdf` |
| DOM-003 | 금융보안원 | 보도자료 HTML/PDF | `01_research/raw/finance_policy/DOM-003_2024_FSEC_financial_AI_safety_framework.pdf` |
| DOM-005 | 기업/회계법인 웹 | AX Node, KSOX AI 각각 HTML/PDF 스냅샷 | `01_research/raw/corporate_web/DOM-005_undated_SamilPwC_AX_Node_KSOX_AI_snapshot.pdf` |
| DOM-006 | 기업/회계법인 웹 | 보도자료 HTML/PDF | `01_research/raw/corporate_web/DOM-006_2025_Deloitte_Korea_Omnia_GenAI_snapshot.pdf` |
| DOM-007 | 기업/로펌 웹 | 공식 소식 HTML/PDF | `01_research/raw/corporate_web/DOM-007_2022_BKL_RPA_AI_translation_snapshot.pdf` |
| DOM-008 | 해외 감독기관 | 발표문 HTML/PDF | `01_research/raw/global/DOM-008_2024_PCAOB_genAI_audit_observations_snapshot.pdf` |

## 우선순위 低

| 코드 | 구분 | 보존 대상 | 권고 저장 경로 |
|---|---|---|---|
| THEORY-001 | 이론 원전 | 서지 페이지 스냅샷, 실제 인용판 별도 확보 | `01_research/raw/theory/THEORY-001_1973_Bell_post_industrial_society_bibliography.pdf` |
| THEORY-002 | 이론 원전 | 출판사 서지 스냅샷, 실제 인용판 별도 확보 | `01_research/raw/theory/THEORY-002_1996_Castells_network_society_bibliography.pdf` |
| THEORY-003 | 이론 원전 | 출판사 서지 스냅샷, 실제 인용판 별도 확보 | `01_research/raw/theory/THEORY-003_2014_Fuchs_digital_labour_bibliography.pdf` |
| THEORY-004 | 이론 원전 | 출판사 서지 스냅샷, 실제 인용판 별도 확보 | `01_research/raw/theory/THEORY-004_2013_Scholz_digital_labor_bibliography.pdf` |
| THEORY-005 | 이론 원전 | 서지 페이지 스냅샷, 실제 인용판 별도 확보 | `01_research/raw/theory/THEORY-005_2019_Gray_Suri_ghost_work_bibliography.pdf` |
| THEORY-006 | 이론 원전 | 출판사 서지 스냅샷, 실제 인용판 별도 확보 | `01_research/raw/theory/THEORY-006_2009_Mosco_political_economy_communication_bibliography.pdf` |

## 수동 확인 로그

| 자료코드 | 저장일 | 저장 파일 | 확인한 페이지/표 | 비고 |
|---|---|---|---|---|
|  |  |  |  |  |
