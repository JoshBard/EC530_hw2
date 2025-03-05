from fastapi import HTTPException, APIRouter
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

@router.get("/test-device")
async def test_device():
    return {"message": "Device API is working"}

class Device(BaseModel):
    id: Optional[int] = None
    name: str
    room: str
    type: int
    setting: str
    data: List[int]
    status: str

# In-memory database (a list of devices)
devices_db = []

# Endpoint to create a device (POST)
@router.post("/devices")
async def create_device(device: Device):
    device.id = len(devices_db) + 1  # Assign an ID
    devices_db.append(device)
    return {"message": "Device created", "device": device}

# Endpoint to get all devices (GET)
@router.get("/devices", response_model=List[Device])
async def get_devices():
    return devices_db

# Endpoint to update a device (PUT)
@router.put("/devices/{device_id}", response_model=Device)
async def update_device(device_id: int, updated_device: Device):
    for index, device in enumerate(devices_db):
        if device.id == device_id:
            devices_db[index] = updated_device
            return devices_db[index]
    
    raise HTTPException(status_code=404, detail="Device not found")

# Endpoint to delete a device (DELETE)
@router.delete("/devices/{device_id}")
async def delete_device(device_id: int):
    global devices_db
    devices_db = [device for device in devices_db if device.id != device_id]
    return {"message": "Device deleted"}
