from fastapi import APIRouter, HTTPException, status
from typing import List
from schemas.course import Course, CourseCreate, CourseUpdate
from schemas.enrollment import EnrollmentWithDetails
from services.course_service import CourseService
from services.enrollment_service import EnrollmentService
from services.user_service import UserService

router = APIRouter(prefix="/courses", tags=["courses"])

# Initialize services
user_service = UserService()
course_service = CourseService()
enrollment_service = EnrollmentService(user_service, course_service)


@router.post("/", response_model=Course, status_code=status.HTTP_201_CREATED)
def create_course(course_data: CourseCreate):
    """Create a new course"""
    return course_service.create_course(course_data)


@router.get("/", response_model=List[Course])
def get_all_courses():
    """Get all courses"""
    return course_service.get_all_courses()


@router.get("/{course_id}", response_model=Course)
def get_course(course_id: int):
    """Get a specific course by ID"""
    course = course_service.get_course(course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    return course


@router.put("/{course_id}", response_model=Course)
def update_course(course_id: int, course_data: CourseUpdate):
    """Update a course"""
    course = course_service.update_course(course_id, course_data)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    return course


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int):
    """Delete a course"""
    if not course_service.delete_course(course_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )


@router.patch("/{course_id}/close-enrollment", response_model=Course)
def close_enrollment(course_id: int):
    """Close enrollment for a course"""
    course = course_service.close_enrollment(course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    return course


@router.get("/{course_id}/enrollments", response_model=List[EnrollmentWithDetails])
def get_course_enrollments(course_id: int):
    """Get all users enrolled in a particular course"""
    # Check if course exists
    course = course_service.get_course(course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    return enrollment_service.get_course_enrollments(course_id)
