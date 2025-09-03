🏟️ ScoreRoute
ScoreRoute는 대형 스포츠 경기 종료 후의 혼잡도를 예측하고, 사용자에게 최적의 귀가 경로를 추천하는 데이터 기반 특화 서비스입니다. 경기 후 스트레스 없이 가장 쾌적하고 빠른 귀갓길을 찾아보세요.

📖 프로젝트 개요
핵심 컨셉
경기 종료 후 예측된 혼잡도를 기반으로, 특정 시간(예: 경기 종료 후 30분)에 최악의 혼잡을 피할 수 있는 최적의 귀가 경로를 추천합니다. '현재'가 아닌 '미래'의 교통 상황을 예측하여 '경기장 좌석'에서 '최종 목적지'까지의 전 과정을 책임지는 End-to-End 경로를 제공하는 것을 목표로 합니다.

주요 기능
미래 혼잡도 예측: LightGBM 모델을 사용하여 경기 관중 수, 요일, 날씨 등을 기반으로 경기장 주변의 미래 혼잡도를 예측합니다.

하이브리드 경로 탐색: 경기장 영향권(반경 2km) 내에서는 자체 예측 모델을, 그 외 지역에서는 실시간 교통 정보를 활용하여 정확성과 효율성을 동시에 확보합니다.

체감 지표 제공: 추상적인 '혼잡' 대신 **'예상 추가 대기 시간(분)'**과 같이 사용자가 체감할 수 있는 구체적인 지표로 예측 결과를 제시합니다.

🛠️ 기술 스택
구분

기술

Backend

Python, FastAPI, Uvicorn

Database

SQLite, SQLAlchemy (ORM)

Frontend

HTML, CSS, JavaScript, Naver Maps API

ML/Data

Pandas, Scikit-learn, LightGBM

Tooling

Git, GitHub, VS Code

📂 폴더 구조
프로젝트는 각 기능의 역할을 명확하게 분리하여 관리의 효율성을 높이는 구조를 따릅니다.

📁 ScoreRoute/ (프로젝트 최상위 폴더)
│
├── 📁 app/               # 🐍 백엔드 FastAPI 서버 코드
│   ├── __init__.py
│   ├── config.py         # config.ini 파일을 읽어오는 설정 모듈
│   ├── database.py       # DB 연결 및 세션 관리
│   ├── main.py           # API 엔드포인트(경로)를 정의하는 메인 파일
│   └── models.py         # DB 테이블 구조를 정의하는 모델 파일
│
├── 📁 data/               # 📊 원본 데이터 파일
│   └── raw/
│       ├── kbo_attendance.csv
│       └── station.csv
│
├── 📁 ml_models/          # 🤖 훈련된 머신러닝 모델 (.pkl 파일 등)
│   └── congestion_model.pkl
│
├── 📁 scripts/            # 🛠️ 일회성 유틸리티 스크립트
│   ├── import_csv.py     # CSV를 DB로 옮기는 스크립트
│   └── check_db.py       # DB 내용을 확인하는 스크립트
│
├── 📁 static/             # 🌐 프론트엔드 (HTML/CSS/JS) 파일
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── 📄 .gitignore          # Git이 버전 관리에서 제외할 파일/폴더 목록
├── 📄 config.ini          # (직접 생성) API 키 등 민감한 정보 저장
├── 📄 requirements.txt    # 프로젝트에 필요한 파이썬 라이브러리 목록
└── 🗄️ scoreroute.db       # (자동 생성) SQLite 데이터베이스 파일

app/: API 서버의 핵심 로직이 모두 들어있는 심장부입니다.

data/: 분석에 사용할 원본 CSV 파일들을 보관합니다.

ml_models/: 훈련을 마친 머신러닝 모델 파일(.pkl)을 저장합니다.

scripts/: DB에 데이터를 넣거나 확인하는 등 개발에 필요한 보조 스크립트들을 모아둡니다.

static/: 사용자가 직접 보게 될 웹페이지 관련 파일들을 모두 이곳에 둡니다.

config.ini: (중요) API 키와 같이 민감한 정보를 저장하는 파일입니다. 보안을 위해 .gitignore에 등록되어 Github에 올라가지 않습니다.

