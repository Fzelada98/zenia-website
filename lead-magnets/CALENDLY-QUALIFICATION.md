# Calendly Pre-Call Qualification Form

5 preguntas para añadir al booking form de Calendly. Sirven dos propósitos:

1. **Filtrar tire-kickers** (gente que reserva sin intención real). El backend agent solo dispara research si las respuestas son sustanciales (filtro `QUALITY_MIN_PRESENCE_CHARS=30`)
2. **Pre-cargar contexto** para que llegues a la call ya con script personalizado generado por Haiku basado en sus respuestas

## Cómo configurarlas en Calendly

1. Ir a Calendly → Event Type "30 min" → Edit
2. Ir a sección "Invitee Questions"
3. Borrar las preguntas default si tienes alguna genérica
4. Añadir las 5 siguientes en este orden exacto

---

## Pregunta 1 (REQUIRED)

**Tipo:** Short Text
**Label:** ¿Cuál es el nombre de tu empresa?
**Required:** Yes

> Mapea al campo `company` del webhook backend.

---

## Pregunta 2 (REQUIRED)

**Tipo:** Single Select (Dropdown)
**Label:** ¿En qué sector operas?
**Required:** Yes
**Opciones:**
- Restaurantes / hostelería
- Gimnasios / fitness
- Centros de estética / belleza / spa
- Ecommerce / tienda online
- Peluquerías / salones
- Hoteles / turismo
- Servicios profesionales (consultoría, despacho, salud, etc.)
- Retail físico
- Otros

> Mapea al campo `area` del webhook (renombrar/ajustar VALID_AREAS en server.js si es necesario).

---

## Pregunta 3 (REQUIRED)

**Tipo:** Single Select (Dropdown)
**Label:** ¿Cuántos empleados tiene tu empresa?
**Required:** Yes
**Opciones:**
- Solo yo / autónomo
- 2-10 empleados
- 11-50 empleados
- 51-200 empleados
- 200+ empleados

> Mapea al campo `size` del webhook.

---

## Pregunta 4 (REQUIRED — esta es la que filtra calidad)

**Tipo:** Long Text (Paragraph)
**Label:** Cuéntame en 2-3 líneas: ¿qué problema concreto te gustaría resolver con un agente de IA + WhatsApp? (cuanto más específico, mejor preparo la call)
**Required:** Yes
**Min characters:** 30 (forces real answer)

> Mapea al campo `onlinePresence` del webhook. **CRÍTICO:** el filtro A+C del backend skipea Haiku si esto es <30 chars. Forzar respuesta sustancial garantiza que solo leads serios disparan el agent.

---

## Pregunta 5 (OPTIONAL pero recomendada)

**Tipo:** Single Select (Dropdown)
**Label:** ¿Cuándo te gustaría empezar (si todo encaja)?
**Required:** No
**Opciones:**
- Esta semana / lo antes posible
- En 2-4 semanas
- En 1-3 meses
- Solo estoy investigando, sin urgencia

> No mapea a webhook actual pero sirve para ti como señal de urgencia. Si "esta semana" → priorizar la call. Si "solo investigando" → call de bajo esfuerzo, mover a nurture.

---

## Resultado esperado

- **Tire-kickers** que solo querían "ver qué es esto" → no llenan pregunta 4 con sustancia → backend skipea Haiku → no waste de tokens
- **Leads serios** → llenan los 5 campos completos → backend dispara research personalizado → tú llegas a la call con script Haiku-generated en email + briefing específico al problema que dijeron

## Métricas a trackear

- % de bookings que pasan el filtro de calidad (esperado: 60-75%)
- % bookings que terminan en call ejecutada (no-show rate, esperado: <15%)
- % calls ejecutadas que se cierran en 30 días (esperado: 15-25% mes 1, sube con seguimiento)

## Si no quieres tocar Calendly directamente

Alternativa: en lugar de Calendly nativo, redirigir el lead a un mini-form en zeniapartners.com/agenda que llene los 5 campos, mande al webhook backend, y SOLO si pasan el filtro vea el embed de Calendly. Más fricción pero filtrado total.
