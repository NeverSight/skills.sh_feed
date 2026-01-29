---
name: commit
description: Generates Conventional Commits messages and can stage/commit changes. Use when asked to create git commit messages or perform a commit.
---

# Commit Message Generator (Conventional Commits)

Generate commit messages following [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/).

## Execution Style

- Be concise and direct; avoid preambles or long plans.
- Use explicit formatting and exact output requirements.
- Infer type, scope, and breaking from the changes when possible; ask only if truly ambiguous.
- Prefer tool-driven git commands over manual edits.

## Workflow

1. Run `git status` and `git diff HEAD`.
2. Stage only user-specified files; if user requests "all", use `git add -A`.
3. Infer type/scope/breaking from the diff when possible; ask only if needed.
4. Draft subject, body, and footers.
5. Commit using HEREDOC:

   ```bash
   git commit -m "$(cat <<'EOF'
   <type>(<scope>): <description>

   <body>

   <footer>
   EOF
   )"
   ```

6. Output `<hash> <subject>` only.

## Scope Boundaries

- Do: analyze changes, generate message, stage files, commit.
- Don't: modify code, push, create branches, amend unless asked.

## Format

```text
<type>[optional scope][!]: <description>

[optional body]

[optional footer(s)]
```

## Spec Requirements

- Type is required; scope is optional and uses `(<noun>)`.
- Description must follow `: ` and be a short summary.
- Body is separated from subject by one blank line.
- Footer is separated from body by one blank line and uses `<token>: <value>` or `<token> #<value>`.
- Breaking change must use `!` or a `BREAKING CHANGE:`/`BREAKING-CHANGE:` footer.

## Types

- `feat`: new feature (SemVer minor)
- `fix`: bug fix (SemVer patch)
- `perf`: performance improvement
- `refactor`: restructure without behavior change
- `style`: formatting only
- `test`: add/update tests
- `docs`: documentation only
- `build`: build system/deps
- `ci`: CI config
- `chore`: other maintenance
- `revert`: revert commit

Breaking changes: use `!` or `BREAKING CHANGE:` footer (MAJOR).

## Subject

- Max 72 chars (50 preferred).
- Imperative, present tense; lowercase first letter.
- No trailing period.

## Scope

- Optional; use a noun for the affected module or area.
- Omit if unclear.

## Body

- Explain what/why, not how; wrap at 72.

## Footer

- Common tokens: `BREAKING CHANGE`, `Refs`, `Closes`, `Fixes`, `Co-authored-by`, `Reviewed-by`, `Acked-by`.

## Examples

```text
feat: add email notifications for new messages
```

```text
fix(cart): prevent ordering with empty shopping cart
```

```text
feat(api)!: redesign authentication endpoints

Migrate from session-based auth to JWT tokens.

BREAKING CHANGE: /api/login now returns JWT instead of session cookie.
```
