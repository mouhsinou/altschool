from fastapi import APIRouter, HTTPException, status
from typing import List
from schemas.user import User, UserCreate, UserUpdate
from services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])

# Initialize user service
user_service = UserService()


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate):
    """Create a new user"""
    return user_service.create_user(user_data)


@router.get("/", response_model=List[User])
def get_all_users():
    """Get all users"""
    return user_service.get_all_users()


@router.get("/{user_id}", response_model=User)
def get_user(user_id: int):
    """Get a specific user by ID"""
    user = user_service.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user_data: UserUpdate):
    """Update a user"""
    user = user_service.update_user(user_id, user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    """Delete a user"""
    if not user_service.delete_user(user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )


@router.patch("/{user_id}/deactivate", response_model=User)
def deactivate_user(user_id: int):
    """Deactivate a user"""
    user = user_service.deactivate_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user
