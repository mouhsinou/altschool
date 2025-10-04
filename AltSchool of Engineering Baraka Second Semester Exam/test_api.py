import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestUserEndpoints:
    """Test cases for User endpoints"""
    
    def test_create_user(self):
        """Test creating a new user"""
        user_data = {
            "name": "Alice Johnson",
            "email": "alice@example.com"
        }
        response = client.post("/users/", json=user_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == user_data["name"]
        assert data["email"] == user_data["email"]
        assert data["is_active"] is True
        assert "id" in data
        assert "created_at" in data

    def test_get_all_users(self):
        """Test getting all users"""
        # Create a user first
        user_data = {"name": "Bob Smith", "email": "bob@example.com"}
        client.post("/users/", json=user_data)
        
        response = client.get("/users/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert any(user["name"] == "Bob Smith" for user in data)

    def test_get_user_by_id(self):
        """Test getting a specific user by ID"""
        # Create a user first
        user_data = {"name": "Charlie Brown", "email": "charlie@example.com"}
        create_response = client.post("/users/", json=user_data)
        user_id = create_response.json()["id"]
        
        response = client.get(f"/users/{user_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == user_data["name"]
        assert data["email"] == user_data["email"]

    def test_get_nonexistent_user(self):
        """Test getting a user that doesn't exist"""
        response = client.get("/users/999")
        assert response.status_code == 404
        assert "User not found" in response.json()["detail"]

    def test_update_user(self):
        """Test updating a user"""
        # Create a user first
        user_data = {"name": "David Wilson", "email": "david@example.com"}
        create_response = client.post("/users/", json=user_data)
        user_id = create_response.json()["id"]
        
        # Update the user
        update_data = {"name": "David Wilson Jr.", "email": "david.jr@example.com"}
        response = client.put(f"/users/{user_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == update_data["name"]
        assert data["email"] == update_data["email"]

    def test_deactivate_user(self):
        """Test deactivating a user"""
        # Create a user first
        user_data = {"name": "Eve Adams", "email": "eve@example.com"}
        create_response = client.post("/users/", json=user_data)
        user_id = create_response.json()["id"]
        
        # Deactivate the user
        response = client.patch(f"/users/{user_id}/deactivate")
        assert response.status_code == 200
        data = response.json()
        assert data["is_active"] is False

    def test_delete_user(self):
        """Test deleting a user"""
        # Create a user first
        user_data = {"name": "Frank Miller", "email": "frank@example.com"}
        create_response = client.post("/users/", json=user_data)
        user_id = create_response.json()["id"]
        
        # Delete the user
        response = client.delete(f"/users/{user_id}")
        assert response.status_code == 204
        
        # Verify user is deleted
        get_response = client.get(f"/users/{user_id}")
        assert get_response.status_code == 404


class TestCourseEndpoints:
    """Test cases for Course endpoints"""
    
    def test_create_course(self):
        """Test creating a new course"""
        course_data = {
            "title": "Python Basics",
            "description": "Learn Python programming fundamentals"
        }
        response = client.post("/courses/", json=course_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == course_data["title"]
        assert data["description"] == course_data["description"]
        assert data["is_open"] is True
        assert "id" in data
        assert "created_at" in data

    def test_get_all_courses(self):
        """Test getting all courses"""
        # Create a course first
        course_data = {"title": "JavaScript Advanced", "description": "Advanced JavaScript concepts"}
        client.post("/courses/", json=course_data)
        
        response = client.get("/courses/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert any(course["title"] == "JavaScript Advanced" for course in data)

    def test_get_course_by_id(self):
        """Test getting a specific course by ID"""
        # Create a course first
        course_data = {"title": "React Fundamentals", "description": "Learn React basics"}
        create_response = client.post("/courses/", json=course_data)
        course_id = create_response.json()["id"]
        
        response = client.get(f"/courses/{course_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == course_data["title"]
        assert data["description"] == course_data["description"]

    def test_update_course(self):
        """Test updating a course"""
        # Create a course first
        course_data = {"title": "Vue.js Basics", "description": "Learn Vue.js"}
        create_response = client.post("/courses/", json=course_data)
        course_id = create_response.json()["id"]
        
        # Update the course
        update_data = {"title": "Vue.js Advanced", "description": "Advanced Vue.js concepts"}
        response = client.put(f"/courses/{course_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == update_data["title"]
        assert data["description"] == update_data["description"]

    def test_close_enrollment(self):
        """Test closing enrollment for a course"""
        # Create a course first
        course_data = {"title": "Angular Basics", "description": "Learn Angular"}
        create_response = client.post("/courses/", json=course_data)
        course_id = create_response.json()["id"]
        
        # Close enrollment
        response = client.patch(f"/courses/{course_id}/close-enrollment")
        assert response.status_code == 200
        data = response.json()
        assert data["is_open"] is False

    def test_delete_course(self):
        """Test deleting a course"""
        # Create a course first
        course_data = {"title": "Node.js Basics", "description": "Learn Node.js"}
        create_response = client.post("/courses/", json=course_data)
        course_id = create_response.json()["id"]
        
        # Delete the course
        response = client.delete(f"/courses/{course_id}")
        assert response.status_code == 204
        
        # Verify course is deleted
        get_response = client.get(f"/courses/{course_id}")
        assert get_response.status_code == 404


class TestEnrollmentEndpoints:
    """Test cases for Enrollment endpoints"""
    
    def test_create_enrollment(self):
        """Test creating a new enrollment"""
        # Create a user and course first
        user_data = {"name": "Grace Lee", "email": "grace@example.com"}
        user_response = client.post("/users/", json=user_data)
        user_id = user_response.json()["id"]
        
        course_data = {"title": "Django Basics", "description": "Learn Django"}
        course_response = client.post("/courses/", json=course_data)
        course_id = course_response.json()["id"]
        
        # Create enrollment
        enrollment_data = {"user_id": user_id, "course_id": course_id}
        response = client.post("/enrollments/", json=enrollment_data)
        assert response.status_code == 201
        data = response.json()
        assert data["user_id"] == user_id
        assert data["course_id"] == course_id
        assert data["completed"] is False
        assert "enrolled_date" in data

    def test_create_enrollment_inactive_user(self):
        """Test creating enrollment with inactive user"""
        # Create a user and deactivate them
        user_data = {"name": "Henry Ford", "email": "henry@example.com"}
        user_response = client.post("/users/", json=user_data)
        user_id = user_response.json()["id"]
        client.patch(f"/users/{user_id}/deactivate")
        
        # Create a course
        course_data = {"title": "Flask Basics", "description": "Learn Flask"}
        course_response = client.post("/courses/", json=course_data)
        course_id = course_response.json()["id"]
        
        # Try to create enrollment
        enrollment_data = {"user_id": user_id, "course_id": course_id}
        response = client.post("/enrollments/", json=enrollment_data)
        assert response.status_code == 400
        assert "Cannot enroll user" in response.json()["detail"]

    def test_create_enrollment_closed_course(self):
        """Test creating enrollment in closed course"""
        # Create a user
        user_data = {"name": "Ivy Chen", "email": "ivy@example.com"}
        user_response = client.post("/users/", json=user_data)
        user_id = user_response.json()["id"]
        
        # Create a course and close enrollment
        course_data = {"title": "FastAPI Basics", "description": "Learn FastAPI"}
        course_response = client.post("/courses/", json=course_data)
        course_id = course_response.json()["id"]
        client.patch(f"/courses/{course_id}/close-enrollment")
        
        # Try to create enrollment
        enrollment_data = {"user_id": user_id, "course_id": course_id}
        response = client.post("/enrollments/", json=enrollment_data)
        assert response.status_code == 400
        assert "Cannot enroll user" in response.json()["detail"]

    def test_create_duplicate_enrollment(self):
        """Test creating duplicate enrollment"""
        # Create a user and course
        user_data = {"name": "Jack Wilson", "email": "jack@example.com"}
        user_response = client.post("/users/", json=user_data)
        user_id = user_response.json()["id"]
        
        course_data = {"title": "SQL Basics", "description": "Learn SQL"}
        course_response = client.post("/courses/", json=course_data)
        course_id = course_response.json()["id"]
        
        # Create first enrollment
        enrollment_data = {"user_id": user_id, "course_id": course_id}
        client.post("/enrollments/", json=enrollment_data)
        
        # Try to create duplicate enrollment
        response = client.post("/enrollments/", json=enrollment_data)
        assert response.status_code == 400
        assert "Cannot enroll user" in response.json()["detail"]

    def test_get_all_enrollments(self):
        """Test getting all enrollments"""
        # Create enrollment first
        user_data = {"name": "Kate Brown", "email": "kate@example.com"}
        user_response = client.post("/users/", json=user_data)
        user_id = user_response.json()["id"]
        
        course_data = {"title": "MongoDB Basics", "description": "Learn MongoDB"}
        course_response = client.post("/courses/", json=course_data)
        course_id = course_response.json()["id"]
        
        enrollment_data = {"user_id": user_id, "course_id": course_id}
        client.post("/enrollments/", json=enrollment_data)
        
        response = client.get("/enrollments/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert any(enrollment["user_name"] == "Kate Brown" for enrollment in data)

    def test_get_user_enrollments(self):
        """Test getting enrollments for a specific user"""
        # Create user and enrollments
        user_data = {"name": "Liam Davis", "email": "liam@example.com"}
        user_response = client.post("/users/", json=user_data)
        user_id = user_response.json()["id"]
        
        # Create multiple courses and enroll user
        course1_data = {"title": "Redis Basics", "description": "Learn Redis"}
        course1_response = client.post("/courses/", json=course1_data)
        course1_id = course1_response.json()["id"]
        
        course2_data = {"title": "PostgreSQL Basics", "description": "Learn PostgreSQL"}
        course2_response = client.post("/courses/", json=course2_data)
        course2_id = course2_response.json()["id"]
        
        # Enroll user in both courses
        client.post("/enrollments/", json={"user_id": user_id, "course_id": course1_id})
        client.post("/enrollments/", json={"user_id": user_id, "course_id": course2_id})
        
        response = client.get(f"/enrollments/user/{user_id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(enrollment["user_id"] == user_id for enrollment in data)

    def test_get_course_enrollments(self):
        """Test getting enrollments for a specific course"""
        # Create course and multiple users
        course_data = {"title": "Docker Basics", "description": "Learn Docker"}
        course_response = client.post("/courses/", json=course_data)
        course_id = course_response.json()["id"]
        
        # Create multiple users and enroll them
        user1_data = {"name": "Maya Patel", "email": "maya@example.com"}
        user1_response = client.post("/users/", json=user1_data)
        user1_id = user1_response.json()["id"]
        
        user2_data = {"name": "Noah Kim", "email": "noah@example.com"}
        user2_response = client.post("/users/", json=user2_data)
        user2_id = user2_response.json()["id"]
        
        # Enroll both users in the course
        client.post("/enrollments/", json={"user_id": user1_id, "course_id": course_id})
        client.post("/enrollments/", json={"user_id": user2_id, "course_id": course_id})
        
        response = client.get(f"/courses/{course_id}/enrollments")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(enrollment["course_id"] == course_id for enrollment in data)

    def test_mark_course_completion(self):
        """Test marking course completion"""
        # Create enrollment first
        user_data = {"name": "Olivia Taylor", "email": "olivia@example.com"}
        user_response = client.post("/users/", json=user_data)
        user_id = user_response.json()["id"]
        
        course_data = {"title": "Kubernetes Basics", "description": "Learn Kubernetes"}
        course_response = client.post("/courses/", json=course_data)
        course_id = course_response.json()["id"]
        
        enrollment_data = {"user_id": user_id, "course_id": course_id}
        enrollment_response = client.post("/enrollments/", json=enrollment_data)
        enrollment_id = enrollment_response.json()["id"]
        
        # Mark completion
        response = client.patch(f"/enrollments/{enrollment_id}/complete")
        assert response.status_code == 200
        data = response.json()
        assert data["completed"] is True

    def test_delete_enrollment(self):
        """Test deleting an enrollment"""
        # Create enrollment first
        user_data = {"name": "Paul Anderson", "email": "paul@example.com"}
        user_response = client.post("/users/", json=user_data)
        user_id = user_response.json()["id"]
        
        course_data = {"title": "AWS Basics", "description": "Learn AWS"}
        course_response = client.post("/courses/", json=course_data)
        course_id = course_response.json()["id"]
        
        enrollment_data = {"user_id": user_id, "course_id": course_id}
        enrollment_response = client.post("/enrollments/", json=enrollment_data)
        enrollment_id = enrollment_response.json()["id"]
        
        # Delete enrollment
        response = client.delete(f"/enrollments/{enrollment_id}")
        assert response.status_code == 204
        
        # Verify enrollment is deleted
        get_response = client.get(f"/enrollments/{enrollment_id}")
        assert get_response.status_code == 404


class TestIntegrationScenarios:
    """Integration test scenarios"""
    
    def test_complete_workflow(self):
        """Test complete workflow: create user, course, enroll, complete"""
        # Create user
        user_data = {"name": "Rachel Green", "email": "rachel@example.com"}
        user_response = client.post("/users/", json=user_data)
        user_id = user_response.json()["id"]
        
        # Create course
        course_data = {"title": "Complete Python Course", "description": "Full Python course"}
        course_response = client.post("/courses/", json=course_data)
        course_id = course_response.json()["id"]
        
        # Enroll user
        enrollment_data = {"user_id": user_id, "course_id": course_id}
        enrollment_response = client.post("/enrollments/", json=enrollment_data)
        enrollment_id = enrollment_response.json()["id"]
        
        # Mark completion
        completion_response = client.patch(f"/enrollments/{enrollment_id}/complete")
        assert completion_response.status_code == 200
        assert completion_response.json()["completed"] is True
        
        # Verify user enrollments show completion
        user_enrollments = client.get(f"/enrollments/user/{user_id}")
        assert user_enrollments.status_code == 200
        completed_enrollment = next(
            (e for e in user_enrollments.json() if e["id"] == enrollment_id), None
        )
        assert completed_enrollment is not None
        assert completed_enrollment["completed"] is True

    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "docs" in data

    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
