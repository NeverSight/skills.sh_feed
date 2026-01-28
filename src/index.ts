/**
 * Skills.sh Crawler Script
 * Fetches skill data from skills.sh and outputs as JSON format
 */

import { writeFileSync, mkdirSync, existsSync, readFileSync } from 'fs';
import { join } from 'path';
import { Feed } from 'feed';
import matter from 'gray-matter';

// Type definitions
interface Skill {
  source: string;
  skillId: string;
  name: string;
  installs: number;
}

interface HotSkill extends Skill {
  installsYesterday?: number;
  change?: number;
}

interface SkillsData {
  updatedAt: string;
  providerId: string;
  allTime: Skill[];
  trending: Skill[];
  hot: HotSkill[];
}

interface ProviderInfo {
  id: string;
  name: string;
  link: string;
}

interface SkillIndexItem {
  id: string; // <source>/<skillId>
  providerId: string;
  source: string; // GitHub repo (owner/repo)
  skillId: string;
  title: string;
  link: string; // skills.sh page
  installsAllTime: number;
  installsTrending?: number;
  installsHot?: number;
  description?: string;
  skillMdPath?: string; // repo-relative path to cached SKILL.md
}

interface FeedItem {
  id: string;
  title: string;
  source: string;
  installs: number;
  link: string;
  description?: string;
  providerId: string;
}

interface FeedJson {
  title: string;
  description: string;
  link: string;
  updatedAt: string;
  providers: ProviderInfo[];
  topAllTime: FeedItem[];
  topTrending: FeedItem[];
  topHot: FeedItem[];
}

function skillsShSkillUrl(source: string, skillId: string) {
  // Example: https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices
  return `https://skills.sh/${source}/${skillId}`;
}

function githubRawUrl(source: string, branch: string, path: string) {
  return `https://raw.githubusercontent.com/${source}/${branch}/${path}`;
}

function githubApiUrl(source: string, path: string, branch: string) {
  if (!path) return `https://api.github.com/repos/${source}/contents?ref=${branch}`;
  return `https://api.github.com/repos/${source}/contents/${path}?ref=${branch}`;
}

function localSkillMdPath(source: string, skillId: string) {
  // Cache fetched SKILL.md files to avoid re-downloading every run.
  // Layout:
  // data/skills-md/<owner>/<repo>/<skillId>/SKILL.md
  return join(process.cwd(), 'data', 'skills-md', source, skillId, 'SKILL.md');
}

function repoRelativeSkillMdPath(source: string, skillId: string) {
  return `data/skills-md/${source}/${skillId}/SKILL.md`;
}

function extractDescriptionFromSkillMd(md: string): string | undefined {
  try {
    const parsed = matter(md);
    const desc = (parsed?.data as Record<string, unknown> | undefined)?.description;
    if (typeof desc === 'string' && desc.trim()) return desc.trim();
  } catch {
    // ignore
  }

  // Fallback: first non-empty paragraph line that isn't a heading/list/code fence.
  const lines = md.split('\n').map(l => l.trim());
  for (const line of lines) {
    if (!line) continue;
    if (line.startsWith('#')) continue;
    if (line.startsWith('```')) continue;
    if (line.startsWith('- ')) continue;
    if (line.startsWith('* ')) continue;
    if (line.startsWith('>')) continue;
    if (line === '---') continue;
    return line;
  }
  return undefined;
}

async function fetchText(url: string): Promise<string | null> {
  try {
    const res = await fetch(url, {
      headers: {
        'user-agent': USER_AGENT,
        'accept': 'text/plain,*/*',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
      },
    });
    if (res.status === 404) return null;
    if (!res.ok) return null;
    return await res.text();
  } catch {
    return null;
  }
}

async function fetchGithubJson<T>(url: string): Promise<T | null> {
  try {
    const headers: Record<string, string> = {
      'accept': 'application/vnd.github+json',
      'user-agent': USER_AGENT,
    };
    if (process.env.GITHUB_TOKEN) {
      headers['authorization'] = `Bearer ${process.env.GITHUB_TOKEN}`;
    }
    const res = await fetch(url, { headers });
    if (res.status === 404) return null;
    if (!res.ok) return null;
    return (await res.json()) as T;
  } catch {
    return null;
  }
}

