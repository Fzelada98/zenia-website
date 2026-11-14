#!/usr/bin/env python3
"""ZENIA v2 (rebrand nov-2026, estilo producto): portada ES y páginas por nicho.

Uso: python3 scripts/rebrand-v2/build.py <raíz_del_sitio> [--preview]
  --preview  escribe en <raíz>/v2/es/... con noindex (para revisar antes de publicar)
  sin flag   escribe la portada en <raíz>/es/index.html y los nichos en <raíz>/es/<nicho>/index.html
Siempre copia z2.css y z2.js a <raíz>/assets/z2/ con ?v=<epoch>.
Contenido: solo cifras de casos reales (GWB, Throwin' Salt); las conversaciones y el panel son de un
negocio de EJEMPLO y lo dicen."""
import html
import json
import os
import shutil
import sys
import time
import urllib.parse

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(sys.argv[1])
PREVIEW = '--preview' in sys.argv
V = str(int(time.time()))
PRE = '/v2' if PREVIEW else ''
E = lambda s: html.escape(str(s), quote=True)
WA_NUM = '34677612799'
CALENDLY = 'https://calendly.com/zeladauriartef/30min'
CF = 'eceeed460f6d465bba3b970417d5f6b0'


def wa(texto):
    return f'https://wa.me/{WA_NUM}?text=' + urllib.parse.quote(texto)


MARK = ('<svg viewBox="0 0 140 140" aria-hidden="true"><defs><linearGradient id="zb" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#2563EB"/><stop offset="1" stop-color="#3B82F6"/></linearGradient>'
        '<linearGradient id="zv" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#6366F1"/>'
        '<stop offset="1" stop-color="#7C3AED"/></linearGradient></defs>'
        '<rect width="140" height="140" rx="30" fill="#111A2E"/>'
        '<path d="M70 18Q18 18 18 38v19q0 6 6 6h64Z" fill="url(#zb)"/>'
        '<path d="M70 122q52 0 52-20V83q0-6-6-6H52Z" fill="url(#zv)"/></svg>')
MARK_SOLO = MARK.replace('<rect width="140" height="140" rx="30" fill="#111A2E"/>', '').replace('id="zb"', 'id="zb2"').replace('id="zv"', 'id="zv2"').replace('url(#zb)', 'url(#zb2)').replace('url(#zv)', 'url(#zv2)')
WA_ICO = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.47 14.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.16-.17.2-.35.22-.64.07-.3-.15-1.26-.46-2.39-1.47-.88-.79-1.48-1.76-1.65-2.06-.17-.3-.02-.46.13-.6.13-.14.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.03-.52-.07-.15-.67-1.61-.92-2.2-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.8.37-.27.3-1.04 1.02-1.04 2.48s1.07 2.88 1.21 3.07c.15.2 2.1 3.2 5.08 4.49.71.31 1.26.49 1.7.63.71.22 1.36.19 1.87.12.57-.09 1.76-.72 2-1.41.25-.7.25-1.29.18-1.41-.08-.13-.27-.2-.57-.35M12.05 21.79h-.01a9.87 9.87 0 0 1-5.03-1.38l-.36-.21-3.74.98 1-3.65-.24-.37a9.86 9.86 0 0 1-1.51-5.26c0-5.45 4.44-9.88 9.89-9.88 2.64 0 5.12 1.03 6.99 2.9a9.83 9.83 0 0 1 2.89 6.99c0 5.45-4.44 9.88-9.88 9.88M20.46 3.49A11.82 11.82 0 0 0 12.05 0C5.5 0 .16 5.34.16 11.89c0 2.1.55 4.14 1.59 5.95L.06 24l6.3-1.65a11.88 11.88 0 0 0 5.68 1.45h.01c6.55 0 11.89-5.34 11.89-11.89 0-3.18-1.24-6.17-3.48-8.42"/></svg>')
PLAY = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="m10 8 6 4-6 4z" fill="currentColor"/></svg>'
ICO = {
    'clinica': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 3c-2 0-3.5 1.6-3.5 4 0 3 1.4 4.6 2.3 8.3.5 2 1 5.7 2.4 5.7 1.6 0 1.3-5 3.8-5s2.2 5 3.8 5c1.4 0 1.9-3.7 2.4-5.7.9-3.7 2.3-5.3 2.3-8.3 0-2.4-1.5-4-3.5-4-1.9 0-2.9 1-5 1S8.9 3 7 3z"/></svg>',
    'taller': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94z"/></svg>',
    'autoescuela': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="2"/><path d="M12 14v7M10 11.5 3.5 9.5M14 11.5l6.5-2"/></svg>',
}
INTEG = json.load(open(os.path.join(AQUI, 'iconos-integraciones.json'), encoding='utf-8'))

# ---------------------------------------------------------------- datos de ejemplo (WhatsApp vivo)
NEGOCIOS = {
    'clinica': {
        'nombre': 'Clínica dental · ejemplo', 'inicial': 'C', 'vertical': 'clinica',
        'saludo': '¡Hola! Soy el asistente de la clínica. Te ayudo con citas, precios y horarios. ¿Qué necesitas?',
        'cita': {'chip': 'Pedir cita', 'p': 'Hola, quería pedir cita para una limpieza dental',
                 'intro': '¡Claro! Te busco hueco para la limpieza. Tengo estos:', 'servicio': 'limpieza dental'},
        'preguntas': [
            {'p': '¿La primera visita tiene coste?', 'r': 'La primera visita es gratis: te revisa el dentista y sales con el presupuesto por escrito. ¿Te busco hueco?'},
            {'p': '¿Abrís los sábados?', 'r': 'Sí, los sábados de 10:00 a 14:00. Entre semana, de 9:30 a 20:30 sin cerrar a mediodía.'},
            {'p': '¿Se puede pagar la ortodoncia a plazos?', 'r': 'Sí, puedes pagarla en cuotas. Te lo detallamos en la primera visita, con el presupuesto delante.'},
            {'p': 'Me duele mucho una muela', 'r': 'Siento que estés así. Aviso ahora a recepción para que te llamen y te den la primera hora libre de hoy.'},
        ]},
    'taller': {
        'nombre': 'Taller mecánico · ejemplo', 'inicial': 'T', 'vertical': 'taller',
        'saludo': '¡Hola! Soy el asistente del taller. Te doy precios, citas y te digo cómo va tu coche. ¿En qué te ayudo?',
        'cita': {'chip': 'Pedir cita en el taller', 'p': 'Quiero llevar el coche a revisión esta semana',
                 'intro': 'Perfecto, te busco hueco para la revisión. Tengo estos:', 'servicio': 'revisión del coche'},
        'preguntas': [
            {'p': '¿Cuánto cuesta cambiar el aceite?', 'r': 'Depende del motor y del aceite que lleve. Pásame marca, modelo y año y te digo el precio exacto.'},
            {'p': '¿Tenéis coche de sustitución?', 'r': 'Sí, para reparaciones de más de un día y según disponibilidad. Te lo reservo junto con la cita si lo necesitas.'},
            {'p': '¿Hacéis pre-ITV?', 'r': 'Sí: lo revisamos antes de que pases la ITV y te decimos qué hay que arreglar. ¿Te reservo hueco?'},
            {'p': '¿Está listo mi coche? Es el 1234 KLM', 'r': 'Le paso tu matrícula al jefe de taller para que te confirme cómo va. En cuanto me conteste, te escribo por aquí.'},
        ]},
    'autoescuela': {
        'nombre': 'Autoescuela · ejemplo', 'inicial': 'A', 'vertical': 'autoescuela',
        'saludo': '¡Hola! Soy el asistente de la autoescuela. Te cuento precios, packs y cómo matricularte. ¿Qué necesitas?',
        'cita': {'chip': 'Quiero apuntarme', 'p': 'Hola, quiero sacarme el carné B',
                 'intro': '¡Genial! Te reservo una visita para hacer la matrícula. Tengo estos huecos:', 'servicio': 'visita para la matrícula del carné B'},
        'preguntas': [
            {'p': '¿Cuánto cuesta el carné B?', 'r': 'Tenemos packs con teórico y prácticas. Te mando el precio de cada uno y lo que incluye, para que elijas el tuyo.'},
            {'p': '¿El teórico se puede hacer online?', 'r': 'Sí: tests desde el móvil y, si quieres, clases en la autoescuela por la tarde.'},
            {'p': '¿Cuántas prácticas voy a necesitar?', 'r': 'Depende de cada alumno. Lo vemos en la primera práctica y te decimos cuántas te recomendamos.'},
            {'p': 'Quiero cambiar mi examen de fecha', 'r': 'Eso lo gestiona secretaría con la DGT. Les paso tu nombre y te llaman hoy para ver la nueva fecha.'},
        ]},
}

