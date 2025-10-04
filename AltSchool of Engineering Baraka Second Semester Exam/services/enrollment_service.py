from typing import List, Optional, Dict
from datetime import datetime, date
from schemas.enrollment import Enrollment, EnrollmentCreate, EnrollmentUpdate, EnrollmentWithDetails
from services.user_service import UserService
from services.course_service import CourseService


class EnrollmentService:
    def __init__(self, user_service: UserService, course_service: CourseService):
        self.enrollments: Dict[int, Enrollment] = {}
        self.next_id = 1
        self.user_service = user_service
        self.course_service = course_service

    def create_enrollment(self, enrollment_data: EnrollmentCreate) -> Optional[Enrollment]:
        # Check if user exists and is active
        user = self.user_service.get_user(enrollment_data.user_id)
        if not user or not user.is_active:
            return None
        
        # Check if course exists and is open
        course = self.course_service.get_course(enrollment_data.course_id)
        if not course or not course.is_open:
            return None
        
        # Check if user is already enrolled in this course
        for enrollment in self.enrollments.values():
            if (enrollment.user_id == enrollment_data.user_id and 
                enrollment.course_id == enrollment_data.course_id):
                return None
        
        enrollment = Enrollment(
            id=self.next_id,
            user_id=enrollment_data.user_id,
            course_id=enrollment_data.course_id,
            enrolled_date=date.today(),
            completed=False,
            created_at=datetime.now()
        )
        self.enrollments[self.next_id] = enrollment
        self.next_id += 1
        return enrollment

    def get_enrollment(self, enrollment_id: int) -> Optional[Enrollment]:
        return self.enrollments.get(enrollment_id)

    def get_all_enrollments(self) -> List[EnrollmentWithDetails]:
        enrollments_with_details = []
        for enrollment in self.enrollments.values():
            user = self.user_service.get_user(enrollment.user_id)
            course = self.course_service.get_course(enrollment.course_id)
            
            if user and course:
                enrollment_detail = EnrollmentWithDetails(
                    **enrollment.dict(),
                    user_name=user.name,
                    course_title=course.title
                )
                enrollments_with_details.append(enrollment_detail)
        
        return enrollments_with_details

    def get_user_enrollments(self, user_id: int) -> List[EnrollmentWithDetails]:
        user_enrollments = []
        for enrollment in self.enrollments.values():
            if enrollment.user_id == user_id:
                user = self.user_service.get_user(enrollment.user_id)
                course = self.course_service.get_course(enrollment.course_id)
                
                if user and course:
                    enrollment_detail = EnrollmentWithDetails(
                        **enrollment.dict(),
                        user_name=user.name,
                        course_title=course.title
                    )
                    user_enrollments.append(enrollment_detail)
        
        return user_enrollments

    def get_course_enrollments(self, course_id: int) -> List[EnrollmentWithDetails]:
        course_enrollments = []
        for enrollment in self.enrollments.values():
            if enrollment.course_id == course_id:
                user = self.user_service.get_user(enrollment.user_id)
                course = self.course_service.get_course(enrollment.course_id)
                
                if user and course:
                    enrollment_detail = EnrollmentWithDetails(
                        **enrollment.dict(),
                        user_name=user.name,
                        course_title=course.title
                    )
                    course_enrollments.append(enrollment_detail)
        
        return course_enrollments

    def update_enrollment(self, enrollment_id: int, enrollment_data: EnrollmentUpdate) -> Optional[Enrollment]:
        if enrollment_id not in self.enrollments:
            return None
        
        enrollment = self.enrollments[enrollment_id]
        update_data = enrollment_data.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(enrollment, field, value)
        
        return enrollment

    def mark_completion(self, enrollment_id: int) -> Optional[Enrollment]:
        if enrollment_id not in self.enrollments:
            return None
        
        self.enrollments[enrollment_id].completed = True
        return self.enrollments[enrollment_id]

    def delete_enrollment(self, enrollment_id: int) -> bool:
        if enrollment_id in self.enrollments:
            del self.enrollments[enrollment_id]
            return True
        return False