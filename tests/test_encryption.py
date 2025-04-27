import os
import json
import pytest
import subprocess
from unittest import mock
from cryptography.fernet import Fernet
from keysentinel.encryption import (
    generate_key,
    encrypt_token,
    find_existing_item,
    upsert_encrypted_fields,
)
from keysentinel.exceptions import VaultOperationError

# --- Tests for generate_key ---

def test_generate_key_creates_new_key(tmp_path):
    """Test if a new key is generated when file does not exist."""
    key_path = tmp_path / "test_key.key"
    key = generate_key(filepath=str(key_path))

    assert os.path.exists(key_path)
    assert isinstance(key, bytes)
    assert len(key) > 0

def test_generate_key_loads_existing_key(tmp_path):
    """Test if an existing key is loaded properly."""
    key_path = tmp_path / "test_key.key"
    original_key = Fernet.generate_key()
    key_path.write_bytes(original_key)

    loaded_key = generate_key(filepath=str(key_path))

    assert loaded_key == original_key

# --- Tests for encrypt_token ---

def test_encrypt_token_and_decrypt():
    """Test token encryption and that it can be decrypted."""
    key = Fernet.generate_key()
    token = "super_secret_token"
    encrypted = encrypt_token(token, key)

    cipher = Fernet(key)
    decrypted = cipher.decrypt(encrypted.encode()).decode()

    assert decrypted == token

# --- Tests for find_existing_item ---

@mock.patch("keysentinel.encryption.subprocess.run")
def test_find_existing_item_found(mock_run):
    """Test finding an existing item by title."""
    mock_run.return_value.stdout = json.dumps([
        {"title": "My Token", "id": "abc123"},
        {"title": "Other Token", "id": "xyz789"},
    ])
    result = find_existing_item("My Token", "my-vault")

    assert result == "abc123"

@mock.patch("keysentinel.encryption.subprocess.run")
def test_find_existing_item_not_found(mock_run):
    """Test when item is not found."""
    mock_run.return_value.stdout = json.dumps([
        {"title": "Other Token", "id": "xyz789"},
    ])
    result = find_existing_item("Missing Token", "my-vault")

    assert result is None

@mock.patch("keysentinel.encryption.subprocess.run", side_effect=subprocess.CalledProcessError(1, "cmd"))
def test_find_existing_item_failure(mock_subprocess):
    """Test when subprocess.run fails in find_existing_item."""
    with pytest.raises(VaultOperationError):
        find_existing_item("Any Token", "my-vault")

# --- Tests for upsert_encrypted_fields ---

@mock.patch("keysentinel.encryption.find_existing_item", return_value=None)
@mock.patch("keysentinel.encryption.subprocess.run")
def test_upsert_encrypted_fields_create(mock_run, mock_find, tmp_path):
    """Test creating a new item in the vault."""
    key_path = tmp_path / "test_key.key"
    generate_key(filepath=str(key_path))

    upsert_encrypted_fields(
        fields={"field1": "value1"},
        item_title="New Item",
        key_path=str(key_path),
        vault="TestVault"
    )

    assert mock_run.called

@mock.patch("keysentinel.encryption.find_existing_item", return_value="existing-item-id")
@mock.patch("keysentinel.encryption.subprocess.run")
def test_upsert_encrypted_fields_update(mock_run, mock_find, tmp_path):
    """Test updating an existing item in the vault."""
    key_path = tmp_path / "test_key.key"
    generate_key(filepath=str(key_path))

    upsert_encrypted_fields(
        fields={"field2": "value2"},
        item_title="Existing Item",
        key_path=str(key_path),
        vault="TestVault"
    )

    assert mock_run.called

@mock.patch("keysentinel.encryption.find_existing_item", return_value=None)
@mock.patch("keysentinel.encryption.subprocess.run", side_effect=subprocess.CalledProcessError(1, "cmd"))
def test_upsert_encrypted_fields_failure(mock_run, mock_find, tmp_path):
    """Test failure when subprocess.run raises an exception in upsert."""
    key_path = tmp_path / "test_key.key"
    generate_key(filepath=str(key_path))

    with pytest.raises(VaultOperationError):
        upsert_encrypted_fields(
            fields={"field3": "value3"},
            item_title="Fail Item",
            key_path=str(key_path),
            vault="TestVault"
        )