GUION = {
    'clinica': {'nombre': 'Clínica dental · ejemplo', 'pasos': [
        ('El paciente escribe por WhatsApp', 'A cualquier hora. También a las 23:40, cuando ya has cerrado.'),
        ('El agente contesta con tu información', 'Tratamientos, precios, horarios y sedes de tu web, con tu tono.'),
        ('Ofrece huecos reales de tu agenda', 'Lee tu calendario y propone solo horas libres.'),
        ('Reserva y lo apunta en tu CRM', 'La cita queda en la agenda y en la ficha del paciente, sin teclear nada.'),
        ('Recuerda la cita el día antes', 'Y si el paciente no puede venir, la cambia por el mismo chat.'),
        ('Lo clínico pasa a tu equipo', 'Dolor, urgencias o dudas médicas: aviso a recepción con la conversación entera.')],
        'mensajes': [
            {'dir': 'tag', 't': 'Lunes · 23:40', 'paso': 0},
            {'dir': 'in', 't': 'Hola, ¿tenéis cita para una limpieza esta semana?', 'paso': 0},
            {'dir': 'out', 't': '¡Hola! Sí. La limpieza dura unos 30 minutos y la primera visita es gratis. ¿Mejor por la mañana o por la tarde?', 'paso': 1},
            {'dir': 'in', 't': 'Por la tarde', 'paso': 1},
            {'dir': 'out', 't': 'Tengo estos huecos en Chamberí:', 'botones': ['Jueves 17:00', 'Jueves 18:30', 'Viernes 17:30'], 'elegido': 0, 'paso': 2},
            {'dir': 'in', 't': 'Jueves 17:00. Laura Gómez', 'paso': 2},
            {'dir': 'out', 't': 'Hecho, Laura: limpieza el jueves a las 17:00 en Chamberí. Ya está en la agenda.', 'paso': 3},
            {'dir': 'tag', 't': 'Miércoles · 18:00', 'paso': 4},
            {'dir': 'out', 't': 'Hola, Laura: te recuerdo tu cita de mañana a las 17:00. Contesta «sí» para confirmarla o dime si necesitas cambiarla.', 'paso': 4},
            {'dir': 'in', 't': 'Sí. Por cierto, me sangran un poco las encías, ¿es normal?', 'paso': 5},
            {'dir': 'out', 't': 'Mejor que lo vea la higienista mañana. Le paso tu mensaje para que lo tenga en cuenta en la visita.', 'paso': 5},
        ]},
    'taller': {'nombre': 'Taller mecánico · ejemplo', 'pasos': [
        ('El cliente escribe por WhatsApp', 'Mientras tú estás debajo de un coche.'),
        ('El agente pide lo que necesita', 'Marca, modelo, año y matrícula, antes de dar un precio.'),
        ('Ofrece huecos reales del taller', 'Por centro y por tipo de trabajo.'),
        ('Reserva y lo apunta en tu CRM', 'La cita y el coche quedan en la ficha del cliente.'),
        ('Avisa cuando el coche está listo', 'Tu equipo lo marca como terminado y el cliente recibe el aviso.'),
        ('Lo complicado pasa al jefe de taller', 'Averías raras, quejas o garantías, con la conversación entera.')],
        'mensajes': [
            {'dir': 'tag', 't': 'Martes · 8:05', 'paso': 0},
            {'dir': 'in', 't': 'Buenas, ¿cuánto me cobráis por cambiar las pastillas de freno?', 'paso': 0},
            {'dir': 'out', 't': '¡Buenas! Para darte el precio exacto, ¿me dices marca, modelo y año del coche?', 'paso': 1},
            {'dir': 'in', 't': 'Seat León de 2019', 'paso': 1},
            {'dir': 'out', 't': 'Gracias. Te paso el presupuesto con las pastillas delanteras y la mano de obra. ¿Quieres que te reserve hueco?', 'paso': 2},
            {'dir': 'out', 't': 'Tengo estos huecos:', 'botones': ['Miércoles 9:00', 'Miércoles 16:30', 'Jueves 11:00'], 'elegido': 0, 'paso': 2},
            {'dir': 'in', 't': 'Miércoles a las 9. Matrícula 1234 KLM', 'paso': 3},
            {'dir': 'out', 't': 'Reservado: miércoles a las 9:00, Seat León 1234 KLM, cambio de pastillas.', 'paso': 3},
            {'dir': 'tag', 't': 'Miércoles · 12:40', 'paso': 4},
            {'dir': 'out', 't': 'Tu Seat León ya está listo para recoger. Abrimos hasta las 19:00.', 'paso': 4},
            {'dir': 'in', 't': 'Genial. Oye, ¿podéis mirar también un ruido raro en la dirección?', 'paso': 5},
            {'dir': 'out', 't': 'Se lo comento al jefe de taller ahora para que le eche un vistazo cuando vengas.', 'paso': 5},
        ]},
    'autoescuela': {'nombre': 'Autoescuela · ejemplo', 'pasos': [
        ('El futuro alumno escribe', 'A las once de la noche, después de mirar tres autoescuelas.'),
        ('El agente contesta precios y packs', 'Los de tu web, con lo que incluye cada uno.'),
        ('Le reserva la matrícula', 'Con huecos reales de secretaría.'),
        ('Lo apunta en tu CRM', 'Con el pack que le interesa y cómo te encontró.'),
        ('Hace seguimiento', 'Si no se matricula, le escribe a los días con lo que preguntó.'),
        ('Lo de la DGT pasa a secretaría', 'Exámenes, tasas y casos especiales, con la conversación entera.')],
        'mensajes': [
            {'dir': 'tag', 't': 'Jueves · 22:55', 'paso': 0},
            {'dir': 'in', 't': 'Hola! Cuánto cuesta sacarse el B con vosotros?', 'paso': 0},
            {'dir': 'out', 't': '¡Hola! Tenemos tres packs con teórico y prácticas. Te mando el precio de cada uno y lo que incluye 👇', 'paso': 1},
            {'dir': 'in', 't': 'Me interesa el de 15 prácticas', 'paso': 1},
            {'dir': 'out', 't': 'Buena elección. Para matricularte, pásate por la oficina con el DNI. Tengo estos huecos:', 'botones': ['Viernes 18:00', 'Lunes 11:00', 'Lunes 19:00'], 'elegido': 0, 'paso': 2},
            {'dir': 'in', 't': 'Viernes a las 6. Soy Marta Ruiz', 'paso': 3},
            {'dir': 'out', 't': 'Apuntada, Marta: viernes a las 18:00 en secretaría, pack de 15 prácticas.', 'paso': 3},
            {'dir': 'tag', 't': 'Viernes · 10:00', 'paso': 4},
            {'dir': 'out', 't': 'Hola, Marta: te esperamos hoy a las 18:00. Recuerda traer el DNI.', 'paso': 4},
            {'dir': 'in', 't': 'Vale. Y si ya suspendí el teórico en otra autoescuela, ¿cambia algo?', 'paso': 5},
            {'dir': 'out', 't': 'Eso te lo explica secretaría con tu caso delante. Les paso tu pregunta para que lo tengan listo esta tarde.', 'paso': 5},
        ]},
}

