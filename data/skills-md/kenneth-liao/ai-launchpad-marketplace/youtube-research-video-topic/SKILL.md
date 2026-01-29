---
name: youtube-research-video-topic
description: Conduct pure research for YouTube video topics by analyzing competitors, identifying content gaps, and documenting strategic insights. Use when you need to research a video topic before planning. Produces concise, insight-focused research documents that identify the biggest opportunities for video performance.
---

# YouTube Video Topic Research

## Overview

This skill conducts pure research for YouTube video topics. Execute all steps to produce actionable insights that identify content gaps and analyze competitors. This skill focuses ONLY on research - it does not generate titles, thumbnails, or hooks.

**Core Principle**: Focus on insights and big levers, not data dumping. Research should be comprehensive yet concise, backed by data, and designed to inform strategic decisions.

## When to Use

Use this skill when:
- You need to research a video topic before planning production
- The user asks to research a video idea or topic
- You want to understand the competitive landscape
- You need to identify content gaps and opportunities

## Youtube Researcher Subagents

You have access to youtube research subagents that can be used to conduct specific, focused research tasks. Youtube Researchers have access to all of the youtube analytics tools.

### Subagent Usage

Youtube Researchers can be invoked using the `Task` tool. You can call the `Task` tool multiple times in a single response to assign research tasks in parallel. This greatly improves performance. All research findings will be reported back to you for synthesis.

Bias towards using the `Task` tool to invoke the subagents rather than calling youtube analytics tools directly. Each `Task` prompt should be focused and specific, with a clear objective.

## Research Workflow

Execute all steps below to complete the research.

### Step 0: Create Research.md

Create a new research file for the video idea under `./youtube/episode/[episode]/`. If the user is organizing their videos into a series, include the episode number in the folder name. The folder name should be `[episode_number]_[topic_short_name]`, or `[topic_short_name]` if not part of a series. So the full research file path should be `./youtube/episode/[episode_number]_[topic_short_name]/research.md`.

All research **MUST** be written to this file.

If the file already exists, read it to understand what research has been done so far and continue from there.

### Step 1: Understand the Topic

Analyze and document:
- What problem does this video solve?
- Why would someone click on this video?
- What makes this topic relevant now?

### Step 2: Research User's Related Videos

Execute these actions:
1. Use `mcp__plugin_yt-content-strategist_youtube-analytics__search_videos` to find related videos from user's channel
2. Use `mcp__plugin_yt-content-strategist_youtube-analytics__get_video_details` for performance metrics
3. Identify what's already been covered and how to differentiate

Document in research file:
- Related videos (title, video ID, URL, key metrics)
- Performance insights (what worked, what didn't)
- Differentiation strategy for new video

### Step 3: Competitor Research

Execute these actions:
1. Use `mcp__plugin_yt-content-strategist_youtube-analytics__search_videos` to find 5-8 top videos on the topic
2. Filter for recent videos with high engagement
3. Use `mcp__plugin_yt-content-strategist_youtube-analytics__get_video_details` for each top video
4. Analyze patterns in successful videos

Document for each competitor:
- Title, channel, video ID, URL
- Subscriber count, views, engagement
- Focus/angle and what makes it successful

Synthesize key insights: Identify common patterns and different approaches across competitors.

### Step 4: Content Gap Analysis

Analyze and identify:
- What topics are saturated?
- What's missing or underexplored?
- Where can the user add unique value?

Document in research file:
- **What's Already Well-Covered**: 3-5 saturated topics/approaches
- **Content Gaps (Opportunities)**: Specific opportunities rated ⭐⭐⭐ (high), ⭐⭐ (medium), ⭐ (low)
- **Recommended Focus**: The specific angle and unique value proposition

**Rating Criteria**:
- ⭐⭐⭐ High: Significant gap, strong demand, clear differentiation
- ⭐⭐ Medium: Moderate gap, some competition, good potential
- ⭐ Low: Minor gap, heavily competed

## Output Structure

Save all research to: `./youtube/episode/[episode_number]_[topic_short_name]/research.md`

Use this template structure:
```markdown
# [Episode_Number]: [Topic] - Research

## Episode Overview
**Topic**: [Brief description]
**Target Audience**: [Who this is for]
**Goal**: [What viewers will learn/gain]

## Research Notes
### Key Concepts to Cover
[High-level list]

## YouTube Research
### Related Videos
**Your Previous Videos:** [Analysis]
**Top Competing Videos:** [5-8 videos with analysis]
**Key Insights:** [Patterns and findings]

## Content Gap Analysis
### What's Already Well-Covered: [List]
### Content Gaps (Opportunities): [Rated list]
### Recommended Focus: [Specific angle and value prop]

## Technical Implementation
[Only if applicable]

## Production Notes
**Episode Number**: [Number]
**Status**: Research Complete
**Created/Updated**: [Dates]

## Execution Guidelines

### Focus on Insights, Not Data
Execute research with these principles:
- Synthesize patterns from research
- Identify 3-5 key insights with supporting data
- Explain WHY approaches work
- Limit competitor research to 5-8 videos

### Prioritize Big Levers
Focus research on these impact areas in order:
1. Content Gaps (Unique value)
2. Competitor Patterns
3. Audience Needs
4. Technical Requirements

### Back Recommendations with Data
When documenting findings:
- ❌ "Make a video about AI agents"
- ✅ "Focus on AI agent memory systems (⭐⭐⭐ gap) - competitors get 50K+ views but don't cover persistent memory"

### Maintain Episode Continuity
During research:
- Reference previous episode research
- Check for topic overlap
- Identify opportunities to build on previous content

## Quality Checklist

Verify completion before finalizing research:
- [ ] Related videos and 5-8 competitors documented with analysis
- [ ] Content gaps identified with ⭐ ratings
- [ ] Research is concise yet comprehensive (not data dumping)
- [ ] All recommendations backed by data
- [ ] Unique value proposition clearly stated

## Tools to Use

Execute research using these tools:

**YouTube Analytics MCP**:
- `mcp__plugin_yt-content-strategist_youtube-analytics__search_videos` - Find videos by query
- `mcp__plugin_yt-content-strategist_youtube-analytics__get_video_details` - Get video metrics
- `mcp__plugin_yt-content-strategist_youtube-analytics__get_channel_details` - Get channel info

**Web Research**: Use `web-search` and `web-fetch` for industry trends and context

**Filesystem**: Use `view` for channel context and previous research

## Common Pitfalls to Avoid

1. **Data Dumping**: Listing every video found without synthesis → Limit to 5-8 top videos, focus on patterns
2. **Vague Content Gaps**: "Not much content on this topic" → Identify specific angles missing
3. **Over-Researching Technical Details**: Deep implementation research → Keep high-level, focus on what to cover
4. **Long Reports**: 800+ line documents → Focus on insights and big levers

## Example Execution

**Scenario**: User requests research for video about "Building AI agents with memory"

Execute workflow:
1. Load channel context → Read CLAUDE.md, get channel details (1,500 subs, tech tutorial niche)
2. Find related videos → Search user's channel, find Episode 15 on personal assistants, viewers asked about memory
3. Competitor research → Search and analyze 8 top videos, identify they cover theory not implementation
4. Gap analysis → Document ⭐⭐⭐ opportunity for practical memory implementation
6. Save research → Write to `./youtube/18_ai_agents_with_memory/research.md`

**Result**: Comprehensive research document ready for review or to proceed to the planning phase.

**Next Step**: If the user has asked to plan the video, invoke the `youtube-plan-new-video` skill to generate title, thumbnail, and hook concepts based on this research.
