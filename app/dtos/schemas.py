# app/dtos/schemas.py

import datetime
from pydantic import BaseModel
from typing import Optional
from app.repositories.models import ReservationStatus

class AvailableReservation(BaseModel):
    id: int
    date_time: datetime
    total_count: int

    class Config:
        orm_mode = True

class Reservation(BaseModel):
    id: int
    member_id: int
    reservation_time_id: int
    count: int
    status: ReservationStatus
    created_at: datetime

    class Config:
        orm_mode = True