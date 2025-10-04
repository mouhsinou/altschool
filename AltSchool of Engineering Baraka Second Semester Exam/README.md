# EduTrack Lite API

A simple course management system for tracking user enrollments and course completion built with FastAPI.

## Features

- **User Management**: Create, read, update, delete, and deactivate users
- **Course Management**: Create, read, update, delete courses and manage enrollment status
- **Enrollment Management**: Enroll users in courses, track completion, and view enrollment details
- **Data Validation**: Pydantic models for request/response validation
- **In-Memory Storage**: Simple data persistence using Python dictionaries
- **Comprehensive Testing**: Full test coverage for all endpoints

## Project Structure

```
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── test_api.py            # Comprehensive test suite
├── schemas/               # Pydantic models
│   ├── __init__.py
│   ├── user.py           # User schemas
│   ├── course.py         # Course schemas
│   └── enrollment.py     # Enrollment schemas
├── services/             # Business logic layer
│   ├── __init__.py
│   ├── user_service.py   # User operations
│   ├── course_service.py # Course operations
│   └── enrollment_service.py # Enrollment operations
└── routes/               # API endpoints
    ├── __init__.py
    ├── users.py          # User endpoints
    ├── courses.py        # Course endpoints
    └── enrollments.py    # Enrollment endpoints
```

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- **Interactive API docs**: `http://localhost:8000/docs`
- **ReDoc documentation**: `http://localhost:8000/redoc`

## API Endpoints

### Users (`/users`)

- `POST /users/` - Create a new user
- `GET /users/` - Get all users
- `GET /users/{user_id}` - Get a specific user
- `PUT /users/{user_id}` - Update a user
- `DELETE /users/{user_id}` - Delete a user
- `PATCH /users/{user_id}/deactivate` - Deactivate a user

### Courses (`/courses`)

- `POST /courses/` - Create a new course
- `GET /courses/` - Get all courses
- `GET /courses/{course_id}` - Get a specific course
- `PUT /courses/{course_id}` - Update a course
- `DELETE /courses/{course_id}` - Delete a course
- `PATCH /courses/{course_id}/close-enrollment` - Close course enrollment
- `GET /courses/{course_id}/enrollments` - Get all users enrolled in a course

### Enrollments (`/enrollments`)

- `POST /enrollments/` - Enroll a user in a course
- `GET /enrollments/` - Get all enrollments
- `GET /enrollments/{enrollment_id}` - Get a specific enrollment
- `PUT /enrollments/{enrollment_id}` - Update an enrollment
- `PATCH /enrollments/{enrollment_id}/complete` - Mark course completion
- `GET /enrollments/user/{user_id}` - Get all enrollments for a user
- `DELETE /enrollments/{enrollment_id}` - Delete an enrollment

## Data Models

### User
```json
{
  "id": 1,
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "is_active": true,
  "created_at": "2025-01-16T10:30:00"
}
```

### Course
```json
{
  "id": 1,
  "title": "Python Basics",
  "description": "Learn Python programming fundamentals",
  "is_open": true,
  "created_at": "2025-01-16T10:30:00"
}
```

### Enrollment
```json
{
  "id": 1,
  "user_id": 1,
  "course_id": 1,
  "enrolled_date": "2025-01-16",
  "completed": false,
  "created_at": "2025-01-16T10:30:00",
  "user_name": "Alice Johnson",
  "course_title": "Python Basics"
}
```

## Business Rules

### Enrollment Rules
- Only active users can enroll in courses
- Courses must be open for enrollment
- Users cannot enroll twice in the same course
- Enrollment date is automatically set to the current date

### User Management
- Users are active by default when created
- Deactivated users cannot enroll in new courses
- Existing enrollments remain valid for deactivated users

### Course Management
- Courses are open for enrollment by default
- Closing enrollment prevents new enrollments
- Existing enrollments remain valid for closed courses

## Running Tests

```bash
pytest test_api.py -v
```

The test suite includes:
- Unit tests for all endpoints
- Integration tests for complete workflows
- Error handling tests
- Business rule validation tests

## Example Usage

### Create a User
```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice Johnson", "email": "alice@example.com"}'
```

### Create a Course
```bash
curl -X POST "http://localhost:8000/courses/" \
  -H "Content-Type: application/json" \
  -d '{"title": "Python Basics", "description": "Learn Python programming"}'
```

### Enroll User in Course
```bash
curl -X POST "http://localhost:8000/enrollments/" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "course_id": 1}'
```

### Mark Course Completion
```bash
curl -X PATCH "http://localhost:8000/enrollments/1/complete"
```

## Status Codes

- `200` - Success
- `201` - Created
- `204` - No Content (for deletions)
- `400` - Bad Request (validation errors, business rule violations)
- `404` - Not Found
- `422` - Unprocessable Entity (Pydantic validation errors)

## Notes

- Authentication is not required for this API
- Data is stored in memory and will be lost when the server restarts
- Email validation is enforced using Pydantic's EmailStr
- All timestamps are in ISO format
- The API includes CORS middleware for cross-origin requests
