# SECURITY.md

# 🔐 KeySentinel Security Model

KeySentinel is designed from the ground up with a **Zero Trust Local Environment** philosophy.
It aims to deliver robust, production-grade security for CLI secrets management while preserving usability.

This document outlines the security principles, design decisions, and operational practices when using KeySentinel.

---

## ⚡️ Core Security Principles

| Principle | Description |
|:----------|:------------|
| Two-Layer Encryption | Local symmetric encryption + Vault storage protected by biometric or user presence validation. |
| No Plaintext Persistence | Secrets are never written to disk in plaintext, even temporarily. |
| Memory-Only Decryption | Secrets exist only in RAM during the process lifetime and are discarded immediately after use. |
| Vault as Transport | Vaults store already-encrypted blobs, not raw tokens. |
| Explicit User Awareness | Users are always warned when decrypted secrets are displayed. |
| Zero Trust Local Machine | Local environments are treated as inherently untrusted. No assumption of local safety is made. |

---

## 🔒 Encryption Model

KeySentinel applies a two-step encryption model:

1. **Local Symmetric Encryption**
   Each token or credential is encrypted using a Fernet symmetric key generated and stored securely on the local machine.

2. **Vault Storage**
   The encrypted blob is stored inside a vault (currently 1Password).
   Vault access requires biometric authentication or user validation.

Compromise of either the vault **or** the local key alone is insufficient to retrieve the plaintext secret.
**Both layers must be breached simultaneously**.

---

## 🔐 Secret Retrieval and Display

When retrieving a secret:

- The vault item is accessed securely via 1Password CLI (`op`).
- The encrypted value is decrypted in-memory using the local key.
- The decrypted secret is printed **directly to stdout**, never to disk.
- A **security warning** is shown before any decrypted information is displayed.

No decrypted secret is ever saved to logs, cache, or persistent files.

---

## 💔 Prohibited Practices

KeySentinel strictly avoids:

- Saving `.env` files or other plaintext dumps of secrets.
- Exporting decrypted tokens to files.
- Local caching of decrypted secrets.
- Logging decrypted secrets.

> **Secrets live only in memory, during the execution, and are discarded immediately after use.**

---

## 🔗 Related Reading

- [Zero Trust Architecture (NIST)](https://csrc.nist.gov/publications/detail/sp/800-207/final)
- [Zero Trust Local Environment Manifesto](https://daviguides.github.io/articles/devsecops/2025/04/25/zero-trust-manifest.html)
- [Two-Layer Security Architecture for Token Management](https://daviguides.github.io/articles/devsecops/2025/04/24/bulding-secure-cli-python.html)

---

## 🔧 Operational Requirements

- The user must have 1Password CLI (`op`) installed and authenticated.
- Local encryption key is stored under `~/.mycli_key` securely.
- Key compromise alone does not expose secrets.
- Vault compromise alone does not expose secrets.
- **Dual compromise (vault + key) is required** for a breach.

---

## 🛡 Future Enhancements

- Multi-key rotation support.
- Abstract vault providers (Bitwarden, custom vaults).
- Auto-expiring secrets in memory.
- Advanced logging without sensitive data.

---

## 💡 Summary

KeySentinel enforces:

- Strict Zero Trust principles.
- Ephemeral memory-only decryption.
- Two-layered protection: Vault + local key.
- Immediate explicit user awareness.

It is built for developers who treat **local machines as attack surfaces, not safe havens**.

> Encrypt everything. Assume breach. Trust nothing.

🔐 **KeySentinel — Secure your CLI workflows.**
