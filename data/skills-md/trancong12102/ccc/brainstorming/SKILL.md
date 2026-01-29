---
name: brainstorming
description: "Collaboratively explore ideas and design solutions through guided dialogue before implementation. Use this skill when creating features, building components, adding functionality, designing systems, or when the user says \"brainstorm\", \"design this\", \"help me think through\", or \"let's plan\"."
---

# Brainstorming Ideas Into Designs

## Overview

Help turn ideas into fully formed designs and specs through natural collaborative dialogue.

Start by understanding the current project context, then ask questions one at a time to refine the idea. Once you understand what you're building, present the design in small sections (200-300 words), checking after each section whether it looks right so far.

## Tool Usage

**ALWAYS use the `AskUserQuestion` tool** when asking questions to the user. This provides a structured interface for gathering input.

- Use `multiSelect: false` for single-choice questions (most common)
- Use `multiSelect: true` when multiple options can be selected together
- Provide 2-4 clear options with descriptions
- Keep the `header` short (max 12 chars) - e.g., "Approach", "Auth type", "Storage"
- **Always include your recommendation**: Put your recommended option first and add "(Recommended)" to the label
- **Always explain why**: In the question text or option descriptions, explain your reasoning for the recommendation

## The Process

**Understanding the idea:**

- Check out the current project state first (files, docs, recent commits)
- Use `AskUserQuestion` to ask one question at a time to refine the idea
- Prefer multiple choice questions when possible, but open-ended is fine too
- Only one question per message - if a topic needs more exploration, break it into multiple questions
- Focus on understanding: purpose, constraints, success criteria

**Exploring approaches:**

- Propose 2-3 different approaches with trade-offs
- Present options conversationally with your recommendation and reasoning
- Lead with your recommended option and explain why
- **Consult the Oracle** when facing complex architectural decisions (see below)

**Presenting the design:**

- Once you believe you understand what you're building, present the design
- Break it into sections of 200-300 words
- Use `AskUserQuestion` after each section to validate (e.g., "Does this section look right?")
- Cover: architecture, components, data flow, error handling, testing
- Be ready to go back and clarify if something doesn't make sense

## Key Principles

- **Use AskUserQuestion tool** - Always use the tool for structured user input
- **Recommend with reasoning** - Every question must include your recommendation and why
- **Consult Oracle proactively** - Get second opinions on complex decisions
- **One question at a time** - Don't overwhelm with multiple questions
- **Multiple choice preferred** - Easier to answer than open-ended when possible
- **YAGNI ruthlessly** - Remove unnecessary features from all designs
- **Explore alternatives** - Always propose 2-3 approaches before settling
- **Incremental validation** - Present design in sections, validate each
- **Be flexible** - Go back and clarify when something doesn't make sense

## Oracle Consultation

**Proactively invoke the Oracle skill** to get a second opinion when:

- **Complex architectural decisions** - Multiple viable patterns with significant trade-offs (e.g., microservices vs monolith, event-driven vs request-response)
- **Security-sensitive designs** - Authentication flows, data encryption, access control patterns
- **Performance-critical choices** - Caching strategies, database indexing, algorithm selection
- **You're uncertain** - When you have a recommendation but want validation before presenting to the user

### How to Consult

Use the **Skill tool** to invoke the oracle: `Skill(skill: "oracle")`. The oracle's instructions will be loaded and guide you through the consultation process.

### Reaching Consensus

When Oracle's opinion differs from yours:

1. **Present both perspectives** to the user with clear reasoning
2. **Highlight where opinions align** - these are likely the right choices
3. **Explain disagreements honestly** - "Oracle suggests X because [reason], but I lean toward Y because [reason]"
4. **Let the user decide** on contentious points with full context

### When NOT to Consult

- Simple, straightforward decisions with obvious answers
- Minor implementation details that don't affect architecture
- When the user has already expressed a strong preference
