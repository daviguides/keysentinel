import os
import json
import subprocess
from cryptography.fernet import Fernet
from .config import DEFAULT_KEY_PATH, DEFAULT_VAULT_NAME
from .exceptions import VaultOperationError


def generate_key(filepath: str = DEFAULT_KEY_PATH) -> bytes:
    """Generate or load a symmetric key for local encryption."""
    if os.path.exists(filepath):
        with open(filepath, "rb") as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        with open(filepath, "wb") as f:
            f.write(key)
        return key


def encrypt_token(token: str, key: bytes) -> str:
    """Encrypt a token using the provided key."""
    cipher = Fernet(key)
    encrypted = cipher.encrypt(token.encode())
    return encrypted.decode()


def find_existing_item(title: str, vault: str) -> str | None:
    """Check if an item already exists in the vault."""
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

def upsert_encrypted_fields(
    fields: dict[str, str],
    item_title: str,
    vault: str = DEFAULT_VAULT_NAME,
    key_path: str = DEFAULT_KEY_PATH,
) -> None:
    """Encrypt and save or update multiple fields in the vault."""
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