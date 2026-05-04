# Loom Recording Cheatsheet — Walk-through 90 seg

**Marca demo:** OLIVAR DEL SUR (importadora ficticia de aceite de oliva)
**Cliente del demo:** Carmen Alvarez (ficticia)

> Marca y nombres son inventados a proposito para no confundir con clientes reales (Yenifer / Golden Oil). El video es publico, no debe haber datos reales.

---

## 1. Setup previo (5 min, una sola vez)

### a) Subir el Sheet demo a Drive

1. Tenes el archivo en: `c:\Users\Usuario\AI\zenia-website\posts\demo-sheet-for-loom.xlsx`
2. Abri Google Drive en el navegador.
3. Click derecho en cualquier carpeta → "Subir archivos" → seleccionalo.
4. Cuando termine, click derecho → "Abrir con" → "Hojas de calculo de Google".
5. Drive lo convierte a Sheet nativo. Renombralo en Drive a **"OLIVAR DEL SUR · Repositorio Zelle"** (eso aparece en la grabacion arriba).
6. Dejalo abierto en una pestaña, **arranca en la pestaña "Portada"**.

### b) Abrir las 4 capturas Zelle/Wire

Estan listas en `c:\Users\Usuario\AI\zenia-website\posts\`:
- `zelle-fake-01-maria.png` — Maria Gonzalez $500 (la "magic" del demo)
- `zelle-fake-02-carlos.png` — Carlos Perez $700
- `zelle-fake-03-lucia.png` — Lucia Ramirez $650
- `wire-fake-04-andes.png` — Wire saliente $2,800 a Logistica Andes

Abrilas todas en el visor de imagenes de Windows en orden. Vas a ir alternando entre ellas durante el video.

### c) WhatsApp Web abierto (opcional)

- web.whatsapp.com → cualquier chat (no se ve el contenido, solo el header).
- Sirve para mostrar 1 segundo "asi llega la captura".

### d) Loom

- Extension Chrome de Loom (loom.com/download).
- Modo **"Screen + Cam"** → tu cara aparece como burbuja en la esquina inferior derecha.
- Resolucion HD (1080p).

---

## 2. Antes de darle REC

- Cerrá Slack, Telegram, mail, notificaciones del sistema.
- Tene 3 ventanas abiertas:
  - **Pestaña Chrome 1:** Google Sheets (OLIVAR DEL SUR · Repositorio Zelle), pestaña "Portada"
  - **Pestaña Chrome 2:** WhatsApp Web (opcional)
  - **Visor de imagenes** con las 4 capturas
- Test 5 segundos primero: audio + tu cara visible en la burbuja.

---

## 3. Script con marcas de tiempo (ESPAÑOL)

> **TIP:** No leas. Memoriza los 5 puntos clave abajo y habla natural.

### [0:00 – 0:10] Hook (camara solo, sin compartir)

> "Hola, soy Fabrizzio de Zenia. Si tu negocio recibe pagos por Zelle o transferencia y aun cuadras los libros a mano, este video es para vos. Te muestro en 90 segundos como trabaja una de nuestras clientas."

### [0:10 – 0:25] Demo: el Sheet vivo (Portada)

**ACCION:** comparti pantalla, pestaña Portada del Sheet. Visibles: logo OLIVAR DEL SUR + EFECTIVO TRAZADO TOTAL + 3 buckets + KPIs + alertas.

> "Esto es el repositorio vivo de Olivar del Sur, una importadora de aceite de oliva. Mira: arriba el efectivo total trazado, los tres buckets de cash, los KPIs del mes, las alertas operativas. Esto se actualiza solo cuando le llega un pago."

### [0:25 – 0:40] Demo problema → captura llega

**ACCION:** alt+tab al visor de imagenes, mostra `zelle-fake-01-maria.png` (Maria Gonzalez $500).

> "Le llega esta captura de Bank of America. Maria Gonzalez le mando 500 dolares por aceite de oliva. Antes ella copiaba esto a Excel a mano. Ahora simplemente lo reenvia al WhatsApp de la asistente como si se lo mandara a una amiga. Sin app, sin login, sin formulario."

**(opcional 2 seg)** alt+tab a WhatsApp Web → "asi le llega":
> "Lo reenvia aca, listo."

### [0:40 – 1:00] Demo magia → resultado en Sheet

**ACCION:** volve al Sheet, click en pestaña **"Transacciones"**. Apunta con cursor a la PRIMERA FILA (Maria Gonzalez $500 cobro_cliente con Conf# ABC123XYZ).

> "En menos de 8 segundos, la asistente lee la captura, identifica el cliente, el monto, el codigo de confirmacion, la categoriza correctamente entre 16 categorias contables, valida que no sea duplicada, y la escribe aca."

**ACCION:** click en pestaña **"Cashflow"** → muestra el grafico de cashflow diario.

> "Y todo lo que entra alimenta el cashflow diario. Aca ves la curva acumulada del mes."

**ACCION:** click vuelta a **"Portada"** → pointer a los 3 buckets.

> "Y los tres buckets se recalculan solos: cuanto tiene en banco, cuanto esta en gandolas, cuanto le deben. Cero data-entry."

### [1:00 – 1:20] Diferenciadores rapidos

**ACCION:** mostra otras 2-3 capturas rapido (alt+tab):
- `zelle-fake-02-carlos.png` ($700)
- `zelle-fake-03-lucia.png` ($650)
- `wire-fake-04-andes.png` ($2,800 wire saliente)

> "Da igual el banco, da igual si es Zelle, wire o transferencia. Si es ingreso o gasto. Da igual el monto. La asistente las procesa todas igual."

**ACCION:** click en pestaña **"Deudas"**.

> "Tracker de prestamos con interes mensual, exposicion neta, audit log con timestamp para revision fiscal."

**ACCION:** volve a camara (cierra share o aumenta tu burbuja).

> "Nuestra clienta paso de seis horas semanales en Excel a cero. Esto es lo que hacemos en Zenia: asistentes de IA personalizadas para tu operacion especifica."

### [1:20 – 1:30] Cierre + CTA

> "Si tu negocio recibe Zelle o transferencias y aun las cuadras a mano, agenda una llamada de 30 minutos en el link debajo. Te muestro que se veria con tus capturas reales. Hasta pronto."

---

## 4. Despues de grabar

1. Loom genera el link automatico cuando le das stop.
2. Edicion opcional: corta silencios al inicio/final.
3. Configura thumbnail: elegi un frame con el Sheet visible (Portada con buckets) o tu cara hablando.
4. **Mandame el link.** Yo lo embebo en:
   - 30 landings programaticas (`/en/ai-bookkeeping-importer-*` y `/es/contabilidad-ia-importadora-*`)
   - Case study principal (`/cases/whatsapp-bookkeeping-importer.html`)
   - Lead magnet thank-you page (`/lead-magnets/cashflow-importer.html`)
   - Templates SmartLead (reemplazo del placeholder `[LOOM_LINK]`)
   - Email signature (opcional)

---

## 5. Tiempo total para vos

- Setup: 5 min
- 1 grabacion buena: 2 min
- Buffer si re-grabas: 5 min
- **Total: 10-15 min maximo**

---

## 6. Que NO hacer

- No improvises cifras que no esten en el Sheet.
- No uses nombres de clientes reales (Yenifer, Golden Oil, etc). El demo dice **OLIVAR DEL SUR** y **Carmen Alvarez** a proposito.
- No prometas 100% precision. Decí "menos de 8 segundos" y "categoriza entre 16 categorias" sin claim absoluto.
- No te pases de 1:30 min. Si pasaste de 1:40, regraba.

---

## 7. Version INGLES

Esta en [loom-walkthrough-script.md](loom-walkthrough-script.md) bajo "SCRIPT VERSION INGLES". Mismo timing, mismas acciones, brand OLIVAR DEL SUR.
