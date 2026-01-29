---
name: business-competitor-analysis
description: Perform comprehensive competitor analysis for any business. Produces an executive-summary markdown report with target customer profile, market positioning, pricing/business model, product features, funding/company size, SWOT analysis, and competitive matrix. All findings are data-grounded. Use when the user asks to analyze competitors, understand competitive landscape, compare a business to alternatives, or perform market research.
---

# Competitor Analysis Skill

Perform data-grounded competitor analysis producing an executive-summary markdown document with cited sources.

## Workflow Overview

1. **Extract business information** from provided details or website
2. **Define target customer profile** (required)
3. **Identify top 5 competitors** via web search
4. **Research each competitor** across key dimensions
5. **Identify market gaps and opportunities**
6. **Synthesize findings** into structured report with citations

## Step 1: Extract Business Information

**If user provides a website URL:**
1. Fetch the URL using `web_fetch`
2. Extract: company name, value proposition, target market, products/services, pricing (if visible), key differentiators

**If user provides business details directly:**
1. Parse the provided information
2. Identify any gaps that require web research to fill

<REQUIRED>
For both cases, you may perform web research to fill in any missing information or gather the required context outlined below.
</REQUIRED>

**Required business context to gather:**
- Company name and description
- Industry/vertical
- Target customer segment (B2B/B2C, size, geography)
- Core products/services
- Pricing model (if discoverable)
- Key value propositions

## Step 2: Define Target Customer Profile

**This step is required.** Understanding the target customer enables accurate assessment of direct vs. indirect competitors and market positioning.

Research and document the target customer across these dimensions:

### Firmographics
- Company size (employees, revenue range)
- Industry/vertical focus
- Geographic markets served
- Technology maturity level

### Psychographics & Pain Points
- Top 3-5 pain points the product addresses
- Primary goals and desired outcomes
- Current alternatives or workarounds
- Decision-making criteria and priorities
- Budgetary constraints

### Behavioral Patterns
- How customers currently solve this problem
- Where they search for solutions
- Typical buying process and timeline
- Key stakeholders in purchase decision

### Market Sizing (if discoverable)
- Total addressable market (TAM) estimates
- Serviceable addressable market (SAM)
- Market growth trends and projections

**Research approaches:**
- Search "[industry] market size" and "[product category] target market"
- Review the subject company's "customers" or "case studies" pages
- Check industry reports, analyst research, market studies
- Use the subject company's messaging to infer customer profile

For detailed examples and frameworks, refer to `references/competitive-analysis-framework.md`.

## Step 3: Identify Top 5 Competitors

Run targeted searches to find direct competitors:

```
Search queries to use:
- "[company name] competitors"
- "[product category] companies"
- "[industry] [target market] solutions"
- "alternatives to [company name]"
- "[core service] providers [geography if relevant]"
```

Select the top 5 most relevant direct competitors based on:
- Similar target market and customer segment
- Overlapping product/service offerings
- Comparable business model
- Market presence and visibility in search results

## Step 4: Research Each Competitor

For each competitor, gather data across four dimensions:

### 4a. Market Positioning & Messaging
- Fetch competitor homepage and about page
- Extract: tagline, value proposition, target audience messaging
- Note: tone, positioning (premium/budget/mid-market), key claims

### 4b. Pricing & Business Model
- Search "[competitor] pricing" and fetch pricing pages
- Document: pricing tiers, model (subscription/one-time/freemium), entry price point
- If pricing not public, note this and search for any available information

### 4c. Product/Feature Comparison
- Review product pages and feature lists
- Identify: core features, unique capabilities, integrations, limitations
- Note any recent product launches or announcements

### 4d. Funding & Company Size
- Search "[competitor] funding" and "[competitor] company size"
- Check for: Crunchbase mentions, LinkedIn company size, press releases
- Document: funding rounds, total raised, employee count estimates, founding year

## Step 5: Identify Market Gaps & Opportunities

After researching competitors, systematically identify gaps in the competitive landscape:

### What to Look For

**Underserved customer segments:**
- Which customer types or use cases do competitors ignore or serve poorly?
- Are there geographic, size, or industry segments with limited options?

**Feature/capability gaps:**
- What functionality is missing across all competitors?
- What do customers request that no one provides well?
- What emerging needs are competitors slow to address?

**Positioning gaps:**
- What market positions are unclaimed? (e.g., "affordable enterprise-grade", "developer-first", "compliance-focused")
- Are there price points without strong offerings?
- Are there business models (e.g., usage-based, freemium) competitors avoid?