async function fetchGithubRawFile(source: string, branch: string, path: string): Promise<string | null> {
  try {
    // Prefer raw.githubusercontent.com first to avoid GitHub API rate limits
    // when syncing a large number of skills.
    const rawUrl = githubRawUrl(source, branch, path);
    const raw = await fetchText(rawUrl);
    if (raw) return raw;

    const headers: Record<string, string> = {
      // Return the file as raw bytes/text from the contents API (avoids raw.githubusercontent.com).
      'accept': 'application/vnd.github.raw',
      'user-agent': USER_AGENT,
    };
    if (process.env.GITHUB_TOKEN) {
      headers['authorization'] = `Bearer ${process.env.GITHUB_TOKEN}`;
    }
    const url = githubApiUrl(source, path, branch);
    const res = await fetch(url, { headers });
    if (res.status === 404) return null;
    if (!res.ok) {
      // If we're rate-limited (common without a token), try raw.githubusercontent.com as a fallback.
      if (res.status === 403 && !process.env.GITHUB_TOKEN) {
        // Already tried raw first above, but keep this for clarity.
        const fallback = await fetchText(rawUrl);
        if (fallback) return fallback;
      }
      return null;
    }
    return await res.text();
  } catch {
    return null;
  }
}

type GithubContentEntry = {
  type: 'file' | 'dir';
  name: string;
  path: string;
};

const repoSkillIndexCache = new Map<string, Map<string, { branch: string; path: string }>>();

async function getRepoSkillIndex(source: string) {
  const cached = repoSkillIndexCache.get(source);
  if (cached) return cached;

  const branches = ['main', 'master'];
  const baseDirs = [
    // Repo root (some repos put skill folders directly at root)
    '',
    'skills',
    '.claude/skills',
    '.cursor/skills',
    '.codex/skills',
    '.agents/skills',
    '.agent/skills',
    '.github/skills',
    '.gemini/skills',
    '.goose/skills',
    '.opencode/skills',
    '.roo/skills',
    '.windsurf/skills',
    '.kilocode/skills',
    '.factory/skills',
  ];

  const index = new Map<string, { branch: string; path: string }>();

  for (const branch of branches) {
    const dynamicBaseDirs = [...baseDirs];

    // Also scan plugin-style layouts, e.g.
    // plugins/<plugin-name>/skills/<skillId>/SKILL.md
    const pluginsListing = await fetchGithubJson<GithubContentEntry[] | GithubContentEntry>(
      githubApiUrl(source, 'plugins', branch),
    );
    if (pluginsListing) {
      const entries = Array.isArray(pluginsListing) ? pluginsListing : [pluginsListing];
      for (const entry of entries) {
        if (entry.type === 'dir') {
          dynamicBaseDirs.push(`plugins/${entry.name}/skills`);
        }
      }
    }

    // Also scan monorepo layouts, e.g. <product>/<skillFolder>/SKILL.md
    // We do this by adding top-level dirs as potential baseDirs.
    const rootListing = await fetchGithubJson<GithubContentEntry[] | GithubContentEntry>(
      githubApiUrl(source, '', branch),
    );
    if (rootListing) {
      const entries = Array.isArray(rootListing) ? rootListing : [rootListing];
      const topDirs = entries
        .filter(e => e.type === 'dir' && e.name && !e.name.startsWith('.'))
        .slice(0, 40)
        .map(e => e.name);
      dynamicBaseDirs.push(...topDirs);
    }

    for (const baseDir of dynamicBaseDirs) {
      const url = githubApiUrl(source, baseDir, branch);
      const listing = await fetchGithubJson<GithubContentEntry[] | GithubContentEntry>(url);
      if (!listing) continue;

      const entries = Array.isArray(listing) ? listing : [listing];

      // Most repos structure: <baseDir>/<skillFolder>/SKILL.md
      for (const entry of entries) {
        if (entry.type !== 'dir') continue;
        const candidatePaths = [
          baseDir ? `${baseDir}/${entry.name}/SKILL.md` : `${entry.name}/SKILL.md`,
          baseDir ? `${baseDir}/${entry.name}/skill.md` : `${entry.name}/skill.md`,
        ];

        for (const p of candidatePaths) {
          const raw = await fetchGithubRawFile(source, branch, p);
          if (!raw) continue;

          try {
            const parsed = matter(raw);
            const name = (parsed?.data as Record<string, unknown> | undefined)?.name;
            if (typeof name === 'string' && name.trim()) {
              index.set(name.trim(), { branch, path: p });
            }
          } catch {
            // ignore
          }
        }
      }
    }
  }

  repoSkillIndexCache.set(source, index);
  return index;
}

