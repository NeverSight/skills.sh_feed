---
name: deploy-bot
description: Safe deployment of Polymarket trading bot with regression tests and active trade protection
when_to_use: When deploying ANY changes to the polymarket-bot application
script: agents/skills/deploy-bot/deploy.sh
---

# Deploy Polymarket Bot

**WARNING: ALWAYS USE THIS SKILL** when deploying changes. Never use manual docker commands.

Safe deployment workflow for the Polymarket arbitrage trading bot that:
1. Runs regression tests to catch bugs before deployment
2. Checks for active trades to prevent interrupting pending positions

## Why This Matters

The bot executes real-money arbitrage trades on Polymarket. Deploying broken code or restarting during active trades can cause:

1. **Bugs**: Untested code can break execution, tracking, or settlement
2. **Lost visibility**: Restarting during active trades loses pending position data
3. **Missed resolutions**: Container restart can miss market resolution events
4. **Financial losses**: All of the above can result in real money losses

## Quick Deploy

```bash
# From the polyjuiced repo root
./agents/skills/deploy-bot/deploy.sh

# Skip tests only (still checks active trades)
./agents/skills/deploy-bot/deploy.sh --skip-tests

# Force deploy (DANGEROUS - skips ALL safety checks)
./agents/skills/deploy-bot/deploy.sh --force
```

## What the Script Does

1. **Run Regression Tests** (Step 0)
   - Builds a fresh container with latest code
   - Runs `pytest tests/ -v` to verify all tests pass
   - Blocks deployment if any tests fail
   - Exit code 3 = tests failed

2. **Check Active Trades** (Step 1)
   - Runs `scripts/check_active_trades.py` in the container
   - Queries the database for unresolved real trades
   - Checks if market has resolved (safe) vs still active (danger)
   - Blocks deployment if active trades exist
   - Exit code 1 = active trades

3. **Deploy** (Steps 2-4)
   - Git push + pull to sync code
   - Docker compose rebuild and restart

4. **Verify** (Step 5)
   - Shows startup logs to confirm success

## Manual Pre-Checks

Run the checks independently:

```bash
# Run regression tests locally
docker compose run --rm --build polymarket-bot python3 -m pytest tests/ -v

# Check active trades (requires running container)
docker exec polymarket-bot python3 /app/scripts/check_active_trades.py

# Exit codes:
#   0 = Safe to deploy
#   1 = Active trades exist (don't deploy)
#   2 = Error checking
#   3 = Tests failed
```

## When to Skip Tests

Use `--skip-tests` when:
- You've already run tests manually
- Making config-only changes (.env)
- Urgent fix with verified minimal change

## When to Force Deploy

Only use `--force` when:

- The bot is crashed/hung and needs restart
- You're certain any active trades are already lost
- Emergency security fix is needed
- User explicitly approves the risk

## Trade Lifecycle

```
Trade Executed → status='pending' → Market Resolves → status='won'/'lost'
                     ↑                                      ↓
              ⚠️ DANGER ZONE                          Safe to deploy
```

## Troubleshooting

### "Regression tests failed"

Fix the failing tests before deploying:

```bash
docker compose run --rm --build polymarket-bot python3 -m pytest tests/ -v --tb=long
```

### "Container may not be running"

The pre-check failed because the bot isn't running. This is safe to deploy.

### Stuck in "not safe" state

If trades are stuck as pending after market resolution:

```bash
# Check database state
docker exec polymarket-bot python3 -c "
import asyncio
import aiosqlite
async def check():
    async with aiosqlite.connect('/app/data/gabagool.db') as db:
        db.row_factory = aiosqlite.Row
        async with db.execute('SELECT id, asset, status, market_end_time FROM trades WHERE dry_run=0 ORDER BY created_at DESC LIMIT 5') as cur:
            for row in await cur.fetchall():
                print(dict(row))
asyncio.run(check())
"
```

## Related Files

- `tests/` - Regression test suite
- `scripts/check_active_trades.py` - Pre-deployment trade check
- `src/persistence.py` - Database schema
- `src/strategies/gabagool.py` - Trading logic
