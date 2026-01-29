---
name: debugging
description: Use when investigating bugs, diagnosing issues, or understanding unexpected behavior. Provides systematic approaches to finding root causes.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Debugging Skill

Systematic approaches to investigating and diagnosing bugs.

## Core Principle

**Understand before fixing.** A proper diagnosis leads to a proper fix.

## The Scientific Method for Debugging

### 1. Observe

**Gather all the facts:**

- What's the symptom? (What's happening that shouldn't?)
- When does it happen? (Always, sometimes, specific conditions?)
- Who's affected? (All users, some users, specific scenarios?)
- Error messages? (Exact text, stack traces, error codes?)
- Recent changes? (What changed before this started?)

**Evidence to collect:**

- Error messages and stack traces
- Application logs
- User reports
- Reproduction steps
- Environment details (browser, OS, versions)
- Network requests/responses
- Database query logs

### 2. Form Hypothesis

**Based on symptoms, what could cause this?**

**Common categories:**

- **Logic error:** Code does wrong thing
- **State management:** State gets out of sync
- **Async/timing:** Race condition, callback hell
- **Data issue:** Unexpected input format
- **Integration:** API change, service down
- **Environment:** Config, permissions, network
- **Resource:** Memory leak, connection pool exhausted

**Prioritize hypotheses:**

1. Most likely causes first
2. Easiest to test first (when equal likelihood)
3. Most impactful if true

### 3. Test Hypothesis

**Design experiment to prove/disprove:**

- Add logging to see values
- Add breakpoints to pause execution
- Modify input to isolate variable
- Disable feature to rule out
- Compare with working version

**Keep notes:**

```markdown
**Hypothesis:** Database query timeout
**Test:** Add query timing logs
**Result:** Query completes in 50ms
**Conclusion:** Not the database ❌

**Hypothesis:** Network latency
**Test:** Check network tab, add timing
**Result:** API call takes 5 seconds
**Conclusion:** Found the issue ✅
```

### 4. Analyze Results

**What did you learn?**

- Hypothesis confirmed or rejected?
- New questions raised?
- Unexpected findings?
- Root cause identified?

### 5. Repeat or Conclude

**If root cause found:**

- Document findings
- Estimate impact
- Plan fix

**If not found:**

- Form new hypothesis
- Repeat cycle

## Debugging Strategies

### Strategy 1: Add Logging

**Most universally useful technique:**

```typescript
// Strategic console.log placement
function processOrder(order) {
  console.log('processOrder START:', { orderId: order.id })

  const items = order.items
  console.log('items:', items.length)

  const validated = validate(items)
  console.log('validation result:', validated)

  if (!validated.success) {
    console.log('validation failed:', validated.errors)
    throw new Error('Invalid order')
  }

  const total = calculateTotal(items)
  console.log('total calculated:', total)

  console.log('processOrder END')
  return total
}
```

**Logging guidelines:**

- Log function entry/exit
- Log branching decisions
- Log external calls (API, database)
- Log unexpected values
- Include context (IDs, user info)

### Strategy 2: Use Debugger

**Interactive debugging:**

```typescript
// Browser
function buggyFunction(input) {
  debugger;  // Execution pauses here
  const result = transform(input)
  debugger;  // And here
  return result
}

// Node.js
node --inspect app.js
# Then open chrome://inspect in Chrome
```

**Debugger features:**

- Step over (next line)
- Step into (into function call)
- Step out (back to caller)
- Watch expressions
- Call stack inspection
- Variable inspection

### Strategy 3: Binary Search

**Isolate the problem area:**

```typescript
// 100 lines of code, bug somewhere

// Comment out lines 50-100
// Bug still happens? It's in lines 1-50

// Comment out lines 25-50
// Bug disappears? It's in lines 25-50

// Comment out lines 37-50
// Bug still happens? It's in lines 25-37

// Continue until isolated to specific lines
```

### Strategy 4: Rubber Duck Debugging

**Explain the problem out loud:**