async function fetchSkillMdFromGithub(source: string, skillId: string) {
  const branches = ['main', 'master'];
  const baseDirs = [
    // Repo root (some repos put skill folders directly at root)
    '',
    // Most common
    'skills',
    // Common tool-specific locations
    '.claude/skills',
    '.cursor/skills',
    '.codex/skills',
    '.agents/skills',
    '.agent/skills',
    '.github/skills',
    '.gemini/skills',
    '.goose/skills',
    '.opencode/skills',
    '.roo/skills',
    '.windsurf/skills',
    '.kilocode/skills',
    '.factory/skills',
  ];
  const filenames = ['SKILL.md', 'skill.md'];

  // 1) Fast path: direct guess (most repos use <baseDir>/<skillId>/SKILL.md)
  for (const branch of branches) {
    for (const baseDir of baseDirs) {
      for (const filename of filenames) {
        const relPath = baseDir ? `${baseDir}/${skillId}/${filename}` : `${skillId}/${filename}`;
        const url = githubRawUrl(source, branch, relPath);
        const text = await fetchGithubRawFile(source, branch, relPath);
        if (text) return { url, text };
      }
    }
  }

  // 2) Fallback: discover SKILL.md files and match by frontmatter name
  const index = await getRepoSkillIndex(source);
  const resolved = index.get(skillId);
  if (resolved) {
    const url = githubRawUrl(source, resolved.branch, resolved.path);
    const text = await fetchGithubRawFile(source, resolved.branch, resolved.path);
    if (text) return { url, text };
  }

  return null;
}

async function ensureSkillMdCached(source: string, skillId: string) {
  const cachedPath = localSkillMdPath(source, skillId);
  if (existsSync(cachedPath)) return cachedPath;

  const fetched = await fetchSkillMdFromGithub(source, skillId);
  if (fetched?.text) {
    mkdirSync(join(process.cwd(), 'data', 'skills-md', source, skillId), { recursive: true });
    writeFileSync(cachedPath, fetched.text);
    return cachedPath;
  }

  return null;
}

type SyncProgress = {
  updatedAt: string;
  attempted: number;
  fetched: number;
  missing: number;
};

function progressPath() {
  return join(process.cwd(), 'data', 'skills-md', '_sync_progress.json');
}

function readProgress(): SyncProgress | null {
  return readJsonFile<SyncProgress>(progressPath());
}

function writeProgress(progress: SyncProgress) {
  mkdirSync(join(process.cwd(), 'data', 'skills-md'), { recursive: true });
  writeFileSync(progressPath(), JSON.stringify(progress, null, 2));
}

async function buildSkillsIndex(data: SkillsData) {
  const providerId = data.providerId;

  // allTime contains the full unique set and the best "canonical" installs count.
  const trendingInstallsById = new Map<string, number>();
  for (const s of data.trending) {
    trendingInstallsById.set(`${s.source}/${s.skillId}`, s.installs);
  }

  const hotInstallsById = new Map<string, number>();
  for (const s of data.hot) {
    hotInstallsById.set(`${s.source}/${s.skillId}`, s.installs);
  }

  const items: SkillIndexItem[] = new Array(data.allTime.length);

  await mapWithConcurrency(data.allTime, 24, async (s, i) => {
    const id = `${s.source}/${s.skillId}`;
    const mdAbs = localSkillMdPath(s.source, s.skillId);
    let description: string | undefined;
    let skillMdPath: string | undefined;

    if (existsSync(mdAbs)) {
      try {
        const md = readFileSync(mdAbs, 'utf-8');
        description = extractDescriptionFromSkillMd(md);
        skillMdPath = repoRelativeSkillMdPath(s.source, s.skillId);
      } catch {
        // ignore read errors
      }
    }

    items[i] = {
      id,
      providerId,
      source: s.source,
      skillId: s.skillId,
      title: s.name,
      link: skillsShSkillUrl(s.source, s.skillId),
      installsAllTime: s.installs,
      installsTrending: trendingInstallsById.get(id),
      installsHot: hotInstallsById.get(id),
      description,
      skillMdPath,
    };

    return null;
  });

  const output = {
    updatedAt: data.updatedAt,
    providerId,
    count: items.length,
    items,
  };

  const outPath = join(process.cwd(), 'data', 'skills_index.json');
  writeFileSync(outPath, JSON.stringify(output, null, 2));
  console.log(`Skills index saved to: ${outPath}`);
}