**Approach/philosophy gaps:**
- Do all competitors share assumptions the subject company challenges?
- Are there cultural or regional needs competitors overlook?

Document 3-5 specific gaps with supporting evidence from competitor research.

## Step 6: Synthesize Report

Generate markdown report following the exact structure below.

## Output Template

<REQUIRED>
Save the output to a markdown file with the template structure below.
</REQUIRED>

```markdown
# Competitive Analysis: [Subject Company Name]

**Analysis Date:** [Current Date]  
**Industry:** [Industry/Vertical]  
**Target Market:** [B2B/B2C, segment details]

---

## Executive Summary

[2-3 paragraph synthesis of competitive landscape. Include: market position of subject company relative to competitors, key competitive advantages and vulnerabilities, most significant competitive threats. Every claim must reference a source using format [Source N](#Sources).]

---

## Target Customer Profile

### Primary Target Segment

**Firmographics:**
- Company size: [Employee count, revenue range]
- Industry focus: [Primary industries/verticals]
- Geographic markets: [Regions served]
- Technology maturity: [Early adopter/mainstream/conservative]

**Pain Points & Goals:**
- [Pain point 1 with description] [Source N](#Sources)
- [Pain point 2 with description] [Source N](#Sources)
- [Pain point 3 with description] [Source N](#Sources)
- Current alternatives: [What customers use today without this product]
- Decision criteria: [What matters most when evaluating solutions]

**Behavioral Patterns:**
- Current solution approach: [How they solve this problem today]
- Search/discovery: [Where they look for solutions]
- Buying process: [Typical purchase timeline and stakeholders]

**Market Sizing (if discoverable):**
- Total addressable market: [TAM estimate] [Source N](#Sources)
- Serviceable addressable market: [SAM for realistic target] [Source N](#Sources)
- Market growth: [YoY growth rate or projections] [Source N](#Sources)

---

## Competitive Matrix

| Dimension | [Subject] | [Competitor 1] | [Competitor 2] | [Competitor 3] | [Competitor 4] | [Competitor 5] |
|-----------|-----------|----------------|----------------|----------------|----------------|----------------|
| **Positioning** | [Premium/Mid/Budget] | ... | ... | ... | ... | ... |
| **Target Customer** | [Segment] | ... | ... | ... | ... | ... |
| **Pricing Model** | [Model] | ... | ... | ... | ... | ... |
| **Entry Price** | [$X/mo or N/A] | ... | ... | ... | ... | ... |
| **Key Differentiator** | [1-liner] | ... | ... | ... | ... | ... |
| **Primary Weakness vs [Subject]** | N/A | [Weakness] | [Weakness] | [Weakness] | [Weakness] | [Weakness] |
| **Funding Stage** | [Stage/Amount] | ... | ... | ... | ... | ... |
| **Est. Company Size** | [Employees] | ... | ... | ... | ... | ... |

---

## Market Gaps & Opportunities

### Underserved Customer Segments
- **[Gap 1]:** [Description of customer segment or use case competitors miss] [Source N](#Sources)
- **[Gap 2]:** [Description] [Source N](#Sources)

### Feature/Capability Gaps
- **[Gap 1]:** [Functionality that no competitor provides well] [Source N](#Sources)
- **[Gap 2]:** [Description] [Source N](#Sources)

### Positioning/Business Model Gaps
- **[Gap 1]:** [Market position or business model no one claims] [Source N](#Sources)
- **[Gap 2]:** [Description] [Source N](#Sources)

### Strategic Implications
[1-2 sentences on how these gaps create opportunity for the subject company or reveal market evolution trends] [Source N](#Sources)

---

## Competitor Deep Dives

### [Competitor 1 Name]

**Overview:** [1-2 sentences on what they do and who they serve] [Source N](#Sources)

**Market Positioning:** [How they position themselves, key messaging themes] [Source N](#Sources)

**Pricing & Business Model:** [Pricing structure, tiers, model] [Source N](#Sources)

**Key Products/Features:** [Core offerings, standout capabilities] [Source N](#Sources)

**Funding & Scale:** [Funding history, company size indicators] [Source N](#Sources)

**Competitive Threat Level:** [High/Medium/Low] — [1 sentence justification]

---

[Repeat for Competitors 2-5]

---

## SWOT Analysis: [Subject Company]

### Strengths
- [Strength 1 with supporting evidence] [Source N](#Sources)
- [Strength 2 with supporting evidence] [Source N](#Sources)
- [Strength 3 with supporting evidence] [Source N](#Sources)

### Weaknesses
- [Weakness 1 based on competitive gaps] [Source N](#Sources)
- [Weakness 2 based on competitive gaps] [Source N](#Sources)
- [Weakness 3 based on competitive gaps] [Source N](#Sources)

### Opportunities
- [Opportunity 1 based on market/competitor analysis] [Source N](#Sources)
- [Opportunity 2 based on market/competitor analysis] [Source N](#Sources)
- [Opportunity 3 based on market/competitor analysis] [Source N](#Sources)

### Competitive Moats & Defensibility

Identify what makes the subject company's competitive advantages sustainable and difficult to replicate:

- **[Moat Type 1]:** [Description of the moat] — [Why it's defensible: time, cost, network effects, etc.] [Source N](#Sources)
- **[Moat Type 2]:** [Description] — [Why defensible] [Source N](#Sources)

Common moat types: network effects, data moats, brand moats, regulatory moats, cost advantages, integration depth, specialization/focus, cultural/geographic expertise, switching costs.

---

## Competitive Threats & Mitigation

### Near-Term Threats (0-12 months)

#### [Threat 1 Title]
- **Description:** [What could happen]
- **Likelihood:** [High/Medium/Low] — [Brief justification]
- **Impact:** [High/Medium/Low] — [Potential damage if occurs]
- **Mitigation:** [Specific actions to reduce threat] [Source N](#Sources)

#### [Threat 2 Title]
- **Description:** [What could happen]
- **Likelihood:** [High/Medium/Low] — [Brief justification]
- **Impact:** [High/Medium/Low] — [Potential damage if occurs]
- **Mitigation:** [Specific actions to reduce threat] [Source N](#Sources)

### Medium to Long-Term Threats (12+ months)

#### [Threat 3 Title]
- **Description:** [What could happen]
- **Likelihood:** [High/Medium/Low] — [Brief justification]
- **Impact:** [High/Medium/Low] — [Potential damage if occurs]
- **Mitigation:** [Specific actions to reduce threat] [Source N](#Sources)

*Note: Timeframes and likelihood estimates are flexible. Adapt based on industry velocity and market dynamics.*

---

## Strategic Recommendations

Based on this analysis, consider:

1. **[Recommendation 1]:** [Actionable recommendation with rationale tied to findings] [Source N](#Sources)
2. **[Recommendation 2]:** [Actionable recommendation with rationale tied to findings] [Source N](#Sources)
3. **[Recommendation 3]:** [Actionable recommendation with rationale tied to findings] [Source N](#Sources)

---

## Sources

[1] [Source Title] — [URL] — Accessed [Date]
[2] [Source Title] — [URL] — Accessed [Date]
[3] ...
```

