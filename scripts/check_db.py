import pandas as pd
from sqlalchemy import create_engine
# 현재 파일의 상위 폴더(프로젝트 루트)를 시스템 경로에 추가
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.config import DATABASE_URL # config에서 DB 주소 가져오기

# DB에 연결할 엔진 생성
engine = create_engine(DATABASE_URL)

# 확인하고 싶은 테이블 이름
# 이 이름만 바꾸면 어떤 테이블이든 확인할 수 있습니다.
TABLE_NAME = 'kbo_attendance' 

try:
    # SQLAlchemy 엔진을 사용해 DB 테이블을 직접 DataFrame으로 읽기
    df = pd.read_sql_table(TABLE_NAME, con=engine)

    print(f"✅ '{TABLE_NAME}' 테이블 데이터 불러오기 성공!")
    print("\n[테이블 정보]")
    df.info() # 컬럼별 정보 출력

    print("\n[데이터 미리보기 (상위 5개)]")
    print(df.head()) # 상위 5개 데이터 출력

except Exception as e:
    print(f"❌ 오류 발생: {e}")
    print(f"'{TABLE_NAME}' 테이블이 DB에 존재하는지 확인해주세요.")