async function syncAllSkillMds(data: SkillsData) {
  const onlyMissing = process.env.SYNC_ALL_ONLY_MISSING !== '0';
  const maxToFetch = process.env.SYNC_ALL_MAX ? Number(process.env.SYNC_ALL_MAX) : Number.POSITIVE_INFINITY;
  const timeBudgetMinutes = process.env.SYNC_ALL_TIME_BUDGET_MINUTES
    ? Number(process.env.SYNC_ALL_TIME_BUDGET_MINUTES)
    : Number.POSITIVE_INFINITY;
  const startMs = Date.now();

  const unique = new Map<string, { source: string; skillId: string }>();
  const all = [...data.allTime, ...data.trending, ...data.hot];
  for (const s of all) unique.set(`${s.source}/${s.skillId}`, { source: s.source, skillId: s.skillId });

  const list = Array.from(unique.values()).sort((a, b) => {
    const ka = `${a.source}/${a.skillId}`;
    const kb = `${b.source}/${b.skillId}`;
    return ka.localeCompare(kb);
  });

  console.log(
    `\nSYNC_ALL_SKILL_MDS=1: syncing SKILL.md for ${list.length} skills (onlyMissing=${onlyMissing}, max=${Number.isFinite(maxToFetch) ? maxToFetch : '∞'}, timeBudgetMinutes=${Number.isFinite(timeBudgetMinutes) ? timeBudgetMinutes : '∞'})...`,
  );

  const prev = readProgress();
  const progress: SyncProgress = prev ?? { updatedAt: new Date().toISOString(), attempted: 0, fetched: 0, missing: 0 };

  let fetchedThisRun = 0;

  for (const { source, skillId } of list) {
    if (fetchedThisRun >= maxToFetch) break;
    if (Number.isFinite(timeBudgetMinutes)) {
      const elapsedMinutes = (Date.now() - startMs) / 1000 / 60;
      if (elapsedMinutes >= timeBudgetMinutes) break;
    }

    const targetPath = localSkillMdPath(source, skillId);
    if (onlyMissing && existsSync(targetPath)) continue;

    progress.attempted += 1;
    const cached = await ensureSkillMdCached(source, skillId);
    if (cached) {
      progress.fetched += 1;
      fetchedThisRun += 1;
    } else {
      progress.missing += 1;
    }

    // Persist progress periodically so long runs are resumable.
    if (progress.attempted % 50 === 0) {
      progress.updatedAt = new Date().toISOString();
      writeProgress(progress);
    }
  }

  progress.updatedAt = new Date().toISOString();
  writeProgress(progress);
  console.log(
    `SYNC_ALL summary: attempted=${progress.attempted}, fetched=${progress.fetched}, missing=${progress.missing} (this run fetched=${fetchedThisRun})`,
  );
}

async function mapWithConcurrency<T, R>(
  items: T[],
  concurrency: number,
  fn: (item: T, index: number) => Promise<R>,
): Promise<R[]> {
  const results = new Array<R>(items.length);
  let nextIndex = 0;

  const workers = Array.from({ length: Math.max(1, concurrency) }, async () => {
    while (true) {
      const i = nextIndex++;
      if (i >= items.length) break;
      results[i] = await fn(items[i], i);
    }
  });

  await Promise.all(workers);
  return results;
}

