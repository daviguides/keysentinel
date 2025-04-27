from unittest import mock
from keysentinel.utils import (
    safe_copy_to_clipboard,
    clear_clipboard_after_timeout,
    mask_secret_value,
)

@mock.patch("keysentinel.utils.subprocess.Popen")
@mock.patch("keysentinel.utils.pyperclip")
def test_safe_copy_to_clipboard_and_clear(mock_pyperclip, mock_popen):
    """Test copying text to clipboard and spawning subprocess to clear."""
    text = "secret_text"
    safe_copy_to_clipboard(text, timeout=1)

    mock_pyperclip.copy.assert_called_once_with(text)
    mock_popen.assert_called_once()  # Ensure subprocess was launched

@mock.patch("keysentinel.utils.subprocess.Popen")
@mock.patch("keysentinel.utils.pyperclip")
def test_clear_clipboard_after_timeout_direct_call(mock_pyperclip, mock_popen):
    """Test manual call to clear clipboard spawns subprocess."""
    clear_clipboard_after_timeout(timeout=1)

    mock_popen.assert_called_once()  # subprocess must be called

def test_mask_secret_value_short_secret():
    """Test masking very short secret."""
    assert mask_secret_value("abc") == "***masked***"

def test_mask_secret_value_long_secret():
    """Test masking a longer secret."""
    secret = "1234567890"
    masked = mask_secret_value(secret)
    assert masked.startswith("1234") and masked.endswith("7890")
    assert "..." in masked