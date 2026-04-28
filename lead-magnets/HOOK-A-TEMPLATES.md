# Hook A Email Templates — SmartLead Campaigns

Templates de cold email para SmartLead. Usan custom fields del CSV final (post-personalize_outreach.py).

**Variables disponibles:**
- `{first_name}` — primer nombre del owner si lo tenemos (else "")
- `{company_name}` — nombre del negocio
- `{vertical}` — restaurantes / gimnasios / estética / ecommerce
- `{city}` — Madrid / Bogotá / Lima / Barcelona / CDMX
- `{country}` — España / Colombia / Perú / México
- `{custom_opener}` — frase personalizada generada por Claude Haiku

**Reglas globales:**
- Tildes y eñes siempre
- TUTEAR (cold email B2B)
- Sin em-dashes
- No la palabra "chatbot"
- Sin aperturas de fluff ("hoy en día", "en el mundo actual")

---

## RESTAURANTES

**Subject A:** Plantilla gratis para tu restaurante en {city}
**Subject B:** {company_name}: 47 mensajes WhatsApp listos para usar

**Body:**
```
Hola{first_name_with_space},

{custom_opener}

Soy Fabrizzio, fundador de Zenia Partners.

Vemos que muchos restaurantes en {city} pierden entre 3.000 y 8.000 EUR al mes por dos cosas: no-shows (3.3% media España 2025 según TheFork) y respuestas lentas en WhatsApp e Instagram.

Te paso una plantilla con 47 mensajes pre-armados de WhatsApp para restaurantes que cubre confirmación de reserva, recordatorios 24h y 1h, recuperación de cancelaciones, upselling de menú y petición de reseñas post-visita. La usan 200+ restaurantes en España y LATAM.

Sin captura de email, sin compromiso:
https://zeniapartners.com/lead-magnets/restaurantes.html

Si después de probarla quieres que un agente de IA personalizado los responda automático 24/7 conectado a tu WhatsApp Business, escríbeme y lo vemos.

Un saludo,
Fabrizzio Zelada
Founder · Zenia Partners
zeniapartners.com
```

**Follow-up Email 2 (4 días si no abrió/respondió):**

**Subject:** Re: {Plantilla|Recurso|Material} gratis para tu restaurante en {city}

```
Hola{first_name_with_space},

Reboto por si se te pasó.

La plantilla sigue aquí: https://zeniapartners.com/lead-magnets/restaurantes.html

Si quieres ver cómo aplicaría a {company_name} con un agente de IA personalizado conectado a tu WhatsApp, agendamos 30 min sin compromiso:
https://calendly.com/zeladauriartef/30min

Si los no-shows o WhatsApp no son tu prioridad ahora, dímelo y lo dejo en "más adelante" sin insistir.

Un saludo,
Fabrizzio
```

**Follow-up Email 3 (7 días):**

**Subject:** Última pregunta sobre {company_name}

```
{first_name},

Tres opciones para cerrar esto sin más mensajes:

1. La plantilla te interesó pero no es momento → respondes "junio" y te escribo entonces
2. No te interesa Zenia → respondes "stop" y no insisto
3. Sigues interesado → agenda 30 min aquí: https://calendly.com/zeladauriartef/30min

Cualquiera vale. Sin presión.

Fabrizzio
```

---

## GIMNASIOS

**Subject A:** Plantilla gratis para tu gimnasio en {city}
**Subject B:** {company_name}: 47 mensajes WhatsApp para retención de socios

**Body:**
```
Hola{first_name_with_space},

{custom_opener}

Soy Fabrizzio, fundador de Zenia Partners.

La retención anual en gimnasios de {country} cayó al 66.4% en 2025 (HFA Benchmarking Report). 1 de cada 3 socios cancela cada año, y la mitad lo hace en los primeros 90 días. La causa principal: cero seguimiento personalizado entre la primera visita y los primeros 30 días.

Te paso una plantilla con 47 mensajes pre-armados de WhatsApp para gimnasios que cubre onboarding del nuevo socio, alertas de churn por inactividad, reactivación de socios en pausa, programa de referidos automatizado y renovación con upselling.

Sin captura de email, sin compromiso:
https://zeniapartners.com/lead-magnets/gimnasios.html

Si después de probarla quieres un agente de IA personalizado conectado a tu WhatsApp Business 24/7, escríbeme.

Un saludo,
Fabrizzio Zelada
Founder · Zenia Partners
zeniapartners.com
```

**Follow-up 2:**
```
{first_name},

¿Te sirvió la plantilla para retención de socios?

Si todavía no la has mirado: https://zeniapartners.com/lead-magnets/gimnasios.html

Si la retención no es prioridad ahora, dímelo y lo dejo para junio.

Saludos,
Fabrizzio
```

**Follow-up 3:**
```
{first_name}, último mensaje sobre {company_name}.

Si quieres que te mande un caso real de un gimnasio en {city} que subió retención 12 puntos en 90 días, respondes "caso" y te lo paso por aquí en 1 mensaje.

Si no, sin problema. Saludos.

Fabrizzio
```

---

## ESTÉTICA / BELLEZA

**Subject A:** Plantilla gratis para tu centro de estética en {city}
**Subject B:** {company_name}: 47 mensajes WhatsApp para fidelización

