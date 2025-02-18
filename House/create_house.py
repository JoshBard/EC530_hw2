from typing import Tuple, List

def create_house(name: str, address: str, location: Tuple[float, float], owner: str, occupants: List[str]) -> None:
    UUID = 1
    print("Successfully created house:")
    print("With name: ", name)
    print("Address: ", address)
    print("Location: ", location)
    print("Owner: ", owner)
    print("And occupants: ", occupants)
    print("It has been assigned the unique house ID: ", UUID)

if __name__ == "__main__":
    create_house()