scoreroute.db: 서버를 처음 실행할 때 자동으로 생성되는 실제 데이터베이스 파일입니다.

🚀 실행 방법 (Getting Started)
1. 환경 설정 (Environment Setup)
# 1. 프로젝트 저장소를 복제합니다.
git clone [https://github.com/jsm0308/sports.git](https://github.com/jsm0308/sports.git)
cd sports

# 2. 필요한 라이브러리를 설치합니다.
pip install -r requirements.txt

2. API 키 및 설정 (API Keys & Configuration)
config.ini 파일에 Naver Cloud Platform에서 발급받은 API 키와 DB 설정을 입력해야 합니다.

# 1. 프로젝트 최상위 폴더에 config.ini 파일을 생성합니다.

# 2. 아래 내용을 복사하여 붙여넣고, 실제 키 값으로 수정합니다.

[NAVER_API]
CLIENT_ID = YOUR_NAVER_CLIENT_ID
CLIENT_SECRET = YOUR_NAVER_CLIENT_SECRET

[DATABASE]
DB_URL = sqlite:///./scoreroute.db

⚠️ 중요: config.ini 파일은 민감 정보를 담고 있으므로, .gitignore에 반드시 포함하여 외부에 노출되지 않도록 해야 합니다.

3. 데이터베이스 초기화 (Database Initialization)
data/ 폴더에 있는 CSV 데이터를 SQLite 데이터베이스에 저장합니다. 이 과정은 최초 1회만 수행하면 됩니다.

# -m 옵션을 사용하여 프로젝트 모듈로 스크립트를 실행합니다.
python -m scripts.import_csv

4. 머신러닝 모델 학습 (Train ML Model)
저장된 데이터를 기반으로 혼잡도 예측 모델을 학습시키고 ml_models/congestion_model.pkl 파일을 생성합니다.

# (ml_model.py 스크립트 경로에 맞게 수정 필요)
python ml_model.py

5. API 서버 실행 (Run API Server)
모든 설정이 완료되면, FastAPI 서버를 실행합니다.

# 포트 충돌을 피하기 위해 8001번 포트를 사용합니다.
uvicorn app.main:app --reload --port 8001

서버가 성공적으로 실행되면 터미널에 Application startup complete. 메시지가 나타납니다. 이제 웹 브라우저에서 http://127.0.0.1:5500/static/index.html (Live Server 기준)로 접속하여 서비스를 테스트할 수 있으며, API 문서는 http://127.0.0.1:8001/docs에서 확인할 수 있습니다.

🔄 데이터 및 서비스 파이프라인
ScoreRoute는 다음과 같은 흐름으로 동작합니다.

[Offline] 데이터 수집 및 전처리: 국민체육진흥공단의 프로스포츠 관람객 데이터, 경기 일정, 공간/교통 데이터를 수집하고 가공하여 분석용 데이터셋을 구축합니다.

[Offline] 모델 학습: 구축된 데이터셋을 사용하여 LightGBM 알고리즘으로 경기 후 혼잡도를 예측하는 모델(congestion_model.pkl)을 학습시킵니다.

[Online] 경로 요청: 사용자가 웹 화면에서 출발지(경기장)와 목적지를 입력하고 '경로 탐색'을 요청합니다.

[Online] 기본 경로 탐색: 백엔드 서버는 요청을 받아 Naver Directions API를 호출하여 기본적인 대중교통 경로 후보들을 가져옵니다.

[Online] 혼잡도 예측 적용: 백엔드 서버는 미리 학습된 congestion_model.pkl을 로드하여, 경로 후보에 포함된 경기장 주변 정류장/역의 **'예상 추가 대기 시간'**을 계산합니다.

[Online] 최종 경로 결정: A* 알고리즘을 기반으로 기본 경로의 소요 시간과 예측된 '혼잡도 페널티'를 종합하여 사용자에게 가장 쾌적하고 효율적인 최종 경로를 결정합니다.

[Online] 결과 시각화: 백엔드 서버는 최종 경로 데이터를 GeoJSON 형태로 프론트엔드에 전달하고, 프론트엔드는 이를 받아 지도 위에 시각적으로 표시합니다.