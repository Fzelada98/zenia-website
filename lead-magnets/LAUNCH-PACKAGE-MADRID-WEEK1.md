# Launch Package — SmartLead Madrid Gimnasios Week 1

**Lanzamiento:** Lunes 4 mayo 2026, 09:00 CEST (Madrid)
**Strategy:** Opción B Ultra-micro
**Target:** 15 prospects Madrid gimnasios (top calidad, dedup por email)

## CSV listo para subir

**Path:** `C:\Users\Usuario\Downloads\zenia-MADRID-GYM-WEEK1.csv`

15 prospects, columnas SmartLead-ready:
- email, first_name, company_name, vertical, city, country, website, phone, category, rating, reviews_count, google_url, instagram_url, custom_opener

## Daily ramp Week 1

| Día | Volumen | Total acumulado | Decision criteria |
|---|---|---|---|
| Lun 4 may | **5** | 5 | Watch spam rate fin del día |
| Mar 5 may | 5 | 10 | Si spam <10% día 1 → continuar; si >10% → PAUSE |
| Mié 6 may | 5 | 15 (todos enviados) | Email 1 completo |
| Jue 7 may | 0 (gap) | 15 | Esperar respuestas + analizar |
| Vie 8 may | 0 (gap) | 15 | Si reply rate >5% → continuar week 2 |
| Lun 11 may | Email 2 (5/día) | hasta cubrir | Empezar follow-up 2 |

## Sequence: 3 emails Hook A Gimnasios

### EMAIL 1 — Day 0

**Subject (spintax A/B):**
```
{Plantilla|Recurso|Material} gratis para tu gimnasio en Madrid
```

**Body:**
```
Hola{first_name_with_space},

{custom_opener}

Soy Fabrizzio, fundador de Zenia Partners.

La retención anual en gimnasios de España cayó al 66.4% en 2025 (HFA Benchmarking Report). 1 de cada 3 socios cancela cada año, y la mitad lo hace en los primeros 90 días. La causa principal: cero seguimiento personalizado entre la primera visita y los primeros 30 días.

Te paso una plantilla con 47 mensajes pre-armados de WhatsApp para gimnasios que cubre onboarding del nuevo socio, alertas de churn por inactividad, reactivación de socios en pausa, programa de referidos automatizado y renovación con upselling.

Sin captura de email, sin compromiso:
https://zeniapartners.com/lead-magnets/gimnasios.html

Si después de probarla quieres un agente de IA personalizado conectado a tu WhatsApp Business 24/7, escríbeme.

También construimos CRMs y SaaS a medida si tu operativa tiene necesidades específicas (gestión de socios, integración con software de control de acceso, módulos de retención avanzados, dashboards de churn por cohorte, etc).

Un saludo,
Fabrizzio Zelada
Founder · Zenia Partners
zeniapartners.com
```

### EMAIL 2 — Day 4 (jueves 8 mayo si lanzas lunes)

**Subject (spintax):**
```
Re: {Plantilla|Recurso|Material} gratis para tu gimnasio en Madrid
```

**Body:**
```
{first_name},

¿Te sirvió la plantilla para retención de socios?

Si todavía no la has mirado: https://zeniapartners.com/lead-magnets/gimnasios.html

Si quieres ver cómo aplicaría a {company_name} con un agente de IA personalizado conectado a tu WhatsApp, agendamos 30 min sin compromiso:
https://calendly.com/zeladauriartef/30min

Si la retención no es prioridad ahora, dímelo y lo dejo para junio.

Saludos,
Fabrizzio
```

### EMAIL 3 — Day 7 (lunes 11 mayo)

**Subject:**
```
Última pregunta sobre {company_name}
```

**Body:**
```
{first_name},

Tres opciones para cerrar esto sin más mensajes:

1. La plantilla te interesó pero no es momento → respondes "junio" y te escribo entonces
2. No te interesa Zenia → respondes "stop" y no insisto
3. Sigues interesado → agenda 30 min aquí: https://calendly.com/zeladauriartef/30min

Cualquiera vale. Sin presión.

Fabrizzio
```

## SmartLead Campaign Config

### Sender
- **From email:** fabrizzio.zelada@zeniapartners.com
- **From name:** Fabrizzio Zelada
- **Reply-to:** misma

