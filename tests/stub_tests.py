import pytest
from House import create_house, delete_house, update_house, read_house
from Room import create_room, delete_room, update_room, read_room
from User import create_user, delete_user, update_user, read_user
from Device import create_device, delete_device, update_device, read_device

def test_create_house(capfd):
    create_house()
    out, _ = capfd.readouterr()
    assert "house created" in out

def test_delete_house(capfd):
    delete_house()
    out, _ = capfd.readouterr()
    assert "house deleted" in out

def test_update_house(capfd):
    update_house()
    out, _ = capfd.readouterr()
    assert "house updated" in out

def test_read_house(capfd):
    read_house()
    out, _ = capfd.readouterr()
    assert "house retrieved" in out

def test_create_room(capfd):
    create_room()
    out, _ = capfd.readouterr()
    assert "room created" in out

def test_delete_room(capfd):
    delete_room()
    out, _ = capfd.readouterr()
    assert "room deleted" in out

def test_update_room(capfd):
    update_room()
    out, _ = capfd.readouterr()
    assert "room updated" in out

def test_read_room(capfd):
    read_room()
    out, _ = capfd.readouterr()
    assert "room retrieved" in out

def test_create_user(capfd):
    create_user()
    out, _ = capfd.readouterr()
    assert "user created" in out

def test_delete_user(capfd):
    delete_user()
    out, _ = capfd.readouterr()
    assert "user deleted" in out

def test_update_user(capfd):
    update_user()
    out, _ = capfd.readouterr()
    assert "user updated" in out

def test_read_user(capfd):
    read_user()
    out, _ = capfd.readouterr()
    assert "user retrieved" in out

def test_create_device(capfd):
    create_device()
    out, _ = capfd.readouterr()
    assert "device created" in out

def test_delete_device(capfd):
    delete_device()
    out, _ = capfd.readouterr()
    assert "device deleted" in out

def test_update_device(capfd):
    update_device()
    out, _ = capfd.readouterr()
    assert "device updated" in out

def test_read_device(capfd):
    read_device()
    out, _ = capfd.readouterr()
    assert "device retrieved" in out
