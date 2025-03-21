# app/dtos/schemas.py

import datetime
from pydantic import BaseModel
from app.repositories.models import ReservationStatus

class AvailableReservation(BaseModel):
    id: int
    date_time: datetime
    remaining_count: int

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class Reservation(BaseModel):
    id: int
    member_id: int
    reservation_time_id: int
    count: int
    status: ReservationStatus
    created_at: datetime

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ReservationRequest(BaseModel):
    reservation_time_id: int
    count: int

class ReservationUpdateRequest(BaseModel):
    count: int