NICHOS = {
    'clinica': {
        'slug': 'clinicas', 'menu': 'Clínicas', 'sector': 'Clínica', 'quien': 'pacientes',
        'title': 'Agente de IA para el WhatsApp de tu clínica dental o estética | Zenia',
        'desc': 'Un agente de IA en el WhatsApp de tu clínica: responde al momento, reserva por sede y especialidad, recuerda la cita y pasa lo clínico a tu equipo.',
        'label': 'Para clínicas dentales y estéticas',
        'h1': ('Tu clínica contesta, cita y recuerda', 'sin dejar a nadie en visto'),
        'lead': 'Un agente de IA en el WhatsApp de tu clínica que responde al momento con tus tratamientos, precios y horarios, reserva en tu agenda por sede y te pasa lo clínico. Tu recepción deja de vivir pegada al móvil.',
        'tarjeta': ('Clínicas dentales y estéticas', 'Citas, primeras visitas, presupuestos y recordatorios, sin dejar pacientes en visto.',
                    ['Reserva por sede y especialidad', 'Recordatorio el día antes', 'Lo clínico, siempre a tu equipo'],
                    '¿Tenéis cita para una limpieza esta semana?', 'Sí, el jueves a las 17:00 en Chamberí. ¿Te la reservo?'),
        'dolor_h2': 'Lo que pasa hoy en el WhatsApp de una clínica',
        'dolores': [('Horas punta', 'El teléfono suena mientras atiendes en el mostrador, y el WhatsApp se acumula.'),
                    ('Fuera de horario', 'Los mensajes de la noche y del fin de semana se contestan el lunes, cuando el paciente ya ha pedido cita en otra clínica.'),
                    ('Varias sedes', 'Cada clínica con su número y sus horarios: el paciente pregunta en la que no es y nadie le contesta.')],
        'feats_h2': 'Lo que hace el agente en tu clínica',
        'feats': [('Reserva por sede y especialidad', 'Propone huecos libres de la clínica y del profesional que toca.'),
                  ('Primera visita y presupuesto', 'Explica cómo es la primera visita y qué incluye, con tu información.'),
                  ('Recordatorios y cambios de cita', 'Recuerda la cita el día antes y la cambia por el mismo chat.'),
                  ('Lo clínico, a tu equipo', 'Nunca diagnostica: dolor, urgencias y dudas médicas pasan a recepción.'),
                  ('Ficha del paciente en el CRM', 'Cada conversación, cita y tratamiento de interés, en su ficha.'),
                  ('Reseñas después de la visita', 'Si quieres, pide la reseña de Google cuando el paciente sale contento.')],
        'faqs': [('¿El agente da diagnósticos o consejos médicos?', 'No. Contesta lo administrativo (citas, precios, horarios, sedes, financiación) y todo lo clínico pasa a tu equipo con la conversación entera.'),
                 ('¿Se conecta con mi programa de gestión de la clínica?', 'Depende del programa. Si permite conectarse, lo conectamos; si no, el agente trabaja con un calendario compartido y tu equipo confirma. Lo vemos en la demo con tu caso.'),
                 ('¿Y si tengo varias clínicas?', 'El agente sabe qué sede le queda mejor a cada paciente y reserva en la agenda de esa sede. Puede ser un solo número para todas o uno por clínica.')]},
    'taller': {
        'slug': 'talleres', 'menu': 'Talleres', 'sector': 'Taller', 'quien': 'clientes',
        'title': 'Agente de IA para el WhatsApp de tu taller o centro de neumáticos | Zenia',
        'desc': 'Un agente de IA en el WhatsApp de tu taller: pide marca y modelo, da presupuestos con tus precios, reserva hueco por centro y avisa cuando el coche está listo.',
        'label': 'Para talleres y centros de neumáticos',
        'h1': ('Tu taller da presupuestos y citas por WhatsApp', 'mientras tú estás con el coche'),
        'lead': 'Un agente de IA en el WhatsApp de tu taller que pide marca, modelo y matrícula, contesta con tus precios, reserva hueco por centro y avisa al cliente cuando el coche está listo. Tú sigues trabajando.',
        'tarjeta': ('Talleres y neumáticos', 'Presupuestos, citas de taller y avisos de «tu coche está listo».',
                    ['Pide marca, modelo y matrícula', 'Huecos de taller por centro', 'Aviso cuando el coche está listo'],
                    '¿Cuánto me cobráis por las pastillas de freno?', '¿Me dices marca, modelo y año? Te paso el precio exacto.'),
        'dolor_h2': 'Lo que pasa hoy en el WhatsApp de un taller',
        'dolores': [('Manos ocupadas', 'No se puede contestar el móvil con las manos en el motor, y el cliente que pregunta precio no espera.'),
                    ('Presupuestos a medias', 'Preguntan cuánto cuesta sin decir el coche, y el ida y vuelta se queda a mitad.'),
                    ('¿Está listo mi coche?', 'Llamadas y mensajes que interrumpen el trabajo para preguntar lo mismo.')],
        'feats_h2': 'Lo que hace el agente en tu taller',
        'feats': [('Pide los datos del coche', 'Marca, modelo, año y matrícula antes de dar un precio.'),
                  ('Precios y ofertas de tu web', 'Contesta con tus tarifas y tus promociones vigentes, nada inventado.'),
                  ('Huecos de taller por centro', 'Reserva según el tipo de trabajo y el centro que le queda cerca.'),
                  ('Aviso de «tu coche está listo»', 'Tu equipo lo marca como terminado y el cliente recibe el aviso.'),
                  ('Recordatorios de ITV y revisiones', 'Le escribe cuando le toca, con hueco para reservar.'),
                  ('Lo complicado, al jefe de taller', 'Averías raras, garantías o quejas pasan a una persona.')],
        'faqs': [('¿Da precios aunque cada coche sea distinto?', 'Da los precios que publicas y, para el resto, pide los datos del coche y prepara el presupuesto con tus tarifas. Lo que no sabe, lo pasa a tu equipo en vez de inventarlo.'),
                 ('¿Puede avisar cuando el coche está listo?', 'Sí. Tu equipo marca el trabajo como terminado en el CRM (o en tu programa, si se puede conectar) y el agente avisa al cliente por WhatsApp.'),
                 ('¿Sirve para varios talleres?', 'Sí: sabe qué centro hace cada trabajo y reserva en la agenda de ese centro.')]},
    'autoescuela': {
        'slug': 'autoescuelas', 'menu': 'Autoescuelas', 'sector': 'Autoescuela', 'quien': 'alumnos',
        'title': 'Agente de IA para el WhatsApp de tu autoescuela | Zenia',
        'desc': 'Un agente de IA en el WhatsApp de tu autoescuela: contesta precios y packs, reserva la matrícula y las prácticas y hace seguimiento a quien preguntó y no se apuntó.',
        'label': 'Para autoescuelas',
        'h1': ('Tu autoescuela matricula por WhatsApp', 'también a las once de la noche'),
        'lead': 'Un agente de IA en el WhatsApp de tu autoescuela que contesta precios y packs, reserva la matrícula y las prácticas, y escribe de nuevo a quien preguntó y no se apuntó. Secretaría se queda con lo importante.',
        'tarjeta': ('Autoescuelas', 'Matrículas, precios de carné y prácticas, contestados al momento.',
                    ['Precios y packs de tu web', 'Reserva de matrícula y prácticas', 'Seguimiento a quien no se apuntó'],
                    'Hola! Cuánto cuesta sacarse el B?', 'Tenemos tres packs. Te mando el precio de cada uno 👇'),
        'dolor_h2': 'Lo que pasa hoy en el WhatsApp de una autoescuela',
        'dolores': [('Las mismas preguntas', 'Precio del carné, packs, horarios del teórico: lo mismo, cien veces al mes.'),
                    ('Preguntan y no vuelven', 'Quien escribe a las once de la noche compara tres autoescuelas y se queda con la primera que contesta.'),
                    ('Prácticas a mano', 'Cambios de práctica y avisos que se gestionan uno a uno por WhatsApp.')],
        'feats_h2': 'Lo que hace el agente en tu autoescuela',
        'feats': [('Precios y packs', 'Contesta con los packs de tu web y lo que incluye cada uno.'),
                  ('Matrícula y documentación', 'Explica qué traer y reserva la visita a secretaría.'),
                  ('Reserva y cambio de prácticas', 'Con los huecos de tus profesores y vehículos.'),
                  ('Seguimiento a quien no se apuntó', 'Vuelve a escribir a los días con lo que preguntó.'),
                  ('Avisos de examen y teórico', 'Recordatorios a los alumnos, sin mandarlos uno a uno.'),
                  ('Lo de la DGT, a secretaría', 'Exámenes, tasas y casos especiales pasan a una persona.')],
        'faqs': [('¿Puede manejar las prácticas de varios profesores?', 'Sí, si la agenda de prácticas está en un calendario o un programa que se pueda conectar. Si la llevas en papel o en un Excel, lo vemos en la demo.'),
                 ('¿Y los alumnos menores de edad?', 'El agente contesta igual y, para la matrícula, indica lo que pide tu autoescuela (por ejemplo, autorización). Los casos especiales pasan a secretaría.'),
                 ('¿Sirve para varias oficinas?', 'Sí: sabe qué oficina le queda mejor a cada alumno y reserva en la suya.')]},
}

