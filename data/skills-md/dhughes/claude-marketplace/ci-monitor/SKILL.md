---
name: ci-monitor
description: This skill should be used when the user asks to "monitor the PR", "watch the CI", "check if CI passes", "let me know when CI finishes", "watch the checks", "monitor CI status", "tell me when the build completes", or any variation requesting to track GitHub PR check status until completion. Also use this skill proactively after creating or updating a PR when the user would benefit from knowing the CI result.
---

# GitHub CI Monitor

Monitor GitHub Pull Request CI/CD checks continuously until all checks complete, then provide visual and audio notification of the result.

## Core Behavior

**CRITICAL: Be tenacious.** CI pipelines vary wildly in duration—some complete in 2 minutes, others take over an hour. Never give up monitoring. Continue polling until receiving a definitive pass or fail result, or until explicitly stopped by the user.

## Prerequisites

Ensure the GitHub CLI (`gh`) is installed and authenticated. Verify with:

```bash
gh auth status
```

## Monitoring Workflow

### Step 1: Identify the PR

Determine the PR to monitor. If user specifies a PR number, use that. Otherwise, detect from current branch:

```bash
gh pr view --json number,title,url,headRepository
```

If no PR exists for the current branch, inform the user and offer to help create one.

### Step 2: Start Monitoring Loop

Begin the polling loop with clear user feedback:

1. Print initial status message: "Monitoring PR #X: [title]"
2. Print the PR URL for reference
3. Begin polling every 60 seconds

### Step 3: Poll for Check Status

Use `gh pr checks` to get current status:

```bash
gh pr checks <PR_NUMBER> --json name,state,conclusion
```

Check states:
- `PENDING` or `QUEUED` - Still running, continue polling
- `IN_PROGRESS` - Still running, continue polling
- `COMPLETED` - Check finished, examine conclusion

Check conclusions (when completed):
- `SUCCESS` - Check passed
- `FAILURE` - Check failed
- `CANCELLED` - Check was cancelled (treat as failure)
- `SKIPPED` - Check was skipped (treat as success)
- `NEUTRAL` - Neutral result (treat as success)

### Step 4: Determine Overall Status

All checks must complete before announcing results:

- **All checks completed with SUCCESS/SKIPPED/NEUTRAL**: CI passed
- **Any check with FAILURE/CANCELLED**: CI failed
- **Any check still PENDING/QUEUED/IN_PROGRESS**: Continue polling

### Step 5: Handle Completion

When all checks complete:

#### On Success

1. Print success summary:
   ```
   ✅ CI PASSED - PR #X: [title]
   All checks completed successfully.
   URL: [pr_url]
   ```

2. Play audio announcement:
   ```bash
   say "GitHub [repo-name] PR [pr-number] completed CI successfully" 2>/dev/null
   ```

#### On Failure

1. Print failure summary with details:
   ```
   ❌ CI FAILED - PR #X: [title]

   Failed checks:
   - [check_name]: [conclusion]
   - [check_name]: [conclusion]

   URL: [pr_url]
   ```

2. Get detailed failure information if available:
   ```bash
   gh pr checks <PR_NUMBER> --json name,state,conclusion,detailsUrl
   ```

3. Print links to failed check details

4. Play audio announcement:
   ```bash
   say "GitHub [repo-name] PR [pr-number] completed CI unsuccessfully" 2>/dev/null
   ```

## Audio Notification

Use macOS `say` command directly with stderr suppressed:

```bash
say "GitHub [repo-name] PR [pr-number] completed CI successfully" 2>/dev/null
say "GitHub [repo-name] PR [pr-number] completed CI unsuccessfully" 2>/dev/null
```

The `2>/dev/null` silently ignores errors on systems without `say`.

Use the repository name from `gh pr view --json headRepository`, extracting just the repo name (not owner/repo).

## Polling Behavior

### Interval

Poll every 60 seconds. Between polls, simply wait—do not output status unless there are changes.

### Progress Updates

Provide periodic updates to show monitoring is active:
- Every 5 minutes: Print brief status "Still monitoring... X checks pending"
- On state changes: Print when individual checks complete

### Error Handling

Network or API errors should not terminate monitoring:
- On transient error: Wait 60 seconds and retry
- After 3 consecutive errors: Inform user but continue trying
- Never give up unless user explicitly stops

### User Interruption

The user can stop monitoring at any time by:
- Saying "stop monitoring" or similar
- Starting a new task
- Pressing Ctrl+C

## Example Session

```
User: monitor the PR

Claude: Monitoring PR #42: Add user authentication feature
URL: https://github.com/acme/webapp/pull/42

Checking CI status...
- build: ⏳ in progress
- test: ⏳ pending
- lint: ✅ success

[60 seconds later]

- build: ✅ success
- test: ⏳ in progress
- lint: ✅ success

[60 seconds later]

- build: ✅ success
- test: ✅ success
- lint: ✅ success

✅ CI PASSED - PR #42: Add user authentication feature
All checks completed successfully.
URL: https://github.com/acme/webapp/pull/42

[Audio: "GitHub webapp PR 42 completed CI successfully"]
```

## Proactive Monitoring

When working on a PR (creating it, pushing updates, or responding to review), proactively offer to monitor CI if the user would benefit. For example, after running `gh pr create`, offer: "Would you like me to monitor the CI checks for this PR?"

When Claude has been doing automated work and creates or updates a PR, automatically start monitoring unless the user has indicated they don't want notifications.

## Key Points

1. **Never give up**: Some CI pipelines take an hour or more. Keep polling.
2. **Clear output**: Show what's being monitored and current status
3. **Audio alert**: Use `say` on macOS, skip gracefully elsewhere
4. **Failure details**: On failure, provide actionable information
5. **60-second interval**: Balance responsiveness with API rate limits
6. **Graceful errors**: Network issues don't stop monitoring
