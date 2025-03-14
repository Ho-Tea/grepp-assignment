from fastapi import FastAPI
from app.config.database import engine, get_db
from app.repositories import models
from app.controllers import reservation_controller
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
import datetime
import pytz

# FastAPI 인스턴스 생성
app = FastAPI()

# 데이터베이스 테이블 생성 (최초 실행 시)
models.Base.metadata.create_all(bind=engine)

# 서버 시작 시 더미 데이터 삽입
@asynccontextmanager
async def lifespan(app: FastAPI):
    db: Session = next(get_db())
    
    # 한국 타임존 설정
    kst = pytz.timezone('Asia/Seoul')

    # 예약 시간 데이터 추가
    reservation_time_1 = models.ReservationTime(
        date_time=datetime.datetime.now(kst) + datetime.timedelta(days=5),  # 예약 시간 1
        total_count=45000
    )
    reservation_time_2 = models.ReservationTime(
        date_time=datetime.datetime.now(kst) + datetime.timedelta(days=6),  # 예약 시간 2
        total_count=100
    )
    reservation_time_3 = models.ReservationTime(
        date_time=datetime.datetime.now(kst) + datetime.timedelta(days=3) + datetime.timedelta(minutes=100),  # 예약 시간 3
        total_count=3000
    )
    reservation_time_4 = models.ReservationTime(
        date_time=datetime.datetime.now(kst) + datetime.timedelta(days=4),  # 예약 시간 4
        total_count=50000
    )
    reservation_time_5 = models.ReservationTime(
        date_time=datetime.datetime.now(kst) + datetime.timedelta(days=2),  # 예약 시간 5
        total_count=0
    )
    db.add(reservation_time_1)
    db.add(reservation_time_2)
    db.add(reservation_time_3)
    db.add(reservation_time_4)
    db.add(reservation_time_5)

    # 멤버 데이터 추가
    admin = models.Member(name="Admin User", role=models.Role.ADMIN)
    customer_1 = models.Member(name="Customer 1", role=models.Role.CUSTOMER)
    customer_2 = models.Member(name="Customer 2", role=models.Role.CUSTOMER)
    customer_3 = models.Member(name="Customer 3", role=models.Role.CUSTOMER)
    customer_4 = models.Member(name="Customer 4", role=models.Role.CUSTOMER)
    db.add(admin)
    db.add(customer_1)
    db.add(customer_2)
    db.add(customer_3)
    db.add(customer_4)

    # 예약 데이터 추가
    # Customer 1
    reservation_1 = models.Reservation(
        reservation_time_id=1,
        member_id=1,  # Customer 1
        count=40000,
        status=models.ReservationStatus.CONFIRMED
    )
    reservation_2 = models.Reservation(
        reservation_time_id=2,
        member_id=1,  # Customer 1
        count=100,
        status=models.ReservationStatus.CONFIRMED
    )

    # Customer 2
    reservation_3 = models.Reservation(
        reservation_time_id=4,
        member_id=2,  # Customer 2
        count=50000,
        status=models.ReservationStatus.CONFIRMED
    )

    # Customer 3
    reservation_4 = models.Reservation(
        reservation_time_id=3,
        member_id=3,  # Customer 3
        count=3000,
        status=models.ReservationStatus.CONFIRMED
    )
    reservation_5 = models.Reservation(
        reservation_time_id=1,
        member_id=3,  # Customer 3
        count=5000,
        status=models.ReservationStatus.CONFIRMED
    )
    reservation_6 = models.Reservation(
        reservation_time_id=3,
        member_id=3,  # Customer 3
        count=25000,
        status=models.ReservationStatus.PENDING
    )

    # Customer 4 (예약 안함)
    # No reservation for Customer 4

    db.add(reservation_1)
    db.add(reservation_2)
    db.add(reservation_3)
    db.add(reservation_4)
    db.add(reservation_5)
    db.add(reservation_6)

    # 커밋하여 데이터 저장
    db.commit()

    yield  # 서버가 종료될 때까지 대기
    
    # 서버 종료시 모든 데이터 삭제
    models.Base.metadata.drop_all(bind=db.get_bind())

app = FastAPI(lifespan=lifespan, title="시험 일정 예약 시스템 API")

app.include_router(reservation_controller.router)


