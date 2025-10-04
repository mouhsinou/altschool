from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CourseBase(BaseModel):
    title: str
    description: str


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_open: Optional[bool] = None


class Course(CourseBase):
    id: int
    is_open: bool = True
    created_at: datetime

    class Config:
        from_attributes = True


class CourseEnrollmentStatus(BaseModel):
    is_open: bool
