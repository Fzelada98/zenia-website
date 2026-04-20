/**
 * Build prioritized urls.json for Zenia indexing boost.
 * Reads sitemap.xml directly (single source of truth for this static site)
 * and re-orders entries so the GSC Indexing API (50/day budget) submits
 * the most valuable URLs first.
 *
 * Priority order:
 *   1. Homepage (/, /es/)
 *   2. Top-level indexes (/blog/, /privacy/, /es/cases/)
 *   3. Vertical landing pages (/es/crm-*.html — no -city suffix)
 *   4. Recent blog posts (newest first by filesystem mtime)
 *   5. City-specific programmatic landings (/es/crm-*-{city}.html)
 *   6. Everything else listed in sitemap
 */

const fs = require('fs');
const path = require('path');

const SITE = 'https://zeniapartners.com';
const ROOT = process.cwd();

function extractSitemapUrls() {
  if (!fs.existsSync('sitemap.xml')) return [];
  const xml = fs.readFileSync('sitemap.xml', 'utf-8');
  const matches = xml.match(/<loc>([^<]+)<\/loc>/g) || [];
  return matches.map(m => m.replace(/<\/?loc>/g, '').trim()).filter(Boolean);
}

function isHomepage(url) {
  return url === `${SITE}/` || url === `${SITE}/es/`;
}
function isIndexRoot(url) {
  return /\/(blog|privacy|cases|docs)\/?$/.test(url.replace(SITE, ''));
}
function isCityLanding(url) {
  // crm-{vertical}-{city}.html pattern (city = last segment before .html)
  return /\/crm-[a-z-]+-[a-z]+\.html$/.test(url) && /-(?:barcelona|madrid|valencia|sevilla|bilbao|malaga|zaragoza|las-palmas|palma|murcia|lima|bogota|cdmx|santiago|buenos-aires)\.html$/.test(url);
}
function isVerticalLanding(url) {
  return /\/crm-[a-z-]+\.html$/.test(url) && !isCityLanding(url);
}
function isBlogPost(url) {
  return /\/blog\/.+\.html$/.test(url);
}

function getBlogMtime(url) {
  const relPath = url.replace(SITE + '/', '');
  const filePath = path.join(ROOT, relPath);
  try {
    return fs.statSync(filePath).mtimeMs;
  } catch {
    return 0;
  }
}

const all = extractSitemapUrls();

const homepages = all.filter(isHomepage);
const indexRoots = all.filter(isIndexRoot);
const verticals = all.filter(isVerticalLanding);
const blogs = all.filter(isBlogPost).sort((a, b) => getBlogMtime(b) - getBlogMtime(a));
const cities = all.filter(isCityLanding);

const classified = new Set([...homepages, ...indexRoots, ...verticals, ...blogs, ...cities]);
const rest = all.filter(u => !classified.has(u));

const ordered = [...homepages, ...indexRoots, ...verticals, ...blogs, ...cities, ...rest];
const unique = [...new Set(ordered)];

fs.writeFileSync('urls.json', JSON.stringify(unique));
console.log(`Generated ${unique.length} URLs (priority: ${homepages.length} homepages, ${indexRoots.length} index roots, ${verticals.length} verticals, ${blogs.length} blogs, ${cities.length} cities, ${rest.length} other)`);

if (process.env.GITHUB_OUTPUT) {
  fs.appendFileSync(process.env.GITHUB_OUTPUT, `count=${unique.length}\n`);
}
