from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import UserQuery  # UserQuery 모델을 가져옵니다.
import os

# 데이터베이스 URL 가져오기
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/padong"

# 데이터베이스 연결 설정
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def view_user_queries():
    # DB와 연결하고 데이터 조회
    with SessionLocal() as db:
        user_queries = db.query(UserQuery).all()  # UserQuery 테이블의 모든 데이터 가져오기

        # 데이터 출력
        print("User Queries:")
        for query in user_queries:
            print(f"User ID: {query.user_id}, Utterance: {query.utterance}, Created At: {query.created_at}")

if __name__ == "__main__":
    view_user_queries()
