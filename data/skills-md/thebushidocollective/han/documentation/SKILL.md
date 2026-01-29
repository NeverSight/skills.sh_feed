---
name: documentation
description: Use when creating or updating documentation including READMEs, API docs, inline comments, or technical guides. Focuses on clarity and usefulness for the intended audience.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
---

# Documentation Skill

Create clear, useful documentation that helps people understand and use your code.

## Core Principle

**Write for the reader, not for yourself.**

## Types of Documentation

### 1. README Files

**Purpose:** Help users understand what the project does and how to use it

**Audience:** New users, potential contributors

**Key sections:**

- What it does (one paragraph)
- Installation instructions
- Quick start example
- Common use cases
- Link to full documentation
- How to contribute
- License

### 2. API Documentation

**Purpose:** Help developers use your API correctly

**Audience:** Other developers integrating with your code

**Key information:**

- Endpoint/function signature
- Parameters and types
- Return values
- Error cases
- Authentication requirements
- Examples

### 3. Inline Comments

**Purpose:** Explain non-obvious decisions and complex logic

**Audience:** Future developers (including future you)

**When to add:**

- Non-obvious decisions ("why" not "what")
- Complex algorithms
- Workarounds
- Edge cases
- Performance considerations
- Security considerations

### 4. Technical Guides

**Purpose:** Teach how to accomplish specific tasks

**Audience:** Developers working with the system

**Types:**

- How-to guides (step-by-step)
- Architecture overviews (system structure)
- Integration guides (connecting systems)
- Troubleshooting guides (debugging help)

### 5. Architecture Decision Records (ADRs)

**Purpose:** Document important technical decisions and their rationale

**Audience:** Current and future team members

**Key information:**

- Context (what problem exists)
- Decision (what was chosen)
- Alternatives considered
- Consequences (trade-offs)

## README Template

```markdown
# Project Name

Brief description (one paragraph) of what this project does and why it exists.

## Features

- Feature 1
- Feature 2
- Feature 3

## Installation

```bash
npm install project-name
```

## Quick Start

```javascript
import { Thing } from 'project-name'

const thing = new Thing()
thing.doSomething()
// Output: ...
```

## Usage

### Basic Usage

[Most common use case with complete example]

### Advanced Usage

[More complex scenarios]

## API Reference

### `functionName(param1, param2)`

Description of what the function does.

**Parameters:**

- `param1` (string, required): Description of parameter
- `param2` (number, optional): Description with default. Default: 42

**Returns:** `string` - Description of return value

**Throws:**

- `Error` - When parameter is invalid

**Example:**

```javascript
const result = functionName('hello', 10)
console.log(result) // "hello repeated 10 times"
```

## Configuration

[How to configure, if applicable]

## Troubleshooting

### Error: "Cannot find module"

**Cause:** Package not installed
**Solution:**

```bash
npm install project-name
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

MIT License - see [LICENSE](LICENSE) file for details.

```

## API Documentation Template

### REST API

```markdown
## POST /api/users

Create a new user account.

### Authentication

Requires admin access token in Authorization header.

### Request

**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer <admin_token>"
}
```

**Body:**

```json
{
  "email": "user@example.com",
  "name": "John Doe",
  "role": "user"
}
```

**Body Parameters:**

- `email` (string, required): Valid email address. Must be unique.
- `name` (string, required): User's full name. 2-100 characters.
- `role` (string, optional): User role. One of: "user", "admin". Default: "user".

### Response

**Success (201 Created):**

```json
{
  "id": "abc123",
  "email": "user@example.com",
  "name": "John Doe",
  "role": "user",
  "createdAt": "2024-01-01T00:00:00Z"
}
```

**Error Responses:**

**400 Bad Request:**

```json
{
  "error": "Invalid email format",
  "field": "email"
}
```

**401 Unauthorized:**

```json
{
  "error": "Authentication required"
}
```

**403 Forbidden:**

```json
{
  "error": "Admin access required"
}
```

**409 Conflict:**

```json
{
  "error": "Email already exists",
  "field": "email"
}
```

**429 Too Many Requests:**

```json
{
  "error": "Rate limit exceeded. Try again in 60 seconds.",
  "retryAfter": 60
}
```

### Example

**cURL:**

```bash
curl -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer abc123..." \
  -d '{
    "email": "user@example.com",
    "name": "John Doe",
    "role": "user"
  }'
```

**JavaScript:**

```javascript
const response = await fetch('https://api.example.com/users', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer abc123...'
  },
  body: JSON.stringify({
    email: 'user@example.com',
    name: 'John Doe',
    role: 'user'
  })
})