**Body:**
```
Hola{first_name_with_space},

{custom_opener}

Soy Fabrizzio, fundador de Zenia Partners.

Captar una clienta nueva en estética cuesta 5-7 veces más que retener una. Y el 80% de centros invierten en Instagram ads para nuevas mientras descuidan a las leales.

Te paso una plantilla con 47 mensajes pre-armados de WhatsApp para centros de estética que cubre confirmación de cita, recordatorios pre-cita, upselling de tratamientos complementarios, programa de fidelización por puntos, reactivación de clientas inactivas y petición de reseñas.

Sin captura de email, sin compromiso:
https://zeniapartners.com/lead-magnets/estetica.html

Si después de probarla quieres un agente de IA personalizado conectado a tu WhatsApp Business, escríbeme.

Un saludo,
Fabrizzio Zelada
Founder · Zenia Partners
zeniapartners.com
```

**Follow-up Email 2 (4 días):**

**Subject:** Re: {Plantilla|Recurso|Material} gratis para tu centro de estética en {city}

```
Hola{first_name_with_space},

Reboto por si se te pasó.

La plantilla sigue aquí: https://zeniapartners.com/lead-magnets/estetica.html

Si quieres ver cómo aplicaría a {company_name} con un agente de IA personalizado para fidelización y reactivación de clientas, agendamos 30 min sin compromiso:
https://calendly.com/zeladauriartef/30min

Si la fidelización no es prioridad ahora, dímelo y lo dejo en "más adelante" sin insistir.

Un saludo,
Fabrizzio
```

**Follow-up Email 3 (7 días):**

**Subject:** Última pregunta sobre {company_name}

```
{first_name},

Tres opciones para cerrar esto sin más mensajes:

1. La plantilla te interesó pero no es momento → respondes "junio" y te escribo entonces
2. No te interesa Zenia → respondes "stop" y no insisto
3. Sigues interesado → agenda 30 min aquí: https://calendly.com/zeladauriartef/30min

Cualquiera vale. Sin presión.

Fabrizzio
```

---

## ECOMMERCE

**Subject A:** Plantilla gratis carritos abandonados {company_name}
**Subject B:** Recuperar 30% de carritos abandonados con WhatsApp ({city})

**Body:**
```
Hola{first_name_with_space},

{custom_opener}

Soy Fabrizzio, fundador de Zenia Partners.

Las tiendas online pierden entre el 70 y 78% de los carritos iniciados (Baymard 2025). Eso es ingreso que se va sin que nadie lo recupere.

Te paso una plantilla con 47 mensajes pre-armados de WhatsApp para ecommerce que cubre atención pre-venta y dudas, recuperación de carritos abandonados (secuencia de 3 toques), confirmación y seguimiento de pedido, upselling post-compra, programa VIP, reactivación de inactivos y recuperación de clientes en riesgo de churn.

Sin captura de email, sin compromiso:
https://zeniapartners.com/lead-magnets/ecommerce.html

Si después de probarla quieres que un agente de IA personalizado conectado a tu Shopify, WooCommerce o Tiendanube los responda automático 24/7, escríbeme.

Un saludo,
Fabrizzio Zelada
Founder · Zenia Partners
zeniapartners.com
```

**Follow-up Email 2 (4 días):**

**Subject:** Re: {Plantilla|Recurso|Material} para recuperar carritos {company_name}

```
Hola{first_name_with_space},

Reboto por si se te pasó.

La plantilla sigue aquí: https://zeniapartners.com/lead-magnets/ecommerce.html

Si quieres ver cómo aplicaría a {company_name} con un agente de IA personalizado conectado a tu tienda online (Shopify, WooCommerce, Tiendanube) y a tu WhatsApp, agendamos 30 min sin compromiso:
https://calendly.com/zeladauriartef/30min

Si recuperación de carritos no es prioridad ahora, dímelo y lo dejo en "más adelante" sin insistir.

Un saludo,
Fabrizzio
```

**Follow-up Email 3 (7 días):**

**Subject:** Última pregunta sobre {company_name}

```
{first_name},

Tres opciones para cerrar esto sin más mensajes:

1. La plantilla te interesó pero no es momento → respondes "junio" y te escribo entonces
2. No te interesa Zenia → respondes "stop" y no insisto
3. Sigues interesado → agenda 30 min aquí: https://calendly.com/zeladauriartef/30min

Cualquiera vale. Sin presión.

Fabrizzio
```

---

## NOTAS DE CONFIGURACIÓN EN SMARTLEAD

1. **Variables custom CSV:** mapear `{first_name}` `{company_name}` `{vertical}` `{city}` `{country}` `{custom_opener}` desde el CSV final.

2. **`{first_name_with_space}`:** truco para que cuando first_name esté vacío no quede "Hola ," — en SmartLead se hace con conditional logic: si first_name existe → " " + first_name, else → "".

3. **Spintax en subject:** rotar A/B con la sintaxis `{Plantilla|Recurso|Material} gratis` para no triggear filtros antispam.

4. **Schedule sending:** L-V 9:00-17:00 hora del país del prospect. SmartLead lo hace automático con timezone matching.

5. **Daily ramp post-warmup:** 50 → 80 → 100/día max, suba gradual.

6. **Reply tracking:** SmartLead detecta auto-reply y respuestas reales, separa en buckets para procesar.
