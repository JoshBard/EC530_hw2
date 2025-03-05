from fastapi import FastAPI
from main.device import router as device_router
from main.house import router as house_router
from main.room import router as room_router
from main.user import router as user_router

app = FastAPI()

# Include the routers with a prefix
app.include_router(device_router, prefix="/devices", tags=["Devices"])
app.include_router(house_router, prefix="/houses", tags=["Houses"])
app.include_router(room_router, prefix="/rooms", tags=["Rooms"])
app.include_router(user_router, prefix="/users", tags=["Users"])
