import sqlite3
from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from typing import List, Optional, Tuple

app = FastAPI()
router = APIRouter()

# Database connection function
def get_db():
    conn = sqlite3.connect("smart_home.db")
    conn.row_factory = sqlite3.Row  # Enables dictionary-like row access
    return conn

# Create houses table if it doesn't exist
def create_tables():
    conn = get_db()
    cursor = conn.cursor()
    
    # Create users table if not exists (needed for linking)
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

    # Create houses table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS houses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        address TEXT NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        owner_id INTEGER NOT NULL,
        occupants TEXT NOT NULL,
        status INTEGER DEFAULT 0,
        FOREIGN KEY (owner_id) REFERENCES users(id)
    )
    """)

    conn.commit()
    conn.close()

# Ensure tables are created
create_tables()

# House model
class House(BaseModel):
    id: Optional[int] = None
    name: str
    address: str
    location: Tuple[float, float]
    owner_id: int  # Reference to user ID
    occupants: List[int]  # List of user IDs
    status: int = 0  # Default status is 0 (active)

# Test endpoint
@router.get("/test-house")
async def test_house():
    return {"message": "House API is working"}

# Create a house (POST)
@router.post("/houses")
async def create_house(house: House):
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if owner exists
    cursor.execute("SELECT * FROM users WHERE id = ? AND status != -1", (house.owner_id,))
    owner = cursor.fetchone()
    if not owner:
        conn.close()
        raise HTTPException(status_code=400, detail="Owner does not exist")

    # Check if all occupants exist
    for occupant_id in house.occupants:
        cursor.execute("SELECT * FROM users WHERE id = ? AND status != -1", (occupant_id,))
        occupant = cursor.fetchone()
        if not occupant:
            conn.close()
            raise HTTPException(status_code=400, detail=f"Occupant with ID {occupant_id} does not exist")

    # Convert occupants list to string
    occupants_str = ",".join(map(str, house.occupants))

    cursor.execute("""
    INSERT INTO houses (name, address, latitude, longitude, owner_id, occupants, status) 
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (house.name, house.address, house.location[0], house.location[1], house.owner_id, occupants_str, house.status))
    
    conn.commit()
    house.id = cursor.lastrowid
    conn.close()
    
    return {"message": "House created", "house": house}

# Get all houses (GET)
@router.get("/houses", response_model=List[House])
async def get_houses():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM houses WHERE status != -1")  # Exclude soft-deleted houses
    houses = cursor.fetchall()
    
    conn.close()
    
    return [House(
        id=house["id"],
        name=house["name"],
        address=house["address"],
        location=(house["latitude"], house["longitude"]),
        owner_id=house["owner_id"],
        occupants=list(map(int, house["occupants"].split(','))),
        status=house["status"]
    ) for house in houses]

# Update a house (PUT)
@router.put("/houses/{house_id}", response_model=House)
async def update_house(house_id: int, updated_house: House):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM houses WHERE id = ?", (house_id,))
    house = cursor.fetchone()
    
    if not house:
        conn.close()
        raise HTTPException(status_code=404, detail="House not found")

    # Check if new owner exists
    cursor.execute("SELECT * FROM users WHERE id = ? AND status != -1", (updated_house.owner_id,))
    owner = cursor.fetchone()
    if not owner:
        conn.close()
        raise HTTPException(status_code=400, detail="New owner does not exist")

    # Check if all new occupants exist
    for occupant_id in updated_house.occupants:
        cursor.execute("SELECT * FROM users WHERE id = ? AND status != -1", (occupant_id,))
        occupant = cursor.fetchone()
        if not occupant:
            conn.close()
            raise HTTPException(status_code=400, detail=f"Occupant with ID {occupant_id} does not exist")

    # Convert occupants list to string
    occupants_str = ",".join(map(str, updated_house.occupants))

    cursor.execute("""
    UPDATE houses
    SET name = ?, address = ?, latitude = ?, longitude = ?, owner_id = ?, occupants = ?, status = ?
    WHERE id = ?
    """, (updated_house.name, updated_house.address, updated_house.location[0], updated_house.location[1],
          updated_house.owner_id, occupants_str, updated_house.status, house_id))
    
    conn.commit()

    cursor.execute("SELECT * FROM houses WHERE id = ?", (house_id,))
    updated_house = cursor.fetchone()
    
    conn.close()

    return House(
        id=updated_house["id"],
        name=updated_house["name"],
        address=updated_house["address"],
        location=(updated_house["latitude"], updated_house["longitude"]),
        owner_id=updated_house["owner_id"],
        occupants=list(map(int, updated_house["occupants"].split(','))),
        status=updated_house["status"]
    )

# "Delete" a house by setting status to -1
@router.delete("/houses/{house_id}")
async def delete_house(house_id: int):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM houses WHERE id = ?", (house_id,))
    house = cursor.fetchone()
    
    if not house:
        conn.close()
        raise HTTPException(status_code=404, detail="House not found")

    cursor.execute("UPDATE houses SET status = -1 WHERE id = ?", (house_id,))
    conn.commit()
    
    conn.close()
    
    return {"message": "House status set to -1 (soft delete)"}

# Include router
app.include_router(router)
