import pytest

from User.create_user import create_user
from User.delete_user import delete_user
from User.update_user import update_user
from User.read_user import read_user

def test_create_user(capfd):
    # Dummy fields for testing
    dummy_name = "John Doe"
    dummy_username = "johndoe"
    dummy_phone = "555-1234"
    dummy_email = "johndoe@example.com"
    
    # Call create_user with dummy data
    create_user(dummy_name, dummy_username, dummy_phone, dummy_email)
    
    # Capture the output
    out, _ = capfd.readouterr()
    
    # Validate that the output contains expected dummy values
    assert "user succesfully created:" in out.lower()
    assert dummy_name.lower() in out.lower()
    assert dummy_username.lower() in out.lower()
    assert dummy_phone.lower() in out.lower()
    assert dummy_email.lower() in out.lower()

def test_delete_user(capfd):
    # Dummy data for testing delete_user
    dummy_name = "Alice"
    dummy_username = "alice123"
    
    # Call the delete_user function with dummy data
    delete_user(dummy_name, dummy_username)
    
    # Capture the output and clean it up by joining words with a single space
    out, _ = capfd.readouterr()
    out_cleaned = " ".join(out.split())
    
    # Assert that the cleaned output contains the expected substrings
    assert f"User with name: {dummy_name}" in out_cleaned
    assert f"and username: {dummy_username}" in out_cleaned
    assert "deleted." in out_cleaned

def test_update_user(capfd):
    # Dummy data for testing update_user
    dummy_name = "Bob"
    dummy_username = "bob321"
    dummy_phone = "123-4567"
    dummy_email = "bob@example.com"
    
    # Call the update_user function with dummy data
    update_user(dummy_name, dummy_username, dummy_phone, dummy_email)
    
    # Capture and clean the output
    out, _ = capfd.readouterr()
    out_cleaned = " ".join(out.split())
    
    # Assert that the cleaned output contains the expected substrings
    assert "User updated to have the following fields" in out_cleaned
    assert f"Name: {dummy_name}" in out_cleaned
    assert f"Username: {dummy_username}" in out_cleaned
    assert f"Phone number: {dummy_phone}" in out_cleaned
    assert f"Email: {dummy_email}" in out_cleaned


def test_read_user(capfd):
    # Dummy values for testing
    dummy_name = "Alice"
    dummy_username = "alice123"

    # Call the function with dummy data
    read_user(dummy_name, dummy_username)

    # Capture the output
    out, err = capfd.readouterr()

    # Check that the output includes the expected lines
    assert f"Reading from user with name:  {dummy_name}" in out
    assert f"Username:  {dummy_username}" in out
    assert "Phone number:" in out
    assert "Email:" in out