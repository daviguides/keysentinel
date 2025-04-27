"""KeySentinel public API.

Exposes the main encryption and decryption functionalities for secure
token management through 1Password integration.

Modules:
    - encryption: Encrypt and store secrets in the vault.
    - decryption: Retrieve and decrypt secrets from the vault.
    - exceptions: Custom exception classes for vault operations.

Exports:
    - upsert_encrypted_fields
    - retrieve_and_decrypt_fields
    - VaultOperationError
"""

from .encryption import (
    upsert_encrypted_fields,
)
from .decryption import (
    retrieve_and_decrypt_fields,
)
from .exceptions import VaultOperationError

__all__ = [
    "upsert_encrypted_fields",
    "retrieve_and_decrypt_fields",
    "VaultOperationError",
]