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
// GENERATE CALL SCRIPT (Claude API)
// ============================================================
async function generateCallScript(company, size, area) {
  // === ALL 4 CALLS IN PARALLEL (split phases 1-3 / 4-6 for full detail) ===
  console.log(`  Generating all 4 parts in parallel...`);

  const [response1, response2a, response2b, response3] = await Promise.all([
    anthropic.messages.create({
      model: 'claude-haiku-4-5-20251001',
      max_tokens: 8192,
      system: SYSTEM_PROMPT_PART1,
      messages: [{ role: 'user', content: buildUserPromptPart1(company, size, area) }],
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

  // === COMBINE: Insert Parts 2a+2b+3 into Part 1 ===
  const insertContent = `\n${part2aHtml}\n\n${part2bHtml}\n\n${part3Html}\n`;
  let finalHtml;
  if (part1Html.includes('<!-- SCRIPT_INSERT -->')) {
    finalHtml = part1Html.replace('<!-- SCRIPT_INSERT -->', insertContent);
  } else {
    finalHtml = part1Html.replace('</body>', insertContent + '\n</body>');
  }

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
  const callScheduled = req.body.callScheduled || null;
  const id = crypto.randomUUID();

  const booking = {
    id,
    company,
    size,
    area,
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
      const html = await generateCallScript(company, size, area);
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
