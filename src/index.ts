/**
 * Skills.sh Crawler Script
 * Fetches skill data from skills.sh and outputs as JSON format
 */

import { writeFileSync, mkdirSync, existsSync } from 'fs';
import { join } from 'path';

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
  allTime: Skill[];
  trending: Skill[];
  hot: HotSkill[];
}

// Request headers configuration
const headers: HeadersInit = {
  'accept': '*/*',
  'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
  'cache-control': 'no-cache',
  'pragma': 'no-cache',
  'rsc': '1',
  'next-url': '/',
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
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
  
  // Generate simplified feed format
  const feedPath = join(outputDir, 'feed.json');
  const feed = {
    title: 'Skills.sh Feed',
    description: 'Latest skill data from skills.sh',
    link: 'https://skills.sh',
    updatedAt: data.updatedAt,
    topAllTime: allTime.slice(0, 50).map(skill => ({
      id: `${skill.source}/${skill.skillId}`,
      title: skill.name,
      source: skill.source,
      installs: skill.installs,
      link: `https://skills.sh/i/${skill.source}`,
    })),
    topTrending: trending.slice(0, 50).map(skill => ({
      id: `${skill.source}/${skill.skillId}`,
      title: skill.name,
      source: skill.source,
      installs: skill.installs,
      link: `https://skills.sh/i/${skill.source}`,
    })),
    topHot: hot.slice(0, 50).map(skill => ({
      id: `${skill.source}/${skill.skillId}`,
      title: skill.name,
      source: skill.source,
      installs: skill.installs,
      link: `https://skills.sh/i/${skill.source}`,
    })),
  };
  writeFileSync(feedPath, JSON.stringify(feed, null, 2));
  console.log(`Feed saved to: ${feedPath}`);
}

main().catch(console.error);
