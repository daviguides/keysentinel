"""Utility functions for clipboard handling and secret masking.

This module provides secure clipboard management with auto-clear
features and simple masking utilities for sensitive values.
"""

import subprocess
import sys
import pyperclip


def safe_copy_to_clipboard(text: str, timeout: int = 30) -> None:
    """Copy text to clipboard securely and clear it after a timeout.

    Args:
        text (str): The text to copy to the clipboard.
        timeout (int, optional): Timeout in seconds before clearing. Defaults to 30 seconds.
    """
    pyperclip.copy(text)
    clear_clipboard_after_timeout(timeout)


def clear_clipboard_after_timeout(timeout: int = 30) -> None:
    """Spawn a detached subprocess to overwrite and clear the clipboard after a timeout.

    Args:
        timeout (int, optional): Time to wait before clearing the clipboard, in seconds. Defaults to 30 seconds.

    Notes:
        This function works across macOS, Windows, and Linux platforms,
        using a background Python process to avoid blocking the main process.
    """
    subprocess.Popen(
        [sys.executable, "-c", f"""
import time
import platform
import subprocess
import pyperclip
import random
import string

def generate_random_trash(length=100):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

time.sleep({timeout})
try:
    trash = generate_random_trash()
    system = platform.system()
    if system == 'Darwin':
        subprocess.run(f"printf '{{trash}}' | pbcopy", shell=True, check=True)
        time.sleep(0.5)
        subprocess.run("printf '' | pbcopy", shell=True, check=True)
    elif system == 'Windows':
        pyperclip.copy(trash)
        time.sleep(0.5)
        pyperclip.copy('')
    elif system == 'Linux':
        pyperclip.copy(trash)
        time.sleep(0.5)
        pyperclip.copy('')
    else:
        pyperclip.copy(trash)
        time.sleep(0.5)
        pyperclip.copy('')
except Exception:
    pass
"""],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        close_fds=True
    )


def mask_secret_value(value: str) -> str:
    """Mask a secret value for safe display.

    Args:
        value (str): The secret value to mask.

    Returns:
        str: A masked version showing only the first and last 4 characters, or a generic mask if too short.
    """
    if len(value) > 8:
        return value[:4] + "..." + value[-4:]
    return "***masked***"