#DB 설정 및 모델


from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite DB 파일 설정
DATABASE_URL = "sqlite:///./scoreroute.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 'history'라는 이름의 테이블 구조 정의
class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, index=True)
    start = Column(String, index=True)
    destination = Column(String, index=True)

# DB와 테이블을 생성하는 함수
def create_tables():
    Base.metadata.create_all(bind=engine)