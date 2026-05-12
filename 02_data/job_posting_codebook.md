# 채용공고 표본 코딩북

## 수집 방식

- `collection_method=auto`: robots.txt·서비스 약관·공개 API/다운로드 허용 범위 확인 후 저속 자동 수집.
- `collection_method=manual`: 작성자가 브라우저로 직접 확인해 수동 입력.
- 자동 수집 자료도 최종 표본 편입 전 작성자가 수동 검수한다.
- 로그인 우회, 캡차 우회, 유료벽 우회, 비공개 API 접근 자료는 제외한다.

## 직무 7분류

| normalized_role | 포함 기준 | 제외 기준 |
|---|---|---|
| data_scientist | 통계분석, 실험설계, 예측모델, BI/분석 중심 | 단순 리포팅·SQL 운영만 있는 공고 |
| ml_engineer | 모델 학습, 피처 엔지니어링, 모델 서빙, 성능 개선 | 일반 백엔드 개발만 있는 공고 |
| ai_deep_learning_engineer | NLP, CV, 추천, 음성, 딥러닝 모델 개발 | AI API 단순 호출만 있는 공고 |
| mlops_platform_engineer | ML 파이프라인, 배포, 모니터링, GPU/클라우드 인프라 | 일반 DevOps만 있는 공고 |
| applied_ai_developer | LLM API, RAG, 에이전트, AI 기능 제품화 | 단순 챗봇 운영·CS 기획만 있는 공고 |
| prompt_ai_operator | 프롬프트 설계, 평가, AI 운영, 데이터 검수 | 일반 콘텐츠 기획만 있는 공고 |
| ai_researcher | 논문 구현, 모델 구조 연구, 석박사·연구 실적 요구 | 제품 개발 중심 엔지니어 공고 |

## 스킬 태그

| 태그 | 포함 표현 예시 |
|---|---|
| python | Python, 파이썬 |
| pytorch | PyTorch |
| tensorflow | TensorFlow |
| sklearn | scikit-learn |
| sql | SQL, DB query |
| cloud | AWS, GCP, Azure, NCP |
| docker_k8s | Docker, Kubernetes, k8s |
| mlops | MLflow, Kubeflow, Airflow, feature store |
| llm | LLM, GPT, Claude, HyperCLOVA, EXAONE |
| rag | RAG, retrieval, vector DB |
| langchain | LangChain, LangGraph |
| vector_db | Pinecone, Milvus, Weaviate, FAISS |
| nlp | NLP, 자연어처리 |
| cv | Computer Vision, 영상처리 |
| recommender | 추천시스템 |
| data_labeling | 데이터 라벨링, 어노테이션, 검수 |
| domain_finance | 금융, 회계, 세무, 감사, 리스크 |
| domain_legal | 법무, 계약, 리걸테크 |
| domain_healthcare | 의료, 헬스케어 |

## 경험 수준

| experience_level | 기준 |
|---|---|
| entry | 신입, 0~2년 |
| junior | 1~3년 |
| mid | 3~5년 |
| senior | 6년 이상 |
| lead | 리드, 매니저, 아키텍트 |
| unknown | 공고에 명시 없음 |

## 중복 제거 규칙

1. 같은 회사, 같은 직무명, 같은 플랫폼, 같은 URL이면 1건으로 본다.
2. 같은 회사와 직무지만 플랫폼만 다르면 더 상세한 공고 1건만 남긴다.
3. 상시채용은 수집일을 기준일로 기록하고, 동일 분기 내 중복 수집하지 않는다.
4. 헤드헌팅·파견 공고는 원 고용주가 불명확하면 제외하거나 `notes`에 표시한다.

## 자동 수집 로그 필수 필드

| 필드 | 설명 |
|---|---|
| collection_method | `auto` 또는 `manual` |
| robots_terms_checked | robots.txt·약관 확인 여부 |
| source_log_id | `02_data/source_log.csv`의 로그 ID |
| request_interval_seconds | 자동 수집 요청 간격 |
| crawler_user_agent | 사용한 User-Agent |
| manual_reviewed | 작성자 수동 검수 여부 |

## 본문 사용 제한

- 표본 빈도는 시장 전체 비중이 아니라 수집 표본 내 관찰치다.
- 플랫폼·기간·키워드 선택 편향을 본문 방법론에 명시한다.
- 연봉 미공개 공고는 보상 분석에서 제외하고 제외 건수를 기록한다.
- 자동 수집이 허용된 플랫폼과 금지된 플랫폼을 구분해 적는다.
