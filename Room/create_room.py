from typing import Tuple

def create_room(name: str, floor: int, size: Tuple[float, float], house: str, type: int) -> None:
    print("Succesfully created a room: ")
    print("With the name: ", name)
    print("On floor: ", floor)
    print("In the house: ", house)
    print("It has the dimensions: ", size)
    print("It is the type: ", type)

if __name__ == "__main__":
    create_room()