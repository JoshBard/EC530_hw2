from typing import Tuple

def update_room(name: str, floor: int, size: Tuple[float, float], house: str, type: int):
    print("Succesfully updated a room, it now has the following entries: ")
    print("Name: ", name)
    print("On floor: ", floor)
    print("In the house: ", house)
    print("It has the dimensions: ", size)
    print("It is the type: ", type)

if __name__ == "__main__":
    update_room()