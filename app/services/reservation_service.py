# app/services/reservation_service.py

import pytz

from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status
from app.repositories.models import Reservation
from app.repositories.models import ReservationTime
from app.repositories.models import ReservationStatus
from app.repositories.models import Member
from app.exceptions.exceptions import ReservationException
from datetime import datetime, timedelta
from app.dtos.schemas import AvailableReservation

# 한국 타임존 설정
kst = pytz.timezone('Asia/Seoul')

# 상수 값
MAX_CONFIRMED_ATTENDEES = 50000
MIN_DAYS_BEFORE_EXAM = 3

# member_id를 기반으로 role을 가져오는 함수
def get_member_role(db: Session, member_id: int):
    # DB에서 member_id로 해당 Member를 조회하고, 역할을 반환
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise ReservationException("해당하는 멤버를 찾을 수 없습니다.")
    return member.role


def get_all_available_reservations(db: Session):
    three_days_later = datetime.now(kst) + timedelta(days=MIN_DAYS_BEFORE_EXAM)
    available_reservations = db.query(ReservationTime).filter(
        ReservationTime.date_time >= three_days_later,  # 예약 시간이 3일 후 이상
        ReservationTime.total_count < MAX_CONFIRMED_ATTENDEES  # 최대 인원수 기준 필터링
        ).all()
    available_reservations_dto = []
    for reservation_time in available_reservations:
        remaining_count = MAX_CONFIRMED_ATTENDEES - reservation_time.total_count
        available_reservations_dto.append(AvailableReservation(
                id=reservation_time.id,
                date_time=reservation_time.date_time,
                remaining_count=remaining_count
            ))
    return available_reservations_dto


def create_reservation(db: Session, member_id: int, reservation_time_id: int, count: int):
    try:
        # 예약 시간 정보 조회
        reservation_time = db.query(ReservationTime).filter(ReservationTime.id == reservation_time_id).first()
    
        if not reservation_time:
            raise ReservationException("예약 시간 정보가 존재하지 않습니다.")
    
        # 예약 시간 3일 전까지 신청 가능
        current_time = datetime.now(kst)
        if kst.localize(reservation_time.date_time) - current_time < timedelta(days=MIN_DAYS_BEFORE_EXAM):
            raise ReservationException("예약은 시험 시작 3일 전까지만 신청 가능합니다.")
    
        # 해당 예약 시간대의 총 예약 수 확인 (최대 5만명까지 예약 가능)
        # 예약된 참가자 수를 가져올 때, 상태가 CONFIRMED인 예약만 포함하도록 필터링
        total_reserved = db.query(func.sum(Reservation.count)) \
            .filter(Reservation.reservation_time_id == reservation_time_id) \
            .filter(Reservation.status == ReservationStatus.CONFIRMED) \
            .scalar() or 0
    
        if total_reserved + count > MAX_CONFIRMED_ATTENDEES:
            raise ReservationException("해당 시간대에 요청하신 예약인원은 최대 예약 가능 인원을 초과하여 예약할 수 없습니다.")
       
        # 예약 생성
        new_reservation = Reservation(
            member_id=member_id,
            reservation_time_id=reservation_time_id,
            count=count,
            status=ReservationStatus.PENDING
        )
        # 예약 데이터 추가
        db.add(new_reservation)
        db.commit()
        db.refresh(new_reservation)
        return new_reservation
    
    except Exception as e:
        db.rollback()  # 에러 발생 시 롤백
        raise ReservationException(f"예약 처리 중 오류가 발생했습니다: {str(e)}")


def get_reservations_by(db: Session, member_id: int):
    # 특정 고객의 모든 예약 조회
    reservations = db.query(Reservation).filter(Reservation.member_id == member_id).all()
    return reservations


