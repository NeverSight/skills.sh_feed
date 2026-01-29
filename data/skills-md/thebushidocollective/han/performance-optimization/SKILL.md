---
name: performance-optimization
description: Use when optimizing code for performance, reducing bundle size, improving load times, or fixing performance bottlenecks. Emphasizes measurement-driven optimization.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Performance Optimization Skill

Systematic approach to identifying and fixing performance issues.

## Core Principle

**Measure, don't guess.** Optimization without data is guesswork.

## The Cardinal Rule

❌ **NEVER optimize without measuring first**

**Why:** Premature optimization wastes time on non-issues while missing real problems.

**Exception:** Obvious O(n²) algorithms when O(n) alternatives exist.

## Optimization Process

### 1. Measure Current State (Baseline)

**Before touching any code, establish metrics:**

**Frontend Performance:**

```bash
# Chrome DevTools Performance tab
# Lighthouse audit
npm run build && du -sh dist/  # Bundle size
```

**Backend Performance:**

```bash
# Add timing logs
start = Time.now
result = expensive_operation()
elapsed = Time.now - start
Logger.info("Operation took #{elapsed}ms")
```

**Database:**

```bash
# PostgreSQL
EXPLAIN ANALYZE SELECT ...;

# Check query time in logs
grep "SELECT" logs/production.log | grep "Duration:"
```

**Metrics to capture:**

- Load time / response time
- Time to interactive
- Bundle size
- Memory usage
- Query duration
- Render time

### 2. Profile to Find Bottlenecks

**Don't guess where the problem is - profile:**

**Browser Profiling:**

- Chrome DevTools > Performance tab
- Record interaction
- Look for long tasks (> 50ms)
- Check for layout thrashing

**Server Profiling:**

```bash
# Add detailed timing
defmodule Profiler do
  def measure(label, func) do
    start = System.monotonic_time(:millisecond)
    result = func.()
    elapsed = System.monotonic_time(:millisecond) - start
    Logger.info("#{label}: #{elapsed}ms")
    result
  end
end

# Use it
Profiler.measure("Database query", fn ->
  Repo.all(User)
end)
```

**React Profiling:**

```bash
# React DevTools Profiler
# Look for:
# - Unnecessary re-renders
# - Slow components (> 16ms for 60fps)
# - Large component trees
```

### 3. Identify Root Cause

**Common performance issues:**

**Frontend:**

- Large bundle size (lazy load, code split)
- Unnecessary re-renders (memoization)
- Blocking JavaScript (defer, async)
- Unoptimized images (WebP, lazy loading)
- Too many network requests (bundle, cache)
- Memory leaks (cleanup useEffect)

**Backend:**

- N+1 queries (preload associations)
- Missing database indexes
- Expensive computations in loops
- Synchronous external API calls
- Large JSON responses
- Inefficient algorithms

**Database:**

- Missing indexes
- Inefficient query structure
- Too many joins
- Fetching unnecessary columns
- No query result caching

### 4. Apply Targeted Optimization

**One change at a time** - Measure impact of each change

#### Frontend Optimizations

**Bundle Size Reduction:**

```typescript
// Before: Import entire library
import _ from 'lodash'

// After: Import only what's needed
import debounce from 'lodash/debounce'

// Or: Use native alternatives
const unique = [...new Set(array)]  // Instead of _.uniq(array)
```

**React Performance:**

```typescript
// Before: Re-renders on every parent render
function ChildComponent({ items }) {
  return <div>{items.map(...)}</div>
}

// After: Only re-render when items change
const ChildComponent = React.memo(function ChildComponent({ items }) {
  return <div>{items.map(...)}</div>
}, (prev, next) => prev.items === next.items)

// Before: Recreates function every render
function Parent() {
  const handleClick = () => { ... }
  return <Child onClick={handleClick} />
}

// After: Stable function reference
function Parent() {
  const handleClick = useCallback(() => { ... }, [])
  return <Child onClick={handleClick} />
}
```

**Code Splitting:**

```typescript
// Before: All in main bundle
import HeavyComponent from './HeavyComponent'

// After: Lazy load when needed
const HeavyComponent = React.lazy(() => import('./HeavyComponent'))

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <HeavyComponent />
    </Suspense>
  )
}
```

