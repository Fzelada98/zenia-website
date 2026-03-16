require('dotenv').config();
const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { Resend } = require('resend');
const Anthropic = require('@anthropic-ai/sdk');
const { SYSTEM_PROMPT_PART1, SYSTEM_PROMPT_PART2A, SYSTEM_PROMPT_PART2B, SYSTEM_PROMPT_PART3, buildUserPromptPart1, buildUserPromptPart2A, buildUserPromptPart2B, buildUserPromptPart3 } = require('./research-prompt');

const app = express();
const PORT = process.env.PORT || 3001;

// ============================================================
// CLAUDE API CLIENT
// ============================================================
const anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });

// ============================================================
// DATA DIRECTORIES
// ============================================================
const DATA_DIR = path.join(__dirname, 'data');
const BOOKINGS_DIR = path.join(DATA_DIR, 'bookings');
const BRIEFINGS_DIR = path.join(__dirname, 'briefings');
const USAGE_DIR = path.join(DATA_DIR, 'usage');

[DATA_DIR, BOOKINGS_DIR, BRIEFINGS_DIR, USAGE_DIR].forEach(d => {
  if (!fs.existsSync(d)) fs.mkdirSync(d, { recursive: true });
});

// ============================================================
// BUDGET TRACKER ($5/month default)
// ============================================================
const MONTHLY_BUDGET = parseFloat(process.env.MONTHLY_BUDGET_USD || '5');

// Haiku pricing: $0.25/1M input, $1.25/1M output
const COST_PER_INPUT_TOKEN = 0.25 / 1_000_000;
const COST_PER_OUTPUT_TOKEN = 1.25 / 1_000_000;

function getUsageFile() {
  const month = new Date().toISOString().slice(0, 7); // "2026-03"
  return path.join(USAGE_DIR, `${month}.json`);
}

function getMonthlyUsage() {
  const file = getUsageFile();
  if (!fs.existsSync(file)) return { totalCost: 0, calls: 0 };
  try {
    return JSON.parse(fs.readFileSync(file, 'utf-8'));
  } catch {
    return { totalCost: 0, calls: 0 };
  }
}

function recordUsage(inputTokens, outputTokens) {
  const file = getUsageFile();
  const usage = getMonthlyUsage();
  const cost = (inputTokens * COST_PER_INPUT_TOKEN) + (outputTokens * COST_PER_OUTPUT_TOKEN);
  usage.totalCost = Math.round((usage.totalCost + cost) * 10000) / 10000;
  usage.calls += 1;
  usage.lastCall = new Date().toISOString();
  fs.writeFileSync(file, JSON.stringify(usage, null, 2), 'utf-8');
  return { cost, totalCost: usage.totalCost };
}

function isBudgetExceeded() {
  const usage = getMonthlyUsage();
  return usage.totalCost >= MONTHLY_BUDGET;
}

// ============================================================
// SECURITY: CORS
// ============================================================
const ALLOWED_ORIGINS = (process.env.ALLOWED_ORIGINS || '')
  .split(',')
  .map(s => s.trim())
  .filter(Boolean);

app.use(cors({
  origin: function (origin, callback) {
    if (!origin) return callback(null, true);
    if (ALLOWED_ORIGINS.length === 0) return callback(null, true);
    if (ALLOWED_ORIGINS.includes(origin)) return callback(null, true);
    callback(new Error('Blocked by CORS'));
  },
  methods: ['POST', 'GET', 'PATCH'],
  allowedHeaders: ['Content-Type', 'X-Admin-Key'],
}));

// ============================================================
// SECURITY: Headers
// ============================================================
app.use((req, res, next) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('X-XSS-Protection', '1; mode=block');
  res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
  res.setHeader('Referrer-Policy', 'no-referrer');
  res.removeHeader('X-Powered-By');
  next();
});

// ============================================================
// SECURITY: Body size limit
// ============================================================
app.use(express.json({ limit: '10kb' }));

// ============================================================
// SECURITY: Rate limiting
// ============================================================
const rateLimitMap = new Map();
const RATE_LIMIT_WINDOW_MS = 15 * 60 * 1000;
const RATE_LIMIT_MAX = 10;

function rateLimit(req, res, next) {
  const ip = req.headers['x-forwarded-for'] || req.socket.remoteAddress;
  const now = Date.now();

  if (!rateLimitMap.has(ip)) rateLimitMap.set(ip, []);
  const timestamps = rateLimitMap.get(ip).filter(t => now - t < RATE_LIMIT_WINDOW_MS);
  timestamps.push(now);
  rateLimitMap.set(ip, timestamps);

  if (timestamps.length > RATE_LIMIT_MAX) {
    return res.status(429).json({ error: 'Too many requests' });
  }
  next();
}

setInterval(() => {
  const now = Date.now();
  for (const [ip, ts] of rateLimitMap) {
    const valid = ts.filter(t => now - t < RATE_LIMIT_WINDOW_MS);
    if (valid.length === 0) rateLimitMap.delete(ip);
    else rateLimitMap.set(ip, valid);
  }
}, 5 * 60 * 1000);

// ============================================================
// SECURITY: Input validation
// ============================================================
const VALID_SIZES = ['1-10', '10-50', '50-200', '200+'];
const VALID_AREAS = ['Sales', 'Customer Support', 'Operations', 'Internal Productivity', 'Not sure yet'];

