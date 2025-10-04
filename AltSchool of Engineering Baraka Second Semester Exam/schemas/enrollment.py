from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date


class EnrollmentBase(BaseModel):
    user_id: int
    course_id: int


class EnrollmentCreate(EnrollmentBase):
    pass


class EnrollmentUpdate(BaseModel):
    completed: Optional[bool] = None


class Enrollment(EnrollmentBase):
    id: int
    enrolled_date: date
    completed: bool = False
    created_at: datetime

    class Config:
        from_attributes = True


class EnrollmentWithDetails(Enrollment):
    user_name: str
    course_title: str
