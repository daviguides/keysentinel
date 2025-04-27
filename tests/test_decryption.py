import json
import pytest
import subprocess
from unittest import mock
from cryptography.fernet import Fernet
from keysentinel.decryption import (
    get_encrypted_token,
    load_local_key,
    decrypt_token,
    retrieve_and_decrypt_fields,
)
from keysentinel.exceptions import VaultOperationError


# --- Tests for get_encrypted_token ---

@mock.patch("keysentinel.decryption.subprocess.check_output")
def test_get_encrypted_token_with_field(mock_check_output):
    """Test retrieving an encrypted token for a specific field."""
    mock_check_output.return_value = '{"value": "encrypted_token_data"}'
    output = get_encrypted_token("My Item", field_name="password")
    assert isinstance(output, str)

@mock.patch("keysentinel.decryption.subprocess.check_output")
def test_get_encrypted_token_without_field(mock_check_output):
    """Test retrieving the full item without specifying a field."""
    mock_check_output.return_value = '{"fields": []}'
    output = get_encrypted_token("My Item", field_name=None)
    assert isinstance(output, str)

@mock.patch("keysentinel.decryption.subprocess.check_output", side_effect=subprocess.CalledProcessError(1, "op"))
def test_get_encrypted_token_failure(mock_check_output):
    """Test that get_encrypted_token raises VaultOperationError on failure."""
    with pytest.raises(VaultOperationError):
        get_encrypted_token("Broken Item")


# --- Tests for load_local_key ---

def test_load_local_key_reads_file(tmp_path):
    """Test loading a local encryption key."""
    key_path = tmp_path / "keyfile.key"
    key_data = Fernet.generate_key()
    key_path.write_bytes(key_data)

    loaded_key = load_local_key(filepath=str(key_path))
    assert loaded_key == key_data


# --- Tests for decrypt_token ---

def test_decrypt_token_success():
    """Test successful decryption of a token."""
    key = Fernet.generate_key()
    cipher = Fernet(key)
    original = "my_secret_token"
    encrypted = cipher.encrypt(original.encode()).decode()

    decrypted = decrypt_token(encrypted, key)
    assert decrypted == original


# --- Tests for retrieve_and_decrypt_fields ---

@mock.patch("keysentinel.decryption.get_encrypted_token")
@mock.patch("keysentinel.decryption.load_local_key")
def test_retrieve_and_decrypt_fields_success(mock_load_key, mock_get_token):
    """Test retrieving and decrypting multiple fields."""
    key = Fernet.generate_key()
    cipher = Fernet(key)

    fields_payload = {
        "fields": [
            {"id": "aws_access_key_id", "value": cipher.encrypt(b"ACCESSKEY").decode()},
            {"id": "aws_secret_access_key", "value": cipher.encrypt(b"SECRETKEY").decode()},
            {"id": "password", "value": cipher.encrypt(b"DUMMY_PASSWORD_DO_NOT_USE").decode()},  # Should be skipped
        ]
    }

    mock_get_token.return_value = json.dumps(fields_payload)
    mock_load_key.return_value = key

    fields = retrieve_and_decrypt_fields("AWS Credentials Item")

    assert "aws_access_key_id" in fields
    assert fields["aws_access_key_id"] == "ACCESSKEY"
    assert "aws_secret_access_key" in fields
    assert fields["aws_secret_access_key"] == "SECRETKEY"
    assert "password" not in fields


@mock.patch("keysentinel.decryption.get_encrypted_token", side_effect=VaultOperationError)
def test_retrieve_and_decrypt_fields_error(mock_get_token):
    """Test error handling if retrieval fails."""
    with pytest.raises(VaultOperationError):
        retrieve_and_decrypt_fields("Broken Item")

@mock.patch("keysentinel.decryption.decrypt_token", side_effect=Exception)
@mock.patch("keysentinel.decryption.get_encrypted_token")
def test_retrieve_and_decrypt_fields_skips_failed_decrypt(mock_get_token, mock_decrypt, tmp_path):
    """Test retrieve_and_decrypt_fields skips fields that fail decryption."""
    # Simulate an item with one encrypted field
    fake_item = {
        "fields": [
            {"id": "aws_secret_access_key", "value": "dummy_encrypted_value"}
        ]
    }
    mock_get_token.return_value = json.dumps(fake_item)

    # ✅ Create a valid local key (even if it won't be used due to the mock)
    from keysentinel.encryption import generate_key
    key_path = tmp_path / "test_key.key"
    generate_key(filepath=str(key_path))

    # Should skip field because decrypt_token raises Exception
    result = retrieve_and_decrypt_fields("Any Item", key_path=str(key_path))

    assert isinstance(result, dict)
    assert len(result) == 0  # No fields should be returned