## Citation Requirements

**Inline citations are mandatory.** Every factual claim must include `[Source N](#Sources)` reference.

- Number sources sequentially as encountered
- Include the exact URL in the Sources section
- If information comes from multiple sources, cite all: `[Source 1, 3](#Sources)`
- For claims that cannot be verified, explicitly state: "Unable to verify from public sources"
- Prefer primary sources (company websites, press releases) over secondary (news articles, blogs)

## Quality Checklist

Before finalizing report, verify:

- [ ] Target Customer Profile completed with firmographics, pain points, and behavioral patterns
- [ ] All 5 competitors researched across all 4 dimensions
- [ ] Every factual claim has inline citation
- [ ] Competitive matrix is complete with no empty cells (use "N/A" or "Not disclosed" if needed)
- [ ] Market Gaps section identifies at least 3 specific gaps with evidence
- [ ] SWOT items are specific and evidence-based, not generic
- [ ] Competitive Moats explain why advantages are defensible, not just listing strengths
- [ ] Threat analysis includes likelihood/impact ratings and mitigation strategies for each threat
- [ ] Recommendations are actionable and tied to specific findings
- [ ] Sources section includes all referenced URLs

## Error Handling

**If competitor website is inaccessible:** Note in report, use available search results and news coverage instead.

**If pricing not public:** State "Pricing not publicly disclosed" and note any indirect indicators (e.g., "enterprise sales model suggested by 'Contact Us' pricing page").

**If funding data unavailable:** Search for alternative signals: LinkedIn employee count, office locations, news mentions of growth.

**If fewer than 5 clear competitors exist:** Include available competitors and note the market context (e.g., "Emerging market with limited direct competitors").
