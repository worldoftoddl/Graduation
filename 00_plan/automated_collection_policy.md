# 채용공고 자동 수집 정책

## 원칙

학술 목적의 탐색적 표본 구축을 위해 채용공고 자동 수집을 허용한다. 단, 자동 수집은 법적·윤리적 방어 가능성을 확보하기 위해 공개 접근 가능 범위, robots.txt, 서비스 약관, 공식 API 또는 다운로드 기능의 허용 범위 안에서만 수행한다.

## 허용 조건

- 공개 채용공고 페이지, 공식 API, 공식 다운로드/내보내기 기능.
- robots.txt 또는 서비스 약관이 자동 접근을 명시적으로 금지하지 않는 범위.
- 요청 간격을 둔 저속 수집.
- 수집한 원문은 연구 검증용으로만 보관하고, 본문에는 구조화·요약된 필드만 사용.
- 수집 로그를 `02_data/source_log.csv`에 남김.

## 금지 조건

- 로그인 우회, 캡차 우회, 유료벽 우회.
- 비공개 API, 내부 API, 인증 토큰 재사용.
- 서버에 부담을 주는 고빈도 요청.
- 채용공고 원문 대량 재배포.
- 개인 연락처 등 분석에 필요 없는 개인정보 저장.

## 필수 로그

| 필드 | 설명 |
|---|---|
| source_log_id | `LOG-001` 형식 |
| source_name | 플랫폼 또는 회사 채용페이지명 |
| query_condition | 검색어, 기간, 지역, 직무 조건 |
| period_covered | 공고 게시 기간 |
| download_or_access_date | 수집일 |
| collection_method | `auto` 또는 `manual` |
| robots_terms_checked | robots.txt·약관 확인 여부 |
| request_interval_seconds | 요청 간격 |
| crawler_user_agent | User-Agent |
| url | 출처 URL |
| limitations | 플랫폼 편향, 검색어 편향, 누락 가능성 |

## 실행 게이트

자동 수집은 다음 순서가 모두 충족된 뒤 실행한다.

1. `02_data/job_posting_collection_targets_template.csv` 형식으로 후보 URL과 검색 조건을 등록한다.
2. robots.txt, 약관, 공개 API 또는 다운로드 허용 범위를 확인하고 `robots_terms_checked=yes`로 기록한다.
3. 로그인, 캡차, 유료벽, 비공개 API 접근이 필요 없는 대상만 남긴다.
4. `02_data/source_log.csv`에 수집 조건과 한계를 먼저 기록한다.
5. 드라이런으로 제외 대상과 출력 CSV 헤더 호환성을 확인한다.
6. 자동 수집 결과를 수동 검수한 뒤 최종 표본에만 `sample_id`를 부여한다.

## 본문 표현

- “채용공고 자동 수집 + 수동 검수 표본”
- “대표통계가 아니라 탐색적 표본”
- “공고 수는 실제 채용 수와 다르다”
- “플랫폼·검색어·수집 시점 편향이 존재한다”
