import pytest
from typing import List

# Adjust these import paths according to your project's structure
from Device.update_device import update_device
from Device.read_device import read_device
from Device.delete_device import delete_device
from Device.create_device import create_device

def test_update_device(capfd):
    # Dummy data for update_device
    dummy_name = "Device1"
    dummy_room = "RoomA"
    dummy_type = 2
    dummy_setting = "Auto"
    dummy_data: List[int] = [10, 20, 30]
    dummy_status = "Active"
    
    update_device(dummy_name, dummy_room, dummy_type, dummy_setting, dummy_data, dummy_status)
    out, _ = capfd.readouterr()
    
    # Verify that output contains all expected text and dummy data
    assert "Successfully update device" in out
    assert dummy_name in out
    assert dummy_room in out
    assert str(dummy_type) in out
    assert dummy_setting in out
    assert str(dummy_data) in out
    assert dummy_status in out

def test_read_device(capfd):
    # Dummy data for read_device
    dummy_name = "Device2"
    dummy_room = "RoomB"
    
    read_device(dummy_name, dummy_room)
    out, _ = capfd.readouterr()
    
    # Verify the output includes expected labels and dummy values
    assert "Device" in out
    assert dummy_name in out
    assert "in room" in out
    assert dummy_room in out
    assert "Is set at:" in out
    assert "The current reading is:" in out
    assert "And the status is:" in out

def test_delete_device(capfd):
    # Dummy data for delete_device
    dummy_name = "Device3"
    dummy_room = "RoomC"
    
    delete_device(dummy_name, dummy_room)
    out, _ = capfd.readouterr()
    
    # Verify the deletion output
    assert "Succesfully deleted" in out
    assert dummy_name in out
    assert dummy_room in out

def test_create_device(capfd):
    # Dummy data for create_device
    dummy_name = "Device4"
    dummy_room = "RoomD"
    dummy_type = 3
    dummy_setting = "Manual"
    dummy_data: List[int] = [100, 200, 300]
    dummy_status = "Inactive"
    
    create_device(dummy_name, dummy_room, dummy_type, dummy_setting, dummy_data, dummy_status)
    out, _ = capfd.readouterr()
    
    # Verify the creation output contains the expected strings and dummy data
    assert "Successfully created Device:" in out
    assert dummy_name in out
    assert dummy_room in out
    assert str(dummy_type) in out
    assert dummy_setting in out
    assert str(dummy_data) in out
    assert dummy_status in out
