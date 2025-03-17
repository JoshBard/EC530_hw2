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

# Create rooms table if it doesn't exist
def create_tables():
    conn = get_db()
    cursor = conn.cursor()
    
    # Ensure houses table exists first
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

    # Create rooms table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rooms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        floor INTEGER NOT NULL,
        size_x REAL NOT NULL,
        size_y REAL NOT NULL,
        house_id INTEGER NOT NULL,
        type INTEGER NOT NULL,
        status INTEGER DEFAULT 0,
        FOREIGN KEY (house_id) REFERENCES houses(id)
    )
    """)

    conn.commit()
    conn.close()

# Ensure tables are created
create_tables()

# Room model
class Room(BaseModel):
    id: Optional[int] = None
    name: str
    floor: int
    size: Tuple[float, float]  # (width, length)
    house_id: int  # Reference to house ID
    type: int
    status: int = 0  # Default status is 0 (active)

# Test endpoint
@router.get("/test-room")
async def test_room():
    return {"message": "Room API is working"}

# Create a room (POST)
@router.post("/rooms")
async def create_room(room: Room):
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if the house exists
    cursor.execute("SELECT * FROM houses WHERE id = ? AND status != -1", (room.house_id,))
    house = cursor.fetchone()
    if not house:
        conn.close()
        raise HTTPException(status_code=400, detail="House does not exist")

    cursor.execute("""
    INSERT INTO rooms (name, floor, size_x, size_y, house_id, type, status) 
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (room.name, room.floor, room.size[0], room.size[1], room.house_id, room.type, room.status))
    
    conn.commit()
    room.id = cursor.lastrowid
    conn.close()
    
    return {"message": "Room created", "room": room}

# Get all rooms (GET)
@router.get("/rooms", response_model=List[Room])
async def get_rooms():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM rooms WHERE status != -1")  # Exclude soft-deleted rooms
    rooms = cursor.fetchall()
    
    conn.close()
    
    return [Room(
        id=room["id"],
        name=room["name"],
        floor=room["floor"],
        size=(room["size_x"], room["size_y"]),
        house_id=room["house_id"],
        type=room["type"],
        status=room["status"]
    ) for room in rooms]

# Update a room (PUT)
@router.put("/rooms/{room_id}", response_model=Room)
async def update_room(room_id: int, updated_room: Room):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM rooms WHERE id = ?", (room_id,))
    room = cursor.fetchone()
    
    if not room:
        conn.close()
        raise HTTPException(status_code=404, detail="Room not found")

    # Check if new house exists
    cursor.execute("SELECT * FROM houses WHERE id = ? AND status != -1", (updated_room.house_id,))
    house = cursor.fetchone()
    if not house:
        conn.close()
        raise HTTPException(status_code=400, detail="New house does not exist")

    cursor.execute("""
    UPDATE rooms
    SET name = ?, floor = ?, size_x = ?, size_y = ?, house_id = ?, type = ?, status = ?
    WHERE id = ?
    """, (updated_room.name, updated_room.floor, updated_room.size[0], updated_room.size[1], updated_room.house_id,
          updated_room.type, updated_room.status, room_id))
    
    conn.commit()

    cursor.execute("SELECT * FROM rooms WHERE id = ?", (room_id,))
    updated_room = cursor.fetchone()
    
    conn.close()

    return Room(
        id=updated_room["id"],
        name=updated_room["name"],
        floor=updated_room["floor"],
        size=(updated_room["size_x"], updated_room["size_y"]),
        house_id=updated_room["house_id"],
        type=updated_room["type"],
        status=updated_room["status"]
    )

# "Delete" a room by setting status to -1
@router.delete("/rooms/{room_id}")
async def delete_room(room_id: int):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM rooms WHERE id = ?", (room_id,))
    room = cursor.fetchone()
    
    if not room:
        conn.close()
        raise HTTPException(status_code=404, detail="Room not found")

    cursor.execute("UPDATE rooms SET status = -1 WHERE id = ?", (room_id,))
    conn.commit()
    
    conn.close()
    
    return {"message": "Room status set to -1 (soft delete)"}

# Include router
app.include_router(router)