FAQ_GENERAL = [
    ('¿El agente sustituye a mi equipo?', 'No. Contesta lo repetitivo, reserva y recuerda. Lo que necesita a una persona (quejas, casos especiales, urgencias) pasa a tu equipo con la conversación entera, y tu equipo puede entrar en cualquier chat cuando quiera.'),
    ('¿De dónde saca la información?', 'De tu web, tus precios y tus normas. Antes de activarlo lo revisas tú. Lo que no sabe no lo inventa: lo pasa a tu equipo.'),
    ('¿Tengo que cambiar de número de WhatsApp?', 'Trabajamos con la API oficial de WhatsApp Business. Puedes usar tu número actual o uno nuevo; en la llamada te explicamos las opciones y lo que implica cada una.'),
    ('¿Con qué se conecta?', 'Con WhatsApp Business API, Google Calendar, Calendly, HubSpot, Zoho CRM y Odoo, entre otros. Si usas otro programa, lo miramos en la demo.'),
    ('¿Cuánto cuesta?', 'Depende de tu volumen de conversaciones y de lo que haya que conectar. Después de enseñarte la demo con tu negocio te pasamos una propuesta cerrada, con el precio al mes.'),
    ('¿Cómo es la demo en 48 h?', 'Nos dejas la web de tu negocio y preparamos un agente con su información pública. Te mandamos un enlace para probarlo como si fueras un cliente, sin instalar nada.'),
]


# ---------------------------------------------------------------- piezas
def head(title, desc, canon, extra=''):
    robots = '<meta name="robots" content="noindex,nofollow">' if PREVIEW else '<meta name="robots" content="index,follow">'
    return f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
{robots}
<link rel="canonical" href="{E(canon)}">
<link rel="icon" type="image/svg+xml" href="/assets/icons/favicon.svg">
<meta name="theme-color" content="#070B13">
<meta property="og:type" content="website">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{E(canon)}">
<meta property="og:image" content="https://zeniapartners.com/assets/images/og-home-es.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="/assets/z2/z2.css?v={V}">
{extra}
</head>
<body>
<a class="skip" href="#main">Ir al contenido</a>
'''


def nav(es_home):
    h = f'{PRE}/es/'
    ancla = (lambda a: f'#{a}') if es_home else (lambda a: f'{h}#{a}')
    links = [('Cómo funciona', ancla('como-funciona')), ('Soluciones', ancla('soluciones')),
             ('Producto', ancla('producto')), ('Casos', ancla('casos')), ('FAQ', '#faq')]
    wa_txt = wa('Hola, vengo de la web de Zenia y quiero más información')
    li = ''.join(f'<a href="{E(u)}">{E(t)}</a>' for t, u in links)
    return f'''<header class="nav"><div class="wrap">
<a class="brand" href="{h}" aria-label="Zenia, inicio">{MARK}<span>Zenia</span></a>
<nav class="nav-links" aria-label="Principal">{li}</nav>
<div class="nav-cta"><a class="nav-wa" href="{E(wa_txt)}" target="_blank" rel="noopener">WhatsApp</a><a class="btn btn-white" href="#demo">Pide tu demo</a></div>
<details class="menu"><summary aria-label="Abrir menú"><span></span></summary>
<div class="menu-panel">{li}<a href="{E(wa_txt)}" target="_blank" rel="noopener">Escríbenos por WhatsApp</a><a class="btn btn-white" href="#demo">Pide tu demo</a></div></details>
</div></header>
'''


def phone(kind, nombre='', inicial=''):
    return f'''<div class="phone" data-chat="{kind}">
