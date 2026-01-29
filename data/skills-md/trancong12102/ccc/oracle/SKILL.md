---
name: oracle
description: Invoke a powerful reasoning model for complex analysis tasks. Use when facing difficult bugs, reviewing critical code, designing complex refactors, needing architectural analysis, or seeking consensus on decisions. Also use for 'ask the oracle', 'get a second opinion', 'consult oracle', or 'deep analysis'.
---

# Oracle - Second Opinion Model

Invokes OpenAI's GPT-5.2 extra high reasoning model via CLI for complex analysis tasks. It excels at debugging, code review, architecture analysis, and finding better solutions.

**Prerequisite:** Codex CLI installed and authenticated (`codex login`).

**Trade-offs:** Slower and more expensive than the main agent, but significantly better at complex reasoning. Use deliberately, not for every task.

## Invocation

Use `codex exec --profile oracle` to run the reasoning model:

```bash
codex exec --profile oracle "Review @src/auth/jwt.ts for security vulnerabilities"
```

### Examples

```bash
# Security review
codex exec --profile oracle "Review @src/auth/jwt.ts for security vulnerabilities. Provide specific fixes."

# Debugging
codex exec --profile oracle "Find why memory leak in @src/DataFetcher.tsx. Component doesn't clean up on unmount."

# Architecture analysis
codex exec --profile oracle "Analyze how @src/services/payment.ts and @src/services/order.ts interact. Propose refactoring plan."

# Complex bug investigation
codex exec --profile oracle "Bug: Users see stale data after updates. Check @src/cache/invalidation.ts for race conditions."
```

## Prompting for Reasoning Models

Reasoning models work differently from completion models. Follow these guidelines:

**Keep prompts simple and direct:**

- State the goal clearly without excessive context
- Let the model explore and discover relevant information
- Avoid step-by-step instructions - the model reasons on its own

**Focus on WHAT, not HOW:**

- Bad: "First read the file, then analyze each function, then check for..."
- Good: "Review this code for security vulnerabilities"

**Use `@` syntax for file references:**

- Include relevant files directly: `@src/auth/login.ts`
- The model will read and understand the code

**Be specific about expected output:**

- "Provide specific fixes" > "Is this correct?"
- "List all race conditions" > "Are there any bugs?"

## Example Prompts

### Security Review

```text
Review @src/auth/jwt.ts for security vulnerabilities.
Provide specific fixes for any issues found.
```

### Debugging

```text
Find why the memory leak occurs in @src/components/DataFetcher.tsx.
The component fetches data but doesn't clean up on unmount.
```

### Architecture Analysis

```text
Analyze how @src/services/payment.ts and @src/services/order.ts interact.
Propose a refactoring plan that maintains backward compatibility.
```

### Complex Bug Investigation

```text
Bug: Users intermittently see stale data after updates.
Related files: @src/api/update.ts @src/cache/invalidation.ts @src/hooks/useData.ts

Identify race conditions or cache invalidation issues and provide a fix.
```

## Workflow

Think step-by-step:

1. **Gather context first**: Identify relevant files and the specific problem
2. **Formulate a focused prompt**: Include file references with `@`, state the goal directly
3. **Invoke the oracle**: Run `codex exec --profile oracle "prompt"`
4. **Continue if needed**: Use `codex exec resume SESSION_ID "follow-up"` to refine analysis
5. **Act on the analysis**: Implement recommendations from the oracle's response

## Continuing Conversations

Use `codex exec resume SESSION_ID` to continue until satisfied. The session ID is returned from the initial invocation.

```bash
# Initial analysis (returns session ID)
codex exec --profile oracle "Review @src/auth/jwt.ts for security vulnerabilities"
# Output includes: Session ID: abc123...

# Continue with follow-up questions using the session ID
codex exec resume abc123 "Also check for timing attacks in the token validation"

# Keep refining with the same session
codex exec resume abc123 "What about the refresh token rotation logic?"
```

| Argument | Description |
| -------- | ----------- |
| `SESSION_ID` | Session ID returned from the initial invocation |
| `PROMPT` | Follow-up instruction to send after resuming |

## Rules

- Use the oracle for complex problems that require deep reasoning
- Keep prompts focused - one problem per invocation
- Include file references with `@` syntax for relevant code
- Request specific, actionable output
- Chain with main agent: oracle for analysis, main agent for implementation
- Oracle is read-only; use the main agent to implement changes
