/**
 * Bulk indexing forcer.
 *
 * Reads the sitemap and submits every URL to:
 *   1. Google Indexing API (URL_UPDATED notification)
 *   2. IndexNow (Bing + Yandex + Naver) in one batch
 *
 * Also queries the URL Inspection API for a sample to surface the real
 * indexed/not-indexed status (more reliable than the sitemap "indexed"
 * count, which is well known to be delayed by weeks).
 *
 * Usage:
 *   node .github/scripts/bulk-indexing.js
 * or trigger via the bulk-indexing.yml workflow.
 */

const fs = require('fs');
const path = require('path');
const { google } = require('googleapis');

const SITEMAP_PATH = path.join(process.cwd(), 'sitemap.xml');
const SITE_HOST = 'zeniapartners.com';
const SITE_URL = process.env.GSC_SITE_URL || 'sc-domain:zeniapartners.com';
const INDEXNOW_KEY = process.env.INDEXNOW_KEY || '';
const SAMPLE_INSPECT = parseInt(process.env.INSPECT_SAMPLE || '15', 10);

function parseSitemapUrls(xml) {
  const matches = xml.matchAll(/<loc>([^<]+)<\/loc>/g);
  return [...matches].map(m => m[1].trim());
}

async function submitToGoogleIndexing(urls, indexing) {
  console.log(`\n=== Google Indexing API (${urls.length} URLs) ===`);
  let ok = 0, err = 0;
  for (const url of urls) {
    try {
      await indexing.urlNotifications.publish({
        requestBody: { url, type: 'URL_UPDATED' }
      });
      ok++;
      if (ok % 25 === 0) console.log(`  ...${ok}/${urls.length} submitted`);
    } catch (e) {
      err++;
      if (err <= 5) console.error(`  ERR ${url}: ${e.message}`);
    }
  }
  console.log(`  Done: ${ok} ok, ${err} errors`);
  return { ok, err };
}

async function submitToIndexNow(urls) {
  console.log(`\n=== IndexNow (${urls.length} URLs) ===`);
  if (!INDEXNOW_KEY) {
    console.log('  Skipped: INDEXNOW_KEY not set');
    return { ok: 0, err: 0 };
  }

  // IndexNow accepts up to 10,000 URLs per request
  const payload = {
    host: SITE_HOST,
    key: INDEXNOW_KEY,
    keyLocation: `https://${SITE_HOST}/${INDEXNOW_KEY}.txt`,
    urlList: urls
  };

  try {
    const res = await fetch('https://api.indexnow.org/indexnow', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json; charset=utf-8' },
      body: JSON.stringify(payload)
    });
    const status = res.status;
    console.log(`  HTTP ${status} (${status === 200 || status === 202 ? 'accepted' : 'check response'})`);
    return { ok: status === 200 || status === 202 ? urls.length : 0, err: status >= 400 ? urls.length : 0 };
  } catch (e) {
    console.error(`  ERR: ${e.message}`);
    return { ok: 0, err: urls.length };
  }
}

async function inspectSample(urls, webmasters) {
  console.log(`\n=== URL Inspection sample (${SAMPLE_INSPECT} URLs) ===`);
  // Mix of homepage, ES landing, blog post types so the sample is representative
  const sample = [];
  const buckets = {
    home: urls.filter(u => /^https:\/\/zeniapartners\.com\/$/.test(u) || /\/index\.html$/.test(u)).slice(0, 2),
    blog: urls.filter(u => /\/blog\//.test(u)).slice(0, Math.floor(SAMPLE_INSPECT * 0.5)),
    es: urls.filter(u => /\/es\//.test(u)).slice(0, Math.floor(SAMPLE_INSPECT * 0.4)),
    other: urls.filter(u => !/\/blog\//.test(u) && !/\/es\//.test(u) && !/\/$/.test(u)).slice(0, 2)
  };
  for (const arr of Object.values(buckets)) sample.push(...arr);

  const stats = { INDEXED: 0, NOT_INDEXED: 0, ERROR: 0 };
  const notIndexedDetail = [];

  for (const url of sample.slice(0, SAMPLE_INSPECT)) {
    try {
      const res = await webmasters.urlInspection.index.inspect({
        requestBody: { inspectionUrl: url, siteUrl: SITE_URL }
      });
      const verdict = res.data.inspectionResult?.indexStatusResult?.verdict || 'UNKNOWN';
      const coverageState = res.data.inspectionResult?.indexStatusResult?.coverageState || '';
      const lastCrawl = res.data.inspectionResult?.indexStatusResult?.lastCrawlTime || 'never';

      if (verdict === 'PASS') stats.INDEXED++;
      else { stats.NOT_INDEXED++; notIndexedDetail.push({ url, verdict, coverageState, lastCrawl }); }
      console.log(`  ${verdict === 'PASS' ? '✓' : '✗'} ${url} [${verdict}] ${coverageState} (crawl: ${lastCrawl})`);
    } catch (e) {
      stats.ERROR++;
      console.error(`  ! ${url}: ${e.message}`);
    }
  }
  console.log(`\n  Summary: ${stats.INDEXED} indexed, ${stats.NOT_INDEXED} not indexed, ${stats.ERROR} errors`);
  if (notIndexedDetail.length) {
    console.log('\n  Not-indexed reasons (top 5):');
    notIndexedDetail.slice(0, 5).forEach(d => {
      console.log(`    - ${d.url}: ${d.coverageState || d.verdict}`);
    });
  }
  return stats;
}

async function main() {
  if (!fs.existsSync(SITEMAP_PATH)) throw new Error('sitemap.xml not found at repo root');
  const xml = fs.readFileSync(SITEMAP_PATH, 'utf-8');
  const urls = parseSitemapUrls(xml);
  console.log(`Loaded ${urls.length} URLs from sitemap.`);

  const credentials = JSON.parse(process.env.GSC_SERVICE_ACCOUNT_JSON);
  const auth = new google.auth.GoogleAuth({
    credentials,
    scopes: [
      'https://www.googleapis.com/auth/indexing',
      'https://www.googleapis.com/auth/webmasters'
    ]
  });
  const authClient = await auth.getClient();
  const indexing = google.indexing({ version: 'v3', auth: authClient });
  const webmasters = google.webmasters({ version: 'v3', auth: authClient });

  const gIndex = await submitToGoogleIndexing(urls, indexing);
  const indexNow = await submitToIndexNow(urls);
  const inspectStats = await inspectSample(urls, webmasters);

  console.log(`\n=== FINAL ===`);
  console.log(`Sitemap URLs: ${urls.length}`);
  console.log(`Google Indexing API: ${gIndex.ok} ok / ${gIndex.err} err`);
  console.log(`IndexNow: ${indexNow.ok} accepted / ${indexNow.err} err`);
  console.log(`URL Inspection sample (${SAMPLE_INSPECT}): ${inspectStats.INDEXED} indexed, ${inspectStats.NOT_INDEXED} not indexed`);

  const indexedRate = SAMPLE_INSPECT > 0 ? Math.round((inspectStats.INDEXED / (inspectStats.INDEXED + inspectStats.NOT_INDEXED || 1)) * 100) : 0;
  console.log(`Estimated indexation rate: ${indexedRate}% of sitemap`);
}

main().catch(err => {
  console.error('Fatal:', err);
  process.exit(1);
});