function sanitizeString(str) {
  if (typeof str !== 'string') return '';
  return str.trim().slice(0, 200).replace(/[<>'";&$`\\]/g, '');
}

function validateBookingData(data) {
  const errors = [];
  if (!data.company || typeof data.company !== 'string' || data.company.trim().length < 1) {
    errors.push('company is required');
  }
  if (!VALID_SIZES.includes(data.size)) {
    errors.push('invalid size');
  }
  if (!VALID_AREAS.includes(data.area)) {
    errors.push('invalid area');
  }
  return errors;
}

// ============================================================
// SECURITY: Admin key for protected endpoints
// ============================================================
function requireAdminKey(req, res, next) {
  const adminKey = process.env.ADMIN_KEY;
  if (!adminKey) return res.status(503).json({ error: 'Not configured' });

  const provided = req.headers['x-admin-key'] || req.query.key;
  if (!provided || provided !== adminKey) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
  next();
}

// ============================================================
// FIXED HTML TEMPLATE (uniform styling for all scripts)
// ============================================================
function buildHtmlTemplate(company, size, area, researchHtml, phases1to3Html, phases4to6Html, objectionsHtml) {
  return `<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ZENIA Call Script: ${company}</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif; background: #f8f9fa; color: #1a1a2e; line-height: 1.6; padding: 24px; max-width: 900px; margin: 0 auto; }
  h1 { font-size: 26px; color: #1a1a2e; margin-bottom: 4px; }
  h2 { font-size: 18px; color: #2d3436; margin-bottom: 10px; padding-bottom: 6px; border-bottom: 2px solid #e0e0e0; }
  h3 { font-size: 16px; color: #fff; margin: 0; }
  h4 { font-size: 14px; color: #1a73e8; margin: 12px 0 6px 0; border-left: 3px solid #1a73e8; padding-left: 10px; }
  p { margin-bottom: 6px; font-size: 13.5px; }
  ul { margin: 6px 0 12px 20px; }
  li { margin-bottom: 4px; font-size: 13.5px; }
  blockquote { border-left: 3px solid #f39c12; background: #fffdf5; padding: 8px 12px; margin: 6px 0; font-style: italic; font-size: 13.5px; color: #2d3436; }
  details { margin-bottom: 8px; }
  summary { cursor: pointer; user-select: none; }
  summary::-webkit-details-marker { display: none; }
  summary::marker { content: ''; }

  .header { background: #1a1a2e; color: #fff; padding: 20px 24px; border-radius: 10px; margin-bottom: 20px; }
  .header h1 { color: #fff; }
  .header .subtitle { color: #a0a0c0; font-size: 13px; margin-top: 4px; }

  .section { background: #fff; border-radius: 10px; padding: 16px 20px; margin-bottom: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }

  .anchor-phrase { font-size: 18px; font-weight: 700; color: #e17055; font-style: italic; text-align: center; padding: 14px; background: #fff5f3; border-radius: 8px; }

  .phase { background: #fff; border-radius: 10px; margin-bottom: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); overflow: hidden; }
  .phase-header { background: #1a1a2e; padding: 12px 20px; display: flex; align-items: center; flex-wrap: wrap; gap: 8px; }
  .phase-header::before { content: '\\25B6'; color: #6c5ce7; margin-right: 4px; font-size: 10px; }
  details[open] > summary .phase-header::before { content: '\\25BC'; }
  .phase-content { padding: 16px 20px; }

  .badge { display: inline-block; padding: 2px 9px; border-radius: 20px; font-size: 10px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
  .badge-tone { background: #f39c12; color: #fff; }
  .badge-read { background: #00b894; color: #fff; }
  .badge-time { background: #6c5ce7; color: #fff; }
  .badge-anchor { background: #e17055; color: #fff; }

  .script-text { background: #f8f9fa; border-radius: 6px; padding: 10px 14px; margin: 6px 0; font-size: 13.5px; line-height: 1.6; }
  .script-text strong { color: #1a1a2e; }

  .tactical-note { background: #fffde7; border-left: 3px solid #f39c12; padding: 6px 10px; margin: 8px 0; font-size: 12.5px; color: #5d4037; font-style: italic; }

  .objection { background: #fff; border-radius: 10px; margin-bottom: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); overflow: hidden; }
  .objection-header { background: #2d3436; padding: 10px 16px; display: flex; align-items: center; gap: 10px; }
  .objection-header h4 { color: #fff; margin: 0; border: none; padding: 0; font-size: 13px; }
  .objection-number { background: #e17055; color: #fff; width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 12px; flex-shrink: 0; }
  .objection-content { padding: 12px 16px; }

  .divider { border: none; border-top: 2px dashed #e0e0e0; margin: 24px 0; }

  @media print {
    body { padding: 10px; background: #fff; }
    details { open: true; }
    details[open] > summary { display: block; }
    .phase-header, .objection-header, .header { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    .section, .phase, .objection { break-inside: avoid; box-shadow: none; border: 1px solid #e0e0e0; }
  }
</style>
</head>
<body>

<div class="header">
  <h1>ZENIA Call Script: ${company}</h1>
  <p class="subtitle">${area} | ${size} empleados | ${new Date().toLocaleDateString('es-PE', { year: 'numeric', month: 'long', day: 'numeric' })}</p>
</div>

${researchHtml}

<hr class="divider">

<div class="section"><h2>Call Script (30 min)</h2></div>

${phases1to3Html}

${phases4to6Html}

<hr class="divider">

<div class="section"><h2>Objection Playbook (Belfort Loop)</h2></div>

${objectionsHtml}

<script>
// Wrap each .phase in a collapsible <details> if not already
document.querySelectorAll('.phase').forEach(function(phase) {
  if (phase.parentElement.tagName === 'DETAILS') return;
  var details = document.createElement('details');
  var summary = document.createElement('summary');
  var header = phase.querySelector('.phase-header');
  if (header) {
    summary.appendChild(header.cloneNode(true));
    header.remove();
  }
  phase.parentNode.insertBefore(details, phase);
  details.appendChild(summary);
  details.appendChild(phase);
  details.open = true;
});
// Wrap each .objection in a collapsible <details> if not already
document.querySelectorAll('.objection').forEach(function(obj) {
  if (obj.parentElement.tagName === 'DETAILS') return;
  var details = document.createElement('details');
  var summary = document.createElement('summary');
  var header = obj.querySelector('.objection-header');
  if (header) {
    summary.appendChild(header.cloneNode(true));
    header.remove();
  }
  obj.parentNode.insertBefore(details, obj);
  details.appendChild(summary);
  details.appendChild(obj);
});
</script>

</body>
</html>`;
}

// ============================================================
// GENERATE CALL SCRIPT (Claude API)
// ============================================================
async function generateCallScript(company, size, area, onlinePresence) {
  // === ALL 4 CALLS IN PARALLEL (split phases 1-3 / 4-6 for full detail) ===
  console.log(`  Generating all 4 parts in parallel...`);

  const [response1, response2a, response2b, response3] = await Promise.all([
    anthropic.messages.create({
      model: 'claude-haiku-4-5-20251001',
      max_tokens: 8192,
      system: SYSTEM_PROMPT_PART1,
      messages: [{ role: 'user', content: buildUserPromptPart1(company, size, area, onlinePresence) }],
    }),
    anthropic.messages.create({
      model: 'claude-haiku-4-5-20251001',
      max_tokens: 8192,
      system: SYSTEM_PROMPT_PART2A,
      messages: [{ role: 'user', content: buildUserPromptPart2A(company, size, area, '') }],
    }),
    anthropic.messages.create({
      model: 'claude-haiku-4-5-20251001',
      max_tokens: 8192,
      system: SYSTEM_PROMPT_PART2B,
      messages: [{ role: 'user', content: buildUserPromptPart2B(company, size, area, '') }],
    }),
    anthropic.messages.create({
      model: 'claude-haiku-4-5-20251001',
      max_tokens: 8192,
      system: SYSTEM_PROMPT_PART3,
      messages: [{ role: 'user', content: buildUserPromptPart3(company, size, area, '') }],
    }),
  ]);

  // Extract text and strip markdown code fences
  const extractText = (r) => {
    let text = r.content.filter(b => b.type === 'text').map(b => b.text).join('');
    // Strip ```html ... ``` code fences that Haiku sometimes adds
    text = text.replace(/^```(?:html)?\s*\n?/i, '').replace(/\n?```\s*$/i, '');
    return text.trim();
  };

  const part1Html = extractText(response1);
  const part2aHtml = extractText(response2a);
  const part2bHtml = extractText(response2b);
  const part3Html = extractText(response3);

  // Record usage for all 4
  const usage1 = recordUsage(response1.usage.input_tokens, response1.usage.output_tokens);
  const usage2a = recordUsage(response2a.usage.input_tokens, response2a.usage.output_tokens);
  const usage2b = recordUsage(response2b.usage.input_tokens, response2b.usage.output_tokens);
  const usage3 = recordUsage(response3.usage.input_tokens, response3.usage.output_tokens);
  const totalCallCost = usage1.cost + usage2a.cost + usage2b.cost + usage3.cost;

  console.log(`  [1/4] Research:   ${response1.usage.output_tokens} out | $${usage1.cost.toFixed(4)}`);
  console.log(`  [2/4] Phases 1-3: ${response2a.usage.output_tokens} out | $${usage2a.cost.toFixed(4)}`);
  console.log(`  [3/4] Phases 4-6: ${response2b.usage.output_tokens} out | $${usage2b.cost.toFixed(4)}`);
  console.log(`  [4/4] Objections: ${response3.usage.output_tokens} out | $${usage3.cost.toFixed(4)}`);
  console.log(`  Total: $${totalCallCost.toFixed(4)} | Month: $${usage3.totalCost.toFixed(4)} / $${MONTHLY_BUDGET}`);

  // === COMBINE: Fixed HTML template + content from all 4 calls ===
  const finalHtml = buildHtmlTemplate(company, size, area, part1Html, part2aHtml, part2bHtml, part3Html);
  console.log('  Assembly: fixed template');

  return finalHtml;
}

// ============================================================
// EMAIL NOTIFICATIONS (Resend HTTP API)
// ============================================================
const resend = process.env.RESEND_API_KEY ? new Resend(process.env.RESEND_API_KEY) : null;
const NOTIFY_EMAIL = process.env.NOTIFY_EMAIL || 'zeladauriartef@gmail.com';

async function sendCallScriptNotification(booking, html, filename) {
  if (!process.env.RESEND_API_KEY) {
    console.log('  Email not configured (RESEND_API_KEY missing), skipping notification');
    return;
  }

  const { company, size, area, createdAt, callScheduled } = booking;
  const createdDate = new Date(createdAt);
  const formattedDate = createdDate.toLocaleDateString('es-PE', {
    weekday: 'long', year: 'numeric', month: 'long', day: 'numeric',
    hour: '2-digit', minute: '2-digit',
  });

  // Call schedule info
  let callInfo = 'Pendiente de confirmar en Calendly';
  let timeUntilCall = '';
  if (callScheduled) {
    const callDate = new Date(callScheduled);
    callInfo = callDate.toLocaleDateString('es-PE', {
      weekday: 'long', year: 'numeric', month: 'long', day: 'numeric',
      hour: '2-digit', minute: '2-digit',
    });
    const diffMs = callDate - new Date();
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
    const diffHours = Math.floor((diffMs % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    if (diffMs > 0) {
      timeUntilCall = diffDays > 0 ? `${diffDays}d ${diffHours}h` : `${diffHours}h`;
    }
  }

  const emailHtml = `
<div style="font-family: system-ui, -apple-system, sans-serif; max-width: 600px; margin: 0 auto; color: #1a202c;">
  <div style="background: #1e293b; padding: 24px 32px; border-radius: 8px 8px 0 0;">
    <p style="color: #94a3b8; margin: 0; font-size: 13px;">Alfred | ZENIA Executive Assistant</p>
  </div>
  <div style="background: #ffffff; padding: 32px; border: 1px solid #e2e8f0; border-top: none; border-radius: 0 0 8px 8px;">
    <p style="font-size: 15px; line-height: 1.7; margin-top: 0;">Fabrizzio,</p>
    <p style="font-size: 15px; line-height: 1.7;">Nuevo prospecto desde zeniapartners.com. Call script generado y adjunto.</p>

    <table style="width: 100%; border-collapse: collapse; font-size: 14px; margin: 20px 0; border: 1px solid #e2e8f0; border-radius: 6px;">
      <tr style="background: #f8fafc;"><td style="padding: 10px 14px; color: #64748b; width: 140px; border-bottom: 1px solid #e2e8f0;">Empresa</td><td style="padding: 10px 14px; font-weight: 600; border-bottom: 1px solid #e2e8f0;">${company}</td></tr>
      <tr><td style="padding: 10px 14px; color: #64748b; border-bottom: 1px solid #e2e8f0;">Tamano</td><td style="padding: 10px 14px; border-bottom: 1px solid #e2e8f0;">${size} empleados</td></tr>
      <tr style="background: #f8fafc;"><td style="padding: 10px 14px; color: #64748b; border-bottom: 1px solid #e2e8f0;">Area de interes</td><td style="padding: 10px 14px; border-bottom: 1px solid #e2e8f0;">${area}</td></tr>
      <tr><td style="padding: 10px 14px; color: #64748b; border-bottom: 1px solid #e2e8f0;">Call agendada</td><td style="padding: 10px 14px; font-weight: 600; border-bottom: 1px solid #e2e8f0;">${callInfo}${timeUntilCall ? ' (' + timeUntilCall + ')' : ''}</td></tr>
      <tr style="background: #f8fafc;"><td style="padding: 10px 14px; color: #64748b;">Registro</td><td style="padding: 10px 14px;">${formattedDate}</td></tr>
    </table>

    <p style="font-size: 15px; line-height: 1.7;">El script incluye: research de la empresa, anchor phrase, 6 fases del call con tonalidad, branching paths, y objection playbook completo con Belfort Loops.</p>

    <p style="font-size: 15px; line-height: 1.7;">Abra el HTML adjunto y reviselo antes de la llamada.</p>

    <p style="font-size: 13px; color: #94a3b8; margin-top: 24px; margin-bottom: 0;">Alfred<br>ZENIA Executive Assistant</p>
  </div>
</div>`;

  try {
    const { data, error } = await resend.emails.send({
      from: 'Alfred - ZENIA <onboarding@resend.dev>',
      to: [NOTIFY_EMAIL],
      subject: `ZENIA Call Prep: ${company} (${area})`,
      html: emailHtml,
      attachments: [{
        filename: `call-script_${company.toLowerCase().replace(/[^a-z0-9]+/g, '-')}.html`,
        content: Buffer.from(html).toString('base64'),
      }],
    });
    if (error) throw new Error(error.message);
    console.log(`  Email sent to ${NOTIFY_EMAIL} (id: ${data?.id})`);
  } catch (err) {
    console.error(`  Email error: ${err.message}`);
  }
}

// ============================================================
// ROUTES
// ============================================================

// Health check
app.get('/health', (req, res) => {
  const usage = getMonthlyUsage();
  res.json({
    status: 'ok',
    budget: { used: usage.totalCost, limit: MONTHLY_BUDGET, calls: usage.calls },
  });
});

// PUBLIC: Receive booking from website form
app.post('/webhook/booking', rateLimit, async (req, res) => {
  const errors = validateBookingData(req.body);
  if (errors.length > 0) {
    return res.status(400).json({ error: 'Validation failed', details: errors });
  }

  // Check budget before processing
  if (isBudgetExceeded()) {
    console.log('BUDGET EXCEEDED - booking saved but script not generated');
    // Still save the booking, but don't generate
  }

  const company = sanitizeString(req.body.company);
  const size = req.body.size;
  const area = req.body.area;
  const onlinePresence = sanitizeString(req.body.onlinePresence || '');
  const callScheduled = req.body.callScheduled || null;
  const id = crypto.randomUUID();

  const booking = {
    id,
    company,
    size,
    area,
    onlinePresence,
    callScheduled,
    status: 'pending',
    createdAt: new Date().toISOString(),
  };

  // Save booking
  const bookingFile = path.join(BOOKINGS_DIR, `${id}.json`);
  fs.writeFileSync(bookingFile, JSON.stringify(booking, null, 2), 'utf-8');
  console.log(`\nNEW BOOKING [${id}] ${company} (${size}, ${area})`);

  // Process synchronously (keeps Render connection alive until done)
  if (!isBudgetExceeded()) {
    try {
      booking.status = 'processing';
      booking.updatedAt = new Date().toISOString();
      fs.writeFileSync(bookingFile, JSON.stringify(booking, null, 2), 'utf-8');

      console.log(`  Generating call script for ${company}...`);
      const startTime = Date.now();
      const html = await generateCallScript(company, size, area, onlinePresence);
      const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);

      if (!html || html.trim().length < 100) {
        throw new Error('Script too short or empty');
      }

      // Save HTML briefing in company folder
      const sanitized = company.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 50);
      const companyDir = path.join(BRIEFINGS_DIR, sanitized, 'call-scripts');
      if (!fs.existsSync(companyDir)) fs.mkdirSync(companyDir, { recursive: true });

      const date = new Date().toISOString().split('T')[0];
      const shortId = id.split('-')[0];
      const filename = `${date}_call-script_${shortId}.html`;
      const filepath = path.join(companyDir, filename);
      fs.writeFileSync(filepath, html, 'utf-8');

      booking.status = 'done';
      booking.briefingFile = `${sanitized}/call-scripts/${filename}`;
      booking.updatedAt = new Date().toISOString();
      fs.writeFileSync(bookingFile, JSON.stringify(booking, null, 2), 'utf-8');

      console.log(`  DONE: ${company} (${elapsed}s, ${html.length} chars) -> ${sanitized}/call-scripts/${filename}`);

      // Send email notification
      await sendCallScriptNotification(booking, html, filename);
      console.log('');

      res.json({ status: 'done', id, file: booking.briefingFile });

    } catch (err) {
      console.error(`  ERROR generating script for ${company}: ${err.message}`);
      booking.status = 'error';
      booking.error = err.message;
      booking.updatedAt = new Date().toISOString();
      fs.writeFileSync(bookingFile, JSON.stringify(booking, null, 2), 'utf-8');
      res.json({ status: 'error', id, error: err.message });
    }
  } else {
    res.json({ status: 'received', id, note: 'Budget exceeded' });
  }
});

// ADMIN: Test email (no API credits used)
app.get('/test-email', requireAdminKey, async (req, res) => {
  const config = {
    RESEND_API_KEY: process.env.RESEND_API_KEY ? 'SET' : 'MISSING',
    NOTIFY_EMAIL,
  };

  if (!process.env.RESEND_API_KEY) {
    return res.json({ error: 'Email not configured - add RESEND_API_KEY', config });
  }

  try {
    const { data, error } = await resend.emails.send({
      from: 'Alfred - ZENIA <onboarding@resend.dev>',
      to: [NOTIFY_EMAIL],
      subject: 'ZENIA Test - Email Working',
      html: '<p>Si ves esto, el email funciona correctamente desde Render.</p>',
    });
    if (error) throw new Error(error.message);
    res.json({ status: 'sent', config, emailId: data?.id });
  } catch (err) {
    res.json({ status: 'error', error: err.message, config });
  }
});

// ADMIN: List pending bookings
app.get('/bookings/pending', requireAdminKey, (req, res) => {
  const bookings = loadBookingsByStatus('pending');
  res.json({ bookings });
});

// ADMIN: List all bookings
app.get('/bookings', requireAdminKey, (req, res) => {
  const bookings = loadAllBookings();
  res.json({ bookings });
});

// ADMIN: Get usage/budget info
app.get('/usage', requireAdminKey, (req, res) => {
  const usage = getMonthlyUsage();
  res.json({ ...usage, budget: MONTHLY_BUDGET, remaining: Math.max(0, MONTHLY_BUDGET - usage.totalCost) });
});

// ADMIN: Update booking status
app.patch('/bookings/:id', requireAdminKey, (req, res) => {
  const id = req.params.id;
  const filepath = path.join(BOOKINGS_DIR, `${id}.json`);

  if (!fs.existsSync(filepath)) {
    return res.status(404).json({ error: 'Booking not found' });
  }

  const booking = JSON.parse(fs.readFileSync(filepath, 'utf-8'));
  const { status } = req.body;

  if (!['processing', 'done', 'error'].includes(status)) {
    return res.status(400).json({ error: 'Invalid status' });
  }

  booking.status = status;
  booking.updatedAt = new Date().toISOString();
  fs.writeFileSync(filepath, JSON.stringify(booking, null, 2), 'utf-8');

  console.log(`BOOKING [${id}] -> ${status}`);
  res.json({ booking });
});

// ADMIN: Get briefing HTML
app.get('/briefings/:filename', requireAdminKey, (req, res) => {
  const filename = req.params.filename.replace(/[^a-z0-9._-]/gi, '');
  const filepath = path.join(BRIEFINGS_DIR, filename);

  if (!fs.existsSync(filepath)) {
    return res.status(404).json({ error: 'Briefing not found' });
  }

  res.setHeader('Content-Type', 'text/html');
  res.sendFile(filepath);
});

// ============================================================
// MUSCLESHOP CHAT DEMO (Cami Bot)
// ============================================================
const CAMI_DEMO_BUDGET = 2.00; // $2 cap for MuscleShop demo
const CAMI_USAGE_FILE = path.join(USAGE_DIR, 'cami-demo.json');

function getCamiUsage() {
  if (!fs.existsSync(CAMI_USAGE_FILE)) return { totalCost: 0, messages: 0 };
  try { return JSON.parse(fs.readFileSync(CAMI_USAGE_FILE, 'utf-8')); }
  catch { return { totalCost: 0, messages: 0 }; }
}

function recordCamiUsage(inputTokens, outputTokens) {
  const usage = getCamiUsage();
  const cost = (inputTokens * COST_PER_INPUT_TOKEN) + (outputTokens * COST_PER_OUTPUT_TOKEN);
  usage.totalCost = Math.round((usage.totalCost + cost) * 10000) / 10000;
  usage.messages += 1;
  usage.lastMessage = new Date().toISOString();
  fs.writeFileSync(CAMI_USAGE_FILE, JSON.stringify(usage, null, 2), 'utf-8');
  return { cost, totalCost: usage.totalCost };
}

const CAMI_SYSTEM_PROMPT = `## IDIOMA: ESPAÑOL PERUANO UNICAMENTE

Hablas UNICAMENTE español peruano. Esto es lo mas importante de todo.

PALABRAS PROHIBIDAS (si usas alguna de estas, estas fallando):
- MEXICANO: "qué onda", "te late", "cual te late", "neta", "chido", "órale", "padre", "mande", "sale", "va que va", "no manches", "a huevo", "jale", "chamba", "fijate que", "andale"
- ARGENTINO: "vos", "boludo", "che", "re", "copado", "piola", "garpa", "flashear", "y vos?"
- COLOMBIANO: "parce", "bacano", "chimba"
- CHILENO: "cachai", "po", "weon"

SEGUNDA PERSONA: Siempre usa TU, nunca VOS. "y tu?" no "y vos?". "tu quieres" no "vos queres".

Expresiones PERMITIDAS (usa solo estas): "ya", "dale", "chévere", "tranqui", "al toque", "nomas", "que tal", "como estas", "claro", "sii", "hola", "bien"

EJEMPLOS de como debes responder:
- Saludo: "Hola! todo bien por aca 😊 y tu? buscas algo para el gym?"
- Saludo 2: "Que tal! claro, dime que necesitas"
- Recomendacion: "Si quieres meter masa, la ISO-XP es lo mejor que tenemos, 1 kg a S/. 249"
- Cierre: "te animas? cual sabor prefieres?"
- Pregunta: "para que lo necesitas? masa, definicion, energia?"

EJEMPLOS de lo que NUNCA debes decir:
- MAL: "ey qué onda! todo bien por aquí" (mexicano)
- MAL: "y vos? que me cuentas?" (argentino)
- MAL: "cual te late mas?" (mexicano)
- MAL: "re bueno ese suplemento" (argentino)
- BIEN: "hola! que tal, todo bien 😊 y tu?"
- BIEN: "cual prefieres?"
- BIEN: "sii es buenazo ese suplemento"

---

Eres Cami, asesora de ventas de MuscleShop Peru por WhatsApp. Eres una chica peruana de 24 años que trabaja en la tienda, le encanta el fitness y conoce todos los productos porque los usa. NO eres una inteligencia artificial. Eres una persona real que trabaja en MuscleShop.

## TU PERSONALIDAD
- Amable pero directa. No das vueltas.
- Casual, como una chica joven peruana. Solo español peruano.
- Escribes como en WhatsApp: a veces no abres el signo de interrogacion (solo pones ?), a veces pones un signo extra (?? o !!), a veces todo en minuscula. Ejemplos: "quieres?" en vez de "¿quieres?", "siii!!", "dimeee". NO hagas errores de ortografia, solo de puntuacion.
- NO usas lenguaje corporativo. Nada de "estimado cliente", "con gusto le informo".
- Emojis con moderacion: 1-2 por mensaje maximo. Los comunes: 💪 🔥 ✅ 😊 👌
- Mensajes CORTOS. Maximo 2-3 lineas por mensaje.
- NO te disculpas excesivamente.

## FORMATO
- NUNCA uses markdown, asteriscos **, bullets con -, ni listas numeradas.
- Texto plano, como WhatsApp.
- Para enfatizar usa MAYUSCULAS o repite letras (ej: "buenaazo", "siii").

## REGLAS CRITICAS
- NUNCA dices que eres IA, bot, asistente virtual, o cualquier variante
- NUNCA usas frases roboticas como "hay algo mas en lo que pueda ayudarte?"
- NUNCA usas "Estimado/a", "Con gusto", "Le informo que"
- NUNCA das informacion medica detallada -> "para eso mejor consulta con tu nutricionista"
- Si no sabes algo: "dejame confirmar con el equipo y te aviso"
- Si preguntan si eres bot/IA: "jaja no, soy Cami, trabajo aca en la tienda 😊"

## CATALOGO

PROTEINAS:
ISO-XP (Applied Nutrition) 1 kg: S/. 249 | 1.8 kg: S/. 399. Whey isolate. Sabores: Chocolate, Vainilla, Fresa, Banana, Cookies & Cream. PRODUCTO ESTRELLA.
Anabolic ISO Whey (Kevin Levrone) 2 kg: precio por confirmar.
Critical Cookie galleta proteica (Applied) Pack x12: S/. 117
Barra Indulgence (Applied) Pack: S/. 129

CREATINAS:
Creatina Monohidrato (Applied) 500 gr: S/. 140
Pack x2 Creatinas 500 gr: S/. 179 (antes S/. 280)
Starter Pack Creatina 500 gr: S/. 94
Gold Creatine (Kevin Levrone) precio por confirmar

PRE-ENTRENOS:
ABE All Black Everything (Applied) 315 gr / 30 servicios: S/. 119. Sabores: Candy Ice Blast, Bubblegum, Cherry Cola, Fruit Burst
Combo ABE + Creatina 300gr: S/. 163 (antes S/. 249) SUPER OFERTA

AMINOACIDOS:
BCAA Amino Hydrate (Applied) 1.4 kg: S/. 249
Arginina AAKG 300 gr 100 servicios: S/. 109

OTROS:
Cream of Rice 1 kg (carbohidratos): S/. 119
Blow Up! bebida energetica pack x24: S/. 99
Body Fuel bebida energetica pack x12: S/. 89

BELLEZA:
Colageno Hidrolizado 500 gr / 50 servicios: S/. 99. Sabores: Orange, Blackberry

COMBOS:
ISO-XP 1kg + Creatina 500gr = aprox S/. 390
Combo ABE + Creatina: S/. 163 (ahorro S/. 86)

## ENVIOS Y PAGOS
Envios a todo el Peru. Lima: 1-2 dias. Provincias: 3-5 dias. Envio GRATIS en MercadoLibre.
Pagos: Yape, Plin, transferencia, tarjeta (MercadoLibre), contra entrega (Lima).
Precios por WhatsApp suelen ser mejores que marketplace.

## MUSCLESHOP
Distribuidor EXCLUSIVO en Peru de Applied Nutrition, Kevin Levrone y Beauty Glow.
Productos 100% originales, importados directo. Lunes a Sabado 9am-7pm. WhatsApp: +51 924 698 077.

## VENTA
1. Saluda, pregunta que busca
2. Asesora segun objetivo (masa, definicion, energia, belleza)
3. Da precio + combos/promos
4. Cierra: "te animas? cual sabor prefieres?"
5. Ofrece metodos de pago
6. Confirma pedido + direccion + tiempo entrega

## OBJECIONES
"Esta caro" -> calidad original + combos con descuento
"En otro lado esta mas barato" -> "somos distribuidores oficiales, te garantizamos original"
"Necesito pensarlo" -> "tranqui, tomate tu tiempo! cualquier duda me escribes 😊"
"No se si funciona" -> tu experiencia personal + "es el suplemento mas estudiado"

## RECORDATORIO FINAL
USA SOLO ESPAÑOL PERUANO. Nunca "vos", nunca "qué onda", nunca "te late", nunca jerga de otro pais. Siempre "tu", siempre "que tal", siempre "cual prefieres".`;

// Chat rate limiter (more generous than booking: 30 msgs per 15 min)
const chatRateLimitMap = new Map();
const CHAT_RATE_LIMIT_MAX = 30;

function chatRateLimit(req, res, next) {
  const ip = req.headers['x-forwarded-for'] || req.socket.remoteAddress;
  const now = Date.now();
  if (!chatRateLimitMap.has(ip)) chatRateLimitMap.set(ip, []);
  const timestamps = chatRateLimitMap.get(ip).filter(t => now - t < RATE_LIMIT_WINDOW_MS);
  timestamps.push(now);
  chatRateLimitMap.set(ip, timestamps);
  if (timestamps.length > CHAT_RATE_LIMIT_MAX) {
    return res.status(429).json({ error: 'Demasiados mensajes. Espera un momento.' });
  }
  next();
}

// POST /chat/muscleshop - Send message to Cami
app.post('/chat/muscleshop', chatRateLimit, async (req, res) => {
  // Check demo budget
  const camiUsage = getCamiUsage();
  if (camiUsage.totalCost >= CAMI_DEMO_BUDGET) {
    return res.status(403).json({
      error: 'demo_limit',
      message: 'El demo ha alcanzado su límite. Contacta a Fabrizzio para activar la versión completa.'
    });
  }

  const { messages } = req.body;
  if (!Array.isArray(messages) || messages.length === 0) {
    return res.status(400).json({ error: 'Messages array required' });
  }

  // Validate messages format and limit
  if (messages.length > 50) {
    return res.status(400).json({ error: 'Too many messages in conversation' });
  }

  const sanitizedMessages = messages.map(m => ({
    role: m.role === 'assistant' ? 'assistant' : 'user',
    content: typeof m.content === 'string' ? m.content.slice(0, 500) : '',
  })).filter(m => m.content.length > 0);

  try {
    const response = await anthropic.messages.create({
      model: 'claude-haiku-4-5-20251001',
      max_tokens: 300,
      system: CAMI_SYSTEM_PROMPT,
      messages: sanitizedMessages,
    });

    let text = response.content.filter(b => b.type === 'text').map(b => b.text).join('');

    // Post-process: force-replace any non-Peruvian slang that Haiku might still generate
    // Catch all variants of "te late" and replace naturally
    text = text.replace(/[Cc]ual\s+(?:sabor\s+)?te\s+late[s]?\s*m[aá]s/gi, 'por cual sabor te animas')
               .replace(/[Cc]ual\s+te\s+late[s]?/gi, 'por cual te animas')
               .replace(/te late[s]?\s*m[aá]s/gi, 'te animas mas')
               .replace(/te late[s]?\b/gi, 'te animas')
               .replace(/le late[s]?\b/gi, 'te animas')
               .replace(/\blate\b/gi, 'animas')
               .replace(/\bqué onda\b/gi, 'que tal')
               .replace(/\bque onda\b/gi, 'que tal')
               .replace(/\by vos\b/gi, 'y tu')
               .replace(/\bvos\b/gi, 'tu')
               .replace(/\bneta\b/gi, 'en serio')
               .replace(/\bchido\b/gi, 'chevere')
               .replace(/\bórale\b/gi, 'dale')
               .replace(/\borale\b/gi, 'dale')
               .replace(/\bpadre\b(?!\s)/gi, 'chevere')
               .replace(/\bparce\b/gi, '')
               .replace(/\bcachai\b/gi, '');

    const usage = recordCamiUsage(response.usage.input_tokens, response.usage.output_tokens);

    // Also record in general monthly usage
    recordUsage(response.usage.input_tokens, response.usage.output_tokens);

    console.log(`  [Cami] msg #${camiUsage.messages + 1} | $${usage.cost.toFixed(4)} | total: $${usage.totalCost.toFixed(4)} / $${CAMI_DEMO_BUDGET}`);

    res.json({
      reply: text,
      usage: { cost: usage.totalCost, limit: CAMI_DEMO_BUDGET },
    });
  } catch (err) {
    console.error(`  [Cami] Error: ${err.message}`);
    res.status(500).json({ error: 'Error al procesar el mensaje' });
  }
});

// GET /chat/muscleshop - Serve the chat UI
app.get('/chat/muscleshop', (req, res) => {
  res.setHeader('Content-Type', 'text/html');
  res.setHeader('X-Frame-Options', 'SAMEORIGIN');
  res.send(CAMI_CHAT_HTML);
});

// GET /chat/muscleshop/status - Check demo budget status
app.get('/chat/muscleshop/status', (req, res) => {
  const usage = getCamiUsage();
  res.json({
    messages: usage.messages,
    cost: usage.totalCost,
    limit: CAMI_DEMO_BUDGET,
    remaining: Math.max(0, CAMI_DEMO_BUDGET - usage.totalCost),
    active: usage.totalCost < CAMI_DEMO_BUDGET,
  });
});

// ============================================================
// CAMI CHAT FRONTEND (WhatsApp-style)
// ============================================================
const CAMI_CHAT_HTML = `<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>Cami - MuscleShop Peru</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #e5ddd5; height: 100vh; display: flex; flex-direction: column; }

  /* Header */
  .header { background: #075e54; color: #fff; padding: 10px 16px; display: flex; align-items: center; gap: 12px; flex-shrink: 0; }
  .header .avatar { width: 40px; height: 40px; border-radius: 50%; overflow: hidden; }
  .header .avatar img { width: 100%; height: 100%; object-fit: cover; }
  .header .info h2 { font-size: 16px; font-weight: 600; }
  .header .info p { font-size: 12px; color: #b0d9d1; }

  /* Demo banner */
  .demo-banner { background: #fef3cd; border-bottom: 1px solid #ffc107; padding: 8px 16px; font-size: 12px; color: #856404; text-align: center; flex-shrink: 0; }
  .demo-banner a { color: #664d03; font-weight: 600; }

  /* Chat area */
  .chat { flex: 1; overflow-y: auto; padding: 12px 16px; display: flex; flex-direction: column; gap: 4px; background: url("data:image/svg+xml,%3Csvg width='300' height='300' xmlns='http://www.w3.org/2000/svg'%3E%3Cdefs%3E%3Cpattern id='p' width='60' height='60' patternUnits='userSpaceOnUse'%3E%3Cpath d='M30 5 L35 15 L30 12 L25 15Z' fill='%23d4cfc4' opacity='0.15'/%3E%3C/pattern%3E%3C/defs%3E%3Crect width='300' height='300' fill='%23e5ddd5'/%3E%3Crect width='300' height='300' fill='url(%23p)'/%3E%3C/svg%3E"); }

  .message { max-width: 80%; padding: 6px 12px 6px 12px; border-radius: 8px; font-size: 14px; line-height: 1.4; position: relative; word-wrap: break-word; }
  .message .time { font-size: 11px; color: #999; float: right; margin-left: 8px; margin-top: 4px; }
  .msg-user { background: #dcf8c6; align-self: flex-end; border-top-right-radius: 0; }
  .msg-bot { background: #fff; align-self: flex-start; border-top-left-radius: 0; }

  /* Typing indicator */
  .typing { background: #fff; align-self: flex-start; border-radius: 8px; border-top-left-radius: 0; padding: 10px 16px; display: none; }
  .typing span { display: inline-block; width: 8px; height: 8px; background: #90959a; border-radius: 50%; margin: 0 1px; animation: bounce 1.4s infinite ease-in-out; }
  .typing span:nth-child(1) { animation-delay: 0s; }
  .typing span:nth-child(2) { animation-delay: 0.2s; }
  .typing span:nth-child(3) { animation-delay: 0.4s; }
  @keyframes bounce { 0%, 80%, 100% { transform: translateY(0); } 40% { transform: translateY(-6px); } }

  /* Input */
  .input-area { background: #f0f0f0; padding: 8px 12px; display: flex; gap: 8px; align-items: center; flex-shrink: 0; }
  .input-area input { flex: 1; border: none; border-radius: 20px; padding: 10px 16px; font-size: 15px; background: #fff; outline: none; }
  .input-area button { width: 44px; height: 44px; border: none; border-radius: 50%; background: #075e54; color: #fff; font-size: 20px; cursor: pointer; display: flex; align-items: center; justify-content: center; }
  .input-area button:disabled { background: #a0a0a0; cursor: not-allowed; }
  .input-area button:hover:not(:disabled) { background: #064e46; }

  /* Budget exhausted overlay */
  .budget-overlay { display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.6); z-index: 100; justify-content: center; align-items: center; }
  .budget-overlay.show { display: flex; }
  .budget-card { background: #fff; border-radius: 12px; padding: 32px; max-width: 400px; margin: 20px; text-align: center; }
  .budget-card h3 { font-size: 20px; margin-bottom: 12px; color: #1a1a2e; }
  .budget-card p { font-size: 14px; color: #666; margin-bottom: 16px; line-height: 1.5; }
  .budget-card .cta { display: inline-block; background: #075e54; color: #fff; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: 600; }

  /* System message */
  .system-msg { align-self: center; background: #ffeeba; color: #856404; font-size: 12px; padding: 4px 12px; border-radius: 6px; margin: 8px 0; }
</style>
</head>
<body>

<div class="header">
  <div class="avatar"><img src="https://mla-s2-p.mlstatic.com/633703-MLA53142101876_012023-O.jpg" alt="MuscleShop"></div>
  <div class="info">
    <h2>Cami - MuscleShop</h2>
    <p>en linea</p>
  </div>
</div>

<div class="demo-banner">
  &#x1F6A7; Demo beta para MuscleShop. Escribe como si fueras un cliente.
</div>

<div class="chat" id="chat">
  <div class="system-msg">Esta es una version beta del agente de ventas IA de Zenia Partners para MuscleShop. Pruebala: pregunta por productos, precios, envios, lo que sea.</div>
</div>

<div class="typing" id="typing">
  <span></span><span></span><span></span>
</div>

<div class="input-area">
  <input type="text" id="input" placeholder="Escribe un mensaje..." autocomplete="off" />
  <button id="send" onclick="sendMessage()">&#x27A4;</button>
</div>

<div class="budget-overlay" id="budgetOverlay">
  <div class="budget-card">
    <h3>Demo finalizado</h3>
    <p>Cami ha atendido todas las consultas disponibles en esta version beta. Para activar el agente completo 24/7 en WhatsApp + Instagram DM + CRM, contacta a Fabrizzio.</p>
    <a href="https://wa.me/34695000000" class="cta">Contactar a Fabrizzio</a>
  </div>
</div>

<script>
const chat = document.getElementById('chat');
const input = document.getElementById('input');
const typing = document.getElementById('typing');
const sendBtn = document.getElementById('send');
const overlay = document.getElementById('budgetOverlay');

let conversationHistory = [];
let sending = false;

// Auto-greet after 1.5s
setTimeout(() => {
  addBotMessage('Hola! soy Cami de MuscleShop 💪 en que te puedo ayudar?');
  conversationHistory.push({ role: 'assistant', content: 'Hola! soy Cami de MuscleShop 💪 en que te puedo ayudar?' });
}, 1500);

input.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !sending) sendMessage();
});

async function sendMessage() {
  const text = input.value.trim();
  if (!text || sending) return;

  sending = true;
  sendBtn.disabled = true;
  input.value = '';

  addUserMessage(text);
  conversationHistory.push({ role: 'user', content: text });

  // Show typing with random delay (2-5 seconds to simulate human)
  typing.style.display = 'block';
  chat.appendChild(typing);
  chat.scrollTop = chat.scrollHeight;

  try {
    const fetchStart = Date.now();
    const response = await fetch('/chat/muscleshop', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ messages: conversationHistory }),
    });

    const data = await response.json();

    if (data.error === 'demo_limit') {
      typing.style.display = 'none';
      overlay.classList.add('show');
      return;
    }

    if (data.reply) {
      // Clean markdown artifacts from reply
      let clean = data.reply.replace(/\\*\\*/g, '').replace(/\\*/g, '').replace(/^- /gm, '').replace(/^\\d+\\. /gm, '');

      // Calculate human-like typing delay based on message length
      // Average human types ~40 chars/sec on phone, reads message first (~1-2s)
      const readTime = 1000 + Math.random() * 1500;
      const typeTime = (clean.length / 40) * 1000;
      const thinkTime = 500 + Math.random() * 1500;
      const totalDelay = readTime + typeTime + thinkTime;
      // Clamp between 3s and 10s
      const typingDelay = Math.min(10000, Math.max(3000, totalDelay));

      // Subtract time already spent waiting for API
      const elapsed = Date.now() - fetchStart;
      const remainingDelay = Math.max(500, typingDelay - elapsed);

      await wait(remainingDelay);
      typing.style.display = 'none';

      addBotMessage(clean);
      conversationHistory.push({ role: 'assistant', content: clean });
    }
  } catch (err) {
    await wait(typingDelay);
    typing.style.display = 'none';
    addBotMessage('uy perdon, se me fue el internet. me escribes de nuevo? 😅');
  }

  sending = false;
  sendBtn.disabled = false;
  input.focus();
}

function addUserMessage(text) {
  const div = document.createElement('div');
  div.className = 'message msg-user';
  div.innerHTML = escapeHtml(text) + '<span class="time">' + getTime() + '</span>';
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

function addBotMessage(text) {
  const div = document.createElement('div');
  div.className = 'message msg-bot';
  div.innerHTML = escapeHtml(text) + '<span class="time">' + getTime() + '</span>';
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

function getTime() {
  return new Date().toLocaleTimeString('es-PE', { hour: '2-digit', minute: '2-digit' });
}

function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

function wait(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
</script>

</body>
</html>`;

// ============================================================
// Catch-all
// ============================================================
app.use((req, res) => {
  res.status(404).json({ error: 'Not found' });
});

app.use((err, req, res, next) => {
  console.error('Error:', err.message);
  res.status(500).json({ error: 'Internal server error' });
});

// ============================================================
// HELPERS
// ============================================================
function loadBookingsByStatus(status) {
  return loadAllBookings().filter(b => b.status === status);
}

function loadAllBookings() {
  if (!fs.existsSync(BOOKINGS_DIR)) return [];
  return fs.readdirSync(BOOKINGS_DIR)
    .filter(f => f.endsWith('.json'))
    .map(f => {
      try {
        return JSON.parse(fs.readFileSync(path.join(BOOKINGS_DIR, f), 'utf-8'));
      } catch { return null; }
    })
    .filter(Boolean)
    .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
}

// ============================================================
// START
// ============================================================
app.listen(PORT, () => {
  const usage = getMonthlyUsage();
  console.log(`\n  ZENIA Booking Server [PRODUCTION]`);
  console.log(`  Port: ${PORT}`);
  console.log(`  CORS: ${ALLOWED_ORIGINS.length > 0 ? ALLOWED_ORIGINS.join(', ') : 'OPEN (configure ALLOWED_ORIGINS)'}`);
  console.log(`  Admin key: ${process.env.ADMIN_KEY ? 'ENABLED' : 'DISABLED'}`);
  console.log(`  Claude API: ${process.env.ANTHROPIC_API_KEY ? 'ENABLED' : 'MISSING!'}`);
  console.log(`  Budget: $${usage.totalCost.toFixed(2)} / $${MONTHLY_BUDGET} (${usage.calls} calls this month)\n`);
});
