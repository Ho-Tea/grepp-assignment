# app/controllers/reservation_controller.py

import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from app.exceptions import ReservationException
from app.dtos import schemas
from app.services import reservation_service
from app.services.reservation_service import get_member_role
from app.config.database import get_db

router = APIRouter(
    prefix="/reservations", 
    tags=["Reservations"],
    responses={404: {"description" : "Not Found"}}
    )

def check_member_role_admin(member_id: str = Header(...), db: Session = Depends(get_db)):
    # DB에서 member_id로 역할을 조회
    try:
        role = get_member_role(db, int(member_id))  # member_id는 str로 전달되므로 int로 변환
    except Exception as e:
        raise HTTPException(status_code=400, detail="Member not found or error fetching role")
    
    # 역할이 Admin이면 접근 허용, 아니면 거부
    if role != "Admin":
        raise HTTPException(status_code=403, detail="Access forbidden: Admin role required.")
    
    return role

# 예약 신청이 가능한 시간과 인원을 알 수 있습니다. - CUSTOMER, ADMIN 모두 가능
@router.get("/available", response_model=List[schemas.AvailableReservation])
def available_reservations(
    db: Session = Depends(get_db)
):
    data = reservation_service.get_all_available_reservations(db)
    if not data:
        raise HTTPException(status_code=404, detail="예약 가능한 일정 정보가 없습니다.")
    return data

# 고객 예약 생성 API - CUSTOMER, ADMIN 모두 가능
@router.post("", response_model=schemas.Reservation)
def create_reservation(
    request: schemas.ReservationRequest,
    member_id: int = Header(...),
    db: Session = Depends(get_db)
):
    try:
        reservation = reservation_service.create_reservation_service(db, member_id, request.reservation_time_id, request.count)
        return reservation
    except ReservationException as e:
        raise HTTPException(status_code=400, detail=str(e))
    
# 고객의 모든 예약을 조회하는 API - CUSTOMER 전용
@router.get("/customer", response_model=List[schemas.Reservation])
def get_customer_reservations(
    member_id: int = Header(...),
    db: Session = Depends(get_db)
):
    # 해당 member_id의 모든 예약을 조회
    reservations = reservation_service.get_reservations_by_customer(db, member_id)
    
    if not reservations:
        raise HTTPException(status_code=404, detail="조회된 예약이 없습니다.")
    
    return reservations


# 고객의 모든 예약을 조회하는 API - ADMIN 전용
@router.get("/customer-reservation/{member_id}", response_model=List[schemas.Reservation])
def get_customer_reservations_by_admin(
    member_id: int,
    role: str = Depends(check_member_role_admin),
    db: Session = Depends(get_db)
):
    # 해당 member_id의 모든 예약을 조회
    reservations = reservation_service.get_reservations_by_customer(db, member_id)
    
    if not reservations:
        raise HTTPException(status_code=404, detail="조회된 예약이 없습니다.")
    
    return reservations


# 예약 확정 API - ADMIN 전용
@router.post("/confirm/{reservation_id}", response_model=schemas.Reservation)
def confirm_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    role: str = Depends(check_member_role_admin)
):
    try:
        reservation = reservation_service.confirm_reservation(db, reservation_id)
        return reservation
    except HTTPException as e:
        raise e
    

# 고객 예약 수정 API - CUSTOMER 전용
@router.put("/{reservation_id}", response_model=schemas.Reservation)
def update_reservation(
    reservation_id: int,
    request: schemas.ReservationUpdateRequest,
    db: Session = Depends(get_db),
    member_id: int = Header(...),
):
    reservation = reservation_service.update_reservation(db, reservation_id, request.count, member_id)
    return reservation

