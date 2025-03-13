# app/config/database.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# DATABASE_URL: 환경변수에서 가져오고 없으면 기본값 사용
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://test_user:test123@127.0.0.1:5432/test_db")

# 환경변수에서 풀 관련 설정을 가져오되, 없으면 기본 SQLAlchemy 기본값을 사용
# SQLAlchemy의 기본값
# - pool_size: 5
# - max_overflow: 10
# - pool_timeout: 30 (초)
# - pool_recycle: -1 (사용 안 함)
POOL_SIZE = int(os.getenv("PGSQL_POOL_MIN_SIZE", 5))
MAX_OVERFLOW = int(os.getenv("PGSQL_MAX_OVERFLOW", 10))
POOL_TIMEOUT = int(os.getenv("PGSQL_POOL_TIMEOUT", 30))
POOL_RECYCLE = int(os.getenv("PGSQL_POOL_RECYCLE", -1))

engine = create_engine(
    DATABASE_URL,
    pool_size=POOL_SIZE,
    max_overflow=MAX_OVERFLOW,
    pool_timeout=POOL_TIMEOUT,
    pool_recycle=POOL_RECYCLE
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
