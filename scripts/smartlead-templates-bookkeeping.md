# SmartLead Templates — AI Bookkeeping for Transfer-Heavy SMBs

**Pivot date:** 2026-05-04
**Vertical:** Automated bookkeeping + accounts payable for SMBs receiving Zelle / wire transfers
**Case study live:** https://zeniapartners.com/cases/whatsapp-bookkeeping-importer.html

---

## TEMPLATE A — Importadora directa (Yenifer-style)

**Subject options:**
- Quick question about [Company]
- Reconciling Zelle screenshots manually?
- For [Industry] importers receiving wire transfers
- 6 hours per week back

**Body:**

```
Hi [First Name],

Saw you run [Company] importing [product/category] from [LATAM origin] into [US city].

Most owners I talk to in cross-border import spend 6+ hours per week reconciling Zelle screenshots, supplier invoices and Excel. Books always one week behind reality.

We just shipped a case study where a cross-border importer replaced all of that with a WhatsApp-native AI bookkeeper. Captures go in, books update live, three cash buckets calculated automatically: bank, capital in transit (trucks/inventory), and receivables. No more late-night Excel reconciliation.

Case here: https://zeniapartners.com/cases/whatsapp-bookkeeping-importer.html

30 min call to see if it fits how [Company] operates?

Best,
Fabrizzio
Zenia Partners
zeniapartners.com
```

**Follow-up #1 (3 days later):**

```
Hi [First Name],

Following up. The piece that hits hardest with importers is the cash traceability across three buckets — most owners I talk to can't tell at any given moment what's sitting in the bank vs locked in trucks vs owed by clients.

If reconciling that takes you more than an hour a week, worth a 30 min call.

Calendly: https://calendly.com/zeladauriartef/30min

Fabrizzio
```

**Follow-up #2 (7 days later):**

```
Hi [First Name],

Last note from me. If WhatsApp screenshots and Excel are still the spine of your bookkeeping, you're leaving hours and visibility on the table.

We're running pilots with import businesses now. If you want to see what the dashboard looks like for an importer your size, reply with "demo" and I'll send a 90-second video.

Fabrizzio
```

---

## TEMPLATE B — Restaurante multi-proveedor / Catering / Bodega

**Subject options:**
- Paying 5+ suppliers per week?
- For restaurants with daily supplier payments
- Manual accounts payable killing margins?

**Body:**

```
Hi [First Name],

Quick note. Restaurants and food businesses like [Company] typically pay 5-10 suppliers per week, manage Zelle from clients, and reconcile it all manually.

We just published a case study where an SMB receiving daily transfers replaced their entire manual bookkeeping with a WhatsApp-native AI assistant. Captures go in, books update in real time, accounts payable + receivables tracked automatically.

Case here: https://zeniapartners.com/cases/whatsapp-bookkeeping-importer.html

Restaurants have the same operational pattern: high transaction volume, multiple categories (suppliers, payroll, taxes, deliveries), and the owner spending nights catching up on Excel.

30 min call?

Best,
Fabrizzio
Zenia Partners
```

---

## TEMPLATE C — Contador / Bookkeeper (channel partner)

**Subject options:**
- For accountants serving Hispanic SMBs
- Differentiate your bookkeeping practice with AI
- 5% revenue share for referrals

**Body:**

```
Hi [First Name],

You serve PYMEs that probably send you screenshots of Zelle, photos of invoices, and Excel sheets that don't quite match. End-of-month reconciliation eating your hours.

We built an AI bookkeeping assistant tailored for that exact client profile: WhatsApp-native, Spanish-fluent (including regional slang), live Google Sheets dashboard, three cash buckets calculated automatically. Your clients send screenshots like they would to a friend; you receive clean books at month-end.

Two ways to engage:

1. Use it for your own practice (1 client, 1 instance) — $1,500 setup
2. Refer your existing clients and earn 5% setup commission per close. Standard Zenia partner program

Case study showing the system in action: https://zeniapartners.com/cases/whatsapp-bookkeeping-importer.html

30 min call to see if this fits your client base?

Best,
Fabrizzio
Zenia Partners
zeniapartners.com
```

