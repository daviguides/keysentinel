# KeySentinel 🔐

<p align="center">
  <a href="./SECURITY.md"><img src="https://img.shields.io/badge/security-zero%20trust-blue"></a>
  <a href="./LICENSE"><img src="https://img.shields.io/badge/license-MIT-green.svg"></a>
  <a href="http://daviguides.github.io"><img src="https://img.shields.io/badge/built%20with-%E2%9D%A4%EF%B8%8F%20by%20Davi%20Guides-orange"></a>
  <a href="http://daviguides.github.io/posts/link_to_post"><img src="https://img.shields.io/badge/read-architecture%20article-blueviolet"></a>
</p>

**KeySentinel** is a lightweight and secure token encryption library designed for CLI tools.
It implements a two-layer security architecture to encrypt and store sensitive tokens safely, combining local encryption with 1Password vault integration.

[Read the full article explaining the Two-Layer Security Architecture here](http://daviguides.github.io/posts/link_to_post)

---

## Features

- Two-layer token encryption: local key + vault protection
- Secure storage and retrieval of API keys, GitHub tokens, AWS credentials
- Minimal exposure: no plaintext tokens on disk or in environment variables
- Memory-only token decryption after vault access
- Developer-friendly: simple usage with strong security guarantees
- Fully compatible with 1Password CLI ("op")
- Strong Zero-Trust Local Environment enforcement

---

## Why KeySentinel?

Most CLI tools store tokens insecurely in plaintext files or environment variables.
**KeySentinel** eliminates this risk by ensuring that your secrets remain encrypted at rest and are only decrypted in memory after biometric or secure vault access.

This approach significantly reduces the attack surface for local and remote threats while maintaining a seamless developer experience.

**KeySentinel never stores sensitive information as plaintext on disk.**
Decrypted tokens are ephemeral — they live only in memory for the current execution context.

> **Zero Trust Local Environment**: No .env files, no plaintext caches, no filesystem residue.

---

## Usage

### Encrypt and store a token

```python
from keysentinel import upsert_encrypted_token

upsert_encrypted_token(
    token_plain="ghp_xxx123",
    item_title="GitHub CLI Token Enc",
)
```

### Retrieve and decrypt a token

```python
from keysentinel import retrieve_and_decrypt_token

token = retrieve_and_decrypt_token(
    item_name="GitHub CLI Token Enc",
)
print(token)
```

### Using the CLI

```bash
# Encrypt and store fields securely (values prompted securely, not via command line arguments)
keysentinel encrypt-token --title "AWS CLI Credentials" --fields aws_access_key_id --fields aws_secret_access_key

# Retrieve and decrypt fields
keysentinel get-token --title "AWS CLI Credentials"
```

> ⚠️ Sensitive credentials will be decrypted and displayed in your terminal. Do NOT store them in plaintext files.

---

## Security Philosophy

- **Two-Layer Encryption**: Local symmetric key + vault protection.
- **No Plaintext Persistence**: Decrypted data never touches the disk.
- **Memory-Only Decryption**: Secrets exist only temporarily in memory.
- **Vault as Transport, Not Storage**: Vault stores already-encrypted blobs.
- **User Awareness**: Warnings are shown whenever decrypted material is displayed.

**This strict model enforces Zero Trust even against local machine compromises.**

---

## Roadmap

- [x] Support simple token encryption and storage
- [x] Secure multi-field encryption (AWS credentials, etc.)
- [x] Native CLI (Typer-powered)
- [ ] Multi-vault and multi-backend support (e.g., Bitwarden)
- [ ] Advanced token types handling (OAuth, API Secrets)
- [ ] Profile templates for common token types (GitHub, AWS, GCP, etc.)

---

## License

MIT License

---

## Author

Davi Luiz Guides
[Portfolio](http://daviguides.github.io)

---

**Secure your CLI workflows with KeySentinel.**

⚡️ Encrypt, Vault, Protect. 🔐
