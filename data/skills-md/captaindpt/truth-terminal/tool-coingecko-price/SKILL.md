---
name: tool-coingecko-price
description: Use the coingecko_price tool to fetch spot crypto prices (free) for one or more symbols/ids with 24h change and last-updated timestamps.
---

# coingecko_price (CoinGecko spot)

## When to use

- Quick crypto spot check (BTC/ETH/SOL/etc).
- Cheap price context before going deeper (derivatives/order books/etc).

## Parameters

- `query` (string, required): Space/comma-separated symbols or CoinGecko ids (max 25 unique).
  - Built-in symbol mapping includes: BTC/ETH/SOL/DOGE/ADA/BNB/XRP.
  - Otherwise, tokens are treated as CoinGecko ids (lowercased).
- `vsCurrency` (string, optional): Quote currency, default `usd`.

## Examples

```json
{ "name": "coingecko_price", "params": { "query": "BTC ETH solana", "vsCurrency": "usd" } }
```

## Output

- Returns: `{ ids: string[], vsCurrency: string, data: object }` (raw CoinGecko response)
- Rendered:
  - Table `CoinGecko (usd)` with columns: id/price/24h_change_%/updatedAt

## Notes

- This tool does not currently expose CoinGecko market cap/volume endpoints; it’s `simple/price` only.

