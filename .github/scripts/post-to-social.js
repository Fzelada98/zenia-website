/**
 * Post to Social Media via Post for Me
 * Reads blog/social-queue.md, finds entries with status: pending,
 * calls Post for Me API to schedule LinkedIn (English) + Instagram (Spanish),
 * marks entries as "scheduled" with the scheduled_at timestamp.
 *
 * Triggered by GitHub Actions on push to main affecting social-queue.md.
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

const QUEUE_PATH = 'blog/social-queue.md';
const API_KEY = process.env.POSTFORME_API_KEY;
const LINKEDIN_ID = process.env.LINKEDIN_ACCOUNT_ID;
const INSTAGRAM_ID = process.env.INSTAGRAM_ACCOUNT_ID;
const API_HOST = 'api.postforme.dev';

if (!API_KEY) {
  console.error('ERROR: POSTFORME_API_KEY not set.');
  process.exit(1);
}

// Optimal posting times per vertical (UTC converted from CET)
// CET = UTC+1 (winter) or UTC+2 (summer). We use UTC+2 assuming summer for April.
const OPTIMAL_TIMES = {
  gimnasios: { hour: 5, minute: 0, offsetDays: 0 },         // 7:00 CET same day
  restaurantes: { hour: 8, minute: 0, offsetDays: 1 },      // 10:00 CET next day
  belleza: { hour: 7, minute: 0, offsetDays: 1 },           // 9:00 CET next day
  estetica: { hour: 7, minute: 0, offsetDays: 1 },
  retail: { hour: 6, minute: 0, offsetDays: 0 },            // 8:00 CET same day
  ecommerce: { hour: 6, minute: 0, offsetDays: 0 },
  wellness: { hour: 7, minute: 0, offsetDays: 1 },
  clinicas: { hour: 7, minute: 0, offsetDays: 1 },
  abogados: { hour: 7, minute: 0, offsetDays: 1 },
  inmobiliarias: { hour: 7, minute: 0, offsetDays: 1 },
  default: { hour: 7, minute: 0, offsetDays: 1 }
};

function getScheduledAt(vertical) {
  const cfg = OPTIMAL_TIMES[vertical] || OPTIMAL_TIMES.default;
  const now = new Date();
  const scheduled = new Date(Date.UTC(
    now.getUTCFullYear(),
    now.getUTCMonth(),
    now.getUTCDate() + cfg.offsetDays,
    cfg.hour,
    cfg.minute,
    0
  ));
  // If the scheduled time is in the past (e.g., optimal time already passed today),
  // push to next day
  if (scheduled <= now) {
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
    req.setTimeout(30000, () => { req.destroy(); reject(new Error('Request timeout')); });
    req.write(data);
    req.end();
  });
}

// Parse simple YAML-like entries separated by --- lines
function parseQueue(content) {
  const blocks = content.split(/^---\s*$/m).filter(b => b.trim());
  return blocks.map(block => {
    const entry = {};
    const lines = block.split('\n');
    let currentKey = null;
    let buffer = [];
    for (const line of lines) {
      const match = line.match(/^(\w+):\s*(\|)?\s*(.*)$/);
      if (match && !line.startsWith('  ')) {
        if (currentKey && buffer.length) {
          entry[currentKey] = buffer.join('\n').trim();
          buffer = [];
        }
        currentKey = match[1];
        if (match[2] === '|') {
          buffer = [];
        } else {
          entry[currentKey] = match[3].trim();
          currentKey = null;
        }
      } else if (currentKey) {
        buffer.push(line.replace(/^  /, ''));
      }
    }
    if (currentKey && buffer.length) {
      entry[currentKey] = buffer.join('\n').trim();
    }
    return entry;
  });
}

function serializeQueue(entries) {
  const blocks = entries.map(e => {
    const lines = ['---'];
    for (const key of ['date', 'slug', 'vertical', 'url', 'linkedin_en', 'instagram_es', 'status', 'scheduled_at', 'post_ids']) {
      if (e[key] === undefined) continue;
      if (['linkedin_en', 'instagram_es'].includes(key)) {
        lines.push(`${key}: |`);
        e[key].split('\n').forEach(l => lines.push(`  ${l}`));
      } else {
        lines.push(`${key}: ${e[key]}`);
      }
    }
    return lines.join('\n');
  });
  return blocks.join('\n') + '\n---\n';
}

async function main() {
  if (!fs.existsSync(QUEUE_PATH)) {
    console.log('No social-queue.md found. Nothing to do.');
    return;
  }

  const content = fs.readFileSync(QUEUE_PATH, 'utf-8');
  const entries = parseQueue(content);
  const pending = entries.filter(e => e.status === 'pending');

  console.log(`Found ${entries.length} entries, ${pending.length} pending.`);

  for (const entry of pending) {
    const scheduledAt = getScheduledAt(entry.vertical);
    console.log(`\nScheduling: ${entry.slug} at ${scheduledAt} (vertical: ${entry.vertical})`);

    const postIds = [];

    // LinkedIn (English)
    if (LINKEDIN_ID && entry.linkedin_en) {
      try {
        const result = await postApi({
          account_ids: [LINKEDIN_ID],
          caption: entry.linkedin_en,
          scheduled_at: scheduledAt
        });
        const id = result.id || result.data?.id;
        console.log(`  LinkedIn scheduled: ${id}`);
        postIds.push(`linkedin:${id}`);
      } catch (e) {
        console.error(`  LinkedIn error: ${e.message}`);
      }
    }

    // Instagram (Spanish)
    if (INSTAGRAM_ID && entry.instagram_es) {
      try {
        const result = await postApi({
          account_ids: [INSTAGRAM_ID],
          caption: entry.instagram_es,
          scheduled_at: scheduledAt
        });
        const id = result.id || result.data?.id;
        console.log(`  Instagram scheduled: ${id}`);
        postIds.push(`instagram:${id}`);
      } catch (e) {
        console.error(`  Instagram error: ${e.message}`);
      }
    }

    entry.status = 'scheduled';
    entry.scheduled_at = scheduledAt;
    entry.post_ids = postIds.join(', ') || 'none';
  }

  if (pending.length > 0) {
    fs.writeFileSync(QUEUE_PATH, serializeQueue(entries));
    console.log(`\nUpdated ${QUEUE_PATH} with ${pending.length} scheduled entries.`);
  }
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
