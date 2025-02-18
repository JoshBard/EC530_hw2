from typing import Tuple, List

def update_house(name: str, address: str, location: Tuple[float, float], owner: str, occupants: List[str], UUID: int) -> None:
    print("Successfully update house, it now has the following fields: ")
    print("With name: ", name)
    print("Address: ", address)
    print("Location: ", location)
    print("Owner: ", owner)
    print("And occupants: ", occupants)
    print("It has been assigned the unique house ID: ", UUID)

if __name__ == "__main__":
    update_house()