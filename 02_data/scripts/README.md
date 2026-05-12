# 채용공고 수집 스크립트

## 목적

`job_posting_collection_dry_run.py`는 실제 웹 크롤링 전에 후보 URL 목록을 정책 기준으로 검증하고, 기존 표본 CSV·출처 로그 CSV·수동 검수 큐와 호환되는 dry-run 행을 만든다.

이 단계는 네트워크에 접근하지 않는다. 자동 수집 전에 다음 조건을 먼저 확인한다.

- `robots_terms_checked=yes`
- `collection_method=auto`
- 로그인, 캡차, 유료벽이 필요하지 않음
- 허용 판단 근거와 요청 간격, User-Agent 기록

## 실행 예시

```bash
python3 02_data/scripts/job_posting_collection_dry_run.py --help
python3 02_data/scripts/job_posting_collection_dry_run.py \
  --targets 02_data/job_posting_collection_targets_example.csv \
  --write
```

`--write`를 사용하면 다음 파일을 생성한다.

- `02_data/source_log.dry_run.csv`
- `02_data/job_posting_sample.dry_run.csv`
- `02_data/job_posting_manual_review.dry_run.csv`

실제 표본인 `02_data/raw/job_posting_sample.csv`에는 수동 검수 후 확정된 행만 옮긴다.

## Work24 Open API 후보 수집

`work24_job_posting_fetch.py`는 Work24 채용정보 Open API 목록 응답을 표본 후보 CSV와 수동 검수 큐로 변환한다. 기본값에서는 네트워크에 접근하지 않고 요청 URL만 출력한다.

계획 모드:

```bash
python3 02_data/scripts/work24_job_posting_fetch.py \
  --keyword AI \
  --display 10 \
  --max-pages 1
```

오프라인 fixture 검증:

```bash
python3 02_data/scripts/work24_job_posting_fetch.py \
  --input-xml 02_data/fixtures/work24_job_postings_sample.xml \
  --sample-out 02_data/raw/work24_job_posting_candidates.dry_run.csv \
  --review-out 02_data/job_posting_manual_review.work24.dry_run.csv \
  --write
```

실제 API 호출은 인증키를 받은 뒤에만 실행한다.

```bash
WORK24_OPENAPI_AUTH_KEY=발급받은_인증키 \
python3 02_data/scripts/work24_job_posting_fetch.py \
  --fetch \
  --keyword AI \
  --display 10 \
  --max-pages 1 \
  --write
```

생성 파일:

- `02_data/raw/work24_job_posting_candidates.csv`
- `02_data/job_posting_manual_review.work24.csv`
- `01_research/raw/Work24/*.xml` (`--fetch --write` 사용 시)