async function hydrateFeedDescriptions(feed: FeedJson) {
  const allItems = [...feed.topAllTime, ...feed.topTrending, ...feed.topHot];
  const itemsById = new Map<string, FeedItem[]>();
  for (const it of allItems) {
    const existing = itemsById.get(it.id);
    if (existing) existing.push(it);
    else itemsById.set(it.id, [it]);
  }
  const unique = Array.from(itemsById.entries());

  console.log(`\nFetching SKILL.md for ${unique.length} unique skills (top lists only)...`);

  await mapWithConcurrency(unique, 8, async ([id, items]) => {
    const first = items[0];
    const skillId = id.split('/').pop() || id;
    const source = first.source;

    const cachedPath = await ensureSkillMdCached(source, skillId);
    const md = cachedPath ? readFileSync(cachedPath, 'utf-8') : null;

    if (md) {
      const desc = extractDescriptionFromSkillMd(md);
      if (desc) {
        for (const it of items) it.description = desc;
      }
    }

    return null;
  });
}

// Request headers configuration
const USER_AGENT =
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36';

const headers: Record<string, string> = {
  'accept': '*/*',
  'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
  'cache-control': 'no-cache',
  'pragma': 'no-cache',
  'rsc': '1',
  'next-url': '/',
  'user-agent': USER_AGENT,
};

/**
 * Extract skills array from text for a specified field
 */
function extractSkillsArray(text: string, fieldName: string): Skill[] {
  const skills: Skill[] = [];
  
  // Find field start position
  const fieldPattern = `"${fieldName}":[`;
  const startIndex = text.indexOf(fieldPattern);
  
  if (startIndex === -1) {
    console.log(`Field not found: ${fieldName}`);
    return skills;
  }
  
  // Find array start position
  const arrayStart = startIndex + fieldPattern.length - 1;
  
  // Use bracket matching to find array end position
  let depth = 0;
  let arrayEnd = arrayStart;
  
  for (let i = arrayStart; i < text.length; i++) {
    if (text[i] === '[') {
      depth++;
    } else if (text[i] === ']') {
      depth--;
      if (depth === 0) {
        arrayEnd = i + 1;
        break;
      }
    }
  }
  
  try {
    const arrayStr = text.slice(arrayStart, arrayEnd);
    const parsed = JSON.parse(arrayStr);
    if (Array.isArray(parsed)) {
      return parsed;
    }
  } catch (e) {
    console.error(`Failed to parse ${fieldName}:`, e);
  }
  
  return skills;
}

/**
 * Fetch data from specified endpoint
 */
