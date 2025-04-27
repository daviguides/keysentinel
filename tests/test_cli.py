import time
from typer.testing import CliRunner
from unittest import mock
from keysentinel.cli import app

runner = CliRunner()

# --- Tests for encrypt-token ---

@mock.patch("keysentinel.cli.upsert_encrypted_fields")
@mock.patch("keysentinel.cli.typer.prompt", return_value="dummy_secret")
def test_encrypt_token_with_fields(mock_prompt, mock_upsert):
    """Test encrypting with manual fields."""
    result = runner.invoke(app, ["encrypt-token", "--title", "MyItem", "--fields", "api_key"])
    assert result.exit_code == 0
    assert "Encrypted and saved fields" in result.output
    mock_upsert.assert_called_once()

@mock.patch("keysentinel.cli.upsert_encrypted_fields")
@mock.patch("keysentinel.cli.typer.prompt", return_value="dummy_secret")
@mock.patch("keysentinel.cli.get_token_profiles", return_value={"aws": {"fields": ["access_key", "secret_key"]}})
def test_encrypt_token_with_profile(mock_profiles, mock_prompt, mock_upsert):
    """Test encrypting with a predefined profile."""
    result = runner.invoke(app, ["encrypt-token", "--title", "MyAWS", "--profile", "aws"])
    assert result.exit_code == 0
    assert "Encrypted and saved fields" in result.output
    mock_upsert.assert_called_once()

def test_encrypt_token_no_fields_no_profile():
    """Test encrypting without fields or profile (error)."""
    result = runner.invoke(app, ["encrypt-token", "--title", "FailItem"])
    assert result.exit_code != 0
    assert "must provide either --fields or --profile" in result.output

def test_encrypt_token_both_fields_and_profile():
    """Test encrypting with both fields and profile (error)."""
    result = runner.invoke(app, [
        "encrypt-token", "--title", "FailItem",
        "--fields", "api_key", "--profile", "aws"
    ])
    assert result.exit_code != 0
    assert "Cannot use --fields and --profile together" in result.output

@mock.patch("keysentinel.cli.get_token_profiles", return_value={})
def test_encrypt_token_invalid_profile(mock_profiles):
    """Test encrypting with invalid profile."""
    result = runner.invoke(app, ["encrypt-token", "--title", "Invalid", "--profile", "ghost"])
    assert result.exit_code != 0
    assert "Profile 'ghost' not found" in result.output

# --- Tests for get-token ---

@mock.patch("keysentinel.cli.retrieve_and_decrypt_fields", return_value={"api_key": "supersecretvalue"})
@mock.patch("keysentinel.cli.safe_copy_to_clipboard")
def test_get_token_copy(mock_copy, mock_retrieve):
    """Test getting token with clipboard copy."""
    result = runner.invoke(app, ["get-token", "--title", "MyItem", "--copy"])
    assert result.exit_code == 0
    assert "copied to clipboard" in result.output
    mock_copy.assert_called_once()

@mock.patch("keysentinel.cli.retrieve_and_decrypt_fields", return_value={"api_key": "supersecretvalue"})
def test_get_token_masked(mock_retrieve, monkeypatch):
    """Test getting token with safe masked output."""
    monkeypatch.setattr(time, "sleep", lambda x: None)  # Skip sleep
    result = runner.invoke(app, ["get-token", "--title", "MyItem"])
    assert result.exit_code == 0
    assert "..." in result.output

@mock.patch("keysentinel.cli.retrieve_and_decrypt_fields", return_value={"api_key": "supersecretvalue"})
def test_get_token_unsafe(mock_retrieve, monkeypatch):
    """Test getting token with unsafe output."""
    monkeypatch.setattr(time, "sleep", lambda x: None)
    result = runner.invoke(app, ["get-token", "--title", "MyItem", "--unsafe-output"])
    assert result.exit_code == 0
    assert "supersecretvalue" in result.output

def test_get_token_export_env_blocked():
    """Test blocked --export-env option."""
    result = runner.invoke(app, ["get-token", "--title", "MyItem", "--export-env"])
    assert "Do NOT store or copy" in result.output

def test_get_token_export_json_blocked():
    """Test blocked --export-json option."""
    result = runner.invoke(app, ["get-token", "--title", "MyItem", "--export-json"])
    assert "Do NOT store or copy" in result.output

@mock.patch("keysentinel.cli.retrieve_and_decrypt_fields", return_value={})
def test_get_token_not_found(mock_retrieve):
    """Test retrieving token when no fields found."""
    result = runner.invoke(app, ["get-token", "--title", "UnknownItem"])
    assert result.exit_code != 0
    assert "No fields found" in result.output

@mock.patch("keysentinel.cli.safe_copy_to_clipboard", side_effect=RuntimeError("Clipboard not available"))
@mock.patch("keysentinel.cli.retrieve_and_decrypt_fields", return_value={"api_key": "supersecretvalue"})
def test_get_token_copy_failure(mock_retrieve, mock_safe_copy):
    """Test get-token --copy when clipboard copy fails."""
    result = runner.invoke(app, ["get-token", "--title", "MyItem", "--copy"])
    assert result.exit_code != 0
    assert "Clipboard not available" in result.output