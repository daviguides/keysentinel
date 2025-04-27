"""Decryption utilities for KeySentinel.

This module provides functions to securely retrieve and decrypt
encrypted tokens stored within a 1Password vault.
"""

import json
import subprocess
from cryptography.fernet import Fernet
from .config import DEFAULT_KEY_PATH
from .exceptions import VaultOperationError


def retrieve_and_decrypt_fields(
    item_name: str,
    key_path: str = DEFAULT_KEY_PATH,
) -> dict[str, str]:
    """Retrieve and decrypt all fields from a vault item, excluding dummy passwords.

    Args:
        item_name (str): The name of the vault item.
        key_path (str, optional): Path to the local encryption key. Defaults to DEFAULT_KEY_PATH.

    Returns:
        dict[str, str]: A dictionary of decrypted field names and their corresponding values.
    """
    encrypted_item_json = get_encrypted_token(item_name, field_name=None)
    item_data = json.loads(encrypted_item_json)
    fields_data = item_data.get("fields", [])

    key = load_local_key(key_path)
    decrypted_fields = {}

    for field in fields_data:
        field_id = field.get("id")
        encrypted_value = field.get("value")
        if field_id and encrypted_value and field_id != "password":
            try:
                decrypted_value = decrypt_token(encrypted_value, key)
                decrypted_fields[field_id] = decrypted_value
            except Exception:
                continue  # Skip fields that can't be decrypted

    return decrypted_fields


def get_encrypted_token(item_name: str, field_name: str = "password") -> str:
    """Retrieve the encrypted token or the full item JSON from the vault.

    Args:
        item_name (str): The name of the item in the vault.
        field_name (str, optional): Specific field to retrieve. Defaults to "password".

    Returns:
        str: JSON-formatted string representing the field or full item.

    Raises:
        VaultOperationError: If retrieving the item from 1Password fails.
    """
    try:
        if field_name is not None:
            output = subprocess.check_output(
                [
                    "op", "item", "get",
                    item_name,
                    "--field", field_name,
                    "--format", "json",
                ],
                text=True
            )
        else:
            output = subprocess.check_output(
                [
                    "op", "item", "get",
                    item_name,
                    "--format", "json",
                ],
                text=True
            )
    except subprocess.CalledProcessError as e:
        raise VaultOperationError("Failed to retrieve item from 1Password.") from e

    return output


def load_local_key(filepath: str = DEFAULT_KEY_PATH) -> bytes:
    """Load the local symmetric encryption key.

    Args:
        filepath (str, optional): Path to the local key file. Defaults to DEFAULT_KEY_PATH.

    Returns:
        bytes: The encryption key as bytes.
    """
    with open(filepath, "rb") as f:
        return f.read()


def decrypt_token(encrypted_token: str, key: bytes) -> str:
    """Decrypt an encrypted token using the provided symmetric key.

    Args:
        encrypted_token (str): The encrypted token string.
        key (bytes): The encryption key used for decryption.

    Returns:
        str: The decrypted plaintext token.
    """
    cipher = Fernet(key)
    return cipher.decrypt(encrypted_token.encode()).decode()