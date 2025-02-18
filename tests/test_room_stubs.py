import pytest
from typing import Tuple
# Adjust these import paths to match your project's structure
from Room.create_room import create_room
from Room.delete_room import delete_room
from Room.update_room import update_room
from Room.read_room import read_room

def test_create_room(capfd):
    # Dummy data for create_room
    dummy_name = "Conference Room"
    dummy_floor = 2
    dummy_size: Tuple[float, float] = (20.5, 30.5)
    dummy_house = "Main House"
    dummy_type = 1

    create_room(dummy_name, dummy_floor, dummy_size, dummy_house, dummy_type)

    # Capture the output and verify it contains the expected information
    out, _ = capfd.readouterr()
    assert "Succesfully created a room:" in out
    assert "With the name:" in out
    assert dummy_name in out
    assert "On floor:" in out
    assert str(dummy_floor) in out
    assert "In the house:" in out
    assert dummy_house in out
    assert "It has the dimensions:" in out
    assert str(dummy_size) in out
    assert "It is the type:" in out
    assert str(dummy_type) in out

def test_delete_room(capfd):
    # Dummy data for delete_room
    dummy_name = "Conference Room"
    dummy_house = "Main House"

    delete_room(dummy_name, dummy_house)
    
    # Capture the output and verify the deletion message
    out, _ = capfd.readouterr()
    assert "Room" in out
    assert dummy_name in out
    assert "from house" in out
    assert dummy_house in out
    assert "succesfully deleted" in out.lower()

def test_update_room(capfd):
    # Dummy data for update_room
    dummy_name = "Updated Room"
    dummy_floor = 3
    dummy_size: Tuple[float, float] = (25.0, 35.0)
    dummy_house = "Main House"
    dummy_type = 2

    update_room(dummy_name, dummy_floor, dummy_size, dummy_house, dummy_type)
    
    # Capture the output and verify it contains the updated information
    out, _ = capfd.readouterr()
    assert "Succesfully updated a room" in out
    assert "Name:" in out
    assert dummy_name in out
    assert "On floor:" in out
    assert str(dummy_floor) in out
    assert "In the house:" in out
    assert dummy_house in out
    assert "It has the dimensions:" in out
    assert str(dummy_size) in out
    assert "It is the type:" in out
    assert str(dummy_type) in out

def test_read_room(capfd):
    # Dummy data for read_room
    dummy_name = "Meeting Room"
    dummy_house = "Main House"

    read_room(dummy_name, dummy_house)
    
    # Capture the output and verify it contains the expected labels and dummy data
    out, _ = capfd.readouterr()
    assert "reading room:" in out
    assert dummy_name in out
    assert "On floor:" in out
    assert "In the house:" in out
    assert dummy_house in out
    assert "It has the dimensions:" in out
    assert "It is the type:" in out