<div class="phone-status" aria-hidden="true"><span>9:41</span><span><svg viewBox="0 0 16 12"><path fill="currentColor" d="M0 9h2v3H0zM4 6h2v6H4zM8 3h2v9H8zM12 0h2v12h-2z"/></svg><svg viewBox="0 0 24 12"><rect x=".5" y=".5" width="20" height="11" rx="2.5" fill="none" stroke="currentColor"/><rect x="2" y="2" width="16" height="8" rx="1.5" fill="currentColor"/></svg></span></div>
<div class="chat"><div class="chat-head"><span class="chat-avatar" aria-hidden="true">{E(inicial)}</span><div class="chat-who"><strong>{E(nombre)}</strong><span class="chat-status">en línea</span></div></div>
<div class="chat-body" aria-live="polite"><div class="chat-day">Hoy</div></div>
{'<div class="chips" role="group" aria-label="Preguntas de ejemplo"></div>' if kind == 'live' else ''}
<div class="chat-input" aria-hidden="true"><span>Mensaje</span><i></i></div></div></div>'''


def cards_producto():
    return f'''<section class="band" id="canales"><div class="wrap">
<div class="head"><span class="label">Agente + agenda + CRM</span>
<h2>Vende donde tus clientes ya te escriben. <span class="muted">En WhatsApp, con tu agenda y tu CRM al día.</span></h2></div>
<div class="cards3">
<div class="card"><div class="mini" aria-hidden="true"><div class="b in">Hola, ¿cuánto cuesta un blanqueamiento?</div><div class="b out">Hola. Depende del tipo: te explico las dos opciones y lo que incluye cada una.</div><div class="b in">¿Y tenéis hueco el sábado?</div><div class="b out">Sí, a las 11:00 o a las 12:30. ¿Cuál prefieres?</div></div>
<span class="label">WhatsApp + IA</span><h3>Tu agente contesta en segundos</h3><p>Con tu información y tu tono, también de noche y en fin de semana.</p></div>
<div class="card"><div class="mini" aria-hidden="true"><div class="slot"><span><b>Jue 17:00</b> · Limpieza</span><span class="state cita">Reservada por el agente</span></div><div class="slot"><span><b>Jue 18:30</b> · Revisión</span><span class="state ok">Confirmada</span></div><div class="slot on"><span><b>Vie 10:00</b> · Libre</span><span class="muted">Ofrecida</span></div><div class="slot"><span><b>Vie 12:00</b> · Ortodoncia</span><span class="state ok">Confirmada</span></div></div>
<span class="label">Agenda</span><h3>Reserva en tu calendario</h3><p>Propone solo huecos libres, confirma y recuerda la cita el día antes.</p></div>
<div class="card"><div class="mini" aria-hidden="true"><table><tr><td>Laura G.</td><td>Cita jueves</td><td><span class="state cita">Cita</span></td></tr><tr><td>Marcos R.</td><td>Precio ortodoncia</td><td><span class="state ok">Respondido</span></td></tr><tr><td>Ana P.</td><td>Dolor de muela</td><td><span class="state esc">A tu equipo</span></td></tr><tr><td>Pedro L.</td><td>Cambio de cita</td><td><span class="state cita">Cita</span></td></tr></table></div>
<span class="label">CRM a medida</span><h3>Cada conversación, registrada</h3><p>Quién escribió, qué quería y en qué quedó, sin teclear nada.</p></div>
</div></div></section>
'''


def tarjetas_nichos():
    out = []
    for k, n in NICHOS.items():
        t, p, lis, q, a = n['tarjeta']
        out.append(f'''<a class="niche" href="{PRE}/es/{n['slug']}/"><div class="niche-top"><span class="niche-ico">{ICO[k]}</span><h3>{E(t)}</h3><p>{E(p)}</p>
<ul>{''.join(f'<li>{E(x)}</li>' for x in lis)}</ul></div>
<div class="niche-a" aria-hidden="true">{E(q)}</div><div class="niche-q" aria-hidden="true">{E(a)}</div>
<div class="niche-go">Ver la solución para {E(n['menu'].lower())} <span>→</span></div></a>''')
    return ''.join(out)


def como_funciona(k, titulo):
    g = GUION[k]
    pasos = ''.join(f'<li><div><b>{E(a)}</b><span>{E(b)}</span></div></li>' for a, b in g['pasos'])
    return f'''<section class="band alt" id="como-funciona"><div class="wrap">
<div class="head"><span class="label">Así funciona</span><h2>{titulo}</h2>
<p class="lead">Mira una conversación completa: el agente atiende, reserva, recuerda y sabe cuándo pasarle el chat a una persona.</p></div>
<div class="how"><div><ol class="steps">{pasos}</ol><button class="replay" type="button">Volver a reproducir</button></div>
{phone('auto', g['nombre'], g['nombre'][0])}</div>
</div></section>
'''


def producto():
    return '''<section class="band" id="producto"><div class="wrap">
