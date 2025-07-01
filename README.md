# 공주대처럼 챗봇 (RAG 기반)

공주대학교 학생들을 위한 AI 챗봇 시스템입니다. RAG(Retrieval Augmented Generation) 기술을 활용하여 다음과 같은 정보를 제공합니다:

- 📢 공지사항
- 🍽️ 식단메뉴  
- 🚌 셔틀버스 정보
- 📅 학사일정
- 🎯 동아리 정보

## 기술 스택

- **Python 3.10+**
- **LangChain**: RAG 파이프라인 구축
- **ChromaDB**: 벡터 데이터베이스
- **Sentence Transformers**: 한국어 임베딩
- **FastAPI**: API 서버
- **KoNLPy**: 한국어 자연어 처리

## 프로젝트 구조

```
gongju-chatbot/
├── src/                    # 소스 코드
│   ├── config/            # 설정 관리
│   ├── data/              # 데이터 수집 및 전처리
│   ├── vectorstore/       # 벡터DB 관리
│   ├── retrieval/         # 검색 시스템
│   ├── generation/        # LLM 연동
│   └── chatbot/           # 챗봇 인터페이스
├── tests/                 # 테스트 코드
├── data/                  # 로컬 데이터 저장소
├── notebooks/             # 실험용 Jupyter 노트북
└── requirements.txt       # 의존성 관리
```

## 설치 및 실행

### 1. 환경 설정
```bash
# 가상환경 활성화 (PyCharm에서 자동 처리)
pip install -r requirements.txt
```

### 2. 환경 변수 설정
`.env` 파일에서 다음 값들을 설정하세요:
- OpenAI API 키
- 기존 서비스 API URL들

### 3. 실행
```bash
# 개발 서버 시작
python -m src.chatbot.interface
```

## 개발 로드맵

- [x] 프로젝트 초기 설정
- [ ] 데이터 수집 파이프라인 구축
- [ ] 벡터 데이터베이스 구축
- [ ] RAG 시스템 구현
- [ ] 챗봇 인터페이스 개발
- [ ] 성능 최적화
- [ ] 프로덕션 배포

## 기여하기

1. Fork the Project
2. Create your Feature Branch
3. Commit your Changes
4. Push to the Branch
5. Open a Pull Request

## 라이선스

MIT License
