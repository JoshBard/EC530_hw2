from fastapi import HTTPException, APIRouter
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

@router.get("/test-user")
async def test_user():
    return {"message": "User API is working"}

class User(BaseModel):
    id: Optional[int] = None
    name: str
    username: str
    phone: str
    email: str

# In-memory database (a list of users)
users_db = []

# Endpoint to create a user (POST)
@router.post("/users")
async def create_user(user: User):
    user.id = len(users_db) + 1  # Assign an ID
    users_db.append(user)
    return {"message": "User created", "user": user}

# Endpoint to get all users (GET)
@router.get("/users", response_model=List[User])
async def get_users():
    return users_db

# Endpoint to update a user (PUT)
@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, updated_user: User):
    for index, user in enumerate(users_db):
        if user.id == user_id:
            users_db[index] = updated_user
            return users_db[index]
    
    raise HTTPException(status_code=404, detail="User not found")

# Endpoint to delete a user (DELETE)
@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    global users_db
    users_db = [user for user in users_db if user.id != user_id]
    return {"message": "User deleted"}