<div class="head center"><span class="label">Míralo por dentro</span><h2>Todo tu WhatsApp en un solo panel</h2>
<p class="lead">Conversaciones, citas y clientes en tu CRM, hecho a la medida de cómo trabajas. Y el agente, con interruptores que controlas tú.</p></div>
<div class="tabs" role="tablist">
<button role="tab" aria-selected="true" aria-controls="p-conv">Conversaciones</button>
<button role="tab" aria-selected="false" aria-controls="p-citas">Citas</button>
<button role="tab" aria-selected="false" aria-controls="p-cli">Clientes</button>
<button role="tab" aria-selected="false" aria-controls="p-agente">Agente</button></div>
<div class="app"><div class="app-bar"><i></i><i></i><i></i><span>CRM de tu negocio · hecho por Zenia</span></div>
<div class="app-body"><div class="app-side"><b>''' + MARK + '''Tu clínica</b>
<span data-tab="p-conv" class="on">Conversaciones</span><span data-tab="p-citas">Citas</span><span data-tab="p-cli">Clientes</span><span>Campañas</span><span data-tab="p-agente">Agente</span></div>
<div class="app-main">
<div class="app-panel" id="p-conv" role="tabpanel"><div class="convs"><div class="convs-list">
<div><b>Ana P. <span class="state esc">A tu equipo</span></b>Me duele mucho una muela…</div>
<div class="on"><b>Laura Gómez <span class="state cita">Cita</span></b>Jueves 17:00, limpieza</div>
<div><b>Marcos R. <span class="state ok">Respondido</span></b>¿Ortodoncia a plazos?</div>
<div><b>+34 6•• ••• 412 <span class="state ok">Respondido</span></b>¿Abrís los sábados?</div>
<div><b>Pedro L. <span class="state cita">Cita</span></b>Cambia su cita al viernes</div></div>
<div class="thread"><div class="b in">Hola, ¿tenéis cita para una limpieza esta semana?</div><div class="b out">¡Hola! Sí. La primera visita es gratis. ¿Mejor por la mañana o por la tarde?</div><div class="b in">Por la tarde</div><div class="b out">Tengo jueves a las 17:00 o a las 18:30, o viernes a las 17:30.</div><div class="b in">Jueves 17:00. Laura Gómez</div><div class="b out">Hecho, Laura: jueves a las 17:00 en Chamberí. Te lo recuerdo el día antes.</div><span class="tag">Cita creada en la agenda · 23:44</span></div></div></div>
<div class="app-panel" id="p-citas" role="tabpanel" hidden><div class="kpis"><div class="kpi"><small>Citas esta semana</small><strong>38</strong></div><div class="kpi"><small>Reservadas por el agente</small><strong>21</strong></div><div class="kpi"><small>Confirmadas por recordatorio</small><strong>33</strong></div><div class="kpi"><small>Cambiadas por chat</small><strong>4</strong></div></div>
<div class="tbl-wrap"><table class="tbl"><thead><tr><th>Cuándo</th><th>Paciente</th><th>Tratamiento</th><th>Sede</th><th>Estado</th></tr></thead><tbody>
<tr><td><b>Jue 17:00</b></td><td>Laura Gómez</td><td>Limpieza</td><td>Chamberí</td><td><span class="state cita">Por el agente</span></td></tr>
<tr><td><b>Jue 18:30</b></td><td>Diego Marín</td><td>Revisión</td><td>Chamberí</td><td><span class="state ok">Confirmada</span></td></tr>
<tr><td><b>Vie 10:00</b></td><td>Carmen Vidal</td><td>Primera visita</td><td>Salamanca</td><td><span class="state cita">Por el agente</span></td></tr>
<tr><td><b>Vie 12:00</b></td><td>Pedro Lima</td><td>Ortodoncia</td><td>Salamanca</td><td><span class="state ok">Confirmada</span></td></tr>
<tr><td><b>Vie 17:30</b></td><td>Ana Pérez</td><td>Urgencia</td><td>Chamberí</td><td><span class="state esc">Por recepción</span></td></tr></tbody></table></div></div>
<div class="app-panel" id="p-cli" role="tabpanel" hidden><div class="tbl-wrap"><table class="tbl"><thead><tr><th>Cliente</th><th>Último contacto</th><th>Interés</th><th>Próxima cita</th><th>Origen</th></tr></thead><tbody>
<tr><td><b>Laura Gómez</b></td><td>Hoy, 23:44</td><td>Limpieza</td><td>Jueves 17:00</td><td>WhatsApp</td></tr>
<tr><td><b>Marcos Ruiz</b></td><td>Hoy, 19:10</td><td>Ortodoncia invisible</td><td>—</td><td>Google</td></tr>
<tr><td><b>Carmen Vidal</b></td><td>Ayer</td><td>Implantes</td><td>Viernes 10:00</td><td>Instagram</td></tr>
<tr><td><b>Pedro Lima</b></td><td>Lunes</td><td>Ortodoncia</td><td>Viernes 12:00</td><td>WhatsApp</td></tr></tbody></table></div></div>
<div class="app-panel" id="p-agente" role="tabpanel" hidden><div class="toggles">
<div class="toggle"><span><b>Responder fuera de horario</b>Noches, fines de semana y festivos.</span><i class="sw"></i></div>
<div class="toggle"><span><b>Reservar en la agenda</b>Solo en huecos libres de cada sede.</span><i class="sw"></i></div>
<div class="toggle"><span><b>Recordatorio el día antes</b>Con opción de confirmar o cambiar.</span><i class="sw"></i></div>
<div class="toggle"><span><b>Pasar lo clínico a recepción</b>Dolor, urgencias y dudas médicas.</span><i class="sw"></i></div>
<div class="toggle"><span><b>Pedir reseña después de la visita</b>Solo si la visita fue bien.</span><i class="sw off"></i></div></div></div>
</div></div></div>
<p class="app-note">Panel con datos de ejemplo. Cada CRM se hace a la medida del negocio.</p>
</div></section>
'''


def cifras():
    return '''<section class="band alt"><div class="wrap">
<div class="head center"><h2>Lo que cambia desde el primer día</h2></div>
<div class="stats">
<div class="stat"><small>Disponibilidad</small><strong>24/7</strong><span>tu agente no cierra, ni en festivos</span></div>
<div class="stat"><small>Primera respuesta</small><strong>&lt;1 min</strong><span>el cliente no espera a que acabes con otro</span></div>
<div class="stat"><small>Tu demo</small><strong>48 h</strong><span>para probarlo con la información de tu negocio</span></div>
<div class="stat"><small>Caso real</small><strong>831</strong><span>conversaciones de WhatsApp atendidas para Global Watch Buyers</span></div>
</div></div></section>
'''


def casos():
    return '''<section class="band" id="casos"><div class="wrap">
<div class="head"><span class="label">Casos</span><h2>Ya funciona en negocios reales</h2></div>
<div class="cases">
<a class="case" href="/es/caso-global-watch-buyers.html"><div class="case-img" style="background-image:url(/cases/img/gwb-agente-poster.webp)" role="img" aria-label="El agente de Global Watch Buyers atendiendo por WhatsApp"></div>
<div class="case-txt"><span class="label">Global Watch Buyers</span><h3>Vendedores de relojes de lujo de 33 países, atendidos por WhatsApp</h3>
<p>Páginas en 13 idiomas, WhatsApp con cualificación y un agente de IA que contesta, cualifica y agenda.</p>
<div class="case-nums"><div><b>831</b><span>conversaciones</span></div><div><b>33</b><span>países</span></div><div><b>10 de 12</b><span>contactos de anuncios con reloj premium</span></div></div>
<div class="case-go">Ver el caso →</div></div></a>
<a class="case" href="/es/caso-throwin-salt-gaia.html"><div class="case-img" style="background-image:url(/cases/img/ts-gaia-chat.webp)" role="img" aria-label="Gaia, el agente de Throwin' Salt, en WhatsApp"></div>
<div class="case-txt"><span class="label">Throwin’ Salt Co.</span><h3>Relojes de alta gama publicados en eBay desde WhatsApp</h3>
<p>Gaia prepara cada anuncio con título, fotos y precio, y lo publica cuando el equipo dice «publica».</p>
<div class="case-nums"><div><b>54</b><span>relojes en 4 semanas</span></div><div><b>23</b><span>en un solo día</span></div><div><b>2 M$</b><span>de inventario en eBay</span></div></div>
<div class="case-go">Ver el caso →</div></div></a>
</div></div></section>
'''


def integraciones():
    ico = {n: s for n, s in INTEG}
    def nodo(n, s=None):
        s = s or ico.get(n, '')
        return f'<div class="hub-node"><i>{s}</i>{E(n)}</div>'
    cal = '<svg viewBox="0 0 24 24" fill="none" stroke="#006BFF" stroke-width="2.4"><circle cx="12" cy="12" r="8"/><path d="M15.5 9a4.5 4.5 0 1 0 0 6"/></svg>'
    izq = nodo('WhatsApp Business API') + nodo('Google Calendar') + nodo('Calendly', cal)
    der = nodo('HubSpot') + nodo('Zoho CRM') + nodo('Odoo')
    return f'''<section class="band alt"><div class="wrap">
<div class="head center"><span class="label">Integraciones</span><h2>Se conecta con lo que ya usas</h2>
<p class="lead">Sin cambiar de programa: el agente trabaja sobre tu WhatsApp, tu agenda y tu CRM. Si usas otra herramienta, la miramos.</p></div>
<div class="hub"><div class="hub-col">{izq}</div><div><div class="hub-core">{MARK_SOLO}</div><p class="hub-cap">Zenia</p></div><div class="hub-col">{der}</div></div>
</div></section>
'''


def precio():
    return f'''<section class="band" id="precio"><div class="wrap"><div class="price">
