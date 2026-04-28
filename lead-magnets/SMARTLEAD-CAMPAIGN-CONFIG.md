# SmartLead Campaign Configuration — Mayo Blast 2026

Setup paso a paso para configurar las 4 campañas en SmartLead (una por vertical). Lanzamiento programado **lunes 4 mayo 2026, 09:00 hora local del lead**.

## Antes de configurar

- ✅ DKIM/SPF/DMARC verificado PASS en zeniapartners.com
- ✅ Inbox warmup `fabrizzio.zenia.outreach@gmail.com` 100%
- ✅ CSV final: `C:\Users\Usuario\Downloads\zenia-prospects-FINAL.csv` (post personalize_outreach.py)
- ✅ Lead magnets live en zeniapartners.com/lead-magnets/{vertical}.html

## Estrategia: 4 campañas separadas (1 por vertical)

**Razón:** SmartLead permite custom merge fields por campaña, sequence custom, subject lines distintos. Una sola campaña con condicionales por vertical sería más complejo y daría peor visibilidad de KPIs por vertical en el dashboard nativo.

---

## Configuración común (las 4 campañas)

### Sender setup
- **From email:** fabrizzio.zelada@zeniapartners.com
- **From name:** Fabrizzio Zelada
- **Reply-to:** misma
- **Tracking:** opens ON, link clicks ON, **OPENS PIXEL OFF en email 1** (algunos clients flagean cold con pixel; opens en FU2 y FU3 sí ON para medir)

### Daily volume + ramp (post-warmup)

| Día campaña | Día semana | Sends/day cap |
|---|---|---|
| 1 (4 mayo) | Lunes | 30 |
| 2-3 | Martes-Miércoles | 50 |
| 4-5 | Jueves-Viernes | 75 |
| 6+ | Lunes onwards | 100 |

**Reasoning:** ramp gradual aún post-warmup. Subir directo de 0 a 100 puede flagear inbox aunque warmup esté al 100%.

### Sending window
- **L-V 09:00-13:00** hora local del prospect (timezone matching auto en SmartLead)
- **NO sábados ni domingos** (cold B2B en finde tiene 60% peor open rate)
- **No festivos del país** del prospect (configurar holiday calendar en SmartLead)

### Sequence stop conditions
- ✅ Stop on reply (any reply)
- ✅ Stop on link click + open (interpret as "interesado, no insistir")
- ✅ Stop on bounce (hard bounce → unsubscribe automático)
- ✅ Stop on unsubscribe link click

### Spintax en subject lines
- Activar **Subject A/B test** con la sintaxis `{Plantilla|Recurso|Material} gratis`
- SmartLead rota automáticamente y reporta cuál variant performance mejor

### Reply detection
- ✅ AI reply categorization ON (positive / negative / out-of-office / unsubscribe)
- ✅ Webhook a tu inbox principal `fabrizzio.zelada@zeniapartners.com` para replies positive (response time crítico)

---

## Campaña 1: RESTAURANTES

### Audiencia
- Filter CSV: `vertical = "restaurantes"`
- Esperado: ~48 prospects (Barcelona 45 + Lima 3)
- **Submkts:** Barcelona dominante, Lima residual

### Sequence
| Email | Día | Subject (spintax A/B) | Body source |
|---|---|---|---|
| Email 1 | Day 0 | `{Plantilla\|Recurso\|Material} gratis para tu restaurante en {city}` | HOOK-A-TEMPLATES.md → RESTAURANTES Body |
| Email 2 | Day 4 | `Re: {Plantilla\|Recurso\|Material} gratis para tu restaurante en {city}` | HOOK-A → Follow-up Email 2 |
| Email 3 | Day 7 | `Última pregunta sobre {company_name}` | HOOK-A → Follow-up Email 3 |

### Custom fields a mapear desde CSV
- `{first_name}` (puede estar vacío)
- `{first_name_with_space}` → conditional: si first_name → " " + first_name, else → ""
- `{company_name}` ← `company_name`
- `{vertical}` ← "restaurantes"
- `{city}` ← `city`
- `{country}` ← `country`
- `{custom_opener}` ← `custom_opener`

---

## Campaña 2: GIMNASIOS

### Audiencia
- Filter: `vertical = "gimnasios"`
- Esperado: ~124 prospects (Madrid 86 + Bogotá 38)
- **El más fuerte por volumen.** Doble peso en la wave.

