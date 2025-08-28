# 🏟️ Safe Route: 스마트 귀가 비서 프로젝트

대형 스포츠 경기 종료 후의 혼잡도를 예측하고, 사용자에게 최적의 귀가 경로를 추천하는 서비스입니다.

## 🚀 실행 방법

1.  **저장소 복제 (Clone)**
    ```bash
    git clone [https://github.com/jsm0308/sports.git](https://github.com/jsm0308/sports.git)
    cd sports
    ```

2.  **필요한 라이브러리 설치**
    ```bash
    pip install -r requirements.txt
    ```

3.  **⭐️ 혼잡도 예측 모델 학습 (가장 중요)**
    아래 명령어를 실행하여 `models/` 폴더와 `congestion_model.pkl` 파일을 로컬 환경에 생성합니다. 이 과정은 최초 1회만 수행하면 됩니다.
    ```bash
    python app/ml_model.py
    ```

4.  **API 서버 실행**
    ```bash
    uvicorn app.main:app --reload
    ```
    서버가 실행되면 http://127.0.0.1:8000 에서 API를 테스트할 수 있습니다.

    
체육시설 인접 대중교통 정보
https://www.bigdata-culture.kr/bigdata/user/data_market/detail.do?id=615e7eb0-6e17-11ee-88b4-1384e6e2c3c9
    
    
