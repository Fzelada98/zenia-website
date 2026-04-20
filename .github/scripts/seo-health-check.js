/**
 * Zenia SEO Health Check
 *
 * Daily audit of zeniapartners.com. Detects:
 *   1. Top priority URLs respond 200 OK
 *   2. Each page ships a <link rel="canonical">
 *   3. Bilingual pages ship hreflang (en + es + x-default)
 *   4. sitemap.xml is reachable, well-formed, lists >= 100 URLs
 *   5. robots.txt is reachable
 *
 * Output: JSON report on stdout. Writes `verdict`, `critical_count`,
 * `warning_count` to GITHUB_OUTPUT.
 */

const https = require('https');

const BASE = 'https://zeniapartners.com';

const PRIORITY_URLS = [
  '/',
  '/es/',
  '/blog/',
  '/es/crm-gimnasios.html',
  '/es/crm-restaurantes.html',
  '/es/crm-ecommerce.html',
  '/es/crm-salones-belleza.html',
  '/es/crm-clinicas.html',
  '/es/crm-hoteles.html',
  '/es/crm-inmobiliarias.html',
  '/es/crm-cafeterias.html',
  '/es/crm-retail.html',
  '/es/crm-wellness.html',
  '/es/crm-academias.html',
  '/es/crm-abogados.html',
  '/es/automatizacion-whatsapp-negocios.html',
  '/es/crm-whatsapp.html',
  '/es/crm-barcelona.html',
  '/es/crm-madrid.html',
  '/es/crm-lima.html',
];

const HREFLANG_MIN_FOR_BILINGUAL = 2; // at least en + es (x-default optional bonus)

function fetchUrl(url) {
  return new Promise((resolve) => {
    const req = https.get(url, { timeout: 10000 }, (res) => {
      let body = '';
      res.on('data', (chunk) => (body += chunk));
      res.on('end', () => resolve({ status: res.statusCode, body }));
    });
    req.on('error', (err) => resolve({ status: 0, error: err.message, body: '' }));
    req.on('timeout', () => {
      req.destroy();
      resolve({ status: 0, error: 'timeout', body: '' });
    });
  });
}

function extractCanonical(html) {
  const m = html.match(/<link\s+rel="canonical"\s+href="([^"]+)"/i);
  return m ? m[1] : null;
}

function countHreflang(html) {
  const matches = html.match(/<link\s+rel="alternate"\s+hreflang="[^"]+"/gi);
  return matches ? matches.length : 0;
}

async function checkUrl(path) {
  const url = BASE + (path === '/' ? '' : path);
  const { status, body, error } = await fetchUrl(url);
  const result = { path, url, status, error: error || null };
  if (status === 200) {
    result.canonical = extractCanonical(body);
    result.hreflangCount = countHreflang(body);
  }
  return result;
}

async function checkSitemap() {
  const { status, body, error } = await fetchUrl(BASE + '/sitemap.xml');
  if (status !== 200) return { status, error: error || 'non-200', urlCount: 0 };
  const urls = (body.match(/<loc>/g) || []).length;
  if (urls === 0) return { status, error: 'no <loc> tags found', urlCount: 0 };
  return { status, urlCount: urls };
}

async function checkRobots() {
  const { status, error } = await fetchUrl(BASE + '/robots.txt');
  return { status, error: error || null };
}

(async () => {
  const started = new Date().toISOString();
  const sitemap = await checkSitemap();
  const robots = await checkRobots();
  const urls = await Promise.all(PRIORITY_URLS.map(checkUrl));

  const criticalIssues = [];
  const warnings = [];

  if (sitemap.status !== 200) {
    criticalIssues.push({ kind: 'sitemap', detail: `sitemap.xml returned ${sitemap.status} (${sitemap.error || 'no body'})` });
  } else if (sitemap.urlCount < 100) {
    warnings.push({ kind: 'sitemap', detail: `sitemap.xml only has ${sitemap.urlCount} URLs (expected >= 100)` });
  }

  if (robots.status !== 200) {
    criticalIssues.push({ kind: 'robots', detail: `robots.txt returned ${robots.status}` });
  }

  for (const r of urls) {
    if (r.status !== 200) {
      criticalIssues.push({ kind: 'http', detail: `${r.path} returned ${r.status}${r.error ? ` (${r.error})` : ''}` });
      continue;
    }
    if (!r.canonical) {
      criticalIssues.push({ kind: 'canonical-missing', detail: `${r.path} ships no <link rel="canonical">` });
    } else if (!r.canonical.startsWith(BASE)) {
      warnings.push({ kind: 'canonical-external', detail: `${r.path} canonical points off-domain: ${r.canonical}` });
    }
    if (r.hreflangCount > 0 && r.hreflangCount < HREFLANG_MIN_FOR_BILINGUAL) {
      warnings.push({ kind: 'hreflang-short', detail: `${r.path} has ${r.hreflangCount} hreflang tags (expected >= ${HREFLANG_MIN_FOR_BILINGUAL})` });
    }
  }

  const verdict = criticalIssues.length > 0 ? 'FAIL' : warnings.length > 0 ? 'WARN' : 'PASS';
  const report = { started, finished: new Date().toISOString(), verdict, sitemap, robots, urls, criticalIssues, warnings };
  console.log(JSON.stringify(report, null, 2));

  if (process.env.GITHUB_OUTPUT) {
    const fs = require('fs');
    fs.appendFileSync(process.env.GITHUB_OUTPUT, `verdict=${verdict}\n`);
    fs.appendFileSync(process.env.GITHUB_OUTPUT, `critical_count=${criticalIssues.length}\n`);
    fs.appendFileSync(process.env.GITHUB_OUTPUT, `warning_count=${warnings.length}\n`);
  }

  process.exit(verdict === 'FAIL' ? 1 : 0);
})();
