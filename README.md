# Skills.sh Crawler

A crawler script to fetch skill data from [skills.sh](https://skills.sh), automatically executed daily via GitHub Actions.

## Data Sources

Fetches data from three leaderboards:

- **All Time** (`/`) - Total installs ranking
- **Trending** (`/trending`) - Recent growth ranking
- **Hot** (`/hot`) - Daily installs ranking

Current provider:

- **skills.sh** (all data currently comes from this provider; more providers will be added later)

## Output Files

The crawler generates files in the `data/` directory:

### `data/skills.json`

Complete skill data containing all three leaderboards:

```json
{
  "updatedAt": "2024-01-27T00:00:00.000Z",
  "allTime": [...],
  "trending": [...],
  "hot": [...]
}
```

### `data/skills_index.json`

Website-friendly index for *all* skills (built from `data/skills.json`):

- Includes `description` (when a cached `SKILL.md` exists under `data/skills-md/`)
- Includes `skillMdPath` so your website can fetch and render the full markdown

### `data/feed.json`

Simplified feed format (top 50 from each leaderboard).

It also tries to enrich each item with a `description` by fetching the corresponding GitHub `SKILL.md` (cached under `data/skills-md/`):

```json
{
  "title": "Skills.sh Feed",
  "description": "Latest skill data from skills.sh",
  "link": "https://skills.sh",
  "updatedAt": "2024-01-27T00:00:00.000Z",
  "topAllTime": [...],
  "topTrending": [...],
  "topHot": [...]
}
```

### `data/skills-md/`

Cached `SKILL.md` files fetched from GitHub, using common skill folder locations such as:

- `skills/<skillId>/SKILL.md` (most common)
- `.claude/skills/<skillId>/SKILL.md`
- `.cursor/skills/<skillId>/SKILL.md`
- `.codex/skills/<skillId>/SKILL.md`
- `plugins/<plugin-name>/skills/<skillId>/SKILL.md` (common in plugin-based repos, e.g. Expo)

By default, the crawler only fetches `SKILL.md` for skills included in the top lists (to keep the daily job fast).

If you really want to sync *all* skills from `data/skills.json`, you can run:

```bash
SYNC_ALL_SKILL_MDS=1 npm run crawl
```

### `data/feed.xml`

RSS 2.0 feed (XML). This is meant for RSS readers / subscriptions.

- It is generated from the current crawl + the previous `data/feed.json`
- It only publishes meaningful changes (new entries / rank jumps) to avoid spamming

## Usage

### Local Development

```bash
# Install dependencies
npm install

# Run crawler
npm run crawl
```

Tip: if you want more complete GitHub `SKILL.md` coverage (including plugin-style paths like `plugins/*/skills/...`),
set `GITHUB_TOKEN` to avoid GitHub API rate limits:

```bash
export GITHUB_TOKEN=ghp_xxx
npm run crawl
```

### GitHub Actions

After pushing to GitHub, the crawler will:

1. Run automatically daily at UTC 0:00
2. Support manual triggering (click "Run workflow" in Actions tab)
3. Run automatically on push to main branch

## Using in Your Website

You can fetch data directly via GitHub Raw URL:

```
https://raw.githubusercontent.com/<username>/<repo>/main/data/skills.json
```

Or use jsDelivr CDN (faster):

```
https://cdn.jsdelivr.net/gh/<username>/<repo>@main/data/skills.json
```

### RSS Subscription (Recommended)

Subscribe to the RSS feed:

```
https://raw.githubusercontent.com/<username>/<repo>/main/data/feed.xml
```

Or via jsDelivr CDN:

```
https://cdn.jsdelivr.net/gh/<username>/<repo>@main/data/feed.xml
```

### Example Code

```typescript
// In Next.js
const SKILLS_DATA_URL = 'https://cdn.jsdelivr.net/gh/your-username/skills-crawler@main/data/skills.json';

export async function getSkillsData() {
  const res = await fetch(SKILLS_DATA_URL, {
    next: { revalidate: 3600 } // Revalidate every hour
  });
  return res.json();
}
```

## Notes

- Data is updated daily
- Please comply with skills.sh terms of service
- For personal learning and research purposes only
