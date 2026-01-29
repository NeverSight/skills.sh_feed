---
name: project-memory
description: Use when setting up or organizing Claude Code project memory (CLAUDE.md, .claude/rules/) for better context awareness, consistent behavior, and project-specific instructions.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Bash
---

# Project Memory Skill

Set up and organize Claude Code's project memory system for consistent, context-aware assistance.

## Core Principle

**Project memory teaches Claude Code how to work with your specific codebase.** Well-organized project memory leads to more accurate, consistent, and helpful responses.

## Memory Hierarchy

Claude Code reads instructions in this order (higher = more precedence):

1. **Enterprise policy** (managed, highest)
2. **User memory** (`~/.claude/CLAUDE.md`)
3. **Project memory** (`CLAUDE.md` in project root)
4. **Modular rules** (`.claude/rules/*.md`)
5. **Local memory** (`CLAUDE.local.md`, gitignored)

Later sources override earlier ones for conflicting instructions.

## File Types

### CLAUDE.md (Project Root)

**Purpose:** Primary project instructions, conventions, and context

**Location:** Project root directory

**Visibility:** Checked into git, shared with team

**Contents:**

- Project overview and architecture
- Development commands (build, test, lint)
- Coding conventions and patterns
- Important constraints or requirements
- Links to key documentation

### .claude/rules/*.md

**Purpose:** Modular, path-specific rules

**Location:** `.claude/rules/` directory

**Visibility:** Checked into git

**Features:**

- Automatically loaded based on file path
- Supports subdirectories
- Can use YAML frontmatter with `globs` for path-specific targeting

### CLAUDE.local.md

**Purpose:** Personal, machine-specific instructions

**Location:** Project root directory

**Visibility:** Should be gitignored

**Use cases:**

- Personal preferences
- Local environment paths
- Machine-specific configurations
- Experimental instructions

## Setting Up Project Memory

### 1. Create CLAUDE.md

Start with essential project information:

```markdown
# Project Name

Brief description of what this project does.

## Development Commands

    # Build
    npm run build

    # Test
    npm test

    # Lint
    npm run lint

## Architecture

- `src/` - Source code
- `tests/` - Test files
- `docs/` - Documentation

## Conventions

- Use TypeScript for all new code
- Follow existing patterns in the codebase
- Run tests before committing

## Key Files

- `src/index.ts` - Main entry point
- `src/config.ts` - Configuration handling

```

### 2. Add Modular Rules (Optional)

Create path-specific rules in `.claude/rules/`:

```text
.claude/
  rules/
    api.md          # Rules for API code
    tests.md        # Rules for test files
    components/
      forms.md      # Rules for form components
```

### 3. Path-Specific Rules with Globs

Use YAML frontmatter to target specific paths:

```markdown
---
paths: ["src/api/**/*.ts", "src/services/**/*.ts"]
---

# API Development Rules

- All API functions must be async
- Always validate input parameters
- Use consistent error response format
- Include JSDoc with @throws annotations
```

### 4. Import Syntax

Reference other files from CLAUDE.md:

```markdown
# Project Instructions

See architecture: @docs/ARCHITECTURE.md
See API guidelines: @docs/API_GUIDELINES.md
```

Imported files are treated as direct context.

## CLAUDE.md Template

```markdown
# [Project Name]

[One-paragraph description of what this project does]

## Quick Start

    # Install dependencies
    [command]

    # Run development server
    [command]

    # Run tests
    [command]

## Architecture

[Brief overview of project structure]

### Key Directories

- `src/` - [Description]
- `tests/` - [Description]
- `config/` - [Description]

### Key Files

- `src/index.ts` - [Description]
- `src/config.ts` - [Description]

## Development Guidelines

### Code Style

- [Style convention 1]
- [Style convention 2]

### Testing

- [Testing convention 1]
- [Testing convention 2]

### Git Workflow

- [Commit convention]
- [Branch convention]

## Common Tasks

### Adding a New Feature

1. [Step 1]
2. [Step 2]
3. [Step 3]

### Running Tests

    [test command]

## Important Notes

- [Critical constraint or requirement]
- [Security consideration]
- [Performance consideration]

```

## Path-Specific Rules Examples

### For API Code

```markdown
---
paths: ["src/api/**/*.ts"]
---

# API Development Rules

## Request Handling

- Validate all input with zod schemas
- Return consistent error format: `{ error: string, code: string }`
- Always set appropriate HTTP status codes

## Authentication

- All endpoints require auth unless in ALLOWED_PUBLIC_ROUTES
- Use `requireAuth()` middleware

## Response Format

    // Success
    { data: T, meta?: { page, total } }

    // Error
    { error: string, code: string, details?: object }

```