async function fetchEndpoint(endpoint: string): Promise<string> {
  const url = `https://skills.sh${endpoint}?_rsc=${Date.now()}`;
  console.log(`Fetching: ${url}`);
  
  try {
    const response = await fetch(url, {
      headers: {
        ...headers,
        'referer': 'https://skills.sh/',
      },
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.text();
  } catch (error) {
    console.error(`Failed to fetch ${endpoint}:`, error);
    return '';
  }
}

function readJsonFile<T>(path: string): T | null {
  try {
    const raw = readFileSync(path, 'utf-8');
    return JSON.parse(raw) as T;
  } catch {
    return null;
  }
}

type LeaderboardKey = 'topAllTime' | 'topTrending' | 'topHot';

function buildRssItemsFromDiff(previous: FeedJson | null, next: FeedJson) {
  const updatedAt = new Date(next.updatedAt);

  const boards: Array<{ key: LeaderboardKey; label: string }> = [
    { key: 'topAllTime', label: 'All Time' },
    { key: 'topTrending', label: 'Trending' },
    { key: 'topHot', label: 'Hot' },
  ];

  const items: Array<{
    title: string;
    id: string;
    link: string;
    date: Date;
    description: string;
  }> = [];

  for (const board of boards) {
    const nextList = next[board.key] ?? [];
    const prevList = previous?.[board.key] ?? [];

    const prevRankById = new Map<string, { rank: number; installs: number }>();
    prevList.forEach((it, idx) => prevRankById.set(it.id, { rank: idx + 1, installs: it.installs }));

    nextList.forEach((it, idx) => {
      const rank = idx + 1;
      const prev = prevRankById.get(it.id);

      // Use skills.sh skill page; fall back to GitHub repo URL.
      const githubRepoUrl = `https://github.com/${it.source}`;
      const link = it.link || githubRepoUrl;

      if (!prev) {
        items.push({
          title: `[${board.label}] New entry (#${rank}): ${it.title}`,
          id: `${next.updatedAt}:${board.key}:new:${it.id}`,
          link,
          date: updatedAt,
          description: [
            `New entry in ${board.label} leaderboard.`,
            `Rank: #${rank}`,
            `Installs: ${it.installs}`,
            `Source: ${it.source}`,
            it.description ? `Description: ${it.description}` : null,
          ].filter(Boolean).join('\n'),
        });
        return;
      }

      if (prev.rank !== rank) {
        const delta = prev.rank - rank; // positive = up
        const absDelta = Math.abs(delta);

        // Reduce noise: only publish meaningful changes.
        const shouldPublish =
          absDelta >= 10 ||
          (rank <= 20 && absDelta >= 3) ||
          (rank <= 10 && absDelta >= 1);

        if (!shouldPublish) return;

        const direction = delta > 0 ? 'up' : 'down';
        items.push({
          title: `[${board.label}] Rank ${direction} (${prev.rank} → ${rank}): ${it.title}`,
          id: `${next.updatedAt}:${board.key}:rank:${it.id}`,
          link,
          date: updatedAt,
          description: [
            `${board.label} leaderboard rank change.`,
            `Previous rank: #${prev.rank}`,
            `Current rank: #${rank}`,
            `Delta: ${delta > 0 ? '+' : ''}${delta}`,
            `Installs: ${it.installs} (prev ${prev.installs})`,
            `Source: ${it.source}`,
            it.description ? `Description: ${it.description}` : null,
          ].filter(Boolean).join('\n'),
        });
      }
    });
  }

  // New entries first, then rank changes; cap to avoid huge feeds.
  const sorted = items.sort((a, b) => {
    const aIsNew = a.id.includes(':new:') ? 0 : 1;
    const bIsNew = b.id.includes(':new:') ? 0 : 1;
    if (aIsNew !== bIsNew) return aIsNew - bIsNew;
    return a.title.localeCompare(b.title);
  });

  return sorted.slice(0, 50);
}

function buildDailySnapshotRssItem(feed: FeedJson, counts: { allTime: number; trending: number; hot: number }) {
  const updatedAt = new Date(feed.updatedAt);
  const topAllTime = feed.topAllTime?.[0];
  const topTrending = feed.topTrending?.[0];
  const topHot = feed.topHot?.[0];
  const providerNames = (feed.providers || []).map(p => p.name).join(', ') || 'unknown';

  const lines = [
    `Daily snapshot.`,
    `Providers: ${providerNames}`,
    `All Time skills: ${counts.allTime}`,
    `Trending skills: ${counts.trending}`,
    `Hot skills: ${counts.hot}`,
    '',
    topAllTime ? `Top All Time: ${topAllTime.title} (${topAllTime.installs})` : null,
    topTrending ? `Top Trending: ${topTrending.title} (${topTrending.installs})` : null,
    topHot ? `Top Hot: ${topHot.title} (${topHot.installs})` : null,
  ].filter(Boolean).join('\n');

  return {
    title: `[Daily] Skills.sh snapshot (${updatedAt.toISOString().slice(0, 10)})`,
    id: `${feed.updatedAt}:snapshot`,
    link: feed.link,
    date: updatedAt,
    description: lines,
  };
}

/**
 * Main function
 */
async function main() {
  console.log('Starting skills.sh data crawl...\n');
  
  // Fetch all three endpoints
  const [homeText, trendingText, hotText] = await Promise.all([
    fetchEndpoint('/'),
    fetchEndpoint('/trending'),
    fetchEndpoint('/hot'),
  ]);
  
  // Extract allTimeSkills from home page
  const allTime = extractSkillsArray(homeText, 'allTimeSkills');
  
  // Extract trendingSkills from trending page
  const trending = extractSkillsArray(trendingText, 'trendingSkills');
  
  // Extract trulyTrendingSkills from hot page (this is the actual field name for hot)
  const hot = extractSkillsArray(hotText, 'trulyTrendingSkills') as HotSkill[];
  
  console.log(`\nCrawl completed:`);
  console.log(`- All Time: ${allTime.length} skills`);
  console.log(`- Trending: ${trending.length} skills`);
  console.log(`- Hot: ${hot.length} skills`);
  
  // Show top 3 comparison
  console.log('\n=== Top 3 Comparison ===');
  console.log('All Time:', allTime.slice(0, 3).map(s => `${s.name}(${s.installs})`).join(', '));
  console.log('Trending:', trending.slice(0, 3).map(s => `${s.name}(${s.installs})`).join(', '));
  console.log('Hot:', hot.slice(0, 3).map(s => `${s.name}(${s.installs})`).join(', '));
  
  // Build output data
  const data: SkillsData = {
    updatedAt: new Date().toISOString(),
    providerId: 'skills.sh',
    allTime,
    trending,
    hot,
  };
  
  // Ensure output directory exists
  const outputDir = join(process.cwd(), 'data');
  if (!existsSync(outputDir)) {
    mkdirSync(outputDir, { recursive: true });
  }
  
  // Write JSON file
  const outputPath = join(outputDir, 'skills.json');
  writeFileSync(outputPath, JSON.stringify(data, null, 2));
  console.log(`\nData saved to: ${outputPath}`);

  if (process.env.SYNC_ALL_SKILL_MDS === '1') {
    await syncAllSkillMds(data);
  }

  if (process.env.GENERATE_SKILLS_INDEX !== '0') {
    await buildSkillsIndex(data);
  }
  
  // Generate simplified feed format
  const feedPath = join(outputDir, 'feed.json');
  const previousFeed = readJsonFile<FeedJson>(feedPath);
  const feed: FeedJson = {
    title: 'Skills.sh Feed',
    description: 'Latest skill data from skills.sh',
    link: 'https://skills.sh',
    updatedAt: data.updatedAt,
    providers: [
      {
        id: 'skills.sh',
        name: 'skills.sh',
        link: 'https://skills.sh',
      },
    ],
    topAllTime: allTime.slice(0, 50).map(skill => ({
      id: `${skill.source}/${skill.skillId}`,
      title: skill.name,
      source: skill.source,
      installs: skill.installs,
      link: skillsShSkillUrl(skill.source, skill.skillId),
      providerId: 'skills.sh',
    })),
    topTrending: trending.slice(0, 50).map(skill => ({
      id: `${skill.source}/${skill.skillId}`,
      title: skill.name,
      source: skill.source,
      installs: skill.installs,
      link: skillsShSkillUrl(skill.source, skill.skillId),
      providerId: 'skills.sh',
    })),
    topHot: hot.slice(0, 50).map(skill => ({
      id: `${skill.source}/${skill.skillId}`,
      title: skill.name,
      source: skill.source,
      installs: skill.installs,
      link: skillsShSkillUrl(skill.source, skill.skillId),
      providerId: 'skills.sh',
    })),
  };

  // Enrich with description fetched from GitHub SKILL.md (cached in data/skills-md/)
  await hydrateFeedDescriptions(feed);

  writeFileSync(feedPath, JSON.stringify(feed, null, 2));
  console.log(`Feed saved to: ${feedPath}`);

  // Generate RSS feed (XML) based on changes vs previous feed.json
  const rssItems = buildRssItemsFromDiff(previousFeed, feed);

  const rss = new Feed({
    title: feed.title,
    description: feed.description,
    id: feed.link,
    link: feed.link,
    language: 'en',
    updated: new Date(feed.updatedAt),
  });

  // Always publish a daily snapshot item so the RSS never looks "broken" (empty),
  // even when there are no meaningful rank changes.
  const snapshot = buildDailySnapshotRssItem(feed, {
    allTime: allTime.length,
    trending: trending.length,
    hot: hot.length,
  });
  rss.addItem(snapshot);

  for (const item of rssItems) {
    rss.addItem({
      title: item.title,
      id: item.id,
      link: item.link,
      date: item.date,
      description: item.description,
    });
  }

  const rssPath = join(outputDir, 'feed.xml');
  writeFileSync(rssPath, rss.rss2());
  console.log(`RSS saved to: ${rssPath}`);
}

main().catch(console.error);
