import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float # 데이터 타입에 맞게 추가
from app.database import Base, DATABASE_URL

# CSV 파일 경로 (파일 이름은 실제 파일에 맞게 수정하세요)
CSV_PATH = 'data/raw/station.csv' 

# DB 테이블 이름
TABLE_NAME = 'kbo_attendance'

# SQLAlchemy 엔진 생성
engine = create_engine(DATABASE_URL)

# 1. DB에 만들 테이블의 구조를 정의합니다. (CSV 파일의 컬럼과 맞춰주세요)
class KboAttendance(Base):
    __tablename__ = TABLE_NAME
    id = Column(Integer, primary_key=True, index=True)
    date = Column(String)
    stadium = Column(String)
    home_team = Column(String)
    away_team = Column(String)
    attendance = Column(Integer)
    # 필요한 컬럼들을 여기에 추가...

# 2. 테이블이 없다면 새로 생성합니다.
Base.metadata.create_all(bind=engine)

# 3. CSV 파일을 Pandas DataFrame으로 읽어옵니다.
df = pd.read_csv(CSV_PATH)

# 4. DataFrame을 SQL 테이블에 저장합니다.
# if_exists='replace'는 기존에 테이블이 있으면 덮어쓰라는 의미입니다.
df.to_sql(TABLE_NAME, con=engine, if_exists='replace', index=False)

print(f"'{CSV_PATH}' 파일의 데이터가 '{TABLE_NAME}' 테이블에 성공적으로 저장되었습니다.")