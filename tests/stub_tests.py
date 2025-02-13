import pytest
from House.create_house import create_house
from House.delete_house import delete_house
from House.update_house import update_house
from House.read_house import read_house

from Room.create_room import create_room
from Room.delete_room import delete_room
from Room.update_room import update_room
from Room.read_room import read_room

from User.create_user import create_user
from User.delete_user import delete_user
from User.update_user import update_user
from User.read_user import read_user

from Device.create_device import create_device
from Device.delete_device import delete_device
from Device.update_device import update_device
from Device.read_device import read_device

def test_create_house(capfd):
    create_house()
    out, _ = capfd.readouterr()
    assert "house created" in out.lower()

def test_delete_house(capfd):
    delete_house()
    out, _ = capfd.readouterr()
    assert "house deleted" in out.lower()

def test_update_house(capfd):
    update_house()
    out, _ = capfd.readouterr()
    assert "house updated" in out.lower()

def test_read_house(capfd):
    read_house()
    out, _ = capfd.readouterr()
    assert "house read" in out.lower()

def test_create_room(capfd):
    create_room()
    out, _ = capfd.readouterr()
    assert "room created" in out.lower()

def test_delete_room(capfd):
    delete_room()
    out, _ = capfd.readouterr()
    assert "room deleted" in out.lower()

def test_update_room(capfd):
    update_room()
    out, _ = capfd.readouterr()
    assert "room updated" in out.lower()

def test_read_room(capfd):
    read_room()
    out, _ = capfd.readouterr()
    assert "room read" in out.lower()

def test_create_user(capfd):
    create_user()
    out, _ = capfd.readouterr()
    assert "user created" in out.lower()

def test_delete_user(capfd):
    delete_user()
    out, _ = capfd.readouterr()
    assert "user deleted" in out.lower()

def test_update_user(capfd):
    update_user()
    out, _ = capfd.readouterr()
    assert "user updated" in out.lower()

def test_read_user(capfd):
    read_user()
    out, _ = capfd.readouterr()
    assert "user read" in out.lower()

def test_create_device(capfd):
    create_device()
    out, _ = capfd.readouterr()
    assert "device created" in out.lower()

def test_delete_device(capfd):
    delete_device()
    out, _ = capfd.readouterr()
    assert "device deleted" in out.lower()

def test_update_device(capfd):
    update_device()
    out, _ = capfd.readouterr()
    assert "device updated" in out.lower()

def test_read_device(capfd):
    read_device()
    out, _ = capfd.readouterr()
    assert "device read" in out.lower()
