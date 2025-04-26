# SECURITY.md

# KeySentinel Security Model 🔐

KeySentinel is designed from the ground up with a **Zero Trust Local Environment** philosophy.
Its goal is to provide robust, production-grade security for CLI secrets management while preserving usability.

This document outlines the security principles, design decisions, and operational expectations when using KeySentinel.

---

## ⚡️ Core Security Principles

| Principle | Description |
|:----------|:------------|
| Two-Layer Encryption | Local encryption with a symmetric key + Vault storage with biometric/unlock protection. |
| No Plaintext Persistence | Secrets are never written to disk in plaintext, not even temporarily. |
| Memory-Only Decryption | Secrets are decrypted only in RAM during process lifetime and discarded immediately after use. |
| Vault as Transport | The 1Password vault stores already-encrypted blobs, not raw tokens. |
| Explicit User Awareness | Users are always warned when decrypted secrets are displayed. |
| Zero Trust Local Machine | Local environments are treated as inherently untrusted. No sensitive data relies on local security assumptions. |

---

## 🔒 Encryption Model

KeySentinel uses a two-step model:

1. **Local Symmetric Encryption**
   - Each token or credential is encrypted using a symmetric key (Fernet) that is generated and stored securely on the local machine.

2. **Vault Storage**
   - The encrypted token is stored inside 1Password.
   - 1Password provides user presence validation (e.g., TouchID, Password Unlock) to access the blob.

If either layer is compromised alone (vault OR key), the secret remains protected.
Only with both layers combined can the token be recovered.

---

## 🔐 Secret Retrieval and Display

When retrieving a secret:

- The vault item is accessed securely via 1Password CLI (`op`).
- The encrypted blob is decrypted in memory using the local key.
- The decrypted value is **printed immediately** to standard output (**stdout**) only.
- A **security warning** is displayed before showing any secrets.

No secret is ever written to disk, logs, or temporary files.

---

## 💔 Prohibited Practices

KeySentinel deliberately avoids:

- Saving `.env` files with decrypted tokens.
- Exporting tokens to JSON or plaintext files.
- Caching secrets locally.
- Persisting decrypted information across sessions.
- Logging decrypted secrets.

**Secrets only exist ephemerally in memory during usage.**

---

## 🔗 Related Reading

- [Zero Trust Local Environment Manifesto](http://daviguides.github.io/posts/link_to_zero_trust_manifesto) *(coming soon)*
- [Two-Layer Security Architecture for Token Management](http://daviguides.github.io/posts/link_to_post)

---

## 🔧 Operational Notes

- Users must have the 1Password CLI (`op`) installed and authenticated.
- The local encryption key is stored securely under the user's home directory (`~/.mycli_key`).
- If a local key is compromised, vault security still protects the token.
- If the vault is compromised, the local key encryption still protects the token.
- **Both layers must be compromised simultaneously** to access a secret.

---

## 📖 Future Enhancements

- Multi-key rotation support.
- Vault provider abstraction (supporting Bitwarden, custom vaults).
- Auto-expiration timers for secrets in memory.
- Advanced logging with zero-sensitive-data guarantee.

---

## 💡 Summary

KeySentinel enforces:

- Zero Trust principles.
- Memory-only decryption.
- Vault + local key dual protection.
- Immediate user awareness.

It is built for developers who take **serious** care of their credentials, treating the local machine not as a safe, but as an attack surface.

Stay safe. Encrypt everything.

# 🔐 KeySentinel - Secure your CLI workflows
