from typing import List

def create_device(name: str, room: str, type: int, setting: str, data: List[int], status: str) -> None:
    print("Successfully created Device:")
    print("With name: ", name)
    print("In the room: ", room)
    print("And the type is: ", type)
    print("It is set at: ", setting)
    print("The reading is: ", data)
    print("And the status is: ", status)


if __name__ == "__main__":
    create_device()