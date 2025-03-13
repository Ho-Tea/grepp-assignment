# app/services/reservation_service.py

import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status
from app.repositories.models import Reservation
from app.repositories.models import ReservationTime
from app.repositories.models import Customer
from app.dtos.schemas import ReservationCreate, ReservationUpdate

# 상수 값
MAX_CONFIRMED_ATTENDEES = 50000
MIN_DAYS_BEFORE_EXAM = 3


def get_all_available_reservations_service(db: Session):
    # total_count가 50,000 미만인 예약 시간 정보만 가져오기
    available_reservations = db.query(ReservationTime).filter(ReservationTime.total_count < MAX_CONFIRMED_ATTENDEES).all()
    return available_reservations
