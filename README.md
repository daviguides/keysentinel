# KeySentinel 🔐

<p align="center">
  <a href="./SECURITY.md"><img src="https://img.shields.io/badge/security-zero%20trust-blue"></a>
  <a href="./LICENSE"><img src="https://img.shields.io/badge/license-MIT-green.svg"></a>
  <a href="http://daviguides.github.io"><img src="https://img.shields.io/badge/built%20with-%E2%9D%A4%EF%B8%8F%20by%20Davi%20Guides-orange"></a>
  <a href="https://daviguides.github.io/articles/devsecops/2025/04/25/zero-trust-manifest.html"><img src="https://img.shields.io/badge/read-architecture%20article-blueviolet"></a>
</p>

KeySentinel is a lightweight, secure token encryption library and CLI tool for managing sensitive credentials with strong Zero Trust principles.

📖 [Read the full article explaining the Two-Layer Security Architecture here](https://daviguides.github.io/articles/devsecops/2025/04/25/zero-trust-manifest.html)

---

## ✨ Features

- 🔐 Two-layer token encryption: local symmetric key + vault storage
- 🚀 Developer-friendly CLI (keysentinel) with zero plaintext leakage
- 🔥 Predefined profiles for common APIs (AWS, GitHub, OpenAI, GCP, etc.)
- 🛡️ Extensible custom profiles via JSON
- 💩 Zero Trust Local Environment Enforcement
- 🗋 Secure clipboard copy with automatic timeout cleaning
- ❌ Export to plaintext files (.env, .json) intentionally blocked for safety

---

## 🚀 Why KeySentinel?

Most CLI tools expose credentials through .env files or unsecured memory spaces.

KeySentinel breaks this insecure paradigm:

- No unencrypted secrets on disk.
- No unguarded outputs without user consent.
- Ephemeral secrets that self-destroy after a timeout.
- Clear warnings to educate developers about security risks.

> "If it’s not encrypted, it’s exposed. If it’s on disk, it’s compromised." — The Zen of Zero Trust

---

## ⚡ Quick Usage

### Encrypt and store a token via Python

```python
from keysentinel import upsert_encrypted_fields

upsert_encrypted_fields(
    fields={"github_token": "ghp_xxx123"},
    item_title="GitHub CLI Token",
)
```

### Retrieve and decrypt a token via Python

```python
from keysentinel import retrieve_and_decrypt_fields

fields = retrieve_and_decrypt_fields("GitHub CLI Token")
print(fields["github_token"])
```

### Using the CLI (Recommended)

```bash
# Encrypt and store fields securely (values prompted securely)
keysentinel encrypt-token --title "AWS CLI Credentials" --fields aws_access_key_id --fields aws_secret_access_key

# Or use a predefined profile
keysentinel encrypt-token --title "GitHub Token" --profile github

# Retrieve and decrypt fields
keysentinel get-token --title "AWS CLI Credentials"
```

> ⚠️ Credentials will be cleared from your terminal and memory automatically after a short timeout.

---

## 🛡️ Security Model

| Aspect             | Behavior                                  |
|--------------------|-------------------------------------------|
| Local Encryption   | AES256/Fernet with a user-local symmetric key |
| Vault Transport    | Secrets stored inside 1Password CLI (“op”) |
| Decryption         | Memory-only, no disk writes               |
| Export             | Blocked by default (no .env, no .json)    |
| User Awareness     | Visual warnings on decrypted output       |
| Secret Lifecycle   | Timeout auto-clears memory and screen     |

---

## 📂 Token Profiles (Built-in)

KeySentinel supports predefined profiles to simplify common API credential handling:

| Profile  | Fields |
|----------|--------|
| aws      | aws_access_key_id, aws_secret_access_key |
| github   | github_token |
| gcp      | gcp_client_email, gcp_private_key, gcp_project_id |
| openai   | openai_api_key |
| azure    | azure_client_id, azure_client_secret, azure_tenant_id, azure_subscription_id |
| slack    | slack_token |

and many others… (30+ profiles supported!)

You can list and use these profiles by passing `--profile <profile_name>`.

---

## 🛠️ Extend with Custom Profiles

You can extend KeySentinel by creating a file at:

```bash
~/.keysentinel_profiles.json
```

Example content:

```json
{
  "huggingface": {
    "description": "Hugging Face API Token",
    "fields": ["hf_token"]
  },
  "figma": {
    "description": "Figma Personal Access Token",
    "fields": ["figma_token"]
  }
}
```

When running `encrypt-token`, your custom profiles will be automatically available!

---

## ❌ Why Export is Blocked

KeySentinel blocks plaintext exports (`--export-env`, `--export-json`) intentionally.

Attempting to use them shows this educational warning:

> ⚠️  Do NOT store or copy them into plaintext files or version control.
>
> "If it's not encrypted, it's exposed.
> If it's on disk, it's compromised."
>
> from "The Zen of Zero Trust"

For more info:

- run: `import zero_trust`
- read: [Zero Trust Local Environment Manifesto](https://daviguides.github.io/articles/devsecops/2025/04/25/zero-trust-manifest.html)

---

## 📜 Zero Trust Manifest

You can load the philosophy inside Python:

```python
import zero_trust
```

Or read it online:

👉 [Zero Trust Local Environment Manifesto](https://daviguides.github.io/articles/devsecops/2025/04/25/zero-trust-manifest.html)

---

## 🔗 Related Reading

- [Zero Trust Architecture (NIST)](https://csrc.nist.gov/publications/detail/sp/800-207/final)
- [Zero Trust Local Environment Manifesto](https://daviguides.github.io/articles/devsecops/2025/04/25/zero-trust-manifest.html)
- [Two-Layer Security Architecture for Token Management](https://daviguides.github.io/articles/devsecops/2025/04/24/bulding-secure-cli-python.html)

---

## 🛃️ Roadmap

- Secure CLI operations
- Custom and extensible token profiles
- Memory-timeout auto-clear after exposure
- Multi-vault support (future)
- Bitwarden CLI integration (future)

---

## ⚖️ License

MIT License

---

## 👨‍💼 Author

Built with ❤️ by [Davi Luiz Guides](http://daviguides.github.io)

---

# KeySentinel: Secure your tokens, secure your workflows. 🔐