**Image Optimization:**

```typescript
// Before: Full-size image
<img src="/hero.jpg" />

// After: Responsive, lazy-loaded
<img
  src="/hero-800w.webp"
  srcSet="/hero-400w.webp 400w, /hero-800w.webp 800w"
  loading="lazy"
  alt="Hero image"
/>
```

#### Backend Optimizations

**N+1 Query Fix:**

```elixir
# Before: N+1 queries (1 for users + N for posts)
users = Repo.all(User)
Enum.map(users, fn user ->
  posts = Repo.all(from p in Post, where: p.user_id == ^user.id)
  {user, posts}
end)

# After: 2 queries total
users = Repo.all(User) |> Repo.preload(:posts)
Enum.map(users, fn user -> {user, user.posts} end)
```

**Database Indexing:**

```sql
-- Before: Slow query
SELECT * FROM users WHERE email = 'user@example.com';
-- Seq Scan (5000ms)

-- After: Add index
CREATE INDEX idx_users_email ON users(email);
-- Index Scan (2ms)
```

**Caching:**

```elixir
# Before: Expensive calculation every request
def get_popular_posts do
  # Complex aggregation query (500ms)
  Repo.all(from p in Post, ...)
end

# After: Cache for 5 minutes
def get_popular_posts do
  Cachex.fetch(:app_cache, "popular_posts", fn ->
    result = Repo.all(from p in Post, ...)
    {:commit, result, ttl: :timer.minutes(5)}
  end)
end
```

**Batch Processing:**

```elixir
# Before: Process one at a time
Enum.each(user_ids, fn id ->
  user = Repo.get(User, id)
  send_email(user)
end)

# After: Batch fetch
users = Repo.all(from u in User, where: u.id in ^user_ids)
Enum.each(users, &send_email/1)
```

#### Algorithm Optimization

**Reduce Complexity:**

```typescript
// Before: O(n²) - nested loops
function findDuplicates(arr: number[]): number[] {
  const duplicates = []
  for (let i = 0; i < arr.length; i++) {
    for (let j = i + 1; j < arr.length; j++) {
      if (arr[i] === arr[j] && !duplicates.includes(arr[i])) {
        duplicates.push(arr[i])
      }
    }
  }
  return duplicates
}

// After: O(n) - single pass with Set
function findDuplicates(arr: number[]): number[] {
  const seen = new Set<number>()
  const duplicates = new Set<number>()

  for (const num of arr) {
    if (seen.has(num)) {
      duplicates.add(num)
    }
    seen.add(num)
  }

  return Array.from(duplicates)
}
```

### 5. Measure Impact (Proof of Work)

**ALWAYS measure after optimization:**

```markdown
## Optimization: [What was changed]

### Before
- Load time: 3.2s
- Bundle size: 850KB
- Time to interactive: 4.1s

### Changes
- Lazy loaded HeavyComponent
- Switched to lodash-es for tree shaking
- Added React.memo to ProductList

### After
- Load time: 1.8s (-44%)
- Bundle size: 520KB (-39%)
- Time to interactive: 2.3s (-44%)

### Evidence
```bash
# Before
$ npm run build
dist/main.js   850.2 KB

# After
$ npm run build
dist/main.js   520.8 KB
```

```

**Use proof-of-work skill to document evidence**

### 6. Verify Correctness

**Tests must still pass:**

```bash
# Run full test suite
npm test        # Frontend
mix test        # Backend

# Manual verification
# - Feature still works
# - Edge cases handled
# - No new bugs introduced
```

## Common Optimization Targets

### Frontend Checklist

- [ ] Bundle size < 200KB (gzipped)
- [ ] First Contentful Paint < 1.5s
- [ ] Time to Interactive < 3s
- [ ] No layout shift (CLS < 0.1)
- [ ] Images optimized (WebP, lazy loading)
- [ ] Code split by route
- [ ] Unused code removed (tree shaking)
- [ ] CSS critical path optimized

### Backend Checklist

