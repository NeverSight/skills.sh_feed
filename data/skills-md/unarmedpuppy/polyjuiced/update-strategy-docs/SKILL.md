---
name: update-strategy-docs
description: Update Polymarket bot strategy documentation after code changes. Use after modifying gabagool.py, polymarket.py, or any strategy-related code to ensure STRATEGY_ARCHITECTURE.md and strategy-rules.md accurately reflect the implementation.
---

# Update Polymarket Strategy Documentation

Synchronize strategy documentation with actual code implementation after changes.

## When to Use

Call this skill after modifying:
- `src/strategies/gabagool.py` - Strategy logic
- `src/client/polymarket.py` - Order execution
- `src/monitoring/order_book.py` - Opportunity detection
- `src/config.py` - Strategy configuration
- Any file affecting the arbitrage/directional/near-resolution trading flow

## Documentation Files to Update

| File | Purpose |
|------|---------|
| `docs/STRATEGY_ARCHITECTURE.md` | Code flow diagrams, implementation status, discrepancies |
| `docs/strategy-rules.md` | Trading rules, entry/exit conditions, configuration reference |

## Update Checklist

### 1. Verify Code Flow Diagram

Read the actual code path and compare to the diagram in `docs/STRATEGY_ARCHITECTURE.md`:

```bash
# Check opportunity detection flow
grep -n "on_opportunity\|_queue_opportunity\|_process_opportunities" src/strategies/gabagool.py

# Check order execution flow
grep -n "execute_dual_leg_order\|place_order_sync" src/client/polymarket.py
```

Update the ASCII diagram if the flow has changed:
```
Opportunity Detection → Queue → Execution → Persistence
```

### 2. Update Implementation Status

In `docs/STRATEGY_ARCHITECTURE.md`, update the Implementation Status section:

```markdown
## Implementation Status

| Phase | Description | Status |
|-------|-------------|--------|
| 1 | Dynamic pricing with zero slippage | COMPLETE |
| 2 | Strategy-owned persistence | NOT STARTED |
...
```

Mark phases as:
- `COMPLETE` - Fully implemented and tested
- `IN PROGRESS` - Partially implemented
- `NOT STARTED` - Planned but not implemented

### 3. Check for Discrepancies

Compare `docs/strategy-rules.md` rules against actual code:

```python
# Example: Check slippage policy
grep -n "slippage\|limit_price\|price_d" src/client/polymarket.py

# Example: Check position sizing
grep -n "num_pairs\|yes_amount\|no_amount" src/strategies/gabagool.py
```

Document any gaps in the Discrepancies section:
- `IMPLEMENTED` - Code matches documentation
- `GAP` - Documentation describes feature not yet implemented
- `CRITICAL GAP` - Implementation differs from documented behavior

### 4. Update Configuration Reference

If config options changed, update both files:

```bash
# Check actual config options
grep -n "GABAGOOL_" src/config.py
```

Update the Configuration Reference section in `docs/strategy-rules.md`.

### 5. Update Changelog

Add entry to `docs/strategy-rules.md` changelog:

```markdown
## Change Log

| Date | Change |
|------|--------|
| YYYY-MM-DD | Description of what changed |
```

## Example Update Session

After fixing a pricing bug:

```bash
# 1. Verify the fix in code
grep -n "limit_price\|price_d" src/client/polymarket.py

# 2. Update docs/STRATEGY_ARCHITECTURE.md
# - Update code flow diagram to show price passthrough
# - Mark Phase 1 as COMPLETE
# - Update discrepancies section

# 3. Update docs/strategy-rules.md
# - Update Risk Management > Slippage Protection
# - Add changelog entry for zero slippage policy
```

## Verification

After updating documentation:

1. Re-read both docs files to ensure consistency
2. Verify ASCII diagrams match actual code paths
3. Check that all config options mentioned exist in `src/config.py`
4. Ensure changelog is in reverse chronological order

## Quick Reference

```bash
# Files to update
docs/STRATEGY_ARCHITECTURE.md
docs/strategy-rules.md

# Files to reference (actual implementation)
src/strategies/gabagool.py
src/client/polymarket.py
src/monitoring/order_book.py
src/config.py
```