const user = await response.json()
console.log(user.id) // "abc123"
```

### Rate Limiting

- 100 requests per minute per API key
- Returns 429 when exceeded
- Check `X-RateLimit-Remaining` header

```

### Function/Method Documentation

```typescript
/**
 * Calculate the total price including tax and shipping.
 *
 * Tax is calculated on the subtotal, not including shipping.
 * Free shipping is applied for orders over $50.
 *
 * @param items - Array of cart items with price and quantity
 * @param shippingAddress - Shipping address for tax calculation
 * @returns Object containing subtotal, tax, shipping, and total
 *
 * @throws {Error} If items array is empty
 * @throws {Error} If any item has invalid price or quantity
 *
 * @example
 * ```typescript
 * const total = calculateTotal([
 *   { price: 10, quantity: 2 },
 *   { price: 15, quantity: 1 }
 * ], { state: 'CA' })
 *
 * console.log(total)
 * // {
 * //   subtotal: 35,
 * //   tax: 2.80,
 * //   shipping: 0,
 * //   total: 37.80
 * // }
 * ```
 */
function calculateTotal(
  items: CartItem[],
  shippingAddress: Address
): OrderTotal {
  // Implementation...
}
```

## Inline Comment Guidelines

### When to Comment

**✅ DO comment:**

- **Why**: Explains reasoning for non-obvious decisions
- **Trade-offs**: Documents deliberate choices
- **Workarounds**: Explains temporary solutions
- **Complex logic**: Clarifies difficult algorithms
- **Edge cases**: Documents special handling
- **Performance**: Explains optimization choices
- **Security**: Notes security considerations

**❌ DON'T comment:**

- **What**: Code is self-explanatory
- **Redundant**: Comment repeats code
- **Obvious**: Anyone can see what it does

### Good vs Bad Comments

```typescript
// ❌ BAD: States the obvious
// Loop through users
for (const user of users) {
  // Print user name
  console.log(user.name)
}

// ✅ GOOD: Explains why
// Process in creation order to maintain referential integrity
// (newer records may reference older ones)
for (const user of users.sort((a, b) => a.createdAt - b.createdAt)) {
  processUser(user)
}

// ❌ BAD: Redundant
// Add 1 to counter
counter = counter + 1

// ✅ GOOD: Explains non-obvious decision
// +1 offset because API uses 1-based indexing (not 0-based)
const pageNumber = index + 1

// ❌ BAD: Explains what (obvious)
function calculateTotal(price, quantity) {
  // Multiply price by quantity
  return price * quantity
}

// ✅ GOOD: Explains why (non-obvious)
function calculateTotal(price, quantity) {
  // Use Number.toFixed(2) to prevent floating point errors
  // (0.1 + 0.2 !== 0.3 in JavaScript)
  return Number((price * quantity).toFixed(2))
}

// ❌ BAD: Commented-out code
function processOrder(order) {
  // const tax = order.subtotal * 0.08
  const tax = calculateTax(order)
  return order.subtotal + tax
}

// ✅ GOOD: Explains temporary workaround
function processOrder(order) {
  // TODO: Remove when new tax API is deployed (JIRA-123)
  // Using hardcoded rate temporarily during migration
  const tax = order.subtotal * 0.08
  return order.subtotal + tax
}
```

### Comment Formats

**Single-line comments:**

```typescript
// For brief explanations
const tax = subtotal * TAX_RATE  // Updated quarterly
```

**Multi-line comments:**

```typescript
/*
 * For longer explanations that span multiple lines.
 * Use when context requires more detail.
 */
```

**Doc comments (JSDoc/TSDoc):**

```typescript
/**
 * For API documentation.
 * Parsed by documentation generators.
 * @param name - Parameter description
 * @returns Return value description
 */
```

**TODO comments:**

```typescript
// TODO(username): Description of what needs to be done
// FIXME: Description of what's broken and needs fixing
// HACK: Description of temporary workaround
// NOTE: Important information to highlight
```

## Technical Guide Template

```markdown
# How to [Task Name]

Brief description of what this guide teaches and who should use it.

## Prerequisites

- Requirement 1
- Requirement 2
- Knowledge/tools needed

## Overview

High-level explanation of the process or concept.

## Step-by-Step Instructions

### Step 1: [First Action]

Detailed description of what to do.

```bash
# Command to run
command --option value
```

**Expected result:** What you should see.

**If something goes wrong:** How to troubleshoot.

### Step 2: [Next Action]

[Continue with clear steps...]

## Example

Complete working example showing the entire process.

```typescript
// Full code example
```

## Common Issues

### Issue: [Problem Description]

**Symptom:** What you see when this happens.
**Cause:** Why it happens.
**Solution:** How to fix it.

## Related Documentation

- [Link to related guide]
- [Link to API docs]

## Next Steps

- [What to do after completing this guide]

```

