---
name: baseline-restorer
description: Use when multiple fix attempts fail and you need to systematically restore to a working baseline and reimplement instead of fixing broken code.
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
  - Edit
---

# Baseline Restorer

Enforces methodical problem-solving by reverting to last known working state and
reimplementing step-by-step instead of trying to fix accumulated broken changes.

## Core Philosophy

### Reimplement, don't fix the mess

When something breaks after multiple failed fix attempts:

1. Stop trying to fix forward
2. Revert to last known working state
3. Understand what worked and why
4. Reimplement the needed change ONE step at a time
5. Verify each step before proceeding

## When to Use This Skill

### Trigger conditions

- 2+ failed fix attempts for the same issue
- "This should work but doesn't" situations
- Pipeline failures persisting across multiple commits
- User says "the old version worked fine"
- Complex accumulated changes with unclear impact

### Red flags requiring this skill

- Making assumptions about root cause without verification
- Blaming "pre-existing issues"
- Adding more changes to fix previous changes
- Not testing locally before committing

## Systematic Process

### Phase 1: Identify Working Baseline

```bash
# Find last known working state
git log --oneline -20
git show origin/beta:path/to/file.sh  # Check beta/main branch
git diff origin/beta -- path/to/file.sh  # What changed?

# Verify baseline works
git stash
git checkout origin/beta -- path/to/file.sh
# Test it - does it work?
```

### Questions to answer

- What was the last commit where this worked?
- What branch has a working version? (beta, main, prod)
- What specific files/scripts were working?

### Phase 2: Compare Current vs Baseline

```bash
# Get exact differences
git diff baseline..current -- path/to/file.sh

# Understand each change
# For EACH diff hunk, ask:
# - Why was this changed?
# - What problem was it trying to solve?
# - Did it actually solve that problem?
```

### Document findings

- List every change made
- Note which changes were necessary
- Note which changes broke things
- Identify assumptions that were wrong

### Phase 3: Revert to Baseline

```bash
# Hard revert to working state
git checkout origin/beta -- path/to/file.sh
git add path/to/file.sh
git commit -m "Revert to working baseline from beta"

# Verify baseline works
./test-locally.sh
# Must pass before proceeding
```

**Critical:** Don't proceed until baseline is verified working.

### Phase 4: Reimplement ONE Change at a Time

### For each needed change

1. **Make ONE small change**

   ```bash
   # Example: Replace sed with awk in ONE function
   # Don't change 5 things at once
   ```

2. **Test locally immediately**

   ```bash
   ./run-generation-script.sh
   terraform validate
   # Must pass before committing
   ```

3. **Commit if working**

   ```bash
   git add changed-file.sh
   git commit -m "Replace sed with awk in function X"
   ```

4. **If it breaks, revert immediately**

   ```bash
   git reset --hard HEAD~1
   # Try different approach or understand why it broke
   ```

5. **Repeat for next change**

### Phase 5: Verify Complete Solution

```bash
# Run full test suite
make test
terraform validate

# Compare with original broken state
# Did we achieve the goal without breaking things?

# Push only after local verification
git push
```

## Verification Checklist

Before committing ANY change:

- [ ] Tested locally and passes
- [ ] Compared output with baseline (no unexpected differences)
- [ ] Understood why this change is needed
- [ ] Change is minimal and focused
- [ ] Can explain what would break if this change was wrong

## Anti-Patterns to Avoid

### DON'T

- ❌ "Let me try one more fix" (revert instead)
- ❌ "This is probably a pre-existing issue" (verify with baseline)
- ❌ "The logic should work" (test it, don't assume)
- ❌ Change 5 things and hope one fixes it
- ❌ Commit without local verification
- ❌ Blame the user's code/environment

### DO

- ✅ "Let me check what worked in beta"
- ✅ "Reverting to baseline first"
- ✅ "Testing this one change locally"
- ✅ Make ONE change, verify, commit
- ✅ Test before every commit
- ✅ Take responsibility for breakage

## Examples

### Example 1: Terraform Generation Scripts

### Broken approach (Example 1)

```bash
# Made 10 changes trying to "optimize" variable filtering
# Each fix broke something new
# Spent day+ debugging
```

### Baseline approach (Example 1)

```bash
# Check beta branch - does it work?
git show origin/beta:terraform/build-module.sh > /tmp/beta-version.sh
bash /tmp/beta-version.sh  # Verify it works

# Revert to beta version
git checkout origin/beta -- terraform/build-module.sh

# Now reimplement ONLY what's needed (e.g., sed→awk for portability)
# One function at a time, test each change
```

### Example 2: Pipeline Failures

### Broken approach (Example 2)

```bash
# Assume it's a CI environment issue
# Try 5 different "fixes" based on guesses
# Each creates new errors
```

### Baseline approach (Example 2)

```bash
# Find last passing pipeline
git log --oneline | head -20
# Check what changed since then
git diff <last-passing-commit>

# Revert suspicious changes
# Test locally before pushing
```

## Commands

```bash
# Find working baseline
git log --oneline --all | grep "known working feature"
git show origin/beta:path/to/file

# Compare with baseline
git diff origin/beta -- path/to/file
git diff <working-commit> -- path/to/file

# Revert to baseline
git checkout origin/beta -- path/to/file
git checkout <working-commit> -- path/to/file

# Test locally
terraform validate
mix test
yarn test

# Verify no changes after running script
git diff  # Should be empty if script is idempotent
```

## Remember

- **Reimplement, don't fix** - Start from working state
- **One change at a time** - Test each change immediately
- **Local verification first** - Never commit untested changes
- **Baseline is truth** - If baseline works, your changes broke it
- **Stop digging** - After 2 failed fixes, revert and rethink
- **Question assumptions** - Verify, don't assume
- **Take responsibility** - Your changes, your bugs
