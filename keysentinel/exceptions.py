"""Exception definitions for KeySentinel.

This module defines custom exception classes used for handling
errors related to vault operations and encryption processes.
"""

class VaultOperationError(Exception):
    """Raised when an operation with the vault fails.

    This exception is typically raised when communication with
    the external vault (e.g., 1Password) encounters an error,
    such as a CLI failure, retrieval issue, or invalid response.
    """
    pass