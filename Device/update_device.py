from typing import List

def update_device(name: str, room: str, type: int, setting: str, data: List[int], status: str):
    print("Successfully update device, it now has the following fields: ")
    print("With name: ", name)
    print("In the room: ", room)
    print("And the type is: ", type)
    print("It is set at: ", setting)
    print("The reading is: ", data)
    print("And the status is: ", status)

if __name__ == "__main__":
    update_device()