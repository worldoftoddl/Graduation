# 채용공고 수집 후보 플랫폼 검토

## 검토일

2026-05-12

## 판정 기준

- `yes`: 공식 API 또는 다운로드 경로가 있고 이용 조건을 기록할 수 있어 dry-run 통과 가능.
- `pending`: 공개 페이지나 API 문서는 있으나 약관, 인증, 트래픽, robots 조건을 아직 충분히 기록하지 못해 자동 수집 제외.
- `no`: robots.txt 또는 이용 조건상 자동 수집 대상에서 제외해야 하는 근거가 확인됨.
- `hold`: 공식 API는 있으나 현재 신청 가능한 계정 유형으로 필요한 엔드포인트를 사용할 수 없어 보류.

## 파일럿 후보

| target_id | 플랫폼 | 판정 | 근거 | 후속 조치 |
|---|---|---|---|---|
| TGT-101 | Work24 채용정보 Open API | hold | 개인회원 신청 시 채용행사·공채속보·공채기업정보 API만 이용 가능하고, 채용정보목록·채용정보상세 API는 이용 불가 | 기관/사업자 권한이 생기기 전까지 자동 수집 제외 |
| TGT-102 | Saramin 채용정보 API | pending | 사람인 채용정보 API가 별도 사이트로 제공되지만 이용신청·승인 절차와 세부 약관 확인 필요 | API 이용신청 가능 여부와 이용약관 확인 후 재판정 |
| TGT-103 | Wanted 공개 채용 페이지 | pending | 공개 채용 페이지와 이용약관 페이지는 확인되나 자동 수집 허용 여부는 미확정 | robots.txt와 약관을 직접 보관한 뒤 허용 근거가 없으면 제외 |
| TGT-104 | JobKorea 공개 검색 페이지 | no | robots.txt에 검색·채용 관련 경로 제한이 확인됨 | 자동 크롤링 제외. 수동 검수 또는 공식 제공 경로만 사용 |
| TGT-105 | Jumpit 공개 검색 페이지 | pending | 공개 서비스 안내는 있으나 자동 수집 허용 조건 미확정 | robots.txt와 약관 확인 후 재판정 |

## 현재 실행 방침

파일럿 dry-run에서는 현재 통과 후보를 0건으로 둔다. Work24는 개인회원 제한 때문에 보류하고, 민간 플랫폼은 공식 API 승인 또는 명시적 허용 근거를 확보하기 전까지 실제 자동 수집 대상으로 사용하지 않는다.

## Work24 실행 스크립트

- 계획 모드: `python3 02_data/scripts/work24_job_posting_fetch.py --keyword AI --display 10 --max-pages 1`
- 오프라인 파싱 검증: `python3 02_data/scripts/work24_job_posting_fetch.py --input-xml 02_data/fixtures/work24_job_postings_sample.xml --write`
- 실제 API 호출: `WORK24_OPENAPI_AUTH_KEY=... python3 02_data/scripts/work24_job_posting_fetch.py --fetch --keyword AI --display 10 --max-pages 1 --write`

현재 개인회원으로는 채용정보목록·채용정보상세 API를 사용할 수 없으므로 실제 API 호출은 보류한다. 스크립트는 기관/사업자 권한을 확보하거나 저장 XML을 검증할 때만 사용한다. 결과 파일은 최종 표본이 아니라 수동 검수 후보로 취급한다.

## Work24 보류 근거

신청 화면 기준으로 개인회원은 채용행사, 공채속보, 공채기업정보 API만 이용할 수 있고, 채용정보목록·채용정보상세 API는 이용할 수 없다. 본 프로젝트의 채용공고 표본 구축에는 목록·상세 API가 필요하므로 Work24 자동 수집은 현 단계에서 보류한다.

## 확인 URL

- Work24 Open API: `https://www.work24.go.kr/cm/e/a/0110/selectOpenApiSvcInfo.do?fullApiSvcId=000000000000000000000000000000`
- 공공데이터포털 WorkNet 채용정보 API: `https://www.data.go.kr/data/3038225/openapi.do`
- Saramin API: `https://oapi.saramin.co.kr/`
- Wanted Terms: `https://help.wanted.co.kr/hc/en-us/articles/27666894700953-Terms-of-Use`
- JobKorea robots.txt: `https://www.jobkorea.co.kr/robots.txt`
