import subprocess
import sys
import random
import string

try:
    import pyperclip
except ImportError:
    pyperclip = None


def _generate_random_trash(length: int = 100) -> str:
    """Generate a random string to overwrite clipboard."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def clear_clipboard_after_timeout(timeout: int = 30) -> None:
    """Spawn a detached subprocess to clear clipboard after timeout with random trash overwrite."""
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


def safe_copy_to_clipboard(text: str, timeout: int = 30) -> None:
    """Copy text to clipboard and spawn secure cleaning after timeout."""
    if pyperclip is None:
        raise RuntimeError(
            "Clipboard copy requires 'pyperclip' package. Install it first."
        )

    pyperclip.copy(text)
    clear_clipboard_after_timeout(timeout)


def mask_secret_value(value: str) -> str:
    """Mask a secret value, showing only beginning and end."""
    if len(value) > 8:
        return value[:4] + "..." + value[-4:]
    return "***masked***"