import sqlite3
from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()
router = APIRouter()

# Database connection function
def get_db():
    conn = sqlite3.connect("smart_home.db")
    conn.row_factory = sqlite3.Row  # Enables dictionary-like row access
    return conn

# Create users table if it doesn't exist
def create_table():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        username TEXT NOT NULL UNIQUE,
        phone TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        status INTEGER DEFAULT 0
    )
    """)
    conn.commit()
    conn.close()

# Ensure table is created
create_table()

# User model
class User(BaseModel):
    id: Optional[int] = None
    name: str
    username: str
    phone: str
    email: str
    status: int = 0  # Default status is 0 (active)

# Test endpoint
@router.get("/test-user")
async def test_user():
    return {"message": "User API is working"}

# Create a user (POST)
@router.post("/users")
async def create_user(user: User):
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
        INSERT INTO users (name, username, phone, email, status) 
        VALUES (?, ?, ?, ?, ?)
        """, (user.name, user.username, user.phone, user.email, user.status))
        
        conn.commit()
        user.id = cursor.lastrowid
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="Username or email already exists")
    
    conn.close()
    return {"message": "User created", "user": user}

# Get all users (GET)
@router.get("/users", response_model=List[User])
async def get_users():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE status != -1")  # Exclude soft-deleted users
    users = cursor.fetchall()
    
    conn.close()
    
    return [User(
        id=user["id"],
        name=user["name"],
        username=user["username"],
        phone=user["phone"],
        email=user["email"],
        status=user["status"]
    ) for user in users]

# Update a user (PUT)
@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, updated_user: User):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    
    if not user:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")

    cursor.execute("""
    UPDATE users
    SET name = ?, username = ?, phone = ?, email = ?, status = ?
    WHERE id = ?
    """, (updated_user.name, updated_user.username, updated_user.phone, updated_user.email, updated_user.status, user_id))
    
    conn.commit()

    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    updated_user = cursor.fetchone()
    
    conn.close()

    return User(
        id=updated_user["id"],
        name=updated_user["name"],
        username=updated_user["username"],
        phone=updated_user["phone"],
        email=updated_user["email"],
        status=updated_user["status"]
    )

# "Delete" a user by setting status to -1
@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    
    if not user:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")

    cursor.execute("UPDATE users SET status = -1 WHERE id = ?", (user_id,))
    conn.commit()
    
    conn.close()
    
    return {"message": "User status set to -1 (soft delete)"}

# Include router
app.include_router(router)