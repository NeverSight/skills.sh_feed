---
name: user-activity
description: Pull trading activity from Polymarket for any user
when_to_use: When you need to analyze a Polymarket user's trading history, strategy, or patterns
script: scripts/polymarket-user-activity.py
---

# Polymarket User Activity Scraper

Pull trading activity from Polymarket's Data API for any user by username or wallet address.

## Quick Start

```bash
# Analyze gabagool22's last 7 days of trading
python scripts/polymarket-user-activity.py gabagool22 --analyze

# Save to CSV
python scripts/polymarket-user-activity.py gabagool22 --days 7 --output data/gabagool22-trades.csv

# Save as JSON
python scripts/polymarket-user-activity.py gabagool22 --days 7 --output data/gabagool22-trades.json

# Use wallet address directly
python scripts/polymarket-user-activity.py 0x6031b6eed1c97e853c6e0f03ad3ce3529351f96d --analyze
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `user` | Username (e.g. gabagool22) or wallet address (0x...) | Required |
| `--days N` | Number of days of history to fetch | 7 |
| `--limit N` | Maximum number of trades to fetch | 10000 |
| `--output PATH` | Output file (CSV or JSON based on extension) | None |
| `--analyze` | Print analysis summary | False |
| `--json` | Output raw JSON to stdout | False |

## Output Fields (CSV)

| Field | Description |
|-------|-------------|
| datetime | ISO timestamp |
| timestamp | Unix timestamp |
| side | BUY or SELL |
| outcome | Up or Down |
| title | Market question |
| size | Number of shares |
| price | Price per share |
| value | size * price |
| slug | Market URL slug |
| eventSlug | Event identifier |
| conditionId | Market condition hash |
| transactionHash | On-chain tx hash |
| proxyWallet | Trader wallet |

## Analysis Summary

The `--analyze` flag prints:
- Total trade count (BUY/SELL breakdown)
- Total volume in USD
- Date range covered
- Up/Down position breakdown
- Price statistics (avg/min/max)
- Top 5 markets by trade count

## Example Analysis Output

```
============================================================
TRADE ANALYSIS SUMMARY
============================================================

Total trades: 847
  - BUY: 623
  - SELL: 224

Total volume: $42,350.00

Date range: 2024-12-08 09:15 to 2024-12-15 14:30
  (7 days)

Outcome breakdown:
  - UP positions: 412
  - DOWN positions: 435

Price stats:
  - Average: $0.485
  - Min: $0.08
  - Max: $0.92

Top 5 markets by trade count:
  - Bitcoin up or down? (Dec 15, 2:00 PM ET)... (45 trades, $1,250.00)
  - Ethereum up or down? (Dec 15, 10:00 AM ET)... (38 trades, $980.00)
  ...
============================================================
```

## API Details

Uses the Polymarket Data API:
- Base URL: `https://data-api.polymarket.com`
- Endpoint: `/trades?user={wallet}&limit={n}&offset={n}`
- Rate limited: 0.5s delay between paginated requests

## Strategy Analysis Tips

To analyze a trader's strategy:

1. Pull their recent trades:
   ```bash
   python scripts/polymarket-user-activity.py gabagool22 --days 7 --output data/trades.csv
   ```

2. Look for patterns:
   - Average position size
   - Entry price ranges (do they buy near 0.50 or closer to extremes?)
   - How often they add to positions vs close them
   - Time patterns (when do they trade most actively?)
   - Up/Down bias (do they favor one direction?)

3. Compare to market conditions:
   - Do they trade more during high volatility?
   - How do they handle losing positions?
