/**
 * Weekly SEO + Leads Report Generator
 *
 * Genera un informe semanal que sirve como:
 *   1. Dashboard CEO interno (SEO, leads, output de rutinas)
 *   2. Informe cliente (Anthony GWB / Fabrizzio Zenia)
 *
 * Fuentes:
 *   - Google Search Console API (Search Analytics + Sitemaps)
 *   - Filesystem: nuevos blog posts publicados esta semana
 *   - Backend opcional (BACKEND_URL) para leads
 */

const { google } = require('googleapis');
const fs = require('fs');
const path = require('path');
const https = require('https');

const SITE_URL = process.env.GSC_SITE_URL || 'sc-domain:zeniapartners.com';
const SITE_LABEL = process.env.GSC_SITE_LABEL || 'Zenia Partners';
const BLOG_DIR = process.env.BLOG_DIR || 'blog';
const TRACKER_FILE = process.env.TRACKER_FILE || '';
const BACKEND_URL = process.env.BACKEND_URL || '';
const OUTPUT_DIR = 'reports/seo-weekly';

function daysAgoISO(days) {
  const d = new Date();
  d.setUTCDate(d.getUTCDate() - days);
  return d.toISOString().split('T')[0];
}

async function querySearchAnalytics(webmasters, siteUrl, startDate, endDate, dimensions = [], rowLimit = 1000) {
  const res = await webmasters.searchanalytics.query({
    siteUrl,
    requestBody: { startDate, endDate, dimensions, rowLimit, dataState: 'final' }
  });
  return res.data.rows || [];
}

function aggregate(rows) {
  let clicks = 0, impressions = 0, ctr = 0, position = 0;
  for (const r of rows) {
    clicks += r.clicks || 0;
    impressions += r.impressions || 0;
    position += (r.position || 0) * (r.impressions || 0);
  }
  ctr = impressions > 0 ? (clicks / impressions) * 100 : 0;
  position = impressions > 0 ? position / impressions : 0;
  return { clicks, impressions, ctr, position };
}

function pct(a, b) {
  if (b === 0) return a === 0 ? 0 : 100;
  return ((a - b) / b) * 100;
}

function fmtPct(n) {
  const sign = n > 0 ? '+' : '';
  return `${sign}${n.toFixed(1)}%`;
}

function fmtInt(n) {
  return Math.round(n).toLocaleString('en-US');
}

function emoji(change, inverted = false) {
  // inverted=true para "posición" donde bajar es bueno
  const good = inverted ? change < 0 : change > 0;
  const bad = inverted ? change > 0 : change < 0;
  if (Math.abs(change) < 1) return '=';
  if (good) return 'UP';
  if (bad) return 'DOWN';
  return '=';
}

function httpGet(url) {
  return new Promise((resolve, reject) => {
    https.get(url, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => resolve({ status: res.statusCode, body: data }));
    }).on('error', reject);
  });
}

// Cuenta blog posts publicados en los últimos N días
function countNewPosts(blogDir, daysBack = 7) {
  if (!fs.existsSync(blogDir)) return { total: 0, files: [] };
  const now = Date.now();
  const cutoff = now - daysBack * 24 * 60 * 60 * 1000;
  const entries = fs.readdirSync(blogDir, { withFileTypes: true });
  const posts = [];
  for (const e of entries) {
    if (!e.isFile()) continue;
    const ext = path.extname(e.name);
    if (!['.md', '.html', '.mdx'].includes(ext)) continue;
    const filePath = path.join(blogDir, e.name);
    const stat = fs.statSync(filePath);
    if (stat.mtimeMs >= cutoff) {
      posts.push({ name: e.name, date: new Date(stat.mtimeMs).toISOString().split('T')[0] });
    }
  }
  return { total: posts.length, files: posts };
}