<div><span class="label">Precio a medida</span><h2>Cada negocio es distinto. Tu precio también.</h2>
<p class="lead">No vendemos planes cerrados. Primero te enseñamos la demo con tu negocio; después te pasamos una propuesta cerrada: qué hace el agente, qué se conecta y cuánto cuesta al mes.</p>
<div class="btns"><a class="btn btn-white" href="#demo">Pide tu demo</a><a class="btn btn-wa" href="{E(wa('Hola, quiero ver una propuesta de Zenia para mi negocio'))}" target="_blank" rel="noopener">{WA_ICO}Escríbenos por WhatsApp</a></div>
<p class="check">Te respondemos en menos de 24 h · Sin compromiso</p></div>
<ul><li><span><b>Según tu volumen</b>Pagas por lo que tu negocio necesita, no por un plan que te sobra.</span></li>
<li><span><b>Hecho con tu información</b>Precios, horarios y normas de tu negocio, revisados por ti antes de activarlo.</span></li>
<li><span><b>Acompañamiento cercano</b>En español y por WhatsApp, con alguien que conoce tu caso.</span></li></ul>
</div></div></section>
'''


def form_demo(sector=None, quien='clientes'):
    opts = ''.join(f'<option{" selected" if s == sector else ""}>{s}</option>' for s in ['Clínica', 'Taller', 'Autoescuela', 'Otro'])
    return f'''<section class="band alt" id="demo"><div class="wrap"><div class="demo-box">
<div><span class="label">Tu demo en 48 h</span><h2>Pruébalo con tu negocio antes de decidir nada</h2>
<p class="lead">Déjanos tu web y tu contacto. Preparamos el agente con la información pública de tu negocio y te mandamos un enlace para probarlo como lo harían tus {E(quien)}.</p>
<ol class="how-demo"><li><i>1</i><span><b>Nos dejas tu web</b>Un minuto, sin llamadas.</span></li>
<li><i>2</i><span><b>Montamos tu demo</b>Con tus servicios, horarios y sedes, solo datos públicos.</span></li>
<li><i>3</i><span><b>La pruebas desde el móvil</b>Y si te encaja, lo vemos 30 minutos con tus preguntas reales.</span></li></ol></div>
<form class="form" novalidate>
<div class="f" style="display:grid;gap:14px">
<label>Web de tu negocio<input name="web" type="text" inputmode="url" autocomplete="url" placeholder="www.tunegocio.es" required></label>
<label>Tu nombre<input name="nombre" type="text" autocomplete="given-name" placeholder="Nombre"></label>
<label>WhatsApp o email<input name="contacto" type="text" autocomplete="tel" placeholder="+34 600 000 000" required></label>
<label>Sector<select name="sector">{opts}</select></label>
<button class="btn btn-white" type="submit">Quiero mi demo</button>
<small>Solo usamos estos datos para enviarte la demo. Ver la <a href="/privacy/">política de privacidad</a>.</small></div>
<div class="ok" role="status"><b>Recibido.</b> Te escribimos en menos de 24 h con el enlace de tu demo. Si prefieres adelantarlo, <a href="{E(wa('Hola, acabo de pedir mi demo en la web de Zenia'))}" target="_blank" rel="noopener">escríbenos por WhatsApp</a>.</div>
</form></div></div></section>
'''


def faq(items):
    det = ''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in items)
    ld = json.dumps({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in items]}, ensure_ascii=False)
    return f'''<section class="band" id="faq"><div class="wrap">
<div class="head center"><span class="label">FAQ</span><h2>Preguntas frecuentes</h2>
<p class="lead">¿Te queda otra duda? <a href="{E(wa('Hola, tengo una duda sobre Zenia'))}" target="_blank" rel="noopener" style="color:var(--accent)">Escríbenos por WhatsApp</a>.</p></div>
<div class="faq">{det}</div></div></section>
<script type="application/ld+json">{ld}</script>
'''


def final(t1, t2):
    return f'''<section class="wrap"><div class="final">
<h2>{t1}</h2><p class="lead">{t2}</p>
<div class="btns"><a class="btn btn-white" href="#demo">Pide tu demo</a><a class="btn btn-ghost" href="{CALENDLY}" target="_blank" rel="noopener">Agenda 30 minutos</a></div>
</div></section>
'''


def footer():
    nich = ''.join(f'<a href="{PRE}/es/{n["slug"]}/">{E(n["menu"])}</a>' for n in NICHOS.values())
    return f'''<footer><div class="wrap">
<div class="foot"><div><a class="brand" href="{PRE}/es/">{MARK}<span>Zenia</span></a><p>Agentes de IA para el WhatsApp de tu negocio, con tu agenda y un CRM hecho a tu medida.</p></div>
<div><b>Soluciones</b>{nich}<a href="/es/cobertura.html">Todos los sectores</a></div>
<div><b>Zenia</b><a href="/es/casos.html">Casos</a><a href="/blog/">Blog</a><a href="/about.html">Sobre Zenia</a></div>
<div><b>Contacto</b><a href="mailto:fabrizzio.zelada@zeniapartners.com">fabrizzio.zelada@zeniapartners.com</a><a href="{E(wa('Hola, vengo de la web de Zenia y quiero más información'))}" target="_blank" rel="noopener">WhatsApp +34 677 612 799</a><a href="{CALENDLY}" target="_blank" rel="noopener">Agenda una llamada</a></div></div>
<div class="foot-bottom"><span>© 2026 Zenia Partners · Madrid</span><span><a href="/privacy/" style="text-decoration:none">Privacidad</a> · <a href="/?lang=en" style="text-decoration:none">English</a></span></div>
</div></footer>
<a class="wa-float" href="{E(wa('Hola, vengo de la web de Zenia y quiero más información'))}" target="_blank" rel="noopener" aria-label="Escríbenos por WhatsApp" data-directo>{WA_ICO}</a>
'''


def scripts(datos):
    js = json.dumps(datos, ensure_ascii=False).replace('</', '<\\/')
    return f'''<script type="application/json" id="z2-data">{js}</script>
<script src="/assets/z2/z2.js?v={V}" defer></script>
<script>document.addEventListener("click",function(e){{var t=e.target,a=t.closest?t.closest('a[href*="wa.me"]'):null;if(!a)return;try{{navigator.sendBeacon("https://gaia-relojes.onrender.com/gwb/lead",JSON.stringify({{site:"zenia",path:location.pathname+location.search,ref:document.referrer||""}}))}}catch(r){{}}}},true);</script>
<script src="/assets/qualify.js?v=4" defer></script>
<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{{"token": "{CF}"}}'></script>
</body>
</html>
'''


def hero(label, h1a, h1b, lead, seg, datos_nombre, foto=True):
    bg = '<div class="hero-bg" style="background-image:url(/assets/images/hero-madrid.webp)"></div>' if foto else '<div class="hero-bg"></div>'
    segh = ''
    if seg:
        segh = '<div class="seg" role="group" aria-label="Prueba como cliente de">' + ''.join(
            f'<button type="button" data-k="{k}" aria-pressed="false">{E(NICHOS[k]["sector"])}</button>' for k in seg) + '</div>'
    integ = ''.join(f'<span>{s}{E(n)}</span>' for n, s in INTEG[:3])
    return f'''<section class="hero">{bg}<div class="hero-glow"></div><div class="wrap">
