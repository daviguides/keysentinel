# CLAUDE.md

This file provides guidance to Claude Code when working with this project.

## Project Overview

KeySentinel is a production-ready Python library for secure token encryption and management with Zero Trust principles. It provides both a CLI tool and Python API for managing sensitive credentials with two-layer encryption (local symmetric key + 1Password vault storage).

**Type**: Library (Published to PyPI)
**Purpose**: Provide secure, developer-friendly credential management with Zero Trust enforcement
**Status**: Production (v0.2.8)

### Key Features

- Two-layer token encryption (local AES256 + 1Password vault)
- Developer-friendly CLI with zero plaintext leakage
- 30+ predefined API profiles (AWS, GitHub, OpenAI, GCP, etc.)
- Extensible custom profiles via JSON
- Secure clipboard copy with automatic timeout
- Zero Trust Local Environment philosophy
- Memory-only decryption (no disk writes)
- 100% test coverage

---

## Project Structure

```
keysentinel/
├── README.md                      # Full documentation with architecture
├── SECURITY.md                    # Security model documentation
├── pyproject.toml                 # Package configuration
├── keysentinel/
│   ├── __init__.py                # Public API exports
│   ├── cli.py                     # Typer CLI implementation
│   ├── encryption.py              # Encryption logic (AES256/Fernet)
│   ├── decryption.py              # Decryption and retrieval
│   ├── profiles.py                # Token profile definitions (30+)
│   ├── config.py                  # Configuration management
│   ├── utils.py                   # Utilities (clipboard, timeouts)
│   └── exceptions.py              # Custom exceptions
├── zero_trust/
│   └── __init__.py                # Zero Trust philosophy module
└── tests/
    ├── conftest.py                # Pytest fixtures
    ├── test_encryption.py         # Encryption tests
    ├── test_decryption.py         # Decryption tests
    ├── test_cli.py                # CLI command tests
    ├── test_profiles.py           # Profile loading tests
    └── test_utils.py              # Utility tests
```

**Key Files**:
- `keysentinel/cli.py` - Typer CLI interface with subcommands
- `keysentinel/profiles.py` - Built-in profiles (AWS, GitHub, etc.)
- `keysentinel/encryption.py` - AES256/Fernet encryption
- `zero_trust/__init__.py` - Zero Trust manifesto

---

## Common Workflows

### Setup / Installation

```bash
uv sync
```

**Requirements**:
- Python >=3.11
- cryptography >=42.0.0
- pyperclip >=1.9.0
- typer >=0.15.2
- 1Password CLI (`op`) for vault backend

### Running CLI Commands

```bash
# List available profiles
uv run keysentinel list-profiles

# Encrypt a token with predefined profile
uv run keysentinel encrypt-token --title "AWS Credentials" --profile aws

# Encrypt with custom fields
uv run keysentinel encrypt-token --title "Custom API" --fields api_key --fields api_secret

# Retrieve and decrypt a token
uv run keysentinel get-token --title "AWS Credentials"

# Shorthand alias
uv run ks get-token --title "AWS Credentials"
```

### Using Python API

```python
from keysentinel import upsert_encrypted_fields, retrieve_and_decrypt_fields

# Encrypt and store
upsert_encrypted_fields(
    fields={"github_token": "ghp_xxx"},
    item_title="GitHub CLI Token",
)

# Retrieve and decrypt
fields = retrieve_and_decrypt_fields("GitHub CLI Token")
print(fields["github_token"])
```

### Running Tests

```bash
uv run pytest -v                          # All tests
uv run pytest tests/test_encryption.py    # Specific module
uv run pytest --cov=keysentinel           # With coverage
uv run pytest -k "profile"                # Tests matching pattern
```

### Publishing to PyPI

```bash
uv build
uv publish
```

---

## Dependencies

**Core Dependencies**:
- **cryptography** - AES256/Fernet encryption primitives
- **pyperclip** - Secure clipboard operations
- **typer** - CLI framework (Click-based)

**Development Dependencies**:
- pytest, pytest-cov - Testing framework
- coverage - Coverage reporting
- ruff - Code linting
- pre-commit - Git hooks
- build, twine - PyPI publishing

**Dependency Manager**: uv (with setuptools backend)

---

## Important Conventions

- All encryption uses Fernet (AES256-based) with per-user symmetric keys
- Vault backend is 1Password CLI (`op` command)
- Profiles are JSON in `~/.keysentinel_profiles.json` for customization
- CLI commands use Typer with subcommands
- No plaintext `.env` files exported (intentionally blocked)
- All secrets cleared from memory after configured timeout
- Use `zero_trust` module for philosophy/guidelines

---

## Security Model

**Two-Layer Architecture**:
1. **Local Encryption**: AES256 Fernet symmetric key stored locally
2. **Vault Storage**: Encrypted data stored in 1Password vault (requires `op` CLI)

**Decryption Flow**:
1. Retrieve encrypted data from 1Password
2. Decrypt with local symmetric key
3. Return plaintext only in memory (no disk writes)
4. Auto-clear memory after timeout

**Export Blocked**: Intentional security feature - no `.env` or `.json` export allowed

---

## Special Considerations

- **Requires 1Password**: Must have `op` CLI installed and authenticated
- **OS-Specific**: Keyring storage varies by OS (Keychain, Secret Service, etc.)
- **Memory Timeout**: Secrets auto-cleared from memory after ~5 minutes
- **Profile Extensibility**: Custom profiles via `~/.keysentinel_profiles.json`
- **Zero Trust Philosophy**: Read `zero_trust/__init__.py` for principles
- **Production-Ready**: 100% test coverage, security-focused design

---

## Troubleshooting

### "1Password CLI not found"

**Problem**: `op command not found`
**Solution**: Install 1Password CLI: `brew install 1password-cli` (macOS) or `apt install 1password` (Linux)

### "Not authenticated to 1Password"

**Problem**: `OP not authenticated` error
**Solution**: Run `op account get --account=<account>` to authenticate first

### "Profile not found"

**Problem**: Profile defined in `~/.keysentinel_profiles.json` not loaded
**Solution**: Check JSON syntax in custom profiles file, restart CLI

### Clipboard permission denied

**Problem**: Pyperclip can't access clipboard
**Solution**: On Linux, install `xclip` or `xsel`: `apt install xclip`

---

## Testing Strategy

- **test_encryption.py** - Fernet encryption/decryption
- **test_decryption.py** - Vault retrieval and decryption
- **test_cli.py** - CLI command interface and user flows
- **test_profiles.py** - Profile loading (built-in and custom)
- **test_utils.py** - Clipboard and timeout utilities

All tests use fixtures in `conftest.py` with mocked 1Password backend.

---

## Documentation

- **README.md** - Complete feature overview and usage
- **SECURITY.md** - Detailed security model and architecture
- **zero_trust/__init__.py** - Philosophy and principles
- [Architecture Article](https://daviguides.github.io/articles/devsecops/2025/04/25/zero-trust-manifest.html)

---

## Notes for Claude Code

When working on KeySentinel:

1. **Security First** - Any changes must maintain Zero Trust principles
2. **Read SECURITY.md** - Understand two-layer architecture before modifications
3. **Profile System** - Changes to profiles require updating docs
4. **Test Coverage** - Maintain 100% coverage for all new code
5. **CLI Interface** - Use Typer conventions for new commands
6. **Backward Compatibility** - This is a published library; breaking changes require major version bump
7. **1Password Dependency** - All tests mock `op` CLI; don't add real vault calls
8. **Philosophy Integration** - Changes should align with `zero_trust` principles

This is a **production library** with active users. Treat changes carefully and test thoroughly.
