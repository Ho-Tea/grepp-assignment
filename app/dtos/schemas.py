# app/dtos/schemas.py

import datetime
from pydantic import BaseModel
from typing import Optional

class AvailableReservation(BaseModel):
    id: int
    date_time: datetime
    total_count: int

    class Config:
        orm_mode = True
