/**
 * Post to LinkedIn via Post for Me
 * Reads blog/social-queue.md, finds entries not yet marked as "SCHEDULED",
 * calls Post for Me API to schedule LinkedIn posts.
 *
 * Social queue format (markdown, appended by the agent):
 *
 *   ## YYYY-MM-DD - Post title
 *
 *   [LinkedIn post body in English]
 *
 *   #hashtags
 *
 *   ---
 *
 * After posting, appends "<!-- SCHEDULED:<post-id> -->" right after the title so we don't double-post.
 *
 * Triggered by GitHub Actions on push to main affecting social-queue.md.
 */

const fs = require('fs');
const https = require('https');

const QUEUE_PATH = 'blog/social-queue.md';
const API_KEY = process.env.POSTFORME_API_KEY;
const LINKEDIN_ID = process.env.LINKEDIN_ACCOUNT_ID;
const API_HOST = 'api.postforme.dev';

if (!API_KEY) {
  console.error('ERROR: POSTFORME_API_KEY not set.');
  process.exit(1);
}

if (!LINKEDIN_ID) {
  console.error('ERROR: LINKEDIN_ACCOUNT_ID not set.');
  process.exit(1);
}

// Detect vertical from post title / URL
function detectVertical(title, body) {
  const s = (title + ' ' + body).toLowerCase();
  if (/gimnasi|gym|fitness|socio/.test(s)) return 'gimnasios';
  if (/restaurante|reserva|gastro|hosteler/.test(s)) return 'restaurantes';
  if (/belleza|estetica|peluquer|salon/.test(s)) return 'belleza';
  if (/retail|tienda/.test(s) && !/ecommerce/.test(s)) return 'retail';
  if (/ecommerce|carrito|online/.test(s)) return 'ecommerce';
  if (/wellness|spa|clinica|paciente/.test(s)) return 'wellness';
  if (/abogado|inmobiliari|consultor|academ/.test(s)) return 'b2b';
  return 'b2b';
}

// Optimal posting times (UTC, assuming UTC+2 for summer CET)
const OPTIMAL_TIMES = {
  gimnasios: { hour: 15, minute: 0 },     // 17:00 CET
  restaurantes: { hour: 8, minute: 0 },   // 10:00 CET
  belleza: { hour: 7, minute: 0 },        // 09:00 CET
  retail: { hour: 6, minute: 0 },         // 08:00 CET
  ecommerce: { hour: 6, minute: 0 },
  wellness: { hour: 7, minute: 0 },
  b2b: { hour: 7, minute: 0 }             // 09:00 CET
};

function getScheduledAt(vertical) {
  const cfg = OPTIMAL_TIMES[vertical] || OPTIMAL_TIMES.b2b;
  const now = new Date();
  let scheduled = new Date(Date.UTC(
    now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate(),
    cfg.hour, cfg.minute, 0
  ));
  // If target time today already passed (with 10 min buffer), push to tomorrow
  if (scheduled.getTime() - now.getTime() < 10 * 60 * 1000) {
    scheduled.setUTCDate(scheduled.getUTCDate() + 1);
  }
  return scheduled.toISOString();
}

function postApi(payload) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify(payload);
    const req = https.request({
      hostname: API_HOST,
      path: '/v1/social-posts',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Length': Buffer.byteLength(data)
      }
    }, (res) => {
      let body = '';
      res.on('data', c => body += c);
      res.on('end', () => {
        try {
          const json = JSON.parse(body);
          if (res.statusCode >= 200 && res.statusCode < 300) resolve(json);
          else reject(new Error(`HTTP ${res.statusCode}: ${body}`));
        } catch (e) { reject(e); }
      });
    });
    req.on('error', reject);
    req.setTimeout(30000, () => { req.destroy(); reject(new Error('Timeout')); });
    req.write(data);
    req.end();
  });
}

/**
 * Parse markdown social-queue.md into entries.
 * Each entry starts with "## YYYY-MM-DD - Title" and ends with "---"
 */
function parseQueue(content) {
  const entries = [];
  const blocks = content.split(/\n---\n/);
  for (const block of blocks) {
    const titleMatch = block.match(/^##\s+(\d{4}-\d{2}-\d{2})\s*-\s*(.+)$/m);
    if (!titleMatch) continue;

    const date = titleMatch[1];
    const title = titleMatch[2].trim();

    // Body is everything after the ## line, excluding the SCHEDULED marker
    const bodyStart = block.indexOf(titleMatch[0]) + titleMatch[0].length;
    const rawBody = block.substring(bodyStart).trim();

    const scheduledMatch = rawBody.match(/<!--\s*SCHEDULED:([^>]+?)\s*-->/);
    const body = rawBody.replace(/<!--\s*SCHEDULED:[^>]+?-->\s*/, '').trim();

    entries.push({
      date,
      title,
      body,
      scheduled: !!scheduledMatch,
      scheduledId: scheduledMatch ? scheduledMatch[1] : null,
      raw: block
    });
  }
  return entries;
}

async function main() {
  if (!fs.existsSync(QUEUE_PATH)) {
    console.log('No social-queue.md found.');
    return;
  }

  const content = fs.readFileSync(QUEUE_PATH, 'utf-8');
  const entries = parseQueue(content);
  const pending = entries.filter(e => !e.scheduled);

  console.log(`Found ${entries.length} entries, ${pending.length} pending.`);

  if (pending.length === 0) return;

  let updatedContent = content;

  for (const entry of pending) {
    const vertical = detectVertical(entry.title, entry.body);
    const scheduledAt = getScheduledAt(vertical);

    console.log(`\nScheduling LinkedIn: "${entry.title}" (${vertical}) at ${scheduledAt}`);

    try {
      const result = await postApi({
        social_accounts: [LINKEDIN_ID],
        caption: entry.body,
        scheduled_at: scheduledAt
      });
      const postId = result.id || result.data?.id || 'unknown';
      console.log(`  ✓ Scheduled: ${postId}`);

      // Mark as scheduled in the queue (add marker after the title)
      const titleLine = `## ${entry.date} - ${entry.title}`;
      const markedLine = `${titleLine}\n\n<!-- SCHEDULED:${postId} at ${scheduledAt} -->`;
      updatedContent = updatedContent.replace(titleLine, markedLine);
    } catch (e) {
      console.error(`  ✗ Error: ${e.message}`);
    }
  }

  // Save updated queue
  if (updatedContent !== content) {
    fs.writeFileSync(QUEUE_PATH, updatedContent);
    console.log('\nsocial-queue.md updated with SCHEDULED markers.');
  }
}

main().catch(err => {
  console.error('Fatal:', err);
  process.exit(1);
});
