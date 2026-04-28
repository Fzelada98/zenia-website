# KPI Dashboard — Mayo Blast Campaign

Spec para Google Sheet que trackee la campaña SmartLead Mayo 2026. Te paso las pestañas, columnas, fórmulas, y los benchmarks contra los que comparar.

## Setup

1. Crea un Google Sheet nuevo: "Zenia SmartLead Blast Mayo 2026"
2. Comparte con `fabrizzio.zelada@zeniapartners.com` (read+write)
3. Crea las 4 pestañas siguientes en orden

---

## Pestaña 1: `Resumen`

Vista ejecutiva. Una sola fila por día.

| Columna | Tipo | Fórmula / fuente |
|---|---|---|
| Fecha | Date | manual o link a SmartLead daily export |
| Día campaña | Number | `=A2-DATE(2026,5,4)+1` |
| Emails enviados (día) | Number | from SmartLead daily |
| Emails enviados (acum) | Number | `=SUM(C$2:C2)` |
| Open rate (día) | % | from SmartLead |
| Reply rate (día) | % | from SmartLead |
| Replies positive | Number | manual count after triage |
| Replies negative | Number | manual |
| Replies neutral / "send info" | Number | manual |
| Calls booked | Number | from Calendly |
| Calls ejecutadas | Number | manual after the call |
| Cierres (paid setup) | Number | manual |

**Benchmarks objetivo (compárate contra estos):**

- Open rate ≥ 45% (cold outreach con DKIM bueno)
- Reply rate ≥ 8%
- Reply positive rate ≥ 25% de replies totales
- Booking rate ≥ 50% de positive replies
- Show-up rate (calls ejecutadas / booked) ≥ 85%
- Close rate ≥ 15% de calls ejecutadas
- **Total funnel:** 1.500 emails → 600 opens → 120 replies → 30 positive → 15 booked → 13 calls → 2-3 cierres

---

## Pestaña 2: `Por vertical`

Cruzada vertical × KPI. Identifica qué vertical convierte mejor.

| Vertical | Sent | Opens | Open % | Replies | Reply % | Positive | Booked | Calls | Closed | Close % |
|---|---|---|---|---|---|---|---|---|---|---|
| Restaurantes | | | | | | | | | | |
| Gimnasios | | | | | | | | | | |
| Estética | | | | | | | | | | |
| Ecommerce | | | | | | | | | | |
| **Total** | | | | | | | | | | |

Fórmulas de %: `=Opens/Sent`, `=Replies/Sent`, etc.

**Acciones según resultados:**
- Si un vertical tiene reply rate >2x el promedio: subir volumen ahí en wave 2 (junio)
- Si un vertical tiene reply rate <50% del promedio: pausar, revisar mensajes
- Close rate por vertical >20%: ese es tu vertical hero

---

## Pestaña 3: `Por mercado`

Cruzada ciudad/país × KPI.

| Mercado | Sent | Opens | Open % | Replies | Reply % | Calls | Closed |
|---|---|---|---|---|---|---|---|
| Madrid | | | | | | | |
| Barcelona | | | | | | | |
| Bogotá | | | | | | | |
| Lima | | | | | | | |
| CDMX | | | | | | | |

**Sirve para:** decidir dónde escalar wave 2 (más Apify allocation al mercado que mejor performance).

Hipótesis a validar:
- Madrid tendrá el mejor Open rate (DKIM bien configurado, dominio España, audiencia receptiva)
- Bogotá puede tener mejor Reply rate (mercado menos saturado de cold email)
- Lima/CDMX bajos por baja calidad de emails extraídos

---

## Pestaña 4: `Pipeline activo`

Lista de leads que respondieron positive o booked. Tu CRM minimalista durante el blast.

| Fecha | Empresa | Vertical | Mercado | Email | Status | Próxima acción | Notas |
|---|---|---|---|---|---|---|---|

**Status options (data validation dropdown):**
- Replied (positive)
- Replied (info request)
- Booked call
- Call done — pendiente propuesta
- Propuesta enviada
- Negociando
- Cerrado (paid)
- Cerrado (lost)
- Nurture (junio)

**Próxima acción:** texto libre con fecha. Ej: "29/04 — mandar caso de Glow", "04/05 — call 16:00", "10/05 — follow-up propuesta"

---

## Automatización opcional (si tienes tiempo el sábado)

SmartLead permite exportar daily metrics en CSV. Puedes:

1. Crear Google Apps Script que cada día tire de SmartLead API y rellene Pestaña 1 + 2 + 3
2. O hacerlo manual diario (5 min al día con coffee)

API Smartlead: https://api.smartlead.ai/api-reference (free tier permite consultas de tu propia campaña)

---

## Rituales recomendados

**Daily (5 min, mañana):** revisar Pestaña 1 día anterior. ¿Algo fuera de benchmark? ¿Alguna respuesta sin actuar > 4h?

**Cada 3 días (15 min):** revisar Pestañas 2 y 3. ¿Algún vertical/mercado fuera de patrón? ¿Pausar/escalar?

**Semanal (30 min, domingo):** revisar Pestaña 4. ¿Pipeline está moviéndose o está estancado? Identificar leads "Replied (info)" sin acción >5 días → empujar.

**Día 11 mayo:** decisión KEEP/CANCEL Workspace + SmartLead. Ver `project_workspace_trial_cancel.md`.
