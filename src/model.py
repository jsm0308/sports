# app/ml_model.py

import pandas as pd
import numpy as np
import lightgbm as lgb
import joblib
import os

# --- 1. 가상 데이터 생성 ---
def generate_dummy_data(num_rows=10000):
    """모델 학습 및 테스트를 위한 가상 데이터를 생성합니다."""
    data = {
        '관객_수': np.random.randint(0, 30001, size=num_rows),
        '요일': np.random.randint(1, 8, size=num_rows),
        '주말_여부': np.random.randint(0, 2, size=num_rows),
        '시간대': np.round(np.random.uniform(21.0, 23.5, size=num_rows), 1),
        '강수량_mm': np.round(np.random.exponential(1.0, size=num_rows) - 0.5, 1).clip(0),
        '기온_C': np.random.uniform(10, 30, size=num_rows),
    }
    df = pd.DataFrame(data)
    df.loc[df.sample(frac=0.7).index, '관객_수'] = 0
    df['혼잡도_증가량'] = ((df['관객_수'] * 0.005) + (df['주말_여부'] * 10) + 
                       (df['강수량_mm'] * 2) + np.random.normal(0, 5, size=num_rows)).clip(0)
    return df

# --- 2. 모델 학습 ---
def train_and_save_model():
    """LightGBM 모델을 학습시키고 파일로 저장합니다."""
    print("모델 학습을 시작합니다...")
    df = generate_dummy_data()
    features = ['관객_수', '요일', '주말_여부', '시간대', '강수량_mm', '기온_C']
    target = '혼잡도_증가량'
    
    X = df[features]
    y = df[target]
    
    model = lgb.LGBMRegressor(objective='regression_l1', random_state=42)
    model.fit(X, y)
    
    # 모델 저장 디렉토리 생성
    os.makedirs('../models', exist_ok=True)
    model_path = '../models/congestion_model.pkl'
    joblib.dump(model, model_path)
    print(f"모델 학습 완료. '{model_path}'에 저장되었습니다.")
    return model

# --- 3. 모델 예측 ---
# 모델 파일을 불러오기 (없으면 학습)
try:
    model = joblib.load('../models/congestion_model.pkl')
except FileNotFoundError:
    model = train_and_save_model()

def predict_congestion(features_df):
    """학습된 모델로 혼잡도 증가량을 예측합니다."""
    prediction = model.predict(features_df)
    return prediction[0]

# --- 이 파일을 직접 실행할 경우 모델 학습 진행 ---
if __name__ == '__main__':
    train_and_save_model()

    # 예측 함수 테스트
    test_features = pd.DataFrame([{
        '관객_수': 25000, '요일': 5, '주말_여부': 1, 
        '시간대': 22.0, '강수량_mm': 0, '기온_C': 25
    }])
    predicted_increase = predict_congestion(test_features)
    print(f"\n[테스트] 예측된 혼잡도 증가량: {predicted_increase:.2f}%p")