---
name: context7
description: Retrieve current library documentation and code examples from Context7. Use when looking up library APIs, "docs", specific library versions, or "how to use [library]". Prefer over training knowledge for library-specific questions. Do not use for general programming concepts.
---

# Context7 Documentation Lookup

Retrieve current documentation and code examples for any programming library directly from the source.

## Usage

Use the Python script at `scripts/context7.py`.

### Get Documentation

```bash
# Text format (default)
python scripts/context7.py docs \
  --library-id /facebook/react --query "useEffect cleanup function"

# Specific version
python scripts/context7.py docs \
  --library-id /vercel/next.js/v15.1.8 --query "app router middleware"
```

### Search Libraries

Use search only when the library ID is unknown:

```bash
python scripts/context7.py search \
  --library react --query "hooks"
```

## Query Tips

- Use detailed, natural language queries for better results
- Good: `"How to implement authentication with middleware"`
- Bad: `"auth"`

## Common Library IDs

| Library | ID |
| ------- | -- |
| React | `/facebook/react` |
| Next.js | `/vercel/next.js` |
| TailwindCSS | `/tailwindlabs/tailwindcss` |
| Expo | `/expo/expo` |
| ORPC | `middleapi/orpc` |

## Rules

- Query docs directly when you know the library ID
- Use search only if unsure about the library ID
- Use specific version IDs for consistent results (e.g., `/vercel/next.js/v15.1.8`)
- Use `--format json` for structured output