def confirm_reservation(db: Session, reservation_id: int):
    try:
        # 예약 조회
        reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
        if not reservation:
            raise HTTPException(status_code=404, detail="예약을 찾을 수 없습니다.")
        if reservation.status == ReservationStatus.CONFIRMED:
            raise HTTPException(status_code=400, detail="이미 확정된 예약입니다.")
    
        # 예약 시간 조회
        reservation_time = reservation.reservation_time    
        # 최대 인원 수 확인 (예약 시간대의 현재 예약 인원이 최대 인원수를 넘지 않도록 체크)
        total_reserved_count = db.query(func.sum(Reservation.count)) \
            .filter(Reservation.reservation_time_id == reservation_time.id, 
                Reservation.status == ReservationStatus.CONFIRMED) \
            .scalar() or 0
        if total_reserved_count + reservation.count > MAX_CONFIRMED_ATTENDEES:
            raise HTTPException(status_code=400, detail="예약 가능한 최대 인원을 초과하였습니다.")
        
        # 예약 확정
        reservation.status = ReservationStatus.CONFIRMED
        # 예약 시간의 총 예약 수 증가
        reservation_time.total_count += reservation.count
        db.commit()
        db.refresh(reservation)
        db.refresh(reservation_time)
        return reservation

    except Exception as e:
        db.rollback()  # 에러 발생 시 롤백
        raise ReservationException(f"예약 확정 처리 중 오류가 발생했습니다: {str(e)}")
    

def update_reservation(db: Session, reservation_id: int, count: int, member_id: int):
    try:
        # 예약 조회
        reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
        if not reservation:
            raise HTTPException(status_code=404, detail="예약을 찾을 수 없습니다.")
    
        # 예약 수정 권한 체크
        if reservation.member_id != member_id:
            raise HTTPException(status_code=403, detail="예약을 수정할 수 있는 권한이 없습니다.")
        
        # 예약 상태가 CONFIRMED이면 수정할 수 없도록 함
        if reservation.status == ReservationStatus.CONFIRMED:
            raise HTTPException(status_code=403, detail="확정된 예약은 수정할 수 없습니다.")
    
        # 예약 수정
        reservation.count = count
        db.commit()
        db.refresh(reservation)
    
        return reservation
    except Exception as e:
        db.rollback()  # 에러 발생 시 롤백
        raise ReservationException(f"예약 수정 중 오류가 발생했습니다: {str(e)}")
    

def update_reservation_by_admin(db: Session, reservation_id: int, count: int):
    try:
        # 예약 조회
        reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
        if not reservation:
            raise HTTPException(status_code=404, detail="예약을 찾을 수 없습니다.")
    
        # 예약 수정
        reservation.count = count
        db.commit()
        db.refresh(reservation)
    
        return reservation
    except Exception as e:
        db.rollback()  # 에러 발생 시 롤백
        raise ReservationException(f"예약 수정 중 오류가 발생했습니다: {str(e)}")
    
# 고객 예약 삭제 서비스 - CUSTOMER 전용
def delete_reservation(db: Session, reservation_id: int, member_id: int):
    try:
        # 예약 조회
        reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
        if not reservation:
            raise HTTPException(status_code=404, detail="예약을 찾을 수 없습니다.")
    
        # 예약 삭제 권한 체크
        if reservation.member_id != member_id:
            raise HTTPException(status_code=403, detail="예약을 삭제할 수 있는 권한이 없습니다.")
        
        # 예약 상태가 CONFIRMED이면 삭제할 수 없도록 함
        if reservation.status == ReservationStatus.CONFIRMED:
            raise HTTPException(status_code=403, detail="확정된 예약은 삭제할 수 없습니다.")
    
        # 예약 삭제
        db.delete(reservation)
        db.commit()
        return reservation
    except Exception as e:
        db.rollback()  # 에러 발생 시 롤백
        raise ReservationException(f"예약 삭제 중 오류가 발생했습니다: {str(e)}")
    

# 관리자 예약 삭제 서비스 - ADMIN 전용
def delete_reservation_by_admin(db: Session, reservation_id: int):
    try:
        # 예약 조회
        reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
        if not reservation:
            raise HTTPException(status_code=404, detail="예약을 찾을 수 없습니다.")
    
        # 예약 삭제
        db.delete(reservation)
        db.commit()
        return reservation
    except Exception as e:
        db.rollback()  # 에러 발생 시 롤백
        raise ReservationException(f"예약 삭제 중 오류가 발생했습니다: {str(e)}")
