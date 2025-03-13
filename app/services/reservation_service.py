# app/services/reservation_service.py

import pytz

from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status
from app.repositories.models import Reservation
from app.repositories.models import ReservationTime
from app.repositories.models import ReservationStatus
from app.repositories.models import Member
from app.exceptions import ReservationException
from datetime import datetime, timedelta


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
        raise Exception("Member not found")
    return member.role


def get_all_available_reservations(db: Session):
    # total_count가 50,000 미만인 예약 시간 정보만 가져오기
    available_reservations = db.query(ReservationTime).filter(ReservationTime.total_count < MAX_CONFIRMED_ATTENDEES).all()
    return available_reservations


def create_reservation_service(db: Session, member_id: int, reservation_time_id: int, count: int):
    # 예약 시간 정보 조회
    reservation_time = db.query(ReservationTime).filter(ReservationTime.id == reservation_time_id).first()
    
    if not reservation_time:
        raise ReservationException("예약 시간 정보가 존재하지 않습니다.")
    
    # 예약 시간 3일 전까지 신청 가능
    current_time = datetime.now(kst)
    if reservation_time.date_time - current_time > timedelta(days=MIN_DAYS_BEFORE_EXAM):
        raise ReservationException("예약은 시험 시작 3일 전까지 신청 가능합니다.")
    
    # 해당 예약 시간대의 총 예약 수 확인 (최대 5만명까지 예약 가능)
    # 예약된 참가자 수를 가져올 때, 상태가 CONFIRMED인 예약만 포함하도록 필터링
    total_reserved = db.query(func.sum(Reservation.count)) \
        .filter(Reservation.reservation_time_id == reservation_time_id) \
        .filter(Reservation.status == ReservationStatus.CONFIRMED) \
        .scalar() or 0
    
    if total_reserved + count > MAX_CONFIRMED_ATTENDEES:
        raise ReservationException("해당 시간대는 최대 예약 인원(50,000명)을 초과하여 예약할 수 없습니다.")
       # 트랜잭션을 하나로 묶기 위해 db.add(), db.commit(), db.refresh()를 한 번의 세션 내에서 수행
    try:
        # 예약 생성
        new_reservation = Reservation(
            member_id=member_id,
            reservation_time_id=reservation_time_id,
            count=count,
            status=ReservationStatus.PENDING
        )
        # 예약 데이터 추가
        db.add(new_reservation)

        # 예약 시간의 총 예약 수 업데이트
        reservation_time.total_count += count

        # 한 번의 커밋으로 모든 변경 사항 반영
        db.commit()  # 트랜잭션을 한 번만 커밋하여 모든 변경사항을 반영
        db.refresh(new_reservation)  # 새로 고침하여 추가된 예약 정보를 업데이트
        db.refresh(reservation_time)  # 예약 시간 정보도 새로 고침하여 업데이트된 상태 반영

        return new_reservation
    
    except Exception as e:
        db.rollback()  # 에러 발생 시 롤백
        raise ReservationException(f"예약 처리 중 오류가 발생했습니다: {str(e)}")

