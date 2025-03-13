# app/main.py

from fastapi import FastAPI
from app.config.database import engine
from app.repositories import models
from app.controllers import reservation_controller

app = FastAPI(title="시험 일정 예약 시스템 API")

# 데이터베이스 테이블 생성 (최초 실행 시)
models.Base.metadata.create_all(bind=engine)

# 컨트롤러(라우터) 등록
app.include_router(reservation_controller.router)

@app.get("/")
def read_root():
  return {"Hello" : "World"}