1. "This function is supposed to calculate shipping cost"
2. "It takes the weight and destination"
3. "First it... wait, it's using price instead of weight!"
4. *(Bug found)*

**Why this works:** Forces you to examine assumptions.

### Strategy 5: Compare Working vs Broken

**What's different?**

**Version comparison:**

```bash
# Find which commit broke it
git bisect start
git bisect bad HEAD
git bisect good v1.0.0
# Git checks out middle commit
npm test
git bisect good/bad
# Repeat until found
```

**Environment comparison:**

- Works locally but not production?
- Works for some users but not others?
- Worked yesterday but not today?

**What changed?**

### Strategy 6: Simplify

**Reduce to minimal reproduction:**

```typescript
// Complex case with bug
processUserOrderWithDiscountsAndShipping(user, cart, promo, address)

// Simplify inputs one at a time
processUserOrderWithDiscountsAndShipping(user, [], null, null)
// Still breaks? Not discount or address

processUserOrderWithDiscountsAndShipping(null, [], null, null)
// Works now? It's the user object

// What about the user object causes it?
```

### Strategy 7: Check Assumptions

**Question everything:**

```typescript
// Assumption: API returns array
const users = await api.getUsers()
users.forEach(...)  // Crashes

// Check assumption
console.log(typeof users)  // "undefined"
console.log(users)          // undefined

// Assumption was wrong!
```

**Common wrong assumptions:**

- Function returns expected type
- Variable is defined
- Array is not empty
- API will always respond
- Async operation has completed
- State is up to date

## Debugging by Symptom

### "Intermittent failure"

**Likely causes:**

- Race condition (timing-dependent)
- Data-dependent (certain inputs trigger it)
- Resource leak (happens after N operations)
- External service flakiness

**Investigation:**

- Add extensive logging
- Look for async operations
- Check timing between operations
- Look for shared state
- Run many times to see pattern

### "Works locally, fails in production"

**Check differences:**

- Environment variables
- Data (production has different/more data)
- Network (CORS, SSL, proxies)
- Dependencies (versions, OS)
- Resources (memory, connections)

### "Slow performance"

**Don't guess - profile:**

**Frontend:**

- Chrome DevTools > Performance tab
- Look for long tasks (> 50ms)
- Check for layout thrashing
- Look for memory leaks

**Backend:**

- Add timing logs around operations
- Check database query time (EXPLAIN ANALYZE)
- Check external API call time
- Profile with APM tool

### "Memory leak"

**Investigation:**

```typescript
// Take heap snapshot
// Do operation that leaks
// Take another heap snapshot
// Compare - what increased?
```

**Common causes:**

- Event listeners not removed
- Closures holding references
- Global variables accumulating
- Intervals not cleared
- Cache growing unbounded

### "Crash/Exception"

**Read the stack trace:**

```
Error: Cannot read property 'map' of undefined
    at processUsers (app.js:42:15)
    at handleRequest (app.js:23:3)
    at Server.<anonymous> (server.js:12:5)
```

**Stack trace tells you:**

- Line 42: Where it crashed
- Line 23: Where it was called from
- Line 12: Origin of the request

**Then:**

- Go to line 42
- Check what's undefined
- Trace back why it's undefined

## Common Bug Patterns

### Null/Undefined

```typescript
// Bug
function process(user) {
  return user.name.toUpperCase()  // Crashes if user is null
}

// Investigation
console.log('user:', user)  // undefined - why?
// Trace back to where user comes from
```

### Off-by-One

```typescript
// Bug
for (let i = 0; i <= array.length; i++) {  // <= instead of <
  process(array[i])  // Crashes on last iteration
}

// Investigation
console.log('i:', i, 'length:', array.length)
// Notice i === array.length causes array[i] === undefined
```

### Async Timing

```typescript
// Bug
let data
fetchData().then(result => {
  data = result
})
console.log(data)  // undefined - async not complete

// Investigation
console.log('1. Before fetch')
fetchData().then(result => {
  console.log('3. Got result')
  data = result
})
console.log('2. After fetch call')
// Output: 1, 2, 3 - async completes later
```

### State Mutation

