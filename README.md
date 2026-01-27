# Skills.sh Crawler

A crawler script to fetch skill data from [skills.sh](https://skills.sh), automatically executed daily via GitHub Actions.

## Data Sources

Fetches data from three leaderboards:

- **All Time** (`/`) - Total installs ranking
- **Trending** (`/trending`) - Recent growth ranking
- **Hot** (`/hot`) - Daily installs ranking

## Output Files

The crawler generates two files in the `data/` directory:

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

### `data/feed.json`

Simplified feed format (top 50 from each leaderboard):

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

## Usage

### Local Development

```bash
# Install dependencies
npm install

# Run crawler
npm run crawl
```

### GitHub Actions

After pushing to GitHub, the crawler will:

1. Run automatically daily at UTC 0:00 (8:00 AM Beijing Time)
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
