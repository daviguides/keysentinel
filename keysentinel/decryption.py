import json
import subprocess
from cryptography.fernet import Fernet
from .config import DEFAULT_KEY_PATH
from .exceptions import VaultOperationError


def get_encrypted_token(item_name: str, field_name: str = "password") -> str:
    """Retrieve the encrypted token from the vault."""
    try:
        output = subprocess.check_output(
            [
                "op",
                "item",
                "get",
                item_name,
                "--field",
                field_name,
                "--format",
                "json",
            ],
            text=True,
        )
    except subprocess.CalledProcessError as e:
        raise VaultOperationError("Failed to retrieve item from 1Password.") from e

    data = json.loads(output)
    return data["value"]


def load_local_key(filepath: str = DEFAULT_KEY_PATH) -> bytes:
    """Load the local encryption key."""
    with open(filepath, "rb") as f:
        return f.read()


def decrypt_token(encrypted_token: str, key: bytes) -> str:
    """Decrypt the token using the provided key."""
    cipher = Fernet(key)
    return cipher.decrypt(encrypted_token.encode()).decode()


def retrieve_and_decrypt_token(
    item_name: str,
    key_path: str = DEFAULT_KEY_PATH,
) -> str:
    """Convenience function to retrieve and decrypt a token."""
    encrypted_token = get_encrypted_token(item_name)
    key = load_local_key(key_path)
    return decrypt_token(encrypted_token, key)
