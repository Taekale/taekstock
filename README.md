# 📈 스마트 주식 추천 시스템 (Smart Stock Recommendation)

본 프로젝트는 최신 계량투자(Quantitative Investing) 기법과 머신러닝 알고리즘(**XGBoost**)을 융합한 로컬 구동형 주식 가치 평가 및 추천 시스템입니다. 

사용자가 검색하는 미국/한국 개별 종목의 밸류에이션 정보와 핵심 재무 정보를 수집 및 평가하고, 시장 내 상대적 백분위수를 기준으로 다차원 추천 엔진을 가동합니다.

---

## ✨ 핵심 기능 (Key Features)

1. **상대 평가 백분위수 랭킹 시스템**:
   - 주가수익비율(PER), 주가순자산비율(PBR), 주가매출비율(PSR), 자기자본이익률(ROE)을 시장별(US / KR) 유니버스 내에서 상대 순위로 정규화합니다. 특정 국가 및 업종 고유의 밸류에이션 왜곡 현상을 보정합니다.
2. **뉴스 감정 분석 기반 호재 지표 반영**:
   - 야후 파이낸스의 최근 기업 관련 뉴스 헤드라인들을 로컬 감성 어휘 매칭 엔진을 통해 분석하여 0.0 ~ 1.0 범위의 **실시간 뉴스 호재 점수(Sentiment Score)**를 산출합니다.
3. **유동성 팩터 결합**:
   - 일일 거래량(Volume)과 거래대금(Trading Value)을 백분위 랭킹에 편입하여, 거래 유동성이 풍부하고 시장의 주목을 받는 핵심 종목을 변별합니다.
4. **XGBoost Regressor 기보강**:
   - 가치(Valuation 40%), 수익성(ROE 30%), 시장 심리(News Sentiment 20%), 유동성(Volume & Value 10%)을 조합한 종합 매력도 타겟 데이터를 생성하고, 이를 규제화(Regularization)된 XGBoost 모델로 학습시켜 최적의 추천 점수를 예측합니다.
5. **안정적인 25% 분위 분배 (Empty State 방지)**:
   - 예측 점수의 평균 수축 현상을 보완하기 위해 예측 점수의 시장 내 상대 서열을 측정하여 등급을 매깁니다:
     - **상위 10%**: 강력 매수 (Strong Buy)
     - **상위 10% ~ 25%**: 매수 (Buy)
     - **중간 50%**: 관망 (Neutral)
     - **하위 15%**: 매도 (Sell)
     - **최하위 10%**: 강력 매도 (Strong Sell)
6. **실시간 & 자동 백그라운드 업데이트**:
   - **실시간 갱신**: 사용자가 캐싱된 종목을 검색하더라도 5분이 지났다면 실시간 정보로 즉시 강제 리프레시합니다.
   - **자동 백그라운드 동기화**: 서버 실행 시 독립된 데몬 스레드가 작동하여 10분마다 자동으로 전체 시장 동기화(Full Sync)를 실행합니다.
   - **자동 대시보드 리로드**: 브라우저 화면에서 수동 조작 없이 60초 간격으로 대시보드 리스트를 자동 갱신합니다.
7. **프리미엄 다크 글래스모피즘 UI**:
   - 고대비 폰트 및 모던한 블러 배경, 동적 차트 그래픽, 한국어 AI 상세 요약 단락을 지원하는 디테일 모달을 제공합니다.

---

## 🛠 기술 스택 (Tech Stack)

- **Backend**: Python 3.x, FastAPI, Uvicorn, SQLite3
- **Machine Learning**: XGBoost, Scikit-learn, Pandas, Numpy
- **Data Source**: Yahoo Finance API (`yfinance`)
- **Frontend**: HTML5, Vanilla CSS (Variables, Flexbox/Grid), Vanilla Javascript

---

## 🚀 시작하기 (Quick Start)

### 1. 의존성 패키지 설치
로컬 PC의 터미널(Command Prompt 또는 PowerShell)에서 아래 명령어를 실행하여 필수 라이브러리를 설치합니다.
```bash
pip install uvicorn fastapi yfinance pandas xgboost scikit-learn lxml html5lib
```

### 2. 프로그램 실행
프로젝트 루트 폴더에서 제공하는 실행 스크립트를 실행합니다.
```bash
python run.py
```
- 실행 시 자동으로 데이터베이스 스키마와 한국거래소(KRX) 상장사 이름 매핑 데이터를 초기 수립합니다.
- 데이터베이스가 비어 있을 경우 자동으로 백그라운드 동기화를 실행하며, 웹 브라우저가 실행되어 `http://127.0.0.1:8000` 주소로 대시보드 페이지를 띄워줍니다.

---

## 📁 폴더 구조 (Folder Structure)

```text
├── backend/
│   ├── db.py          # SQLite 데이터베이스 생성, 검색 매핑 및 CRUD 로직
│   ├── scanner.py     # 야후 파이낸스 I/O, 뉴스 감성 점수 계산 및 XGBoost 랭킹 처리
│   ├── main.py        # FastAPI 라우팅, 실시간 캐시 갱신 및 백그라운드 동기화 스레드
│   └── test_logic.py  # 단위/통합 알고리즘 및 랭킹 정합성 테스트 코드
├── static/
│   ├── index.html     # 글래스모피즘 레이아웃 및 디테일 모달 뼈대
│   ├── style.css      # 브랜드 가이드라인 CSS 토큰, 모달 및 반응형 그리드 스타일
│   └── app.js         # DOM 이벤트 바인딩, 실시간 갱신 폴러 및 한글 AI 요약 생성기
├── run.py             # 데이터베이스 자가 치유 및 자동 웹 브라우징 구동 런처
├── stocks.db          # 로컬 SQLite 캐시 데이터베이스 파일 (Git 관리 제외)
└── README.md          # 프로젝트 문서
```