- [ ] API response time < 200ms (p95)
- [ ] Database queries optimized (EXPLAIN ANALYZE)
- [ ] No N+1 queries
- [ ] Appropriate indexes exist
- [ ] Expensive operations cached
- [ ] Background jobs for slow tasks
- [ ] Connection pooling configured
- [ ] Pagination for large datasets

### Database Checklist

- [ ] Indexes on frequently queried columns
- [ ] Query execution plan reviewed
- [ ] No full table scans
- [ ] Appropriate use of LIMIT
- [ ] Joins optimized (smallest table first)
- [ ] Statistics up to date (ANALYZE)

## Optimization Patterns

### Lazy Loading Pattern

```typescript
// Route-based code splitting
const routes = [
  {
    path: '/admin',
    component: lazy(() => import('./pages/Admin'))
  },
  {
    path: '/dashboard',
    component: lazy(() => import('./pages/Dashboard'))
  }
]
```

### Memoization Pattern

```typescript
// Expensive calculation
const ExpensiveComponent = ({ data }) => {
  // Only recalculate when data changes
  const processedData = useMemo(() => {
    return data.map(item => expensiveTransform(item))
  }, [data])

  return <div>{processedData.map(...)}</div>
}
```

### Database Query Optimization Pattern

```elixir
# Instead of multiple queries
users = Repo.all(User)
posts = Repo.all(Post)
comments = Repo.all(Comment)

# Use join and preload
users =
  User
  |> join(:left, [u], p in assoc(u, :posts))
  |> join(:left, [u, p], c in assoc(p, :comments))
  |> preload([u, p, c], [posts: {p, comments: c}])
  |> Repo.all()
```

## Anti-Patterns

### ❌ Optimizing the Wrong Thing

```
BAD: Spending hours optimizing function that runs once
GOOD: Optimize the function that runs 10,000 times per page load
```

**Always profile first to find real bottlenecks**

### ❌ Premature Optimization

```
BAD: "This might be slow, let me optimize it"
GOOD: "This IS slow (measured 500ms), let me optimize it"
```

### ❌ Micro-optimizations

```
BAD: Replacing `.map()` with `for` loop to save 1ms
GOOD: Reducing bundle size by 200KB to save 1000ms
```

**Focus on high-impact optimizations**

### ❌ Breaking Functionality for Performance

```
BAD: Remove feature to make it faster
GOOD: Keep feature, make implementation faster
```

**Performance should not come at cost of correctness**

### ❌ Optimizing Without Evidence

```
BAD: "I think this will be faster" [changes code]
GOOD: "Profiler shows this takes 80% of time" [measures, optimizes, measures again]
```

## Trade-offs to Consider

**Performance vs Readability:**

```typescript
// More readable
const result = items
  .filter(item => item.active)
  .map(item => item.name)

// Faster (one loop instead of two)
const result = []
for (const item of items) {
  if (item.active) {
    result.push(item.name)
  }
}
```

**Question:** Is the perf gain worth the readability loss? Profile first.

**Performance vs Maintainability:**

- Caching adds complexity
- Memoization adds memory overhead
- Code splitting adds bundle management

**Always document the trade-off made**

## Tools & Commands

**Frontend:**

```bash
# Bundle analysis
npm run build -- --analyze

# Lighthouse audit
npx lighthouse https://example.com --view

# Size analysis
npx webpack-bundle-analyzer dist/stats.json
```

**Backend:**

```bash
# Database query analysis
EXPLAIN ANALYZE SELECT ...;

# Profile Elixir code
:eprof.start()
:eprof.profile(fn -> YourModule.function() end)
:eprof.stop()
```

## Integration with Other Skills

- Use **proof-of-work** skill to document measurements
- Use **boy-scout-rule** skill while optimizing (leave better than found)
- Use **simplicity-principles** skill (simpler is often faster)
- Use **code-reviewer** skill to verify optimization quality

## Remember

1. **Measure first** - Find real bottlenecks
2. **One change at a time** - Know what helped
3. **Measure impact** - Verify improvement
4. **Preserve correctness** - Tests must pass
5. **Document trade-offs** - Explain why

**Fast code that's wrong is useless. Correct code that's fast enough is perfect.**
