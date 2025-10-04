#!/usr/bin/env python3
"""
Demo script for EduTrack Lite API
This script demonstrates the basic functionality of the API
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_response(response, title):
    """Helper function to print API responses"""
    print(f"\n{'='*50}")
    print(f"{title}")
    print(f"{'='*50}")
    print(f"Status Code: {response.status_code}")
    if response.status_code != 204:  # No content for DELETE
        try:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        except:
            print(f"Response: {response.text}")

def demo_api():
    """Demonstrate the EduTrack Lite API functionality"""
    print("🚀 EduTrack Lite API Demo")
    print("Make sure the API server is running on http://localhost:8000")
    
    # Test root endpoint
    try:
        response = requests.get(f"{BASE_URL}/")
        print_response(response, "🏠 Root Endpoint")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API server.")
        print("Please start the server by running: python main.py")
        return
    
    # Test health check
    response = requests.get(f"{BASE_URL}/health")
    print_response(response, "💚 Health Check")
    
    # Create a user
    user_data = {
        "name": "Alice Johnson",
        "email": "alice@example.com"
    }
    response = requests.post(f"{BASE_URL}/users/", json=user_data)
    print_response(response, "👤 Create User")
    user_id = response.json()["id"] if response.status_code == 201 else None
    
    # Create another user
    user_data2 = {
        "name": "Bob Smith", 
        "email": "bob@example.com"
    }
    response = requests.post(f"{BASE_URL}/users/", json=user_data2)
    print_response(response, "👤 Create Second User")
    user_id2 = response.json()["id"] if response.status_code == 201 else None
    
    # Get all users
    response = requests.get(f"{BASE_URL}/users/")
    print_response(response, "👥 Get All Users")
    
    # Create a course
    course_data = {
        "title": "Python Basics",
        "description": "Learn Python programming fundamentals"
    }
    response = requests.post(f"{BASE_URL}/courses/", json=course_data)
    print_response(response, "📚 Create Course")
    course_id = response.json()["id"] if response.status_code == 201 else None
    
    # Create another course
    course_data2 = {
        "title": "JavaScript Advanced",
        "description": "Advanced JavaScript concepts and patterns"
    }
    response = requests.post(f"{BASE_URL}/courses/", json=course_data2)
    print_response(response, "📚 Create Second Course")
    course_id2 = response.json()["id"] if response.status_code == 201 else None
    
    # Get all courses
    response = requests.get(f"{BASE_URL}/courses/")
    print_response(response, "📖 Get All Courses")
    
    # Enroll users in courses
    if user_id and course_id:
        enrollment_data = {
            "user_id": user_id,
            "course_id": course_id
        }
        response = requests.post(f"{BASE_URL}/enrollments/", json=enrollment_data)
        print_response(response, "📝 Enroll Alice in Python Basics")
        enrollment_id = response.json()["id"] if response.status_code == 201 else None
    
    if user_id2 and course_id:
        enrollment_data2 = {
            "user_id": user_id2,
            "course_id": course_id
        }
        response = requests.post(f"{BASE_URL}/enrollments/", json=enrollment_data2)
        print_response(response, "📝 Enroll Bob in Python Basics")
    
    if user_id and course_id2:
        enrollment_data3 = {
            "user_id": user_id,
            "course_id": course_id2
        }
        response = requests.post(f"{BASE_URL}/enrollments/", json=enrollment_data3)
        print_response(response, "📝 Enroll Alice in JavaScript Advanced")
    
    # Get all enrollments
    response = requests.get(f"{BASE_URL}/enrollments/")
    print_response(response, "📋 Get All Enrollments")
    
    # Get enrollments for Alice
    if user_id:
        response = requests.get(f"{BASE_URL}/enrollments/user/{user_id}")
        print_response(response, f"👤 Get Enrollments for Alice (User ID: {user_id})")
    
    # Get enrollments for Python Basics course
    if course_id:
        response = requests.get(f"{BASE_URL}/courses/{course_id}/enrollments")
        print_response(response, f"📚 Get Enrollments for Python Basics (Course ID: {course_id})")
    
    # Mark Alice's Python course as completed
    if enrollment_id:
        response = requests.patch(f"{BASE_URL}/enrollments/{enrollment_id}/complete")
        print_response(response, "✅ Mark Alice's Python Course as Completed")
    
    # Try to enroll Alice again in the same course (should fail)
    if user_id and course_id:
        enrollment_data = {
            "user_id": user_id,
            "course_id": course_id
        }
        response = requests.post(f"{BASE_URL}/enrollments/", json=enrollment_data)
        print_response(response, "❌ Try to Enroll Alice Again in Python Basics (Should Fail)")
    
    # Close enrollment for JavaScript course
    if course_id2:
        response = requests.patch(f"{BASE_URL}/courses/{course_id2}/close-enrollment")
        print_response(response, "🔒 Close Enrollment for JavaScript Advanced")
    
    # Try to enroll Bob in closed course (should fail)
    if user_id2 and course_id2:
        enrollment_data = {
            "user_id": user_id2,
            "course_id": course_id2
        }
        response = requests.post(f"{BASE_URL}/enrollments/", json=enrollment_data)
        print_response(response, "❌ Try to Enroll Bob in Closed Course (Should Fail)")
    
    # Deactivate Bob
    if user_id2:
        response = requests.patch(f"{BASE_URL}/users/{user_id2}/deactivate")
        print_response(response, "🚫 Deactivate Bob")
    
    # Try to enroll deactivated Bob (should fail)
    if user_id2 and course_id:
        enrollment_data = {
            "user_id": user_id2,
            "course_id": course_id
        }
        response = requests.post(f"{BASE_URL}/enrollments/", json=enrollment_data)
        print_response(response, "❌ Try to Enroll Deactivated Bob (Should Fail)")
    
    print(f"\n{'='*50}")
    print("🎉 Demo completed!")
    print("Visit http://localhost:8000/docs for interactive API documentation")
    print(f"{'='*50}")

if __name__ == "__main__":
    demo_api()
