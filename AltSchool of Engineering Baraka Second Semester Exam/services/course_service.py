from typing import List, Optional, Dict
from datetime import datetime
from schemas.user import User, UserCreate, UserUpdate


class UserService:
    def __init__(self):
        self.users: Dict[int, User] = {}
        self.next_id = 1

    def create_user(self, user_data: UserCreate) -> User:
        user = User(
            id=self.next_id,
            name=user_data.name,
            email=user_data.email,
            is_active=True,
            created_at=datetime.now()
        )
        self.users[self.next_id] = user
        self.next_id += 1
        return user

    def get_user(self, user_id: int) -> Optional[User]:
        return self.users.get(user_id)

    def get_all_users(self) -> List[User]:
        return list(self.users.values())

    def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        if user_id not in self.users:
            return None
        
        user = self.users[user_id]
        update_data = user_data.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(user, field, value)
        
        return user

    def delete_user(self, user_id: int) -> bool:
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False

    def deactivate_user(self, user_id: int) -> Optional[User]:
        if user_id not in self.users:
            return None
        
        self.users[user_id].is_active = False
        return self.users[user_id]
