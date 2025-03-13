# app/controllers/reservation_controller.py

import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session

from app.dtos import schemas
from app.services import reservation_service
from app.config.database import SessionLocal

router = APIRouter(
    prefix="/reservations", 
    tags=["Reservations"],
    responses={404: {"description" : "Not Found"}}
    )

# 데이터베이스 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 간단한 역할 기반 인증 (헤더를 통해 역할과 사용자 ID 전달)
def get_current_user(x_user_role: str = Header(...), x_user_id: str = Header(...)):
    return {"role": x_user_role, "user_id": x_user_id}

# 고객은 예약 신청이 가능한 시간과 인원을 알 수 있습니다.
@router.get("/available", response_model=List[schemas.AvailableReservation])
def available_reservations(
    db: Session = Depends(get_db)
):
    data = reservation_service.get_all_available_reservations_service(db)
    if not data:
        raise HTTPException(status_code=404, detail="예약 가능한 일정 정보가 없습니다.")
    return data

