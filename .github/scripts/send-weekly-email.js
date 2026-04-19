/**
 * Envía el informe semanal por email usando Resend API.
 * Ejecutado por GitHub Actions después de generar el reporte.
 *
 * Convierte el markdown del reporte en HTML branded (estilo Zenia) y envía.
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

const RESEND_API_KEY = process.env.RESEND_API_KEY;
const TO_EMAIL = process.env.TO_EMAIL || 'zeladauriartef@gmail.com';
const BCC_EMAIL = process.env.BCC_EMAIL || '';
const FROM_EMAIL = process.env.FROM_EMAIL || 'Zenia Partners <onboarding@resend.dev>';
const SITE_LABEL = process.env.GSC_SITE_LABEL || 'Zenia Partners';
const REPORT_TYPE = process.env.REPORT_TYPE || 'ceo'; // 'ceo' o 'client'
const LOGO_URL = 'https://zeniapartners.com/assets/logos/zenia-logo.png';
const REPORTS_DIR = 'reports/seo-weekly';

function latestReport() {
  if (!fs.existsSync(REPORTS_DIR)) return null;
  const files = fs.readdirSync(REPORTS_DIR)
    .filter(f => /^\d{4}-\d{2}-\d{2}\.md$/.test(f))
    .sort()
    .reverse();
  return files[0] ? path.join(REPORTS_DIR, files[0]) : null;
}

function parseReport(mdPath) {
  const md = fs.readFileSync(mdPath, 'utf8');

  const r = {
    date: path.basename(mdPath).replace('.md', ''),
    weekRange: '',
    current: { impressions: 0, clicks: 0, ctr: 0, position: 0 },
    previous: { impressions: 0, clicks: 0, ctr: 0, position: 0 },
    changes: { impressions: '', clicks: '', ctr: '', position: '' },
    posBuckets: { top10: 0, mid: 0, low: 0 },
    sitemapSubmitted: 0,
    sitemapIndexed: 0,
    newPostsCount: 0,
    newPostsList: [],
    gainers: [],
    losers: [],
    topQueries: [],
    topPages: []
  };

  const weekMatch = md.match(/\*\*Week:\*\*\s*(\S+)\s*to\s*(\S+)/);
  if (weekMatch) r.weekRange = `${weekMatch[1]} – ${weekMatch[2]}`;

  const kpiRows = md.match(/\| Impressions \| ([\d,]+) \| ([\d,]+) \| ([^|]+) \|/);
  if (kpiRows) {
    r.current.impressions = parseInt(kpiRows[1].replace(/,/g, ''));
    r.previous.impressions = parseInt(kpiRows[2].replace(/,/g, ''));
    r.changes.impressions = kpiRows[3].trim();
  }
  const clicksRow = md.match(/\| Clicks \| ([\d,]+) \| ([\d,]+) \| ([^|]+) \|/);
  if (clicksRow) {
    r.current.clicks = parseInt(clicksRow[1].replace(/,/g, ''));
    r.previous.clicks = parseInt(clicksRow[2].replace(/,/g, ''));
    r.changes.clicks = clicksRow[3].trim();
  }
  const ctrRow = md.match(/\| CTR \| ([\d.]+)% \| ([\d.]+)% \| ([^|]+) \|/);
  if (ctrRow) {
    r.current.ctr = parseFloat(ctrRow[1]);
    r.previous.ctr = parseFloat(ctrRow[2]);
    r.changes.ctr = ctrRow[3].trim();
  }
  const posRow = md.match(/\| Avg Position \| ([\d.]+) \| ([\d.]+) \| ([^|]+) \|/);
  if (posRow) {
    r.current.position = parseFloat(posRow[1]);
    r.previous.position = parseFloat(posRow[2]);
    r.changes.position = posRow[3].trim();
  }

  const top10Match = md.match(/Top 10 posiciones: \*\*(\d+)\*\*/);
  if (top10Match) r.posBuckets.top10 = parseInt(top10Match[1]);
  const midMatch = md.match(/Posiciones 11-30: \*\*(\d+)\*\*/);
  if (midMatch) r.posBuckets.mid = parseInt(midMatch[1]);
  const lowMatch = md.match(/Posiciones 31\+: \*\*(\d+)\*\*/);
  if (lowMatch) r.posBuckets.low = parseInt(lowMatch[1]);

  const sitemapMatch = md.match(/\*\*Indexación:\*\* (\d+) submitted \/ (\d+) indexed/);
  if (sitemapMatch) {
    r.sitemapSubmitted = parseInt(sitemapMatch[1]);
    r.sitemapIndexed = parseInt(sitemapMatch[2]);
  }

  const postsMatch = md.match(/Blog posts publicados \| (\d+)/);
  if (postsMatch) r.newPostsCount = parseInt(postsMatch[1]);

  const postsListMatch = md.match(/\*\*Posts nuevos esta semana:\*\*\n([^\n]+(?:\n- [^\n]+)*)/);
  if (postsListMatch) {
    r.newPostsList = postsListMatch[1].split('\n').map(l => l.replace(/^- /, '').trim()).filter(Boolean).slice(0, 8);
  }

  // Top queries (parse first table of top 25 queries)
  const topQueriesSection = md.match(/## 6\. Top 25 queries esta semana\n\n([\s\S]+?)\n\n---/);
  if (topQueriesSection) {
    const rows = topQueriesSection[1].match(/\| \d+ \| ([^|]+) \| ([\d,]+) \| ([\d,]+) \| ([\d.]+)% \| ([\d.]+) \|/g);
    if (rows) {
      r.topQueries = rows.slice(0, 20).map(row => {
        const m = row.match(/\| \d+ \| ([^|]+) \| ([\d,]+) \| ([\d,]+) \| ([\d.]+)% \| ([\d.]+) \|/);
        return {
          query: m[1].trim(),
          impressions: parseInt(m[2].replace(/,/g, '')),
          clicks: parseInt(m[3].replace(/,/g, '')),
          ctr: parseFloat(m[4]),
          position: parseFloat(m[5])
        };
      });
    }
  }

  // Top pages
  const topPagesSection = md.match(/## 7\. Top 10 páginas esta semana\n\n([\s\S]+?)\n\n---/) ||
                         md.match(/## 7\. Top 15 páginas esta semana\n\n([\s\S]+?)\n\n---/);
  if (topPagesSection) {
    const rows = topPagesSection[1].match(/\| \d+ \| ([^|]+) \| ([\d,]+) \| ([\d,]+) \| ([\d.]+)% \| ([\d.]+) \|/g);
    if (rows) {
      r.topPages = rows.slice(0, 15).map(row => {
        const m = row.match(/\| \d+ \| ([^|]+) \| ([\d,]+) \| ([\d,]+) \| ([\d.]+)% \| ([\d.]+) \|/);
        return {
          page: m[1].trim(),
          impressions: parseInt(m[2].replace(/,/g, '')),
          clicks: parseInt(m[3].replace(/,/g, '')),
          position: parseFloat(m[5])
        };
      });
    }
  }

  return r;
}

function deltaClass(change) {
  const num = parseFloat(change);
  if (isNaN(num) || Math.abs(num) < 1) return { color: '#64748b', bg: '#f1f5f9', label: '= ' + change };
  if (num > 0) return { color: '#059669', bg: '#d1fae5', label: '▲ ' + change };
  return { color: '#dc2626', bg: '#fee2e2', label: '▼ ' + change };
}

function fmt(n) {
  return Math.round(n).toLocaleString('en-US');
}

function bucketQueries(queries) {
  const top10 = queries.filter(q => q.position <= 10);
  const mid = queries.filter(q => q.position > 10 && q.position <= 30);
  const low = queries.filter(q => q.position > 30);
  return { top10, mid, low };
}

function renderEmail(r, type) {
  const isCEO = type === 'ceo';
  const title = isCEO
    ? `Dashboard CEO — ${SITE_LABEL}`
    : `Tu informe semanal — ${SITE_LABEL}`;
  const subtitle = isCEO
    ? 'Snapshot semanal: SEO, leads, output del motor automático'
    : 'Cómo vamos posicionando tu página en Google';

  const impDelta = deltaClass(r.changes.impressions);
  const clicksDelta = deltaClass(r.changes.clicks);
  const ctrDelta = deltaClass(r.changes.ctr);
  const posDelta = deltaClass(r.changes.position);

  const buckets = bucketQueries(r.topQueries);
  const maxImp = Math.max(r.current.impressions, r.previous.impressions, 1);

  return `<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8"><title>${title}</title></head>
<body style="margin:0;padding:40px 20px;background:#f4f6fb;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial,sans-serif;color:#0F172A;line-height:1.6;">
<table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td align="center">
<table width="720" cellpadding="0" cellspacing="0" border="0" style="max-width:720px;background:#ffffff;border-radius:16px;overflow:hidden;border:1px solid #e5e9f2;">

<tr><td style="background:linear-gradient(135deg,#0F172A 0%,#1e1b4b 50%,#2563EB 100%);padding:36px 40px;color:#ffffff;">
  <table cellpadding="0" cellspacing="0" border="0" style="margin-bottom:24px;">
    <tr>
      <td width="44" style="padding-right:14px;"><img src="${LOGO_URL}" width="44" height="44" alt="Zenia" style="display:block;border-radius:10px;"></td>
      <td style="font-size:18px;font-weight:700;letter-spacing:3px;color:#ffffff;">ZENIA</td>
    </tr>
  </table>
  <div style="font-size:24px;font-weight:700;color:#ffffff;margin-bottom:8px;">${title}</div>
  <div style="font-size:14px;color:#cbd5e1;">${subtitle}</div>
  <div style="display:inline-block;background:rgba(255,255,255,0.12);border:1px solid rgba(255,255,255,0.2);padding:6px 14px;border-radius:20px;font-size:12px;font-weight:600;margin-top:14px;color:#ffffff;">Semana: ${r.weekRange}</div>
</td></tr>

<tr><td style="padding:32px 40px 0 40px;">
  ${isCEO ? `<table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:linear-gradient(135deg,#7C3AED 0%,#2563EB 100%);border-radius:10px;margin-bottom:24px;"><tr><td style="padding:12px 18px;color:#ffffff;font-size:13px;font-weight:600;">📊 Vista CEO interna · Datos accionables</td></tr></table>` : ''}
  <div style="font-size:15px;color:#334155;line-height:1.7;margin-bottom:28px;">
    Hola ${isCEO ? 'Fabrizzio' : 'Anthony'},<br><br>
    ${isCEO
      ? `Resumen ejecutivo de la semana en <strong style="color:#0F172A;">${SITE_LABEL}</strong>. Clicks ${r.changes.clicks}, CTR ${r.changes.ctr}, posición media ${r.current.position.toFixed(1)}. ${r.newPostsCount} posts publicados.`
      : `Este es tu informe semanal. Cada lunes te cuento cómo va tu página en Google: cuánta gente la está viendo, en qué búsquedas apareces y qué vamos a hacer la próxima semana. Sin tecnicismos.`}
  </div>
</td></tr>

<tr><td style="padding:0 40px 24px 40px;">
  <div style="font-size:16px;font-weight:700;color:#0F172A;margin-bottom:8px;border-left:4px solid #2563EB;padding-left:10px;">${isCEO ? 'KPIs principales' : 'Cómo te fue esta semana'}</div>
  <div style="font-size:13px;color:#64748b;margin-bottom:16px;margin-left:14px;font-style:italic;">${isCEO ? 'Movimientos clave vs la semana anterior.' : 'Las 4 cifras que resumen el estado de tu página en Google.'}</div>
  <table width="100%" cellpadding="0" cellspacing="0" border="0">
    <tr>
      <td width="50%" style="padding-right:7px;padding-bottom:14px;" valign="top">
        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#f8faff;border:1px solid #e0e7ff;border-radius:12px;"><tr><td style="padding:18px;">
          <div style="font-size:12px;color:#475569;font-weight:600;margin-bottom:8px;">${isCEO ? 'Impresiones' : 'Veces que tu web apareció'}</div>
          <div style="font-size:30px;font-weight:800;color:#0F172A;line-height:1;">${fmt(r.current.impressions)}</div>
          <div style="font-size:12px;color:${impDelta.color};font-weight:600;margin-top:8px;">${impDelta.label}</div>
        </td></tr></table>
      </td>
      <td width="50%" style="padding-left:7px;padding-bottom:14px;" valign="top">
        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#f8faff;border:1px solid #e0e7ff;border-radius:12px;"><tr><td style="padding:18px;">
          <div style="font-size:12px;color:#475569;font-weight:600;margin-bottom:8px;">Clicks${isCEO ? '' : ' desde Google'}</div>
          <div style="font-size:30px;font-weight:800;color:#0F172A;line-height:1;">${fmt(r.current.clicks)}</div>
          <div style="font-size:12px;color:${clicksDelta.color};font-weight:600;margin-top:8px;">${clicksDelta.label}</div>
        </td></tr></table>
      </td>
    </tr>
    <tr>
      <td width="50%" style="padding-right:7px;" valign="top">
        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#f8faff;border:1px solid #e0e7ff;border-radius:12px;"><tr><td style="padding:18px;">
          <div style="font-size:12px;color:#475569;font-weight:600;margin-bottom:8px;">${isCEO ? 'CTR' : 'Qué tan alto aparecemos'}</div>
          <div style="font-size:30px;font-weight:800;color:#0F172A;line-height:1;">${isCEO ? r.current.ctr.toFixed(2) + '%' : r.current.position.toFixed(0) + 'º'}</div>
          <div style="font-size:12px;color:${isCEO ? ctrDelta.color : posDelta.color};font-weight:600;margin-top:8px;">${isCEO ? ctrDelta.label : posDelta.label}</div>
        </td></tr></table>
      </td>
      <td width="50%" style="padding-left:7px;" valign="top">
        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#f8faff;border:1px solid #e0e7ff;border-radius:12px;"><tr><td style="padding:18px;">
          <div style="font-size:12px;color:#475569;font-weight:600;margin-bottom:8px;">${isCEO ? 'Posición media' : 'Páginas que Google ya vio'}</div>
          <div style="font-size:30px;font-weight:800;color:#0F172A;line-height:1;">${isCEO ? r.current.position.toFixed(1) : r.sitemapSubmitted}</div>
          <div style="font-size:12px;color:${isCEO ? posDelta.color : '#64748b'};font-weight:600;margin-top:8px;">${isCEO ? posDelta.label : 'En indexación'}</div>
        </td></tr></table>
      </td>
    </tr>
  </table>
</td></tr>

<tr><td style="padding:0 40px 24px 40px;">
  <div style="font-size:16px;font-weight:700;color:#0F172A;margin-bottom:8px;border-left:4px solid #2563EB;padding-left:10px;">${isCEO ? 'Distribución de posicionamiento' : 'Dónde aparecemos en Google'} · ${r.topQueries.length} ${isCEO ? 'queries' : 'búsquedas'}</div>
  <div style="font-size:13px;color:#64748b;margin-bottom:16px;margin-left:14px;font-style:italic;">Listado completo.</div>

  ${buckets.top10.length ? `<table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#f0fdf4;border:1px solid #86efac;border-radius:10px;margin-bottom:12px;"><tr><td style="padding:16px 20px;">
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:10px;"><tr>
      <td style="font-size:14px;font-weight:700;color:#059669;">🟢 ${isCEO ? 'TOP 10 — Primera página' : 'PRIMERA PÁGINA — Posición 1 a 10'}</td>
      <td align="right" style="font-size:14px;font-weight:800;color:#059669;">${buckets.top10.length} ${isCEO ? 'queries' : 'búsquedas'}</td>
    </tr></table>
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#ffffff;border-radius:6px;">
      ${buckets.top10.map(q => `<tr><td style="padding:8px 12px;font-size:13px;color:#334155;border-bottom:1px solid #dcfce7;"><strong>${q.query}</strong></td><td align="right" style="padding:8px 12px;font-size:13px;color:#64748b;border-bottom:1px solid #dcfce7;">${q.impressions} impr</td><td align="right" style="padding:8px 12px;font-size:13px;font-weight:700;color:#059669;border-bottom:1px solid #dcfce7;">pos ${q.position.toFixed(1)}</td></tr>`).join('')}
    </table>
  </td></tr></table>` : ''}

  ${buckets.mid.length ? `<table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#fffbeb;border:1px solid #fcd34d;border-radius:10px;margin-bottom:12px;"><tr><td style="padding:16px 20px;">
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:10px;"><tr>
      <td style="font-size:14px;font-weight:700;color:#d97706;">🟡 ${isCEO ? 'POSICIONES 11–30 — Cerca del top' : 'SEGUNDA-TERCERA PÁGINA — Posición 11 a 30'}</td>
      <td align="right" style="font-size:14px;font-weight:800;color:#d97706;">${buckets.mid.length} ${isCEO ? 'queries' : 'búsquedas'}</td>
    </tr></table>
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#ffffff;border-radius:6px;">
      ${buckets.mid.map(q => `<tr><td style="padding:8px 12px;font-size:13px;color:#334155;border-bottom:1px solid #fef3c7;"><strong>${q.query}</strong></td><td align="right" style="padding:8px 12px;font-size:13px;color:#64748b;border-bottom:1px solid #fef3c7;">${q.impressions} impr</td><td align="right" style="padding:8px 12px;font-size:13px;font-weight:700;color:#d97706;border-bottom:1px solid #fef3c7;">pos ${q.position.toFixed(1)}</td></tr>`).join('')}
    </table>
  </td></tr></table>` : ''}

  ${buckets.low.length ? `<table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#f8fafc;border:1px solid #cbd5e1;border-radius:10px;"><tr><td style="padding:16px 20px;">
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:10px;"><tr>
      <td style="font-size:14px;font-weight:700;color:#475569;">⚪ ${isCEO ? 'POSICIONES 31+ — Subiendo' : 'MÁS ABAJO — Posición 31+ (subiendo)'}</td>
      <td align="right" style="font-size:14px;font-weight:800;color:#475569;">${buckets.low.length} ${isCEO ? 'queries' : 'búsquedas'}</td>
    </tr></table>
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#ffffff;border-radius:6px;">
      ${buckets.low.slice(0, 20).map(q => `<tr><td style="padding:7px 12px;font-size:13px;color:#334155;border-bottom:1px solid #f1f5f9;">${q.query}</td><td align="right" style="padding:7px 12px;font-size:13px;color:#64748b;border-bottom:1px solid #f1f5f9;">${q.impressions} impr</td><td align="right" style="padding:7px 12px;font-size:13px;color:#64748b;border-bottom:1px solid #f1f5f9;">pos ${q.position.toFixed(1)}</td></tr>`).join('')}
    </table>
  </td></tr></table>` : ''}
</td></tr>

<tr><td style="padding:0 40px 24px 40px;">
  <div style="font-size:16px;font-weight:700;color:#0F172A;margin-bottom:16px;border-left:4px solid #2563EB;padding-left:10px;">${isCEO ? 'Decisiones recomendadas' : 'Qué vamos a hacer la próxima semana'}</div>
  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#fefce8;border-left:4px solid #f59e0b;border-radius:8px;"><tr><td style="padding:18px 22px;">
    <div style="font-size:14px;color:#78350f;line-height:1.7;">
      ${buckets.top10.length ? `<strong style="color:#451a03;">1. Reforzar queries en top 10:</strong> ${buckets.top10.slice(0, 2).map(q => `"${q.query}" (pos ${q.position.toFixed(1)})`).join(', ')}. Internal linking + refresh.<br><br>` : ''}
      ${buckets.mid.length ? `<strong style="color:#451a03;">2. Empujar las que están cerca del top 10:</strong> ${buckets.mid.length} queries entre posición 11-30 con potencial de multiplicar clicks x3-5 si entran al top.<br><br>` : ''}
      ${r.sitemapSubmitted > r.sitemapIndexed ? `<strong style="color:#451a03;">3. Acelerar indexación:</strong> ${r.sitemapSubmitted - r.sitemapIndexed} URLs pendientes de procesar por Google.<br><br>` : ''}
      <strong style="color:#451a03;">4. Contenido:</strong> ${r.newPostsCount} posts publicados esta semana. Rutina diaria activa.
    </div>
  </td></tr></table>
</td></tr>

<tr><td style="background:#0F172A;padding:28px 40px;text-align:center;">
  <table cellpadding="0" cellspacing="0" border="0" align="center" style="margin-bottom:12px;"><tr>
    <td width="22" style="padding-right:8px;"><img src="${LOGO_URL}" width="22" height="22" alt="Zenia" style="display:block;border-radius:5px;"></td>
    <td style="color:#e2e8f0;font-weight:600;letter-spacing:2px;font-size:13px;">ZENIA</td>
  </tr></table>
  <div style="color:#94a3b8;font-size:12px;line-height:1.7;">
    Generado automáticamente cada lunes<br>
    <a href="https://zeniapartners.com" style="color:#60a5fa;text-decoration:none;">zeniapartners.com</a><br><br>
    <span style="color:#64748b;font-size:11px;">Este correo es parte de tu servicio con Zenia Partners.</span><br>
    <a href="https://zeniapartners.com/unsubscribe?email=${encodeURIComponent(TO_EMAIL)}" style="color:#64748b;text-decoration:underline;font-size:11px;">Dejar de recibir estos informes</a>
  </div>
</td></tr>

</table></td></tr></table></body></html>`;
}

function renderPlainText(r, type) {
  const isCEO = type === 'ceo';
  const greeting = isCEO ? 'Hola Fabrizzio' : 'Hola Anthony';
  const siteLabel = SITE_LABEL;
  const buckets = bucketQueries(r.topQueries);

  let txt = `${greeting},\n\n`;
  txt += `${isCEO ? 'Dashboard CEO' : 'Tu informe semanal'} de ${siteLabel} — semana ${r.weekRange}\n`;
  txt += '='.repeat(60) + '\n\n';

  txt += 'KPIs PRINCIPALES\n';
  txt += `- Impresiones: ${fmt(r.current.impressions)} (${r.changes.impressions})\n`;
  txt += `- Clicks: ${fmt(r.current.clicks)} (${r.changes.clicks})\n`;
  txt += `- CTR: ${r.current.ctr.toFixed(2)}% (${r.changes.ctr})\n`;
  txt += `- Posicion media: ${r.current.position.toFixed(1)} (${r.changes.position})\n\n`;

  txt += 'POSICIONAMIENTO\n';
  txt += `- Top 10: ${buckets.top10.length} queries\n`;
  txt += `- Posiciones 11-30: ${buckets.mid.length} queries\n`;
  txt += `- Posiciones 31+: ${buckets.low.length} queries\n\n`;

  if (buckets.top10.length) {
    txt += 'QUERIES EN TOP 10:\n';
    buckets.top10.forEach(q => {
      txt += `- ${q.query} (${q.impressions} impr, pos ${q.position.toFixed(1)})\n`;
    });
    txt += '\n';
  }

  if (buckets.mid.length) {
    txt += 'QUERIES POSICIONES 11-30:\n';
    buckets.mid.forEach(q => {
      txt += `- ${q.query} (${q.impressions} impr, pos ${q.position.toFixed(1)})\n`;
    });
    txt += '\n';
  }

  txt += `CONTENIDO PUBLICADO: ${r.newPostsCount} posts nuevos esta semana\n`;
  txt += `INDEXACION: ${r.sitemapIndexed} / ${r.sitemapSubmitted} paginas en Google\n\n`;

  txt += 'Este informe se genera automaticamente cada lunes.\n';
  txt += 'Informe completo en HTML con graficos en la version visual de este correo.\n\n';
  txt += 'Zenia Partners\n';
  txt += 'https://zeniapartners.com\n';
  txt += `Para dejar de recibir estos informes, responde STOP a este correo.\n`;

  return txt;
}

async function sendEmail(html, text, subject) {
  return new Promise((resolve, reject) => {
    const payload = {
      from: FROM_EMAIL,
      to: [TO_EMAIL],
      reply_to: 'reports@zeniapartners.com',
      subject,
      html,
      text,
      headers: {
        'List-Unsubscribe': '<mailto:reports@zeniapartners.com?subject=unsubscribe>, <https://zeniapartners.com/unsubscribe>',
        'List-Unsubscribe-Post': 'List-Unsubscribe=One-Click',
        'Precedence': 'bulk',
        'X-Entity-Ref-ID': `zenia-weekly-${Date.now()}`
      }
    };
    if (BCC_EMAIL) payload.bcc = [BCC_EMAIL];

    const body = JSON.stringify(payload);
    const req = https.request({
      hostname: 'api.resend.com',
      path: '/emails',
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${RESEND_API_KEY}`,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(body)
      }
    }, (res) => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        console.log(`Email status: ${res.statusCode}`);
        console.log(`Response: ${data}`);
        resolve({ status: res.statusCode, body: data });
      });
    });
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

async function main() {
  if (!RESEND_API_KEY) {
    console.error('RESEND_API_KEY not set. Skipping email send.');
    process.exit(0);
  }

  const reportPath = latestReport();
  if (!reportPath) {
    console.error('No report found in', REPORTS_DIR);
    process.exit(1);
  }

  console.log('Parsing report:', reportPath);
  const r = parseReport(reportPath);
  const html = renderEmail(r, REPORT_TYPE);
  const text = renderPlainText(r, REPORT_TYPE);

  const subject = REPORT_TYPE === 'ceo'
    ? `Informe semanal ${SITE_LABEL} — ${r.weekRange}`
    : `Informe semanal ${SITE_LABEL} — ${r.weekRange}`;

  await sendEmail(html, text, subject);
}

main().catch(err => {
  console.error('Fatal:', err);
  process.exit(1);
});
