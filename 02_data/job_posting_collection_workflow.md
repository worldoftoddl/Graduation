# 채용공고 수집 실행 절차

## 1. 수집 대상 후보 등록

`02_data/job_posting_collection_targets_template.csv`를 복사해 실제 수집 대상 파일을 만든다. 후보는 플랫폼 검색 결과 페이지, 회사 공식 채용페이지, 공개 API, 공식 다운로드 파일만 등록한다.

필수 확인:

- robots.txt URL
- 약관 또는 API 문서 URL
- 로그인, 캡차, 유료벽 필요 여부
- 자동 수집 허용 판단 근거
- 요청 간격
- `02_data/source_log.csv`에 연결할 `source_log_id`

`robots_terms_checked`는 확인이 끝난 경우에만 `yes`로 적는다. 확인 전이면 `pending`, 금지 또는 불명확하면 `no`로 두고 자동 수집 대상에서 제외한다.

## 2. 출처 로그 작성

자동 수집 전에 `02_data/source_log.csv`에 수집 조건을 먼저 남긴다. 수집 후에 적으면 검색 조건, 접근일, 제외 판단을 재현하기 어렵다.

필수 로그:

- `source_log_id`
- `source_name`
- `query_condition`
- `period_covered`
- `download_or_access_date`
- `collection_method`
- `robots_terms_checked`
- `request_interval_seconds`
- `crawler_user_agent`
- `url`
- `limitations`

## 3. 드라이런

수집 스크립트는 기본적으로 네트워크 접근 없이 실행한다. 드라이런에서는 후보 URL 중 `robots_terms_checked=yes`, `requires_login=no`, `has_captcha=no`, `has_paywall=no`인 행만 처리 대상으로 표시한다.

드라이런 결과에서 제외된 후보는 `notes` 또는 별도 검수 큐에 제외 사유를 남긴다.

실행 예시:

```bash
python3 02_data/scripts/job_posting_collection_dry_run.py --help
python3 02_data/scripts/job_posting_collection_dry_run.py \
  --targets 02_data/job_posting_collection_targets_example.csv \
  --write
python3 02_data/scripts/job_posting_collection_dry_run.py \
  --targets 02_data/job_posting_collection_targets_pilot.csv \
  --write
```

위 명령은 실제 웹페이지에 접근하지 않고 다음 드라이런 파일만 만든다.

- `02_data/source_log.dry_run.csv`
- `02_data/job_posting_sample.dry_run.csv`
- `02_data/job_posting_manual_review.dry_run.csv`

실제 표본 CSV인 `02_data/raw/job_posting_sample.csv`에는 수동 검수 후 확정된 행만 옮긴다.

## 4. 자동 수집

자동 수집은 드라이런을 통과한 후보에 대해서만 실행한다. 요청 간격을 두고 저속으로 접근하며, 원문 대량 복제 대신 최종 분석에 필요한 구조화 필드만 추출한다.

수집 중 로그인 화면, 캡차, 유료벽, 비공개 API 호출이 감지되면 해당 대상은 즉시 제외한다.

## 5. 수동 검수

자동 수집 후보는 `02_data/job_posting_manual_review_template.csv` 형식으로 검수한다. 최종 표본에 넣을 때만 `sample_id`를 부여하고 `02_data/raw/job_posting_sample.csv`에 반영한다.

검수 기준:

- AI 직무 포함 기준 충족 여부
- 중복 공고 여부
- 회사명, 직무명, URL, 요구 스킬 등 핵심 필드 완전성
- 직무 7분류와 스킬 태그의 일관성
- 원문 스냅샷 또는 PDF 보존 여부

## 6. 본문 반영

본문에는 표본 수, 수집 기간, 플랫폼, 검색어, 제외 기준, 수동 검수 방식, 대표성 한계를 함께 적는다. 공고 수를 실제 채용 수나 시장 점유율로 해석하지 않는다.
