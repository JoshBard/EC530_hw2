import pytest
from typing import Tuple, List
# Adjust the import paths according to your project structure
from House.read_house import read_house
from House.delete_house import delete_house
from House.create_house import create_house
from House.update_house import update_house

def test_read_house(capfd):
    # Dummy data for read_house
    dummy_name = "Test House"
    dummy_uuid = 123
    read_house(dummy_name, dummy_uuid)
    
    # Capture the output
    out, _ = capfd.readouterr()
    
    # Verify expected output lines
    assert "Reading House:" in out
    assert dummy_name in out
    assert "Address:" in out
    assert "Location:" in out
    assert "Owner:" in out
    assert "And occupants:" in out
    assert str(dummy_uuid) in out

def test_delete_house(capfd):
    # Dummy data for delete_house
    dummy_name = "Test House"
    dummy_uuid = 123
    delete_house(dummy_name, dummy_uuid)
    
    # Capture the output
    out, _ = capfd.readouterr()
    
    # Verify expected output lines
    assert "House with name:" in out
    assert dummy_name in out
    assert "and UUID:" in out
    assert str(dummy_uuid) in out
    assert "deleted" in out.lower()

def test_create_house(capfd):
    # Dummy data for create_house
    dummy_name = "Test House"
    dummy_address = "123 Test Lane"
    dummy_location: Tuple[float, float] = (40.7128, -74.0060)
    dummy_owner = "John Doe"
    dummy_occupants: List[str] = ["Alice", "Bob"]
    
    create_house(dummy_name, dummy_address, dummy_location, dummy_owner, dummy_occupants)
    
    # Capture the output
    out, _ = capfd.readouterr()
    
    # Verify expected output lines
    assert "Successfully created house:" in out
    assert dummy_name in out
    assert dummy_address in out
    assert str(dummy_location) in out
    assert dummy_owner in out
    assert str(dummy_occupants) in out
    assert "unique house id:" in out.lower()

def test_update_house(capfd):
    # Dummy data for update_house
    dummy_name = "Updated House"
    dummy_address = "456 Updated Ave"
    dummy_location: Tuple[float, float] = (41.0, -75.0)
    dummy_owner = "Jane Smith"
    dummy_occupants: List[str] = ["Charlie", "Dana"]
    dummy_uuid = 2
    
    update_house(dummy_name, dummy_address, dummy_location, dummy_owner, dummy_occupants, dummy_uuid)
    
    # Capture the output
    out, _ = capfd.readouterr()
    
    # Verify expected output lines
    assert "Successfully update house" in out
    assert dummy_name in out
    assert dummy_address in out
    assert str(dummy_location) in out
    assert dummy_owner in out
    assert str(dummy_occupants) in out
    assert str(dummy_uuid) in out
