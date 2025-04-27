import json
import subprocess
from cryptography.fernet import Fernet
from .config import DEFAULT_KEY_PATH
from .exceptions import VaultOperationError


def get_encrypted_token(item_name: str, field_name: str = "password") -> str:
    """Retrieve the encrypted token or the full item from the vault."""
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
    """Load the local encryption key."""
    with open(filepath, "rb") as f:
        return f.read()


def decrypt_token(encrypted_token: str, key: bytes) -> str:
    """Decrypt the token using the provided key."""
    cipher = Fernet(key)
    return cipher.decrypt(encrypted_token.encode()).decode()


def retrieve_and_decrypt_fields(
    item_name: str,
    key_path: str = DEFAULT_KEY_PATH,
) -> dict[str, str]:
    """Retrieve and decrypt all fields from the vault item, excluding the dummy password."""
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
                continue  # skip fields that can't be decrypted

    return decrypted_fields