```typescript
// Bug
function addItem(cart, item) {
  cart.items.push(item)  // Mutates input!
  return cart
}

const originalCart = { items: [] }
const newCart = addItem(originalCart, item)
// originalCart was modified - unexpected!

// Investigation
console.log('before:', originalCart)
const newCart = addItem(originalCart, item)
console.log('after:', originalCart)  // Changed!
```

### Scope Issues

```typescript
// Bug
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100)
}
// Prints: 3, 3, 3 (expected 0, 1, 2)

// Investigation
// var is function-scoped, i is shared
// By time timeout fires, loop is done, i === 3

// Fix: Use let (block-scoped) or capture i
```

## Debugging Tools

### Browser Developer Tools

**Console:**

- `console.log()` - Print values
- `console.table()` - Display arrays/objects as table
- `console.trace()` - Print stack trace
- `console.time()` / `console.timeEnd()` - Measure duration

**Debugger:**

- Set breakpoints
- Step through code
- Inspect variables
- Watch expressions
- Call stack

**Network:**

- View all requests
- See request/response headers and bodies
- Measure timing
- Replay requests

**Performance:**

- Record profile
- See function call tree
- Identify bottlenecks
- Check memory usage

### Command Line Tools

```bash
# Search for text in files
grep -r "error" logs/

# Follow log file
tail -f logs/app.log

# Search with context
grep -B 5 -A 5 "ERROR" logs/app.log

# Find large files
du -sh *

# Check disk space
df -h

# Check memory
free -m

# Check running processes
ps aux | grep node
```

### Database Debugging

```sql
-- PostgreSQL
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';

-- Show slow queries
SELECT * FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10;

-- Check table size
SELECT pg_size_pretty(pg_total_relation_size('users'));

-- Check indexes
\d users
```

## Debugging Checklist

### Before Starting

- [ ] Can reproduce the issue reliably?
- [ ] Have error message or symptom description?
- [ ] Know when it started happening?
- [ ] Checked if recent changes related?
- [ ] Checked logs for clues?

### During Investigation

- [ ] Formed clear hypothesis?
- [ ] Testing hypothesis systematically?
- [ ] Taking notes on findings?
- [ ] Not making random changes hoping to fix?
- [ ] Questioning assumptions?

### After Finding Root Cause

- [ ] Understand WHY it happens?
- [ ] Can explain it to someone else?
- [ ] Documented findings?
- [ ] Estimated impact?
- [ ] Identified proper fix?

## Anti-Patterns

### ❌ Random Code Changes

```
BAD: "Maybe if I change this... nope, try this... nope, try this..."
GOOD: "Hypothesis: X causes Y. Test: Change X. Result: Y still happens.
       Conclusion: X is not the cause."
```

### ❌ Assuming Without Verifying

```
BAD: "The API must be returning valid data"
GOOD: "Let me log the API response to see what it actually returns"
```

### ❌ Stopping at Symptoms

```
BAD: "The page is blank. Fixed by adding a null check."
GOOD: "The page is blank because user is null. User is null because
       authentication token expired. Root cause: token not being refreshed."
```

### ❌ Debugging in Production

```
BAD: "Let me add console.log to production to see..."
GOOD: "Let me reproduce locally and debug there, or use proper logging"
```

### ❌ No Reproduction Steps

```
BAD: "It crashed once, let me guess why"
GOOD: "Let me find reliable way to reproduce it first"
```

## Integration with Other Skills

- Use **proof-of-work** skill to document evidence
- Use **test-driven-development** skill to add regression test after fix
- Use **explainer** skill when explaining bug to others
- Use **boy-scout-rule** skill while fixing (improve surrounding code)

## Remember

1. **Reproduce first** - If you can't reproduce, you can't debug
2. **Gather evidence** - Don't guess, look at data
3. **Form hypothesis** - What do you think is wrong?
4. **Test systematically** - Prove or disprove hypothesis
5. **Find root cause** - Not just symptoms
6. **Document** - Help future you and others

**Debugging is detective work. Be methodical, not random.**
