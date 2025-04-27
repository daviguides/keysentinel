import json
import tempfile
import os
from keysentinel import profiles
from keysentinel.profiles import (
    TOKEN_PROFILES,
    load_custom_profiles_from_json,
    get_token_profiles,
)

# --- Tests for default profiles ---

def test_default_profiles_exist():
    """Check if some known default profiles exist."""
    assert "aws" in TOKEN_PROFILES
    assert "github" in TOKEN_PROFILES
    assert "openai" in TOKEN_PROFILES
    assert isinstance(TOKEN_PROFILES["aws"]["fields"], list)

# --- Tests for loading custom profiles ---

def test_load_custom_profiles_from_json_success():
    """Test loading custom profiles from a JSON file."""
    custom_profiles = {
        "huggingface": {
            "description": "Hugging Face Token",
            "fields": ["hf_token"]
        }
    }
    with tempfile.NamedTemporaryFile("w", delete=False) as tmpfile:
        json.dump(custom_profiles, tmpfile)
        tmpfile_path = tmpfile.name

    loaded = load_custom_profiles_from_json(filepath=tmpfile_path)

    assert "huggingface" in loaded
    assert loaded["huggingface"]["fields"] == ["hf_token"]

    os.remove(tmpfile_path)

def test_load_custom_profiles_from_json_missing_file():
    """Test behavior when the custom profile JSON file is missing."""
    non_existent_path = "/tmp/non_existent_custom_profiles.json"
    loaded = load_custom_profiles_from_json(filepath=non_existent_path)

    assert loaded == {}

def test_load_custom_profiles_from_json_invalid_file(tmp_path):
    """Test behavior when JSON is invalid (corrupted file)."""
    bad_json_path = tmp_path / "bad.json"
    bad_json_path.write_text("{not_valid_json}")

    loaded = load_custom_profiles_from_json(filepath=str(bad_json_path))

    assert loaded == {}

# --- Tests for merging profiles ---

def test_get_token_profiles_merges_defaults_and_customs():
    """Test merging default and custom profiles."""
    custom_profiles = {
        "figma": {
            "description": "Figma Token",
            "fields": ["figma_token"]
        }
    }
    merged = get_token_profiles(custom_profiles)

    assert "aws" in merged  # Default
    assert "figma" in merged  # Custom
    assert merged["figma"]["fields"] == ["figma_token"]

def test_get_token_profiles_conflict_custom_overrides_default():
    """Custom profiles should override defaults if conflict (simulate conflict)."""
    custom_profiles = {
        "aws": {
            "description": "Custom AWS Override",
            "fields": ["custom_access_key", "custom_secret_key"]
        }
    }
    merged = get_token_profiles(custom_profiles)

    assert merged["aws"]["description"] == "Custom AWS Override"
    assert "custom_access_key" in merged["aws"]["fields"]

def test_load_custom_profiles_from_json_default(tmp_path, monkeypatch):
    """Test loading custom profiles using default path (patched variable, not just env)."""
    dummy_profiles = {"custom_api": {"description": "Custom API", "fields": ["token"]}}
    dummy_path = tmp_path / ".keysentinel_profiles.json"
    dummy_path.write_text(json.dumps(dummy_profiles))

    monkeypatch.setattr(profiles, "DEFAULT_CUSTOM_PROFILES_PATH", str(dummy_path))

    loaded = profiles.load_custom_profiles_from_json()

    assert "custom_api" in loaded
    assert loaded["custom_api"]["fields"] == ["token"]

def test_get_token_profiles_uses_default(tmp_path, monkeypatch):
    """Test get_token_profiles() auto loads default if custom not passed."""
    dummy_profiles = {"custom_gpt": {"description": "Custom GPT", "fields": ["api_key"]}}
    dummy_path = tmp_path / ".keysentinel_profiles.json"
    dummy_path.write_text(json.dumps(dummy_profiles))

    monkeypatch.setattr(profiles, "DEFAULT_CUSTOM_PROFILES_PATH", str(dummy_path))

    token_profiles = profiles.get_token_profiles()

    assert "custom_gpt" in token_profiles
    assert "aws" in token_profiles  # default profiles still merged