---
name: tool-nasdaq-candles
description: Use the nasdaq_candles tool to fetch OHLCV candles (free) with caching and latency metadata; good for quick charting.
---

# nasdaq_candles (Nasdaq OHLCV)

## When to use

- Pull short-horizon OHLCV for quick trend context or charting.

## Parameters

- `symbol` (string, required): e.g. `"AAPL"`.
- `range` (string, optional): `1d | 5d | 1mo` (default `1d`).
- `interval` (string, optional): `1m | 5m | 30m` (default `1m`).
  - For `5d`/`1mo`, interval is effectively ignored (Nasdaq returns daily-ish points).

## Examples

1-day minute-ish candles:
```json
{ "name": "nasdaq_candles", "params": { "symbol": "AAPL", "range": "1d", "interval": "5m" } }
```

5-day:
```json
{ "name": "nasdaq_candles", "params": { "symbol": "AAPL", "range": "5d" } }
```

## Output

- Returns: `{ candles: { t,o,h,l,c,v,meta }, meta: { cached,durationMs,timeoutMs } }`
- Rendered:
  - `Meta` (cached/durationMs/points)
  - `Last Candle` (json: last bar only; full arrays are still in `candles`)

## Notes

- This tool is optimized for “get me data quickly”; for heavy analytics, you probably want a dedicated market data provider later.
- `targetWindow`: `des`