### Tracking
- **Open tracking:** OFF para Email 1 (algunos providers flagean cold con pixel)
- **Open tracking:** ON para Email 2 y 3
- **Link clicks:** ON todos
- **Custom tracking domain:** si lo configura SmartLead, mejor

### Daily volume
- Cap: **5 emails/día** semana 1
- Sending window: **L-V 09:00-13:00 CEST** (timezone matching auto)
- NO sábados ni domingos

### Sequence stop conditions
- ✅ Stop on reply (any reply)
- ✅ Stop on link click + open
- ✅ Stop on bounce
- ✅ Stop on unsubscribe link click

### Reply detection
- ✅ AI reply categorization ON
- ✅ Webhook a fabrizzio.zelada@zeniapartners.com para replies positive

### Custom fields a mapear
- `{first_name}` ← first_name (puede estar vacío)
- `{first_name_with_space}` ← conditional: si first_name → " " + first_name, else → ""
- `{company_name}` ← company_name
- `{custom_opener}` ← custom_opener

### Suppression list global (importar antes de lanzar)
- tu email personal: zeladauriartef@gmail.com
- dominios competidores: manychat.com, sirena.app, gupshup.io, zenvia.com
- gmail/hotmail/yahoo personales (cold B2B solo a empresas)

## QA Pre-Launch (10 min, hacer domingo 3 mayo noche)

### 1. Test sends a tu inbox personal
- SmartLead → campaign → "Send test email" → tu Gmail (zeladauriartef@gmail.com)
- Email debe llegar en **< 30 segundos**
- **CRÍTICO:** debe llegar a **Inbox**, NO a Spam ni Promociones
  - Si llega Spam → PARA, no lances. Spam rate 100% = dominio quemado en 1 hora
  - Si llega Promociones → tolerable pero subóptimo
  - Si llega Inbox → ok, lanza

### 2. Verificar variables se reemplazan
- En el test send, comprobar:
  - `{first_name_with_space}` aparece como " Pepe" o vacío (no "Hola{first_name_with_space}")
  - `{company_name}` se reemplaza
  - `{custom_opener}` aparece la frase Haiku
- Si alguna no se reemplaza → revisar mapping CSV columns en SmartLead

### 3. Verificar links
- Click en link lead-magnet → abre `zeniapartners.com/lead-magnets/gimnasios.html` ✅
- Click en link Calendly → abre booking page ✅

### 4. Verificar firma
- "Fabrizzio Zelada" aparece como nombre, NO email raw
- "Zenia Partners" aparece en footer
- "zeniapartners.com" link clickeable

### 5. Spam score check
- SmartLead built-in spam analyzer → score objetivo: <2 (10 = todo spam)

### 6. Schedule confirmar
- Lunes 4 mayo, 09:00 CEST
- 5 emails ese día
- Cap diario 5

## Métricas a watch primer día (lunes 4 mayo EOD)

| Métrica | Verde | Amarillo | Rojo (PAUSAR) |
|---|---|---|---|
| Bounce rate | <2% | 2-4% | >4% |
| Open rate | >40% | 30-40% | <30% |
| Reply rate | n/a (esperar 24h) | n/a | >0 unsubscribe |
| Spam complaint | 0 | <1 | >1 |

**Si rojo en cualquiera:** pausar campaña inmediato, replantear.

## Decisión continuar / pausar week 2

**Lunes 11 mayo (después de 1 semana data):**
- Reply rate >5% (1+ replies) → continuar Email 2 + escalar a 10/día Madrid
- Reply rate 2-5% → continuar Email 2 a mismo volumen 5/día
- Reply rate <2% → PAUSAR + investigar (mensaje? targeting? domain?)

## Si firma 1 cliente esta semana

Mover a `project_zenia_first_client.md`. Activar:
- Workspace + SmartLead trial decision: KEEP (pagar Pro $39)
- Plan beta default B (1.591€ 3m + bonus reactivación)
- Retainer mes 2 a 297€/mes empieza después de mes 1 gratis

## Si NO firma esta semana

- Domingo 10 mayo: revisar funnel completo
- Decidir launch wave 2 con learnings (subject lines, opener variations, segmentation)
- Trial expira lunes 11. Decisión KEEP/CANCEL basada en métricas.
