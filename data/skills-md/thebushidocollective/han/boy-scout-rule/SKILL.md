---
name: boy-scout-rule
description: Use when modifying existing files, refactoring, improving code quality, or touching legacy code by applying the Boy Scout Rule to leave code better than you found it.
allowed-tools:
  - Read
  - Edit
  - Grep
  - Bash
---

# Boy Scout Rule

> "Leave the campground cleaner than you found it."

**Always leave code better than you found it.** Make incremental
improvements when you touch a file.

## What to Improve

**Code Quality**:

- Remove dead code (commented blocks, unused functions)
- Fix linting issues in files you touch
- Improve unclear naming (`x`, `temp`, `data` → descriptive)
- Add type annotations (TypeScript/Elixir @spec)
- Extract magic numbers to named constants
- Simplify complex logic
- Add missing error handling
- Update outdated comments
- Fix formatting
- Remove unused imports/variables
- Consolidate duplication

## What NOT to Do

- ❌ Massive unrelated refactors
- ❌ Change behavior without tests
- ❌ Fix everything in the file (stay focused)
- ❌ Breaking changes without tests
- ❌ Premature optimization
- ❌ Change unrelated sections

## Process

1. **Before changes**: Read file, note obvious issues, run linter
2. **Make primary changes**: Implement feature/fix, write tests
3. **Apply improvements**: Fix linting, improve naming, add types,
   extract constants, remove dead code
4. **Run verification**: `mix lint && mix test` or
   `yarn test:lint && yarn ts:check && yarn test`
5. **Document**: Include boy scout changes in commit message

## Example Commit Message

```text
Add worker search filter

- Implement location-based filtering
- Add tests for search radius

Boy Scout improvements:
- Extract SEARCH_RADIUS constant
- Add type annotations to helper functions
- Remove unused import statements
- Improve variable naming in search logic
```

## Example Improvements

**Before**:

```typescript
function calculateTotal(items) {  // No types
  let t = 0;  // Poor naming
  for (let i = 0; i < items.length; i++) {  // Old-style
    t += items[i].price * 1.08;  // Magic number
  }
  return t;
}
```

**After**:

```typescript
const TAX_RATE = 1.08;

function calculateTotal(items: Item[]): number {
  return items.reduce((total, item) => {
    return total + (item.price * TAX_RATE);
  }, 0);
}
```

Improvements: types, constant, naming, modern syntax, simplified.

## Critical Rules

- Keep improvements in same commit as primary changes
- Focus on "blast radius" (code near your changes)
- Prioritize readability over cleverness
- Always run full test suite after improvements
- Ask for help when unsure about business logic
- Small improvements > perfect refactors

## Checklist

- [ ] Removed dead code in files I touched
- [ ] Fixed linting issues
- [ ] Improved naming where I made changes
- [ ] Added type annotations where missing
- [ ] Extracted magic numbers
- [ ] Updated outdated comments
- [ ] Removed unused imports
- [ ] Simplified complex logic
- [ ] Added error handling
- [ ] All tests pass
- [ ] No new linting errors
- [ ] Documented in commit message

## Integration

**During implementation**: Make changes, apply boy scout, verify, commit together

**During code review**: Look for boy scout opportunities, recognize good boy scouting

**During bug fixes**: Fix bug, improve surrounding code, add tests, clean up

## Remember

### Incremental improvement, not perfection

- Small improvements compound over time
- Every file touched is an opportunity
- Be a good steward of the codebase
- When in doubt, ask for review on larger improvements
