from fastapi import HTTPException, APIRouter
from pydantic import BaseModel
from typing import Tuple, List, Optional

router = APIRouter()

@router.get("/test-house")
async def test_house():
    return {"message": "House API is working"}

class House(BaseModel):
    id: Optional[int] = None
    name: str
    address: str
    location: Tuple[float, float]
    owner: str
    occupants: List[str]

# In-memory database (a list of houses)
houses_db = []

# Endpoint to create a house (POST)
@router.post("/houses")
async def create_house(house: House):
    house.id = len(houses_db) + 1  # Assign an ID
    houses_db.append(house)
    return {"message": "House created", "house": house}

# Endpoint to get all houses (GET)
@router.get("/houses", response_model=List[House])
async def get_houses():
    return houses_db

# Endpoint to update a house (PUT)
@router.put("/houses/{house_id}", response_model=House)
async def update_house(house_id: int, updated_house: House):
    for index, house in enumerate(houses_db):
        if house.id == house_id:
            houses_db[index] = updated_house
            return houses_db[index]
    
    raise HTTPException(status_code=404, detail="House not found")

# Endpoint to delete a house (DELETE)
@router.delete("/houses/{house_id}")
async def delete_house(house_id: int):
    global houses_db
    houses_db = [house for house in houses_db if house.id != house_id]
    return {"message": "House deleted"}
