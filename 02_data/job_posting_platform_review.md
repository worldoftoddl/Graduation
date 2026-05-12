# 채용공고 수집 후보 플랫폼 검토

## 검토일

2026-05-12

## 판정 기준

- `yes`: 공식 API 또는 다운로드 경로가 있고 이용 조건을 기록할 수 있어 dry-run 통과 가능.
- `pending`: 공개 페이지나 API 문서는 있으나 약관, 인증, 트래픽, robots 조건을 아직 충분히 기록하지 못해 자동 수집 제외.
- `no`: robots.txt 또는 이용 조건상 자동 수집 대상에서 제외해야 하는 근거가 확인됨.

## 파일럿 후보

| target_id | 플랫폼 | 판정 | 근거 | 후속 조치 |
|---|---|---|---|---|
| TGT-101 | Work24 채용정보 Open API | yes | 고용24/워크넷 계열 채용정보 Open API가 문서화되어 있으며 인증키 기반으로 채용정보 목록·상세를 XML로 제공 | 인증키 발급 후 API 파라미터를 확정하고 호출량 제한 확인 |
| TGT-102 | Saramin 채용정보 API | pending | 사람인 채용정보 API가 별도 사이트로 제공되지만 이용신청·승인 절차와 세부 약관 확인 필요 | API 이용신청 가능 여부와 이용약관 확인 후 재판정 |
| TGT-103 | Wanted 공개 채용 페이지 | pending | 공개 채용 페이지와 이용약관 페이지는 확인되나 자동 수집 허용 여부는 미확정 | robots.txt와 약관을 직접 보관한 뒤 허용 근거가 없으면 제외 |
| TGT-104 | JobKorea 공개 검색 페이지 | no | robots.txt에 검색·채용 관련 경로 제한이 확인됨 | 자동 크롤링 제외. 수동 검수 또는 공식 제공 경로만 사용 |
| TGT-105 | Jumpit 공개 검색 페이지 | pending | 공개 서비스 안내는 있으나 자동 수집 허용 조건 미확정 | robots.txt와 약관 확인 후 재판정 |

## 현재 실행 방침

파일럿 dry-run에서는 TGT-101만 통과시키고, 나머지는 안전하게 제외한다. 민간 플랫폼은 공식 API 승인 또는 명시적 허용 근거를 확보하기 전까지 실제 자동 수집 대상으로 사용하지 않는다.

## 확인 URL

- Work24 Open API: `https://www.work24.go.kr/cm/e/a/0110/selectOpenApiSvcInfo.do?fullApiSvcId=000000000000000000000000000000`
- 공공데이터포털 WorkNet 채용정보 API: `https://www.data.go.kr/data/3038225/openapi.do`
- Saramin API: `https://oapi.saramin.co.kr/`
- Wanted Terms: `https://help.wanted.co.kr/hc/en-us/articles/27666894700953-Terms-of-Use`
- JobKorea robots.txt: `https://www.jobkorea.co.kr/robots.txt`
