---
name: tool-grok-search
description: Use the grok_search tool to search X/web/news via xAI Grok Live Search (paid) and return an answer plus citations.
---

# grok_search (xAI Grok Live Search)

## When to use

- Real-time/current-event lookup where you need **fresh sources** (X + web + news) and citations.
- Social sentiment / “what are people saying on X” for a market or entity.

## Don’t use

- When free sources suffice (try `gdelt_news` first for background headlines).
- When you don’t need citations and want zero cost.

## Cost + keys

- Paid. Cost scales mainly with `maxResults` (`~$0.025/source` per `src/agents/grok.ts`).
- Requires `XAI_API_KEY` or `GROK_API_KEY` in env.

## Parameters

- `query` (string, required): Be specific. Include the entity + timeframe + what you want extracted.
- `sources` (array of `"web" | "x" | "news"`, optional): Restrict which channels are searched.
- `maxResults` (int, optional, 1–50): Higher = more sources/cost; default is 20.

## Examples

**Tool call (agent / MCP style):**
```json
{ "name": "grok_search", "params": { "query": "Polymarket Venezuela election market latest developments", "sources": ["news","web"], "maxResults": 12 } }
```

**HTTP:**
```bash
curl -sS -X POST http://127.0.0.1:7777/api/tools/execute \
  -H 'Content-Type: application/json' \
  -d '{"name":"grok_search","params":{"query":"what changed in CPI print today","sources":["news"],"maxResults":10}}'
```

## Output

- Returns: `{ content: string, citations: string[], sourcesUsed: number, model: string }`
- Rendered:
  - `Answer` (text)
  - `Citations` (table)
  - `Meta` (text: model + sourcesUsed)

## Notes / extensions

- The underlying Grok client supports richer filters (date range, domain allow/deny, X handle allow/deny, engagement thresholds), but the current `grok_search` tool only exposes `query/sources/maxResults`. If you need those filters, extend `src/tools/grok-search.ts` to pass them through.

