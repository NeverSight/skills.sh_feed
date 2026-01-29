---
name: tool-polymarket-book
description: Use the polymarket_book tool to fetch Polymarket CLOB order book depth (YES/NO) via Gamma + CLOB and expose best bid/ask/mid.
---

# polymarket_book (Polymarket CLOB book)

## When to use

- Liquidity check before sizing into a market.
- Spread + depth + mid estimation.

## Parameters

- `marketId` (string, required): Gamma numeric id (e.g. `"516710"`) or conditionId hex (`"0x..."`).
- `outcome` (`"YES" | "NO"`, optional): Defaults to `"YES"`.
- `depth` (int, optional, 1–200): Levels per side; default 20.

## Examples

```json
{ "name": "polymarket_book", "params": { "marketId": "0xabc...def", "outcome": "YES", "depth": 50 } }
```

## Output

- Returns: `{ marketId, conditionId, question, slug, endDate, outcome, tokenId, bookAvailable, bestBid, bestAsk, mid, bids[], asks[], ts }`
- Rendered:
  - Emits a JSON output with title `orderbook` (used by the UI to open/focus a book window when available).
  - `Market` (text with mid/bid/ask and “no CLOB orderbook” when missing)
  - `Asks` + `Bids` (tables)

## Notes

- Some markets have **no CLOB orderbook**; the tool returns `bookAvailable=false` and empty bids/asks.
- `targetWindow`: `book`

