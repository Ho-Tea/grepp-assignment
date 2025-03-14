# app/repositories/models.py

import pytz
import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as PyEnum

Base = declarative_base()

# 한국 타임존 설정
kst = pytz.timezone('Asia/Seoul')

# 예약 상태 정의
class ReservationStatus(PyEnum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"

# 권한 정의
class Role(PyEnum):
    CUSTOMER = "CUSTOMER"
    ADMIN = "ADMIN"

class Reservation(Base):
    __tablename__ = "reservations"
    
    id = Column(Integer, primary_key=True, index=True)
    reservation_time_id = Column(Integer, ForeignKey('reservation_times.id'), nullable=False)  # reservation_time 테이블과의 관계
    member_id = Column(Integer, ForeignKey('members.id'), nullable=False)  # member 테이블과의 관계
    count = Column(Integer, nullable=True)  # 예비 참가자 수
    status = Column(Enum(ReservationStatus), default=ReservationStatus.PENDING)  # 상태 (PENDING 기본값)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now(kst))

    # 예약 시간과 멤버와의 관계 설정
    reservation_time = relationship("ReservationTime", back_populates="reservations")
    member = relationship("Member", back_populates="reservations")

class ReservationTime(Base):
    __tablename__ = "reservation_times"
    
    id = Column(Integer, primary_key=True, index=True)
    date_time = Column(DateTime, nullable=False)  # 예약 날짜 및 시간
    total_count = Column(Integer, nullable=False)  # 예약한 수

    # 예약 시간과 예약 테이블과의 관계 설정
    reservations = relationship("Reservation", back_populates="reservation_time")

class Member(Base):
    __tablename__ = "members"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    role = Column(Enum(Role), default=Role.CUSTOMER)  # 상태 (CUSTOMER 기본값)
    # 멤버와 예약 테이블과의 관계 설정
    reservations = relationship("Reservation", back_populates="member")