### For Test Files

```markdown
---
paths: ["**/*.test.ts", "**/*.spec.ts"]
---

# Testing Rules

## Structure

- Use `describe()` for grouping related tests
- Use `it()` with descriptive names: "should [action] when [condition]"
- One assertion per test when possible

## Mocking

- Prefer dependency injection over mocking
- Mock at boundaries (API, database, file system)
- Clear mocks between tests

## Coverage

- All public functions need tests
- Test happy path and error cases
- Include edge cases
```

### For React Components

```markdown
---
paths: ["src/components/**/*.tsx"]
---

# Component Rules

## Structure

- One component per file
- Export component as default
- Co-locate styles with component

## Props

- Define props interface above component
- Use destructuring in function signature
- Document required vs optional props

## State

- Prefer controlled components
- Lift state up when shared between components
- Use hooks for complex state logic
```

## Best Practices

### Keep It Concise

**Bad:**

```markdown
## Introduction

This project is a web application that allows users to manage their tasks.
It was started in 2023 and has grown to include many features including
task creation, task editing, task deletion, task filtering, task sorting,
task searching, task sharing, and task exporting...
```

**Good:**

```markdown
Task management web app. Users create, edit, filter, and share tasks.
```

### Be Specific and Actionable

**Bad:**

```markdown
Write good code and follow best practices.
```

**Good:**

```markdown
- Use TypeScript strict mode
- Run `npm run lint` before committing
- All functions need JSDoc comments
```

### Include Commands

**Bad:**

```markdown
Build the project before deploying.
```

**Good:**

```markdown
    npm run build
    npm run deploy
```

### Use Imports for Long Content

**Bad:** Everything in one huge CLAUDE.md

**Good:**

```markdown
# Project

Quick overview here.

## Detailed Documentation

Architecture: @docs/ARCHITECTURE.md
API Guide: @docs/API.md
Deployment: @docs/DEPLOYMENT.md
```

### Path-Specific Over Generic

**Bad:**

```markdown
# CLAUDE.md
When writing tests, always use Jest.
When writing API code, always validate input.
When writing components, always use TypeScript.
```

**Good:**

```
.claude/rules/tests.md     -> Jest rules
.claude/rules/api.md       -> Validation rules
.claude/rules/components.md -> TypeScript rules
```

## When to Update Project Memory

### Add New Instructions

- Onboarding reveals missing context
- Repeated questions indicate gaps
- New conventions are established
- Architecture changes significantly

### Review Existing Instructions

- Code changes make instructions outdated
- Team feedback indicates confusion
- Patterns evolve over time

## Common Patterns

### Monorepo Setup

```markdown
# Monorepo

## Packages

- `packages/core/` - Core library
- `packages/cli/` - CLI tool
- `packages/web/` - Web application

## Commands

    # Build all packages
    npm run build

    # Test specific package
    npm run test --workspace=packages/core

## Rules

See package-specific rules in each package's `.claude/rules/` directory.
```

### Environment-Specific Notes

Keep in `CLAUDE.local.md` (gitignored):

```markdown
# Local Setup Notes

## Environment

- Using Node 20.x
- PostgreSQL running on port 5433 (not default)
- Redis running in Docker

## Personal Preferences

- Prefer verbose test output
- Always run lint before suggesting changes
```

## Integration with Han Plugins

Han plugins can contribute to project memory through hooks:

- **SessionStart hooks** can inject plugin-specific context
- **UserPromptSubmit hooks** can add reminders about conventions
- **Blueprints** complement CLAUDE.md with detailed system documentation

## Troubleshooting

### Claude Code ignores instructions

1. Check file location (must be project root for CLAUDE.md)
2. Check syntax (YAML frontmatter must be valid)
3. Check glob patterns match the files you're editing
4. More specific rules override general ones

### Rules conflict between files

- Later in hierarchy wins
- More specific globs win over general
- Local overrides project

### Performance with large CLAUDE.md

- Use imports for detailed docs
- Keep CLAUDE.md focused on essentials
- Move detailed rules to `.claude/rules/`

## Remember

1. **Start small** - Basic commands and conventions first
2. **Be specific** - Actionable instructions, not vague guidelines
3. **Stay current** - Update when code changes
4. **Use hierarchy** - Modular rules for path-specific needs
5. **Test it** - Verify Claude Code follows your instructions

**Good project memory makes Claude Code a better collaborator.**
