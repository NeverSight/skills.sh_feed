---
name: tool-nasdaq-quote
description: Use the nasdaq_quote tool to fetch a US equity quote (free; delayed) with lightweight caching and latency metadata.
---

# nasdaq_quote (Nasdaq quote)

## When to use

- Lightweight US stock quote (price/change/%change) for dashboarding or quick checks.

## Parameters

- `symbol` (string, required): e.g. `"AAPL"`. Allowed: `[A-Z0-9.\\-=_^]{1,15}`

## Examples

```json
{ "name": "nasdaq_quote", "params": { "symbol": "AAPL" } }
```

## Output

- Returns: `{ quote: { symbol,name,exchange,currency,price,change,changePercent,marketCap,time }, meta: { cached,durationMs,timeoutMs } }`
- Rendered:
  - `Meta` (text: cached/durationMs)
  - `Quote` (table)

## Notes

- Data is typically delayed (~15m) and can rate-limit; treat as “good enough” not authoritative.
- `targetWindow`: `des`

