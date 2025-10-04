from services.user_service import UserService
from services.course_service import CourseService
from services.enrollment_service import EnrollmentService

# Initialize services
user_service = UserService()
course_service = CourseService()
enrollment_service = EnrollmentService(user_service, course_service)
