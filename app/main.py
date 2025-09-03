#FastAPI 메인 앱



from fastapi import FastAPI
from pydantic import BaseModel

# FastAPI 앱 생성
app = FastAPI()

# 프론트엔드에서 받을 데이터 형식을 미리 정의
class RouteRequest(BaseModel):
    start: str
    destination: str
    mode: str # 'fastest' 또는 'comfortable'

# 기본 접속(루트) 주소
@app.get("/")
def read_root():
    return {"message": "ScoreRoute API 서버에 오신 것을 환영합니다!"}

# 경로 추천 API 엔드포인트
@app.post("/route")
def get_route(request: RouteRequest):
    print(f"경로 탐색 요청 수신: {request.start} -> {request.destination} (모드: {request.mode})")

    # 1. TODO: 혼잡도 예측 모델 로드 (.pkl 파일)

    # 2. TODO: 네이버 길찾기 API 호출 (안전하게 Client Secret 사용)

    # 3. TODO: 예측된 혼잡도를 반영하여 A* 알고리즘으로 최종 경로 계산

    # 4. 계산된 최종 경로 데이터를 GeoJSON 형태로 프론트엔드에 반환
    mock_path_data = {
        "path": [
            [127.0982, 37.5113], [127.099, 37.5105], [127.100, 37.5090],
            [127.028, 37.4982]
        ]
    }
    return mock_path_data