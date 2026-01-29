---
name: tool-gdelt-news
description: Use the gdelt_news tool to fetch recent headlines via GDELT (free) with shared caching, rate limiting, and basic query normalization.
---

# gdelt_news (GDELT headlines)

## When to use

- Fast, free headline scan for an entity/topic.
- Background news context to seed further research (then escalate to `grok_search` only if needed).

## Parameters

- `query` (string, optional): Search query. If omitted/blank, defaults to a broad breaking-news query.
  - Special-case: `"ai"` expands to `"artificial intelligence"`.
  - Too-short queries (<3 chars) error (except `"ai"`).
- `limit` (int, optional, 1–50): Default 20.

## Examples

```json
{ "name": "gdelt_news", "params": { "query": "tesla", "limit": 10 } }
```

Blank query (broad scan):
```json
{ "name": "gdelt_news", "params": { "limit": 20 } }
```

## Output

- Returns: `{ query: string, items: Array<{title,url,source,publishedAt}>, cached: boolean, meta: { cached, shared, durationMs, timeoutMs } }`
- Rendered:
  - `Query` (text)
  - `Meta` (text: cached/shared/durationMs/timeoutMs)
  - `Headlines` (table: publishedAt/source/title/url)

## Reliability notes

- Provider layer includes:
  - Shared in-flight dedupe (`shared=true` when you joined an ongoing identical request)
  - Cache TTL ~30s
  - Global gate ~1 request per ~5.2s (GDELT-friendly)
  - Timeout defaults to 15s

