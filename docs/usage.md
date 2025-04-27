---
title: Usage
nav_order: 3
description: How to use KeySentinel CLI and library.
permalink: /usage/
---

# Usage

## Encrypting a Token

```bash
keysentinel encrypt-token --title "MyAPIKey" --fields api_key
```

or use a predefined profile:

```bash
keysentinel encrypt-token --title "MyAWSKeys" --profile aws
```

## Retrieving a Token

```bash
keysentinel get-token --title "MyAPIKey"
```

- `--copy`: Copy to clipboard temporarily
- `--unsafe-output`: Show real credentials
