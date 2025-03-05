from fastapi import HTTPException, APIRouter
from pydantic import BaseModel
from typing import Tuple, List, Optional

router = APIRouter()

@router.get("/test-room")
async def test_room():
    return {"message": "Room API is working"}

class Room(BaseModel):
    id: Optional[int] = None
    name: str
    floor: int
    size: Tuple[float, float]
    house: str
    type: int

# In-memory database (a list of rooms)
rooms_db = []

# Endpoint to create a room (POST)
@router.post("/rooms")
async def create_room(room: Room):
    room.id = len(rooms_db) + 1  # Assign an ID
    rooms_db.append(room)
    return {"message": "Room created", "room": room}

# Endpoint to get all rooms (GET)
@router.get("/rooms", response_model=List[Room])
async def get_rooms():
    return rooms_db

# Endpoint to update a room (PUT)
@router.put("/rooms/{room_id}", response_model=Room)
async def update_room(room_id: int, updated_room: Room):
    for index, room in enumerate(rooms_db):
        if room.id == room_id:
            rooms_db[index] = updated_room
            return rooms_db[index]
    
    raise HTTPException(status_code=404, detail="Room not found")

# Endpoint to delete a room (DELETE)
@router.delete("/rooms/{room_id}")
async def delete_room(room_id: int):
    global rooms_db
    rooms_db = [room for room in rooms_db if room.id != room_id]
    return {"message": "Room deleted"}