### Sequence
| Email | Día | Subject | Body |
|---|---|---|---|
| Email 1 | Day 0 | `{Plantilla\|Recurso\|Material} gratis para tu gimnasio en {city}` | HOOK-A → GIMNASIOS Body |
| Email 2 | Day 4 | `Re: {Plantilla\|Recurso\|Material} gratis para tu gimnasio en {city}` | HOOK-A → Follow-up 2 |
| Email 3 | Day 7 | `Última pregunta sobre {company_name}` | HOOK-A → Follow-up 3 |

---

## Campaña 3: ESTÉTICA

### Audiencia
- Filter: `vertical = "estetica"`
- Esperado: ~88 prospects (Madrid 56 + Bogotá 30 + CDMX 2)

### Sequence
| Email | Día | Subject | Body |
|---|---|---|---|
| Email 1 | Day 0 | `{Plantilla\|Recurso\|Material} gratis para tu centro de estética en {city}` | HOOK-A → ESTÉTICA Body |
| Email 2 | Day 4 | `Re: {Plantilla\|Recurso\|Material} gratis para tu centro de estética en {city}` | HOOK-A → Follow-up 2 |
| Email 3 | Day 7 | `Última pregunta sobre {company_name}` | HOOK-A → Follow-up 3 |

**Nota:** lead magnet específico ya disponible en `/lead-magnets/estetica.html` (ya no apunta a restaurantes).

---

## Campaña 4: ECOMMERCE

### Audiencia
- Filter: `vertical = "ecommerce"`
- Esperado: ~39 prospects (Madrid 39, CDMX descartado)

### Sequence
| Email | Día | Subject | Body |
|---|---|---|---|
| Email 1 | Day 0 | `{Plantilla\|Recurso\|Material} gratis carritos abandonados {company_name}` | HOOK-A → ECOMMERCE Body |
| Email 2 | Day 4 | `Re: {Plantilla\|Recurso\|Material} para recuperar carritos {company_name}` | HOOK-A → Follow-up 2 |
| Email 3 | Day 7 | `Última pregunta sobre {company_name}` | HOOK-A → Follow-up 3 |

---

## QA antes de lanzar (sábado-domingo)

1. **Test sends:** desde SmartLead, mandar 1 email de cada campaña a 3 inboxes propios:
   - tu email principal Gmail (`zeladauriartef@gmail.com`)
   - un Outlook si tienes
   - un Yahoo si tienes
   
   Verificar:
   - Llegan a Inbox (no Spam ni Promociones)
   - Variables {company_name} {city} {custom_opener} se reemplazan correctamente
   - Links Calendly funcionan
   - Lead magnet links abren correctamente
   - From name aparece como "Fabrizzio Zelada" no como email raw

2. **Spam score check:** SmartLead tiene built-in spam analyzer. Score objetivo: <2 (10 = todo spam, 0 = perfecto)

3. **Preview rendering:** SmartLead muestra preview en mobile + desktop. Revisar que no haya emojis raros, líneas cortadas

4. **Suppression list global:** importar tu lista de suppress (gente que ya unsubscribed previamente, gmail propios, dominios competidores). Si no tienes lista previa, mínimo añadir:
   - tu email personal
   - dominios de competidores (zenvia.com, manychat.com, sirena.app, gupshup.io, etc)
   - cualquier @gmail/@hotmail/@yahoo personal (cold B2B solo a empresas)

---

## Métricas a watch en primeros 3 días

| Métrica | Verde | Amarillo | Rojo (pausar) |
|---|---|---|---|
| Open rate | >45% | 35-45% | <35% |
| Reply rate | >8% | 4-8% | <4% |
| Bounce rate | <2% | 2-4% | >4% |
| Spam complaint | 0 | <0.1% | >0.1% |

**Si rojo:** pausar campaña, investigar (probable problema con subject line, contenido, o lista). NO seguir mandando con métricas rojas — quema reputación inbox.

---

## Post-campaña (día 12 mayo, fin de blast)

1. Export full metrics CSV de SmartLead
2. Llenar Pestaña 1, 2, 3 del KPI Dashboard
3. Decidir KEEP/CANCEL SmartLead Pro + Workspace según `project_workspace_trial_cancel.md`
4. Si reply rate fue >8%: planificar wave 2 junio (escalar el vertical/mercado ganador)
5. Si fue <8%: revisar HOOK-A templates, considerar A/B test con nuevo subject + opener strategy
