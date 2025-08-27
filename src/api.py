# app/main.py

from fastapi import FastAPI
import pandas as pd
from . import ml_model  # ml_model.py의 함수들을 import
from . import pathfinder # pathfinder.py의 함수들을 import

app = FastAPI()

# 교통 네트워크 그래프는 서버 시작 시 한 번만 생성
transport_graph = pathfinder.create_transport_graph()

@app.get("/")
def read_root():
    return {"message": "Safe Route API"}

@app.post("/route")
def get_route(
    start: str = "경기장", 
    end: str = "집", 
    mode: str = "comfortable", 
    spectators: int = 25000
    ):
    """
    입력된 정보를 바탕으로 최적 경로를 계산하여 반환합니다.
    """
    # 1. 혼잡도 예측
    # 실제로는 날씨, 시간 등 더 많은 피처가 필요하지만, MVP에서는 관객 수만으로 단순화
    features_for_prediction = pd.DataFrame([{
        '관객_수': spectators, '요일': 5, '주말_여부': 1, 
        '시간대': 22.0, '강수량_mm': 0, '기온_C': 25
    }])
    predicted_increase = ml_model.predict_congestion(features_for_prediction)
    
    # 평상시 혼잡도(예: 80%)에 증가량을 더함
    final_congestion = 80 + predicted_increase
    
    # 2. 경로 탐색
    optimal_path = pathfinder.find_optimal_path(
        graph=transport_graph,
        start=start,
        end=end,
        mode=mode,
        predicted_congestion=final_congestion
    )
    
    return {
        "mode": mode,
        "predicted_congestion_percent": round(final_congestion, 2),
        "optimal_path": optimal_path
    }