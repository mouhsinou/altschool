from fastapi import APIRouter, HTTPException, status
from typing import List
from schemas.enrollment import Enrollment, EnrollmentCreate, EnrollmentUpdate, EnrollmentWithDetails
from services.enrollment_service import EnrollmentService
from services.user_service import UserService
from services.course_service import CourseService

router = APIRouter(prefix="/enrollments", tags=["enrollments"])

# Initialize services
user_service = UserService()
course_service = CourseService()
enrollment_service = EnrollmentService(user_service, course_service)


@router.post("/", response_model=Enrollment, status_code=status.HTTP_201_CREATED)
def create_enrollment(enrollment_data: EnrollmentCreate):
    """Enroll a user in a course"""
    enrollment = enrollment_service.create_enrollment(enrollment_data)
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot enroll user. User may not exist, be inactive, course may not exist, be closed, or user may already be enrolled."
        )
    return enrollment


@router.get("/", response_model=List[EnrollmentWithDetails])
def get_all_enrollments():
    """Get all enrollments"""
    return enrollment_service.get_all_enrollments()


@router.get("/{enrollment_id}", response_model=EnrollmentWithDetails)
def get_enrollment(enrollment_id: int):
    """Get a specific enrollment by ID"""
    enrollment = enrollment_service.get_enrollment(enrollment_id)
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )
    
    # Get user and course details
    user = user_service.get_user(enrollment.user_id)
    course = course_service.get_course(enrollment.course_id)
    
    if not user or not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Associated user or course not found"
        )
    
    return EnrollmentWithDetails(
        **enrollment.dict(),
        user_name=user.name,
        course_title=course.title
    )


@router.put("/{enrollment_id}", response_model=Enrollment)
def update_enrollment(enrollment_id: int, enrollment_data: EnrollmentUpdate):
    """Update an enrollment"""
    enrollment = enrollment_service.update_enrollment(enrollment_id, enrollment_data)
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )
    return enrollment


@router.patch("/{enrollment_id}/complete", response_model=Enrollment)
def mark_course_completion(enrollment_id: int):
    """Mark course completion for an enrollment"""
    enrollment = enrollment_service.mark_completion(enrollment_id)
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )
    return enrollment


@router.get("/user/{user_id}", response_model=List[EnrollmentWithDetails])
def get_user_enrollments(user_id: int):
    """Get all enrollments for a specific user"""
    # Check if user exists
    user = user_service.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return enrollment_service.get_user_enrollments(user_id)


@router.delete("/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_enrollment(enrollment_id: int):
    """Delete an enrollment"""
    if not enrollment_service.delete_enrollment(enrollment_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )
