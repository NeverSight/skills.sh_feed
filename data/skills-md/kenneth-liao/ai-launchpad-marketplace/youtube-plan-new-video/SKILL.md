---
name: youtube-plan-new-video
description: Generate a complete video plan with optimized title, thumbnail, and hook concepts based on research. Orchestrates specialized skills (youtube-title, youtube-thumbnail, youtube-video-hook) to create production-ready video plans. Use after research is complete or when the user wants to plan a new video.
---

# YouTube Video Planning

## Overview

This skill generates complete video plans by orchestrating specialized skills to create optimized titles, thumbnails, and hooks. It takes research as input and produces a production-ready plan with all creative elements needed to maximize video performance.

**Core Principle**: Leverage specialized skills to ensure proven patterns for CTR (title/thumbnail) and retention (hook). Never generate these elements manually.

## When to Use

Use this skill when:
- Research has been completed and you need to generate title/thumbnail/hook concepts
- The user asks to plan a new video
- You need to create production-ready creative elements
- You want to generate multiple options for the user to choose from

## Prerequisites

**MANDATORY**: Research for the new video must be completed first. Either:
1. Research file exists at `./youtube/episode/[episode_number]_[topic_short_name]/`, OR
2. Invoke `youtube-research-video-topic` skill to conduct research first

## Planning Workflow

Execute all steps below to complete the video plan. Add these as ToDos so that you can systematically track your progress.

### Step 0: Load Research

Read the research file for this episode:
- Location: `./youtube/episode/[episode_number]_[topic_short_name]/research.md`

If research doesn't exist, invoke `youtube-research-video-topic` skill first.

The video plan **MUST** incorporate research findings at each step.

### Step 1: Create a new plan file at: `./youtube/episode/[episode_number]_[topic_short_name]/plan.md`

If a plan file already exists, read it to understand what has been done so far and continue from there.

You will update this document as you progress through the planning steps.

The plan file **MUST** include the following sections (to be populated in later steps):

```markdown
# [Episode_Number] (if applicable): [Topic] - Video Plan

## Research Summary
[Summary of research insights]

## Titles
[Title 1]
[Title 2]
[Title 3]

Each title should include:
1. Title text
2. The rationale for why it is predicted to perform well and how it aligns with the research insights

Include a star rating from 1-3 stars (⭐) indicating your recommendation rating for each title. (⭐⭐⭐) is your top recommendation.

Once the user has made their selection, update the title section to indicate the user's selection with a (✅ User Selection) next to the selected title.

## Thumbnails
[Thumbnail 1 for Title 1]
[Thumbnail 2 for Title 1]
[Thumbnail 1 for Title 2]
[Thumbnail 2 for Title 2]
[Thumbnail 1 for Title 3]
[Thumbnail 2 for Title 3]

Each thumbnail concept should include:
1. The title that the thumbnail is paired with
2. A description of the thumbnail concept
3. The rationale for why it is predicted to perform well, how it aligns with the research insights, and how it complements the title

Include a star rating from 1-3 stars (⭐) indicating your recommendation rating for the top 3 thumbnail concepts you recommend. (⭐⭐⭐) is your top recommendation.

Once the user has made their selection, update the thumbnail section to indicate the user's selection with a (✅ User Selection) next to the selected thumbnail concept.

## Hooks
[Hook 1 for Selected Title + Thumbnail]
[Hook 2 for Selected Title + Thumbnail]
[Hook 3 for Selected Title + Thumbnail]

Each hook should include:
1. A description of the hook strategy (including the actual hook script)
2. The rationale for why it is predicted to perform well, how it aligns with the research insights, and how it complements the title + thumbnail.

Include a star rating from 1-3 stars (⭐) indicating your recommendation rating for each hook. (⭐⭐⭐) is your top recommendation.

Once the user has made their selection, update the hook section to indicate the user's selection with a (✅ User Selection) next to the selected hook.

## High-Level Content Outline
[Outline]

## Final Plan
[Title]
[Thumbnails]
[Hook]
[Outline]
```

### Step 2: Generate Title Options

1. **MANDATORY**: Invoke `youtube-title` skill to generate 3 optimized titles.

2. Document all title options in the plan file including:
- Title
- Rationale
- Star rating

**NOTE**: You MUST complete title generation before proceeding to thumbnails, as thumbnails need to complement the titles.

### Step 3: Generate Thumbnail Concepts

1. **MANDATORY**: Invoke `youtube-thumbnail` skill to generate 2 thumbnail concepts for each title. These should be concept descriptions only, not actual images yet.

2. Document all thumbnail concepts in the plan file including:
- Title Pairing
- Concept
- Rationale
- Star rating

### Step 4: Present Recommendation and Get User Selection

1. Present all title/thumbnail combinations to the user, along with your top 3 recommended title + thumbnail pairings.

2. Ask the user to select their one preferred title + thumbnail pairing to proceed with.

3. Update both the title and thumbnail sections in the plan file to indicate the user's selection with a (✅ User Selection). 

### Step 5: Generate Hook Strategy

1. **MANDATORY**: Invoke `youtube-video-hook` skill to generate 3 retention-optimized hooks, only for the user's selected title + thumbnail pairing.

2. Document all hook strategies in the plan file including:
- Hook Strategy
- Rationale
- Star rating

3. Present all hook options to the user and ask the user to select their preferred hook strategy to proceed with.

4. Update the hook section in the plan file to indicate the user's selection with a (✅ User Selection).

The plan should now contain a user-selected title, thumbnail, and hook combination!

### Step 6: High-Level Content Outline

Create and document strategic roadmap:
- Break video into sections (Hook, Intro, Main Content, Outro)
- List key points and estimated durations
- Identify critical demonstrations/examples
- Note transitions

You must keep the outline **VERY HIGH-LEVEL**. Keep it strategic: Structure and key points only, no detailed scripts. 

Do not assume any specific content that should be covered/demonstrated, leave that to the content creator. The goal here is to provide a high-level structure that can be fleshed out by the content creator. Focus on what's important to cover from the viewer's perspective.

### Step 7: Finalize Plan with AB Testing Thumbnails

Now that the user has selected their preferred title, thumbnail, and hook, it's time to finalize the plan.

1. **MANDATORY**: Invoke `youtube-thumbnail` skill to generate 3 thumbnail options for AB testing. These should be actual images generated with `thumbkit`, not just concepts. The first thumbnail should be based on the user's selected thumbnail concept. The other 2 should test different visual styles of the first thumbnail.

2. Update the final plan section in the plan file with the complete final selections, including the set of 3 thumbnails for AB testing.

The final plan should include:
- **Title**: [Selected title]
- **Thumbnails**: 
   - ![Thumbnail A](/path/to/thumbnail_a.png)
      Thumbnail A Description
   - ![Thumbnail B](/path/to/thumbnail_b.png)
      Thumbnail B Description
   - ![Thumbnail C](/path/to/thumbnail_c.png)
      Thumbnail C Description
- **Hook**: [Selected hook strategy]
- **Rationale**: [Why this combination works]

Thumbnails should be the actual generated images embedded in the markdown file. A final selection should **ALWAYS** have 3 thumbnails to test. 

## Execution Guidelines

### Always Invoke Specialized Skills

**NEVER** generate titles, thumbnails, or hooks manually. Always invoke:
- `youtube-title` for title generation
- `youtube-thumbnail` for thumbnail concepts
- `youtube-video-hook` for hook strategies

### Provide Multiple Options

**CRITICAL**: Always include ALL options so the user can make an informed decision. Do not simply select one option and tell the user to use it.

### Ensure Complementarity

Verify that title/thumbnail/hook work together:
- Thumbnail complements title visually
- Hook extends curiosity (doesn't repeat title)
- All elements align with the unique value proposition

### Back Recommendations with Research

When recommending combinations:
- Reference content gaps from research
- Cite competitor insights
- Explain how the combination addresses the opportunity

## Quality Checklist

Verify completion before finalizing plan:
- [ ] Research file loaded and reviewed
- [ ] **youtube-title skill invoked** - 3 title options generated
- [ ] **youtube-thumbnail skill invoked** - 2 thumbnail concepts for each title
- [ ] **youtube-video-hook skill invoked** - Hook strategies generated
- [ ] Recommendations marked by star rating
- [ ] Title/thumbnail/hook complementarity verified
- [ ] Recommendations backed by research insights

## Tools to Use

Execute planning using these tools:

**Skill Invocations** (MANDATORY):
- `youtube-research-video-topic` - Invoke if research doesn't exist
- `youtube-title` - Invoke to generate title options
- `youtube-thumbnail` - Invoke to generate thumbnail concepts and thumbnail images
- `youtube-video-hook` - Invoke to generate hook strategies

## Common Pitfalls to Avoid

1. **Skipping Skill Invocation**: Generating titles/thumbnails/hooks manually → Must invoke specialized skills
2. **Single Option**: Only providing one recommendation → Provide all options to the user along with your recommendations
3. **Missing Research**: Starting without research → Load research or invoke research skill first
4. **Ignoring Complementarity**: Title/thumbnail/hook don't work together → Verify alignment
5. **No Rationale**: Recommendations without explanation → Back with research insights

## Example Execution

**Scenario**: User requests plan for video about "Building AI agents with memory" (research already complete)

Execute workflow:
1. Load research → Read `18_ai_agents_with_memory.md`, extract ⭐⭐⭐ gap for practical memory implementation
2. Create plan file at `./youtube/episode/18_ai_agents_with_memory/plan.md`
3. Invoke `youtube-title` skill → Generate 5 title options focused on practical implementation
4. Invoke `youtube-thumbnail` skill → Generate 2 concepts for each title (10 total)
5. Invoke `youtube-video-hook` skill → Generate 3 hook strategies for selected title + thumbnail pairing
6. Update the plan file with the user's final selection and set of 3 thumbnails for AB testing

**Result**: Production-ready plan with multiple options for the user to choose from, all backed by research and generated using proven patterns.

**CRITICAL**: Present all options to the user, not just your top recommendation. The user should make the final decision.
