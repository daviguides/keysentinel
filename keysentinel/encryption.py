"""Encryption utilities for KeySentinel.

This module provides functions to securely encrypt tokens,
generate or load local encryption keys, and manage encrypted
items within a 1Password vault.
"""

import os
import json
import subprocess
from cryptography.fernet import Fernet
from .config import DEFAULT_KEY_PATH, DEFAULT_VAULT_NAME
from .exceptions import VaultOperationError


def upsert_encrypted_fields(
    fields: dict[str, str],
    item_title: str,
    vault: str = DEFAULT_VAULT_NAME,
    key_path: str = DEFAULT_KEY_PATH,
) -> None:
    """Encrypt and create or update multiple fields securely in the vault.

    Args:
        fields (dict[str, str]): Dictionary of field names and their plaintext values to encrypt.
        item_title (str): Title of the item in the vault.
        vault (str, optional): Vault name to store the item. Defaults to DEFAULT_VAULT_NAME.
        key_path (str, optional): Path to the local symmetric key file. Defaults to DEFAULT_KEY_PATH.

    Raises:
        VaultOperationError: If creation or update in the vault fails.
    """
    key = generate_key(key_path)
    encrypted_fields = []

    dummy_value = encrypt_token("DUMMY_PASSWORD_DO_NOT_USE", key)
    encrypted_fields.append({
        "id": "password",
        "type": "STRING",
        "label": "Password",
        "value": dummy_value,
        "purpose": "PASSWORD",
    })

    for field_name, field_value in fields.items():
        encrypted_value = encrypt_token(field_value, key)
        encrypted_fields.append({
            "id": field_name,
            "type": "STRING",
            "label": field_name,
            "value": encrypted_value,
        })

    existing_item_id = find_existing_item(item_title, vault)

    item_payload = {
        "title": item_title,
        "fields": encrypted_fields,
        "tags": ["cli-token"],
    }

    command = (
        ["op", "item", "edit", existing_item_id, "-", "--vault", vault]
        if existing_item_id else
        ["op", "item", "create", "--vault", vault, "--category", "Password", "-"]
    )

    try:
        subprocess.run(
            command,
            input=json.dumps(item_payload),
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        raise VaultOperationError("Failed to create or update item in 1Password.") from e


def find_existing_item(title: str, vault: str) -> str | None:
    """Check if an item already exists in the vault by title.

    Args:
        title (str): The title of the item to search for.
        vault (str): The name of the vault to search in.

    Returns:
        str | None: The ID of the existing item if found, otherwise None.

    Raises:
        VaultOperationError: If the 1Password CLI fails to list items.
    """
    try:
        result = subprocess.run(
            ["op", "item", "list", "--vault", vault, "--format", "json"],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        raise VaultOperationError("Could not list items from 1Password.") from e

    items = json.loads(result.stdout)
    for item in items:
        if item.get("title") == title:
            return item.get("id")
    return None


def encrypt_token(token: str, key: bytes) -> str:
    """Encrypt a plaintext token using the provided symmetric key.

    Args:
        token (str): The plaintext token to encrypt.
        key (bytes): The encryption key to use.

    Returns:
        str: The encrypted token encoded as a string.
    """
    cipher = Fernet(key)
    encrypted = cipher.encrypt(token.encode())
    return encrypted.decode()


def generate_key(filepath: str = DEFAULT_KEY_PATH) -> bytes:
    """Generate or load a symmetric encryption key.

    Args:
        filepath (str, optional): Path to the local key file. Defaults to DEFAULT_KEY_PATH.

    Returns:
        bytes: Symmetric encryption key as bytes.
    """
    if os.path.exists(filepath):
        with open(filepath, "rb") as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        with open(filepath, "wb") as f:
            f.write(key)
        return key