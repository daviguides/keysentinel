"""Configuration constants for KeySentinel.

This module defines default paths and vault settings used
throughout the encryption and decryption operations.
"""

import os

# Default path for storing the local symmetric encryption key.
DEFAULT_KEY_PATH = os.path.expanduser("~/.mycli_key")

# Default vault name where encrypted items are stored.
DEFAULT_VAULT_NAME = "CLI Tokens"