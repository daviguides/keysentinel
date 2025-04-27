# 📋 CHANGELOG.md

# Changelog

## [v0.2.0] - 2025-04-27

### Added

- Full **unit test suite** for encryption, decryption, profiles, utils, and CLI.
- **Pytest coverage integration** with `pytest.ini` and updated `Makefile` commands for:
  - Testing
  - Coverage reports
  - Linting and formatting.
- **New CLI behaviors**:
  - Blocked export to `.env` and `.json` explicitly with proper coverage.
  - Secure masked output and unsafe output logic fully tested.
- **Fake clipboard** testing for timeout and clearing clipboard securely.
- **Updated `Makefile`** to include:
  - `test`, `coverage-html`, `coverage-term`, `lint`, `format`, `check-format`, `pre-commit-install`, `pre-commit-test`, `clean`
- **Updated README badges** and added full test coverage explanation.

### Changed

- **Refactored `tests/` structure** to be modular and separated by concern.
- **Corrected coverage handling** for export blocking paths.
- **Removed unnecessary `return` after export block** in CLI.
- **Minor internal adjustments** to tests for robustness.

### Fixed

- CLI tests now properly mock functions (fixing fixture errors).
- Corrected CLI safe masked output test to match actual output.
- Full 100% coverage for `utils.py`, `profiles.py`, `encryption.py`, `decryption.py`.

---

# 🛡 Zero Trust Local Enforcement: Strengthened Further

> "If it's not encrypted, it's exposed. If it's on disk, it's compromised."

---

## [v0.1.0] - 2025-04-25

### Added

- `profiles.py`: Introduced **predefined token profiles** (AWS, GitHub, OpenAI, etc.) with dynamic extension via `~/.keysentinel_profiles.json`.
- `utils.py`: Created utilities for secure clipboard handling and masking secrets.
- `zero_trust/__init__.py`: Added the "Zen of Zero Trust" easter egg importable via `import zero_trust`.

### Changed

- **CLI (`cli.py`) major enhancements**:
  - New `--profile` option to simplify secure token creation.
  - Clipboard copying (`--copy`) with **auto-clear** timeout feature.
  - `--unsafe-output` to view real credentials with auto memory cleanup.
  - Exporting to `.env` or `.json` files is blocked to enforce Zero Trust principles.
- **Updated `README.md`**:
  - Reflects new profile system, usage examples, and security philosophy.
  - Badges updated.

### Fixed

- Improved field input handling and memory clearance in CLI output.
- Minor consistency fixes across encryption and decryption modules.

---

# 🛡 Zero Trust Local Enforcement: Strengthened

> "If it's not encrypted, it's exposed. If it's on disk, it's compromised."

---

# 🛠 [Next Planned Improvements]

- Multi-vault support (e.g., Bitwarden integration)
- OAuth and token auto-refresh profiles
- Improved error handling and diagnostics
- Command aliases for faster CLI usage

---

# 🗓 Versioning

- Current: `v0.2.0`
- Previous: `v0.1.0`

---

# 🧑‍💻 Maintained by [Davi Luiz Guides](https://daviguides.github.io) 🚀