// Cuenta total de posts publicados (del tracker o del dir)
function getPublishedSummary(trackerFile, blogDir) {
  if (trackerFile && fs.existsSync(trackerFile)) {
    try {
      const tracker = JSON.parse(fs.readFileSync(trackerFile, 'utf8'));
      const published = tracker.posts.filter(p => p.status === 'published');
      const pending = tracker.posts.filter(p => p.status === 'pending');
      return { published: published.length, pending: pending.length, source: 'tracker' };
    } catch (e) {
      console.error('Error parsing tracker:', e.message);
    }
  }
  // Fallback: contar archivos
  if (fs.existsSync(blogDir)) {
    const files = fs.readdirSync(blogDir).filter(f => /\.(md|html|mdx)$/.test(f));
    return { published: files.length, pending: null, source: 'filesystem' };
  }
  return { published: 0, pending: null, source: 'none' };
}

async function fetchLeads() {
  if (!BACKEND_URL) return null;
  try {
    const res = await httpGet(`${BACKEND_URL}/api/stats/leads?days=7`);
    if (res.status === 200) {
      return JSON.parse(res.body);
    }
  } catch (e) {
    console.error('Leads fetch failed:', e.message);
  }
  return null;
}

async function main() {
  const credentials = JSON.parse(process.env.GSC_SERVICE_ACCOUNT_JSON);

  const auth = new google.auth.GoogleAuth({
    credentials,
    scopes: ['https://www.googleapis.com/auth/webmasters.readonly']
  });

  const authClient = await auth.getClient();
  const webmasters = google.webmasters({ version: 'v3', auth: authClient });

  const endCurrent = daysAgoISO(3);
  const startCurrent = daysAgoISO(9);
  const endPrevious = daysAgoISO(10);
  const startPrevious = daysAgoISO(16);

  console.log(`Report for ${SITE_LABEL} (${SITE_URL})`);
  console.log(`Current week: ${startCurrent} to ${endCurrent}`);
  console.log(`Previous week: ${startPrevious} to ${endPrevious}`);

  const currentRows = await querySearchAnalytics(webmasters, SITE_URL, startCurrent, endCurrent, []);
  const previousRows = await querySearchAnalytics(webmasters, SITE_URL, startPrevious, endPrevious, []);
  const current = aggregate(currentRows);
  const previous = aggregate(previousRows);

  const topQueries = await querySearchAnalytics(webmasters, SITE_URL, startCurrent, endCurrent, ['query'], 25);
  const topPages = await querySearchAnalytics(webmasters, SITE_URL, startCurrent, endCurrent, ['page'], 15);

  // Queries en top 10 (posiciones relevantes)
  const topRanked = topQueries.filter(q => q.position <= 10).length;
  const midRanked = topQueries.filter(q => q.position > 10 && q.position <= 30).length;
  const lowRanked = topQueries.filter(q => q.position > 30).length;

  // Queries ganadoras (comparativa vs previous)
  const prevTopQueries = await querySearchAnalytics(webmasters, SITE_URL, startPrevious, endPrevious, ['query'], 100);
  const prevMap = new Map(prevTopQueries.map(q => [q.keys[0], q]));
  const gainers = [];
  const losers = [];
  for (const q of topQueries) {
    const prev = prevMap.get(q.keys[0]);
    if (!prev) {
      if (q.impressions >= 5) gainers.push({ query: q.keys[0], current: q, previous: null, deltaImp: q.impressions, new: true });
      continue;
    }
    const deltaImp = q.impressions - prev.impressions;
    const deltaPos = prev.position - q.position; // positive = moved up
    if (deltaImp >= 5 || deltaPos >= 2) gainers.push({ query: q.keys[0], current: q, previous: prev, deltaImp, deltaPos });
    if (deltaImp <= -5 || deltaPos <= -2) losers.push({ query: q.keys[0], current: q, previous: prev, deltaImp, deltaPos });
  }
  gainers.sort((a, b) => b.deltaImp - a.deltaImp);
  losers.sort((a, b) => a.deltaImp - b.deltaImp);

  // Daily trend
  const dailyRows = await querySearchAnalytics(webmasters, SITE_URL, startCurrent, endCurrent, ['date'], 30);
  dailyRows.sort((a, b) => (a.keys[0] < b.keys[0] ? 1 : -1));

  // Sitemap status
  let sitemapInfo = 'N/A';
  let sitemapSubmitted = 0, sitemapIndexed = 0;
  try {
    const sitemapsRes = await webmasters.sitemaps.list({ siteUrl: SITE_URL });
    const sitemaps = sitemapsRes.data.sitemap || [];
    if (sitemaps.length > 0) {
      const main = sitemaps[0];
      sitemapSubmitted = main.contents?.[0]?.submitted || 0;
      sitemapIndexed = main.contents?.[0]?.indexed || 0;
      sitemapInfo = `${sitemapSubmitted} submitted / ${sitemapIndexed} indexed`;
    }
  } catch (e) {
    sitemapInfo = `Error: ${e.message}`;
  }

  // Routines output
  const newPosts = countNewPosts(BLOG_DIR, 7);
  const contentSummary = getPublishedSummary(TRACKER_FILE, BLOG_DIR);

  // Leads (si hay backend)
  const leads = await fetchLeads();

  const today = new Date().toISOString().split('T')[0];
  const impChange = pct(current.impressions, previous.impressions);
  const clicksChange = pct(current.clicks, previous.clicks);
  const ctrChange = pct(current.ctr, previous.ctr);
  const posChange = pct(current.position, previous.position);

  const md = `# SEO + Leads Weekly Report — ${SITE_LABEL}
**Week:** ${startCurrent} to ${endCurrent}
**Previous:** ${startPrevious} to ${endPrevious}
**Generated:** ${today}

---

## 1. KPIs principales (vs semana anterior)

| Metric | This week | Previous week | Change | Signal |
|---|---|---|---|---|
| Impressions | ${fmtInt(current.impressions)} | ${fmtInt(previous.impressions)} | ${fmtPct(impChange)} | ${emoji(impChange)} |
| Clicks | ${fmtInt(current.clicks)} | ${fmtInt(previous.clicks)} | ${fmtPct(clicksChange)} | ${emoji(clicksChange)} |
| CTR | ${current.ctr.toFixed(2)}% | ${previous.ctr.toFixed(2)}% | ${fmtPct(ctrChange)} | ${emoji(ctrChange)} |
| Avg Position | ${current.position.toFixed(1)} | ${previous.position.toFixed(1)} | ${fmtPct(posChange)} | ${emoji(posChange, true)} |

**Posicionamiento actual** (queries con impresiones esta semana):
- Top 10 posiciones: **${topRanked}** queries
- Posiciones 11-30: **${midRanked}** queries
- Posiciones 31+: **${lowRanked}** queries

**Indexación:** ${sitemapInfo}

---

## 2. Leads y conversión

${leads ? `| Metric | Value |
|---|---|
| Total leads esta semana | ${leads.total || 0} |
| Via web booking | ${leads.web || 0} |
| Via WhatsApp | ${leads.whatsapp || 0} |
| Via email | ${leads.email || 0} |
| Conversion rate (leads/clicks) | ${current.clicks > 0 ? ((leads.total / current.clicks) * 100).toFixed(1) + '%' : 'N/A'} |
` : `_Backend integration pendiente. Placeholder para próximas semanas._

**Clicks orgánicos esta semana:** ${fmtInt(current.clicks)} (proxy para leads hasta integrar backend)`}

---

## 3. Output de rutinas automáticas

| Rutina | Output esta semana | Total acumulado |
|---|---|---|
| Blog posts publicados | ${newPosts.total} | ${contentSummary.published}${contentSummary.pending !== null ? ` (pending: ${contentSummary.pending})` : ''} |
| Sitemap indexado | ${sitemapIndexed}/${sitemapSubmitted} URLs | - |

${newPosts.total > 0 ? `**Posts nuevos esta semana:**
${newPosts.files.map(f => `- ${f.name} (${f.date})`).join('\n')}
` : '_No se publicaron posts nuevos esta semana._'}

---

## 4. Queries ganadoras (subida vs semana anterior)

${gainers.length > 0 ? `| Query | This week impr | Prev impr | ΔImp | Position |
|---|---|---|---|---|
${gainers.slice(0, 10).map(g => `| ${g.query} | ${fmtInt(g.current.impressions)} | ${g.previous ? fmtInt(g.previous.impressions) : 'NEW'} | ${g.deltaImp > 0 ? '+' : ''}${g.deltaImp} | ${g.current.position.toFixed(1)} |`).join('\n')}` : '_Sin ganadores significativos esta semana._'}

## 5. Queries perdedoras (bajada vs semana anterior)

${losers.length > 0 ? `| Query | This week impr | Prev impr | ΔImp | Position |
|---|---|---|---|---|
${losers.slice(0, 10).map(l => `| ${l.query} | ${fmtInt(l.current.impressions)} | ${fmtInt(l.previous.impressions)} | ${l.deltaImp} | ${l.current.position.toFixed(1)} |`).join('\n')}` : '_Sin perdedores significativos esta semana._'}

---

## 6. Top 25 queries esta semana

| # | Query | Impressions | Clicks | CTR | Position |
|---|---|---|---|---|---|
${topQueries.map((r, i) => `| ${i + 1} | ${r.keys[0]} | ${fmtInt(r.impressions)} | ${fmtInt(r.clicks)} | ${r.impressions > 0 ? ((r.clicks / r.impressions) * 100).toFixed(2) : '0.00'}% | ${r.position.toFixed(1)} |`).join('\n')}

---

## 7. Top 15 páginas esta semana

| # | Page | Impressions | Clicks | CTR | Position |
|---|---|---|---|---|---|
${topPages.map((r, i) => {
  const url = r.keys[0].replace(/^https?:\/\/[^/]+/, '');
  return `| ${i + 1} | ${url} | ${fmtInt(r.impressions)} | ${fmtInt(r.clicks)} | ${r.impressions > 0 ? ((r.clicks / r.impressions) * 100).toFixed(2) : '0.00'}% | ${r.position.toFixed(1)} |`;
}).join('\n')}

---

## 8. Tendencia diaria

| Date | Impressions | Clicks | CTR | Position |
|---|---|---|---|---|
${dailyRows.map(r => `| ${r.keys[0]} | ${fmtInt(r.impressions)} | ${fmtInt(r.clicks)} | ${r.impressions > 0 ? ((r.clicks / r.impressions) * 100).toFixed(2) : '0.00'}% | ${r.position.toFixed(1)} |`).join('\n')}

---

## 9. Acciones recomendadas

${gainers.length > 0 ? `- **Doblar en ganadores:** las queries que subieron (${gainers.slice(0, 3).map(g => `"${g.query}"`).join(', ')}) merecen contenido de refuerzo o internal linking adicional.` : ''}
${losers.length > 0 ? `- **Recuperar perdedores:** las queries que bajaron (${losers.slice(0, 3).map(l => `"${l.query}"`).join(', ')}) pueden necesitar refresh de contenido, mejor title/description, o backlinks.` : ''}
${midRanked > 0 ? `- **Empujar top 11-30:** hay ${midRanked} queries en posiciones 11-30. Empujarlas al top 10 multiplica clicks por 3-5x. Prioridad: internal linking + CTR optimization.` : ''}
${sitemapIndexed < sitemapSubmitted ? `- **Indexación pendiente:** ${sitemapSubmitted - sitemapIndexed} URLs sin indexar. Revisar URL Inspection en GSC.` : ''}
${newPosts.total === 0 ? `- **Output de rutina a cero:** esta semana no se publicó contenido nuevo. Revisar que la routine esté ejecutándose.` : `- **Rutina funcionando:** ${newPosts.total} posts publicados esta semana.`}

---

_Auto-generated by seo-weekly-report.js_
`;

  if (!fs.existsSync(OUTPUT_DIR)) fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  const outputPath = path.join(OUTPUT_DIR, `${today}.md`);
  fs.writeFileSync(outputPath, md);
  console.log(`\nReport saved to: ${outputPath}`);
  console.log(`Impressions: ${fmtInt(current.impressions)} (${fmtPct(impChange)})`);
  console.log(`Clicks: ${fmtInt(current.clicks)} (${fmtPct(clicksChange)})`);
  console.log(`Top 10 queries: ${topRanked} | New posts this week: ${newPosts.total}`);
}

main().catch(err => {
  console.error('Fatal:', err);
  process.exit(1);
});
