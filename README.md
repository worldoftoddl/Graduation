# 졸업과제 프로젝트 사용 안내

## 파일 구성

- `AGENT.md` — 프로젝트 루트 컨텍스트. Codex/Claude 작업 시 우선 참고할 업무지시서.
- `agents/*.md` — Sub-agent 정의 파일들. `@agent-name` 형식으로 호출.
- `00_plan/` — 목차·방법론·일정·표본 설계.
- `01_research/sources.md` — 자료 인용 DB. 모든 본문 근거 자료는 여기에 먼저 등록.
- `01_research/notes/`, `01_research/raw/` — 자료별 요약 노트와 원문·스냅샷 보관.
- `02_data/` — 정량 데이터 CSV와 분석 노트북.
- `02_data/job_posting_collection_workflow.md` — 채용공고 자동 수집·수동 검수 실행 절차.
- `03_figures/` — 최종 차트 PNG와 생성 스크립트.
- `04_drafts/` — 장별 초안.
- `05_integrated/` — 통합본.
- `06_export/` — 제출용 DOCX/HWP 변환본.
- `99_archive/` — 폐기 초안과 이전 버전.

## Sub-agent 호출법

Claude Code에서 다음과 같이 호출:

```
@industry-analyst SPRi 2024 실태조사에서 한국 AI 산업 매출 규모 데이터를 찾아 정리해줘
@labor-market-analyst 2023~2026년 ML 엔지니어 채용 공고 추이 분석해줘
@domain-expert 삼정KPMG KymChat 도입 사례를 공식 자료 출처와 함께 정리해줘
@media-studies-framer 1장 서론에 카스텔의 네트워크 사회론을 어떻게 박을지 제안해줘
@devils-advocate 3장 초안의 방법론 약점을 검토해줘
@editor 4장 초안의 어색한 표현과 인용 양식 일관성을 점검해줘
```

## 출처 명시 강제 메커니즘

본 프로젝트는 출처 명시를 다음 4중으로 강제합니다:

1. `AGENT.md`에 절대 원칙으로 박힘
2. 각 sub-agent 프롬프트에 도메인별 출처원 화이트리스트와 함께 재명시
3. 표준 출처 양식 통일: `[출처: 기관명/저자, 「자료명」, 발행연도, 페이지(있으면), URL, 접근일 YYYY-MM-DD]`
4. 출처 미확보 시 `⚠ 출처 미확보` 형식으로 보고하도록 행동 규칙 박힘

## 본인 Voice 보존 메커니즘

Claude Code가 본문을 통째로 생성하지 않도록 다음 규칙이 강제됨:

- 모든 sub-agent는 "단락 통째 생성 금지" 원칙을 따름
- `@editor`는 원문을 그대로 두고 (a)·(b) 선택지 형식으로만 제안
- 본문은 작성자가 직접 쓰고, Claude Code는 (1) 구조 제안 (2) 표현 다듬기 (3) 사실 확인 (4) 출처 매칭에 한정

## 권장 Git 워크플로우

면담 시 본인 작성 증빙을 위해 매일 commit 누적:

```bash
git init
git add AGENT.md agents/ 01_research/
git commit -m "초기 프로젝트 셋업"

# 매일 작업 후
git add 04_drafts/
git commit -m "Day N: 3장 1절 초안 작성 (본인 작성)"
```

## 다음 단계 권장

1. **Phase 1 완료 점검**: 디렉토리 구조 생성, `AGENT.md`·sub-agent 배치 완료
2. **Phase 2 시작**: `@industry-analyst`로 SPRi·NIPA·통계청 자료부터 수집
3. **자료 등록**: `01_research/sources.md`에 30~50개 1차 자료 등록 (Phase 2 종료 기준)
4. **Phase 3**: 데이터 분석 노트북 작성, matplotlib 한국어 폰트 셋업
5. **Phase 4**: 장별 초안을 작성자가 직접 작성, Claude Code는 보조