## Architecture Decision Record Template

```markdown
# ADR-###: [Decision Title]

**Status:** Proposed | Accepted | Deprecated | Superseded
**Date:** YYYY-MM-DD
**Deciders:** [Names of decision makers]

## Context

What is the issue we're trying to solve? What factors are at play?
What constraints exist?

## Decision

What did we decide to do?

## Alternatives Considered

### Alternative 1: [Name]

**Description:** Brief explanation

**Pros:**
- Advantage 1
- Advantage 2

**Cons:**
- Disadvantage 1
- Disadvantage 2

**Why not chosen:** Explanation

### Alternative 2: [Name]

[Same structure...]

## Consequences

### Positive

- Benefit 1
- Benefit 2

### Negative

- Drawback 1
- Drawback 2

### Neutral

- Trade-off 1
- Trade-off 2

## Implementation Notes

Any specific guidance for implementing this decision.

## References

- [Related documentation]
- [Discussion links]
- [Research sources]
```

## Documentation Best Practices

### 1. Write for Your Audience

**Different audiences need different docs:**

- **New users:** Quick start, common use cases
- **API consumers:** Complete reference, examples
- **Contributors:** Architecture, dev setup
- **Maintainers:** Design decisions, trade-offs

### 2. Show, Don't Just Tell

**Bad:**

```
The function accepts parameters and returns a result.
```

**Good:**

```typescript
function calculateTotal(items, tax) {
  return items.reduce((sum, item) => sum + item.price, 0) * (1 + tax)
}

// Example usage:
const items = [{ price: 10 }, { price: 20 }]
const total = calculateTotal(items, 0.08) // 32.40
```

### 3. Keep Examples Runnable

**Test your examples:**

- Copy/paste should work
- Include all imports
- Show complete code, not fragments
- Verify examples actually run

### 4. Maintain Documentation

**Documentation rots:**

- Update docs when code changes
- Include doc updates in PRs
- Review docs periodically
- Mark outdated docs clearly

### 5. Use Clear Language

**Avoid jargon:**

- Bad: "Leverages polymorphic memoization"
- Good: "Caches results based on input type"

**Be specific:**

- Bad: "It's fast"
- Good: "Responds in < 100ms for 95% of requests"

**Use active voice:**

- Bad: "The request is processed by the server"
- Good: "The server processes the request"

## Documentation Checklist

### README

- [ ] Clear description of what project does
- [ ] Installation instructions
- [ ] Quick start example
- [ ] Link to full documentation
- [ ] How to contribute
- [ ] License information

### API Docs

- [ ] All public APIs documented
- [ ] Parameters described with types
- [ ] Return values described
- [ ] Error cases documented
- [ ] Examples provided
- [ ] Authentication requirements stated

### Inline Comments

- [ ] Complex logic explained
- [ ] Non-obvious decisions documented
- [ ] Workarounds noted
- [ ] No redundant comments
- [ ] No commented-out code
- [ ] TODOs have owner and context

### Technical Guides

- [ ] Prerequisites listed
- [ ] Steps are clear and ordered
- [ ] Examples are complete and runnable
- [ ] Common issues addressed
- [ ] Related docs linked

## Integration with Other Skills

- Use **explainer** skill for creating clear explanations
- Use **proof-of-work** skill to verify examples actually work
- Reference **architecture-design** skill for architecture documentation
- Reference **technical-planning** skill for implementation guides

## Common Documentation Mistakes

### ❌ No Examples

**Bad:** "Use the function to process data"
**Good:** "Use processData(items) to validate and format user input"

### ❌ Outdated Information

**Bad:** Docs say version 1.0, code is version 3.0
**Good:** Update docs with code changes

### ❌ Assuming Knowledge

**Bad:** "Simply configure the flux capacitor"
**Good:** "Add FLUX_CAPACITOR=true to your .env file"

### ❌ Incomplete Examples

**Bad:**

```typescript
const result = doSomething()
```

**Good:**

```typescript
import { doSomething } from 'my-package'

const result = doSomething({
  option1: 'value',
  option2: 42
})
console.log(result) // Expected output
```

### ❌ Too Much Documentation

**Bad:** Document every single line
**Good:** Document the "why" and non-obvious parts

## Remember

1. **Write for the reader** - What do they need to know?
2. **Show with examples** - Working code is clearer than prose
3. **Keep it updated** - Stale docs are worse than no docs
4. **Test examples** - Verify they actually work
5. **Explain "why"** - The "what" is in the code

**Good documentation helps people use your code correctly and efficiently.**
