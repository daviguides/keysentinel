# 📋 CHANGELOG.md

# Changelog

## [Unreleased]

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

# 🛠 [Next]

- Multi-vault support (e.g., Bitwarden)
- OAuth and token auto-refresh profiles
- Improved error handling and diagnostics

---

# 🗓 Versioning

- Current: Development (Unreleased)
- Next planned release: `v0.2.0`

---

# 🧑‍💻 Maintained by [Davi Luiz Guides](https://daviguides.github.io) 🚀
