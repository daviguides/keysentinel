# KeySentinel 🔐

**KeySentinel** is a lightweight and secure token encryption library designed for CLI tools.
It implements a two-layer security architecture to encrypt and store sensitive tokens safely, combining local encryption with 1Password vault integration.

[Read the full article explaining the Two-Layer Security Architecture here](http://daviguides.github.io/posts/link_to_post)

---

## Features

- Two-layer token encryption: local key + vault protection
- Secure storage and retrieval of API keys, GitHub tokens, AWS credentials
- Minimal exposure: no plaintext tokens on disk or in environment variables
- Developer-friendly: simple usage with strong security guarantees

---

## Why KeySentinel?

Most CLI tools store tokens insecurely in plaintext files or environment variables.
**KeySentinel** eliminates this risk by ensuring that your secrets remain encrypted at rest and are only decrypted in memory after biometric or secure vault access.

This approach significantly reduces the attack surface for local and remote threats while maintaining a seamless developer experience.

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

---

## Roadmap

- [x] Support simple token encryption and storage
- [ ] Support AWS credentials (Access Key ID + Secret Access Key)
- [ ] Native CLI (Typer-powered)
- [ ] Multi-vault and multi-backend support (e.g., Bitwarden)
- [ ] Advanced token types handling (OAuth, API Secrets)

---

## License

MIT License

---

## Author

Davi Luiz Guides
[Portfolio](http://daviguides.github.io)