<div><span class="label">{E(label)}</span>
<h1>{E(h1a)} <span class="hl">{E(h1b)}</span></h1>
<p class="lead">{E(lead)}</p>
<div class="btns"><a class="btn btn-white" href="#demo">Pide tu demo gratis</a><a class="btn btn-ghost" href="#como-funciona">{PLAY}Mira cómo funciona</a></div>
<p class="check">Tu demo con la información de tu negocio en 48 h · Sin compromiso</p>
<div class="trust"><small>Funciona con</small><div class="trust-row">{integ}</div></div></div>
<div class="hero-phone">{segh}{phone('live', datos_nombre, datos_nombre[0])}<p class="seg-note">Toca una pregunta como lo haría un cliente. Negocio de ejemplo.</p></div>
</div></section>
'''


def logos():
    t = [('Global Watch Buyers', '/cases/img/gwb-mark.svg', 'Relojes de lujo · 33 países', '/es/caso-global-watch-buyers.html'),
         ('Throwin’ Salt Co.', '/cases/img/ts-mark.png', 'Relojes de alta gama · EE. UU.', '/es/caso-throwin-salt-gaia.html'),
         ('Croian & Hein', '/cases/img/croian-mark.svg', 'Vinos raros · Suiza', '/es/caso-croian-hein.html'),
         ('Cicero', '/cases/img/cicero-mark.svg', 'Asuntos públicos con IA', '/es/caso-cicero.html')]
    tiles = ''.join(f'<a class="logo-tile" href="{u}"><img src="{s}" alt="" loading="lazy"><span>{E(n)}<em>{E(d)}</em></span></a>' for n, s, d, u in t)
    return f'<section class="logos"><div class="wrap"><small>Negocios que ya trabajan con Zenia</small><div class="logo-row">{tiles}</div></div></section>\n'


# ---------------------------------------------------------------- páginas
def portada():
    canon = 'https://zeniapartners.com/es/'
    datos = {'negocios': NEGOCIOS, 'guion': GUION['clinica']}
    org = json.dumps({'@context': 'https://schema.org', '@type': ['Organization', 'ProfessionalService'], '@id': 'https://zeniapartners.com/#organization',
                      'name': 'Zenia Partners', 'url': 'https://zeniapartners.com/', 'logo': 'https://zeniapartners.com/assets/logos/zenia-logo.png',
                      'email': 'fabrizzio.zelada@zeniapartners.com', 'areaServed': ['ES', 'LATAM'],
                      'description': 'Agentes de IA para el WhatsApp de negocios, con agenda y CRM a medida.'}, ensure_ascii=False)
    h = head('Agentes de IA para el WhatsApp de tu negocio, con agenda y CRM | Zenia',
             'Zenia pone un agente de IA en el WhatsApp de tu negocio: contesta al momento, reserva en tu agenda y registra cada conversación en tu CRM. Pide tu demo en 48 h.',
             canon, f'<script type="application/ld+json">{org}</script>')
    cuerpo = (h + nav(True) + '<main id="main">'
              + hero('Agentes de IA para WhatsApp', 'Tu WhatsApp atiende, agenda y', 'vende 24/7',
                     'Zenia pone un agente de IA en el WhatsApp de tu negocio. Contesta en segundos con tu información, reserva en tu agenda y deja cada conversación en tu CRM. Lo que necesita a una persona, te lo pasa.',
                     list(NICHOS.keys()), NEGOCIOS['clinica']['nombre'])
              + logos() + cards_producto()
              + f'''<section class="band alt" id="soluciones"><div class="wrap"><div class="head"><span class="label">Soluciones por sector</span>
<h2>Hecho para negocios que viven del WhatsApp</h2><p class="lead">Cada sector pregunta cosas distintas. El agente llega sabiendo las de tu negocio.</p></div>
<div class="niches">{tarjetas_nichos()}</div>
<p class="other">¿Otro sector? Restaurantes, inmobiliarias, gimnasios o despachos: <a href="{E(wa('Hola, quiero ver si Zenia encaja en mi sector'))}" target="_blank" rel="noopener">escríbenos y lo vemos</a>.</p></div></section>
'''
              + como_funciona('clinica', 'Una cita completa, sin que toques el móvil').replace('band alt', 'band')
              + producto() + cifras() + casos() + integraciones() + precio() + form_demo()
              + faq(FAQ_GENERAL) + final('¿Lo vemos con tu negocio?', 'Te enseñamos la demo con tu información en 48 h. Sin compromiso.')
              + '</main>' + footer() + scripts(datos))
    return cuerpo


def nicho(k):
    n = NICHOS[k]
    canon = f'https://zeniapartners.com/es/{n["slug"]}/'
    datos = {'negocios': {k: NEGOCIOS[k]}, 'guion': GUION[k]}
    otros = ''.join(f'<a class="btn btn-ghost" href="{PRE}/es/{NICHOS[o]["slug"]}/">{E(NICHOS[o]["menu"])}</a>' for o in NICHOS if o != k)
    h = head(n['title'], n['desc'], canon)
    return (h + nav(False) + '<main id="main">'
            + hero(n['label'], n['h1'][0], n['h1'][1], n['lead'], None, NEGOCIOS[k]['nombre'], foto=False).replace('<h1>', '<h1 class="largo">', 1)
            + f'''<section class="band"><div class="wrap"><div class="head"><span class="label">El problema</span><h2>{E(n['dolor_h2'])}</h2></div>
<div class="pains">{''.join(f'<div class="pain"><h3>{E(a)}</h3><p>{E(b)}</p></div>' for a, b in n['dolores'])}</div></div></section>
<section class="band alt"><div class="wrap"><div class="head"><span class="label">Qué hace</span><h2>{E(n['feats_h2'])}</h2></div>
<div class="feats">{''.join(f'<div class="feat"><h3>{E(a)}</h3><p>{E(b)}</p></div>' for a, b in n['feats'])}</div></div></section>
'''
            + como_funciona(k, 'Así lo vive tu ' + {'clinica': 'paciente', 'taller': 'cliente', 'autoescuela': 'alumno'}[k]).replace('band alt', 'band')
            + integraciones() + form_demo(n['sector'], n['quien'])
            + faq(n['faqs'] + FAQ_GENERAL[:4] + FAQ_GENERAL[5:])
            + f'''<section class="band" style="padding-top:0"><div class="wrap center"><p class="muted" style="margin:0 0 14px">También trabajamos con</p><div class="btns" style="margin-top:0">{otros}<a class="btn btn-ghost" href="{PRE}/es/">Todos los sectores</a></div></div></section>
'''
            + final(f'¿Lo vemos con tu {n["sector"].lower()}?', 'Te enseñamos la demo con tu información en 48 h. Sin compromiso.')
            + '</main>' + footer() + scripts(datos))


def escribir(ruta, txt):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    open(ruta, 'w', encoding='utf-8').write(txt)
    print(ruta.replace(RAIZ, ''), len(txt))


os.makedirs(os.path.join(RAIZ, 'assets/z2'), exist_ok=True)
shutil.copy(os.path.join(AQUI, 'z2.css'), os.path.join(RAIZ, 'assets/z2/z2.css'))
shutil.copy(os.path.join(AQUI, 'z2.js'), os.path.join(RAIZ, 'assets/z2/z2.js'))
base = os.path.join(RAIZ, 'v2') if PREVIEW else RAIZ
escribir(os.path.join(base, 'es/index.html'), portada())
for k in NICHOS:
    escribir(os.path.join(base, f'es/{NICHOS[k]["slug"]}/index.html'), nicho(k))
