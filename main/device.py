import sqlite3
from fastapi import HTTPException, APIRouter
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

# SQLite Database connection
def get_db():
    conn = sqlite3.connect("smart_home.db")
    conn.row_factory = sqlite3.Row  # Allows access by column name
    return conn

# Create the devices table if it doesn't exist
def create_table():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS devices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        room TEXT NOT NULL,
        type INTEGER NOT NULL,
        setting TEXT NOT NULL,
        status INTEGER DEFAULT 0
    )
    """)
    conn.commit()
    conn.close()

# Call this function at the start of the app to ensure the table is created
create_table()

class Device(BaseModel):
    id: Optional[int] = None
    name: str
    room: str
    type: int
    setting: str
    status: int = 0

# Endpoint to create a device (POST)
@router.post("/devices")
async def create_device(device: Device):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO devices (name, room, type, setting, data, status) 
    VALUES (?, ?, ?, ?, ?, ?)
    """, (device.name, device.room, device.type, device.setting, device.status))
    
    conn.commit()
    device.id = cursor.lastrowid
    conn.close()
    
    return {"message": "Device created", "device": device}

# Endpoint to get all devices (GET)
@router.get("/devices", response_model=List[Device])
async def get_devices():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM devices")
    devices = cursor.fetchall()
    
    conn.close()
    
    # Convert rows to device objects
    return [Device(
        id=device["id"],
        name=device["name"],
        room=device["room"],
        type=device["type"],
        setting=device["setting"],
        status=device["status"]
    ) for device in devices]

# Endpoint to update a device (PUT)
@router.put("/devices/{device_id}", response_model=Device)
async def update_device(device_id: int, updated_device: Device):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE devices
    SET name = ?, room = ?, type = ?, setting = ?, status = ?
    WHERE id = ?
    """, (updated_device.name, updated_device.room, updated_device.type, updated_device.setting, updated_device.status, device_id))
    
    conn.commit()

    cursor.execute("SELECT * FROM devices WHERE id = ?", (device_id,))
    device = cursor.fetchone()
    
    conn.close()

    if device:
        return Device(
            id=device["id"],
            name=device["name"],
            room=device["room"],
            type=device["type"],
            setting=device["setting"],
            status=device["status"]
        )
    
    raise HTTPException(status_code=404, detail="Device not found")

# Endpoint to mark a device as deleted by setting status to -1
@router.delete("/devices/{device_id}")
async def delete_device(device_id: int):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM devices WHERE id = ?", (device_id,))
    device = cursor.fetchone()
    
    if not device:
        conn.close()
        raise HTTPException(status_code=404, detail="Device not found")

    # Update the status to -1 instead of deleting the record, this way we can access again if we need to
    cursor.execute("UPDATE devices SET status = ? WHERE id = ?", ("-1", device_id))
    conn.commit()
    
    conn.close()
    
    return {"message": "Device status set to -1 (soft delete)"}

