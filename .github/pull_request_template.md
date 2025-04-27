# 🚀 Pull Request

## 📜 Summary

<!-- Provide a short summary of the changes introduced by this PR -->

## 🔥 Changes

- [x] CLI Improvements (Profile support, Safe Output, Clipboard Timeout)
- [x] Secure Clipboard Utilities
- [x] Predefined and Extendable Token Profiles
- [x] Zero Trust Easter Egg Import
- [x] Documentation and README Updates
- [x] Changelog Created

## 📦 Related Changes

- Modified `README.md`, `cli.py`, `decryption.py`
- Added `profiles.py`, `utils.py`, `zero_trust/__init__.py`
- Updated `pyproject.toml`

## 🧪 Testing

- [x] Manual CLI tests for encrypt-token and get-token
- [x] Clipboard auto-clear functionality verified
- [x] Safe output masking
- [x] Profile-based token creation tested

## 🛡 Security

- [x] Two-Layer Encryption (local key + vault transport)
- [x] No Plaintext Persistence (secrets never touch disk)
- [x] Memory-Only Decryption (secrets exist only during process lifetime)
- [x] Vault as Transport (1Password stores encrypted blobs, not raw secrets)
- [x] Explicit User Awareness (security warnings on output)
- [x] Zero Trust Local Machine (local environment assumed unsafe)
- [x] Secrets cleared automatically from memory and screen after timeout
- [x] Blocked plaintext export (.env, .json)

## 📢 Notes

This PR aligns KeySentinel to a more professional, extensible, and educational security-first toolchain. ✨
