# 공주대처럼 챗봇 (RAG 기반)

공주대학교 학생들을 위한 AI 챗봇 시스템입니다. RAG(Retrieval Augmented Generation) 기술을 활용하여 다음과 같은 정보를 제공합니다:

- 📢 공지사항
- 🍽️ 식단메뉴  
- 🚌 셔틀버스 정보
- 📅 학사일정
- 🎯 동아리 정보

## 기술 스택

- **Python 3.9+**
- **LangChain**: RAG 파이프라인 구축
- **ChromaDB**: 벡터 데이터베이스
- **KoSimCSE**: 한국어 임베딩 (BM-K/KoSimCSE-roberta-multitask)
- **FastAPI**: API 서버 (예정)

## 프로젝트 구조

```
like-knu-rag/
├── src/                    # 소스 코드
│   ├── models.py          # 데이터 모델 정의
│   ├── document_loader.py # 문서 로더
│   ├── embeddings.py      # 임베딩 처리
│   └── __init__.py
├── tests/                 # 테스트 코드
│   ├── test_basic.py      # 기본 기능 테스트
│   └── __init__.py
├── data/                  # 데이터 저장소 (자동 생성)
├── requirements.txt       # 의존성 관리
├── .env                   # 환경 변수
└── README.md
```

## 설치 및 실행

### 1. 환경 설정
```bash
# 가상환경 생성 및 활성화
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

### 2. 환경 변수 설정
`.env` 파일에서 다음 값들을 설정하세요:
```env
EMBEDDING_MODEL=BM-K/KoSimCSE-roberta-multitask
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. 테스트 실행
```bash
python tests/test_basic.py
```

## 현재 구현 상태

- [x] ✅ 프로젝트 초기 설정
- [x] ✅ 데이터 모델링 (공지사항)
- [x] ✅ 문서 로더 구현
- [x] ✅ 한국어 임베딩 시스템
- [x] ✅ 캠퍼스별 필터링
- [ ] 🚧 벡터 데이터베이스 구축 (ChromaDB)
- [ ] 🚧 RAG 검색 시스템
- [ ] 🚧 챗봇 인터페이스
- [ ] 🚧 실제 데이터 연동
- [ ] 🚧 API 서버 구축

## 개발 로드맵

### Phase 1: 기반 시스템 (완료)
- [x] 데이터 모델링
- [x] 문서 처리 파이프라인
- [x] 한국어 임베딩 시스템

### Phase 2: RAG 시스템 (진행 중)
- [ ] ChromaDB 벡터 저장소
- [ ] 문서 검색 시스템
- [ ] 질의응답 파이프라인

### Phase 3: 실용화
- [ ] 실제 데이터 연동
- [ ] REST API 개발
- [ ] 웹 인터페이스
- [ ] 성능 최적화

## 주요 특징

### 🇰🇷 한국어 특화
- **KoSimCSE-RoBERTa-multitask** 모델 사용
- 한국어 문서에 최적화된 성능
- 다국어 모델 대비 **6~10배 향상**된 정확도

### 🎯 캠퍼스별 맞춤형
- 사용자 캠퍼스에 따른 정보 필터링
- 신관/천안/예산 캠퍼스 지원

### 📚 확장 가능한 구조
- 공지사항 외 다양한 정보 타입 지원 가능
- 모듈화된 설계로 기능 추가 용이

## 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 라이선스

MIT License