---

## Apify queries específicas

### LinkedIn Sales Navigator (apify.com/curious_coder/linkedin-sales-navigator)

**Búsqueda 1 — Importadoras LATAM USA:**
- Job titles: Owner, Founder, CEO, Managing Director, President
- Industries: Import & Export, Wholesale, Food & Beverages
- Geography: Miami FL, Doral FL, Hialeah FL, Houston TX, Atlanta GA, Orlando FL, Tampa FL, New York NY, Newark NJ, Los Angeles CA
- Company size: 1-50 employees
- Keywords in profile/company: "import", "distribuidora", "Venezolana", "Colombiana", "LATAM", "Hispanic"

**Búsqueda 2 — Restaurantes con scale:**
- Job titles: Owner, GM, Operations Manager
- Industries: Restaurants, Food Services, Catering
- Geography: same diaspora cities
- Company size: 11-50 employees (suficiente para tener proveedor + payroll)
- Keywords: "Latin", "Hispanic", "Venezuelan", "Colombian", "Peruvian"

**Búsqueda 3 — Contadores boutique (canal):**
- Job titles: Owner, Founder, Partner, CPA, Accountant, Bookkeeper
- Industries: Accounting, Financial Services
- Geography: Miami, Houston, Atlanta + Lima, Bogotá, CDMX
- Keywords: "small business", "bookkeeping", "PYME", "Hispanic", "Latin"

### Apify scrapers complementarios

- **Google Maps Scraper** (compass/google-maps-scraper): "wholesale distributor [city]", "importer [city]", "freight forwarder [city]"
- **Yellow Pages USA scraper**: "import-export companies [state]"
- **Crunchbase scraper**: small import companies con funding < $5M (suelen ser SMB ideales)

---

## Apify allocation revisada (900 prospects, $4.50)

| Mercado | Vertical | Prospects | Tier |
|---|---|---|---|
| Miami / Doral | Importadoras LATAM | 200 | 1 |
| Houston | Importadoras / Distribuidoras | 150 | 1 |
| Atlanta | Importadoras / Distribuidoras | 100 | 1 |
| Orlando / Tampa | Importadoras / Bodegas | 80 | 1 |
| NYC / NJ | Importadoras LATAM | 100 | 1 |
| LA / SoCal | Distribuidoras Hispanic | 70 | 1 |
| Miami / Houston | Restaurantes / Catering Hispanic | 50 | 2 |
| Lima / Bogotá / CDMX | Contadores boutique PYME | 50 | 3 (channel) |
| Miami / Houston / Atlanta | Bookkeepers freelance | 100 | 3 (channel) |

Total: 900 prospects. Tier 1 (importadoras directas) = 700. Tier 3 (canal) = 150. Tier 2 (restaurantes) = 50.

---

## Pre-flight checklist antes de cargar a SmartLead

1. ✅ Apify sacar 900 prospects con queries de arriba
2. ✅ Limpiar duplicados, validar emails (NeverBounce o similar)
3. ✅ Segmentar por Tier 1/2/3 → 3 secuencias SmartLead distintas
4. ✅ Cada secuencia: cold email + follow-up 1 (3 días) + follow-up 2 (7 días)
5. ✅ A/B test subject lines: prefiere mention nombre empresa vs pain genérico
6. ✅ Track replies en CRM o Sheet, marcar warm/hot leads para call-prep agent
7. ✅ Si reply rate > 8% → buen producto-mercado fit, escalar volumen
8. ✅ Si reply rate < 4% → re-iterar copy, posiblemente segmentar más fino

---

## Métricas target (10-day blast)

- Volumen: 50→100 emails/día con ramp gradual = ~820 emails total
- Reply rate target: 6-10% (700 importadoras directas son lead caliente, esperado mayor que CRM gimnasios genérico)
- Call book target: 3-5% de los replies → 5-8 calls
- Close target: 25-40% calls → **2-3 closes en mayo**
- Plus: 1-2 channel partners (contadores) interesados → multiplicador futuro
