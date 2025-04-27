# 🤝 Contributing to KeySentinel

Thank you for considering contributing to KeySentinel!

KeySentinel enforces a strict **Zero Trust Local Environment** model.
All contributions must **preserve**, **strengthen**, and **respect** this security foundation.

---

## 🚀 How to Contribute

- Fork this repository.
- Create a feature branch:

  ```bash
  git checkout -b feature/your-feature-name
  ```

- Make your changes following the contribution guidelines.
- Commit clearly:

  ```bash
  git commit -m "feat: brief description of the change"
  ```

- Push your branch:

  ```bash
  git push origin feature/your-feature-name
  ```

- Open a Pull Request (PR) with a clear and concise description of your changes.

---

## 📋 Pull Request Guidelines

- Focus on **security**, **clarity**, and **minimalism**.
- **Never** introduce plaintext persistence or weaken ephemeral secret handling.
- Maintain **ephemeral** (temporary) treatment of sensitive data.
- Ensure **full type hints** in Python code.
- Write **Google-style** docstrings for all public modules, functions, and classes.
- Update or create documentation if needed (docs/ folder and CLI help).
- Ensure tests pass:

  ```bash
  make test
  ```

- Run pre-commit hooks:

  ```bash
  make pre-commit-test
  ```

---

## 🛡️ Code of Conduct

- Communicate respectfully and constructively.
- Prefer collaboration over confrontation.
- Security and privacy come **first** in every decision.

---

Thank you for helping make KeySentinel even more secure and impactful! 🔥
