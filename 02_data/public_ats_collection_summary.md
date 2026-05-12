# 공개 ATS 채용공고 자동 수집 요약

## 수집일

2026-05-12

## 수집 방식

- 대상: Ashby, Lever 공개 채용 보드 API
- 방식: 인증키 없는 공개 job-board API에 저속 GET 요청
- 요청 간격: 대상별 10초
- User-Agent: `GraduationResearchBot/0.1`
- 로그인, 캡차, 유료벽, 비공개 API 접근 없음

## 대상 보드

| target_id | 회사 | provider | 수집 후보 |
|---|---|---|---:|
| ATS-001 | FuriosaAI | Ashby | 10 |
| ATS-002 | FriendliAI | Ashby | 5 |
| ATS-003 | Speak | Ashby | 0 |
| ATS-004 | ElevenLabs | Ashby | 0 |
| ATS-005 | Gauss Labs | Lever | 2 |
| ATS-006 | Channel Corp | Lever | 1 |
| ATS-007 | Match Group | Lever | 2 |
| ATS-008 | TwelveLabs | Ashby | 16 |
| ATS-009 | CLO Virtual Fashion | Lever | 2 |
| ATS-010 | Fieldguide | Ashby | 2 |
| ATS-011 | Binance | Lever | 2 |
| ATS-012 | Palantir | Lever | 1 |

합계: 43건

## 산출 파일

- 후보 CSV: `02_data/raw/public_ats_job_posting_candidates.csv`
- 수동 검수 큐: `02_data/job_posting_manual_review.public_ats.csv`
- 출처 로그: `02_data/source_log.public_ats.csv`
- 원본 JSON: `01_research/raw/public_ats/*.json`
- 자동 검수 기준: `02_data/public_ats_review_criteria.md`

## 해석상 주의

- 이 파일은 최종 표본이 아니라 자동 수집 후보 목록이다.
- 회사 공식 채용 보드의 현재 게시 공고만 포함하므로 한국 AI 노동시장 전체를 대표하지 않는다.
- 동일 기업의 유사 직무가 여러 건 포함될 수 있으므로 최종 표본 편입 전 중복·유사 직무를 수동 검수해야 한다.
- `required_skills`, `domain_requirement`, `experience_level`은 공고 설명 전체를 검토해 수동 보강한다.

## 다음 단계

1. 자동 검수 결과인 `02_data/processed/public_ats_reviewed_candidates.csv`를 확인한다.
2. `include` 37건은 빠른 원문 확인 후 최종 표본으로 옮긴다.
3. `hold` 6건은 원문 URL과 원본 JSON을 확인해 포함 또는 제외로 확정한다.
4. 최종 표본이 50건 미만이면 공개 ATS 보드를 추가 수집한다.

## 자동 검수 결과

- 결과 파일: `02_data/processed/public_ats_reviewed_candidates.csv`
- 요약 파일: `02_data/processed/public_ats_review_summary.md`
- include: 37건
- hold: 6건
- exclude: 0건
