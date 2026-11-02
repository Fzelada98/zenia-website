// ZENIA, la escena de la portada, v5: un WhatsApp real dentro de un teléfono y, debajo, el CRM
// hecho a la medida de cada negocio, navegable: reservas (o agenda, o leads), clientes, campañas,
// el agente y los ajustes, con datos distintos por negocio y por vista. Cambia de negocio con los
// botones y reproduce la conversación como la vería el cliente: la hora es la del visitante,
// «escribiendo…» en la cabecera, ticks azules al leer, botones de respuesta rápida y, al terminar,
// la fila nueva aparece en la primera vista del CRM y sus cifras suben.
// Sin script, la página muestra el restaurante tal cual, con la fila ya en el CRM.
(function () {
  var DATA = {
    es: {
      caption: { night: 'Lo que hace el agente a las {t}, cuando ya cerraste', day: 'Lo que hace el agente ahora, a las {t}, mientras tú atiendes' },
      status: { online: 'en línea', typing: 'escribiendo…' },
      day: 'Hoy', lock: 'Los mensajes están cifrados de extremo a extremo.', input: 'Mensaje',
      crmTag: 'CRM a medida', updated: 'Actualizado ahora', agentState: 'Por el agente', settings: 'Ajustes',
      onLabel: 'Activado', offLabel: 'Desactivado',
      restaurante: {
        name: 'La Terraza · Restaurante', avatar: 'L', brand: 'La Terraza', where: 'Madrid · 2 salas',
        views: [
          { tab: 'Reservas', kpis: [['Reservas para mañana', '23', '+1'], ['Ocupación a las 21:00', '92 %', ''], ['Atendidas por el agente', '15', '+1']],
            title: 'Reservas de mañana', when: 'Martes', cols: ['Hora', 'Nombre', 'Pax', 'Zona', 'Notas', 'Estado'], opt: [3, 4],
            rows: [
              ['20:00', 'Familia Ortega', '6', 'Salón', 'Cumpleaños', 'ok', 'Confirmada'],
              ['20:30', 'Marc Vidal', '2', 'Terraza', '—', 'ok', 'Confirmada'],
              ['21:00', 'Laura', '4', 'Terraza', 'Sin gluten', 'agent', '', true],
              ['21:00', 'Ana Ruiz', '3', 'Salón', 'Silla bebé', 'wait', 'Pendiente'],
              ['21:30', 'Pedro Lima', '2', 'Terraza', '—', 'ok', 'Confirmada'],
              ['22:00', 'Grupo Sato', '8', 'Salón', 'Menú degustación', 'ok', 'Confirmada']
            ] },
          { tab: 'Clientes', kpis: [['Clientes en el CRM', '1.284', ''], ['Habituales (3 visitas o más)', '412', ''], ['Vuelven tras un recordatorio', '61 %', '']],
            title: 'Clientes', when: 'Últimos 90 días', cols: ['Nombre', 'Visitas', 'Última', 'Preferencias', 'Estado'], opt: [3],
            rows: [
              ['Laura', '1', 'Mañana', 'Sin gluten · Terraza', 'agent', 'Nueva'],
              ['Marc Vidal', '12', 'Mañana', 'Terraza · Vino de la casa', 'ok', 'Habitual'],
              ['Familia Ortega', '6', 'Mañana', 'Salón · Cumpleaños', 'ok', 'Habitual'],
              ['Pedro Lima', '4', 'Mañana', 'Terraza', 'ok', 'Habitual'],
              ['Ana Ruiz', '2', 'Hace 3 semanas', 'Silla bebé', 'wait', 'Recordatorio enviado'],
              ['Grupo Sato', '3', 'Hace 2 meses', 'Menú degustación · Empresa', 'ok', 'Empresa']
            ] },
          { tab: 'Campañas', kpis: [['Reservas por campañas este mes', '62', ''], ['Tasa de respuesta', '14 %', ''], ['Coste por reserva', '0,90 €', '']],
            title: 'Campañas por WhatsApp', when: 'Noviembre', cols: ['Campaña', 'Enviados', 'Respuestas', 'Reservas', 'Estado'], opt: [2],
            rows: [
              ['Menú de temporada', '620', '84', '37', 'ok', 'Activa'],
              ['Recuperar inactivos (90 días)', '240', '31', '14', 'ok', 'Activa'],
              ['Cumpleaños del mes', '48', '19', '11', 'wait', 'Programada'],
              ['Reseñas tras la visita', '310', '92', '—', 'ok', 'Activa'],
              ['Cena de empresa (Navidad)', '—', '—', '—', 'off', 'Borrador']
            ] },
          { tab: 'Agente', kpis: [['Conversaciones hoy', '31', '+1'], ['Resueltas sin intervención', '94 %', ''], ['Tiempo medio de respuesta', '28 s', '']],
            title: 'Conversaciones de hoy', when: 'Última: ahora', cols: ['Hora', 'Cliente', 'Intención', 'Resultado', 'Estado'], opt: [2],
            rows: [
              ['{t}', 'Laura', 'Reserva', 'Mesa para 4 mañana 21:00', 'agent', 'Resuelto', true],
              ['22:31', 'Javier', 'Horario', 'Respondido', 'ok', 'Resuelto'],
              ['21:57', 'Carmen', 'Cancelación', 'Mesa liberada', 'ok', 'Resuelto'],
              ['21:10', 'Hugo', 'Alergias y carta', 'Carta enviada', 'ok', 'Resuelto'],
              ['20:42', 'Marta', 'Evento de 20 personas', 'Pasado al encargado', 'esc', 'Escalado'],
              ['19:30', 'Álvaro', 'Reserva', 'Mesa para 2 el sábado', 'ok', 'Resuelto']
            ] },
          { tab: 'Ajustes', kpis: [['Horario del agente', '24 h', ''], ['Idiomas', '2', ''], ['Integraciones activas', '3', '']],
            title: 'Cómo atiende el agente', when: 'La Terraza', settings: [
              ['Horario', 'Responde 24 horas, 7 días', true],
              ['Tono', 'Cercano, de tú, el de la casa', true],
              ['Idiomas', 'Español e inglés', true],
              ['Pasa a una persona', 'Eventos de más de 12 personas y quejas', true],
              ['Recordatorio de reserva', '3 horas antes, por WhatsApp', true],
              ['Pedir reseña tras la visita', 'Al día siguiente, a las 12:00', true],
              ['Integraciones', 'WhatsApp Business API · Google Calendar · TPV', true]
            ] }
        ],
        msgs: [
          { d: 'in', t: 'Hola, ¿tienen mesa para 4 mañana a las 21:00?', m: 0 },
          { d: 'out', t: '¡Hola! Sí, nos queda mesa para 4 a las 21:00. ¿Dónde prefieres?', buttons: ['Terraza', 'Salón'], tap: 0, m: 0 },
          { d: 'in', t: 'Terraza', m: 1, reply: true },
          { d: 'in', t: 'A nombre de Laura.', m: 1 },
          { d: 'out', t: 'Listo, Laura: mesa para 4 mañana a las 21:00 en la terraza. Te mando un recordatorio mañana a las 18:00. ¿Alguna alergia que debamos saber?', m: 1 },
          { d: 'in', t: 'Sin gluten, gracias', m: 2 },
          { d: 'out', t: 'Anotado, avisamos a cocina. ¡Hasta mañana!', m: 2 }
        ]
      },
      clinica: {
        name: 'Clínica Dental Norte', avatar: 'C', brand: 'Clínica Dental Norte', where: 'Valencia · 3 gabinetes',
        views: [
          { tab: 'Agenda', kpis: [['Citas el jueves', '18', ''], ['Huecos libres', '3', '+1'], ['Cambios hechos por el agente', '6', '+1']],
            title: 'Agenda del jueves · Dra. Ruiz', when: 'Jueves', cols: ['Hora', 'Paciente', 'Tratamiento', 'Recordatorio', 'Estado'], opt: [2, 3],
            rows: [
              ['10:00', 'Libre', '—', '—', 'off', 'Hueco liberado'],
              ['10:30', 'Jorge Peña', 'Limpieza', 'Enviado', 'ok', 'Confirmada'],
              ['12:30', 'Libre', '—', '—', 'off', 'Disponible'],
              ['16:00', 'Elena Soto', 'Revisión', 'Enviado', 'ok', 'Confirmada'],
              ['17:00', 'Marta Gil', 'Revisión', 'Miércoles 17:00', 'agent', '', true],
              ['17:30', 'Luis Mora', 'Empaste', 'Enviado', 'ok', 'Confirmada']
            ] },
          { tab: 'Pacientes', kpis: [['Pacientes activos', '2.140', ''], ['Revisiones al día', '78 %', ''], ['Ausencias este mes', '4 %', '']],
            title: 'Pacientes', when: 'Con cita este mes', cols: ['Paciente', 'Tratamiento', 'Última visita', 'Próxima', 'Estado'], opt: [3],
            rows: [
              ['Marta Gil', 'Revisión', 'Hace 6 meses', 'Jueves 17:00', 'agent', 'Cita cambiada'],
              ['Jorge Peña', 'Limpieza', 'Hace 1 año', 'Jueves 10:30', 'ok', 'Confirmada'],
              ['Elena Soto', 'Revisión', 'Hace 6 meses', 'Jueves 16:00', 'ok', 'Confirmada'],
              ['Nerea Díaz', 'Ortodoncia', 'Hace 1 mes', 'En 4 semanas', 'ok', 'En tratamiento'],
              ['Pablo Ruiz', 'Implante', 'Hace 2 semanas', '—', 'wait', 'Presupuesto enviado'],
              ['Luis Mora', 'Empaste', 'Hace 3 meses', 'Jueves 17:30', 'ok', 'Confirmada']
            ] },
          { tab: 'Campañas', kpis: [['Citas por campañas', '75', ''], ['Confirmaciones automáticas', '96 %', ''], ['Huecos recuperados este mes', '18', '']],
            title: 'Campañas por WhatsApp', when: 'Noviembre', cols: ['Campaña', 'Enviados', 'Respuestas', 'Citas', 'Estado'], opt: [2],
            rows: [
              ['Revisión anual pendiente', '180', '71', '52', 'ok', 'Activa'],
              ['Confirmación 24 h antes', 'Automática', '—', '96 % confirman', 'ok', 'Activa'],
              ['Blanqueamiento de otoño', '420', '58', '23', 'ok', 'Activa'],
              ['Encuesta tras la visita', '140', '97', '4,9 / 5', 'ok', 'Activa'],
              ['Ortodoncia invisible', '—', '—', '—', 'wait', 'Programada']
            ] },
          { tab: 'Agente', kpis: [['Conversaciones hoy', '24', '+1'], ['Resueltas sin intervención', '91 %', ''], ['Tiempo medio de respuesta', '25 s', '']],
            title: 'Conversaciones de hoy', when: 'Última: ahora', cols: ['Hora', 'Paciente', 'Intención', 'Resultado', 'Estado'], opt: [2],
            rows: [
              ['{t}', 'Marta Gil', 'Cambio de cita', 'Jueves 17:00 con la Dra. Ruiz', 'agent', 'Resuelto', true],
              ['21:40', 'Iván', 'Precio de una limpieza', 'Respondido', 'ok', 'Resuelto'],
              ['20:55', 'Rosa', 'Dolor fuerte', 'Pasado a la doctora', 'esc', 'Escalado'],
              ['19:20', 'Tomás', 'Primera visita', 'Cita el viernes 10:30', 'ok', 'Resuelto'],
              ['18:05', 'Lucía', 'Documentación del seguro', 'Enviada', 'ok', 'Resuelto'],
              ['17:12', 'Pablo Ruiz', 'Presupuesto implante', 'Presupuesto enviado', 'wait', 'Pendiente']
            ] },
          { tab: 'Ajustes', kpis: [['Horario del agente', '24 h', ''], ['Idiomas', '2', ''], ['Integraciones activas', '3', '']],
            title: 'Cómo atiende el agente', when: 'Clínica Dental Norte', settings: [
              ['Horario', 'Responde 24 horas, 7 días', true],
              ['Tono', 'Profesional y cercano', true],
              ['Idiomas', 'Español e inglés', true],
              ['Pasa a una persona', 'Urgencias, dolor y presupuestos', true],
              ['Recordatorio de cita', '24 horas antes, con confirmación', true],
              ['Lista de espera', 'Ofrece los huecos liberados a quien espera', true],
              ['Integraciones', 'WhatsApp Business API · Google Calendar · Software clínico', true]
            ] }
        ],
        msgs: [
          { d: 'in', t: 'Buenas noches, ¿puedo cambiar mi cita del jueves? No puedo a las 10.', m: 0 },
          { d: 'out', t: 'Claro, Marta. El jueves hay hueco con la Dra. Ruiz. ¿Cuál te viene mejor?', buttons: ['Jueves 12:30', 'Jueves 17:00'], tap: 1, m: 0 },
          { d: 'in', t: 'Jueves 17:00', m: 1, reply: true },
          { d: 'out', t: 'Hecho: jueves a las 17:00 con la Dra. Ruiz. Te envío un recordatorio el miércoles. Si necesitas moverla otra vez, escríbeme aquí.', m: 1 },
          { d: 'in', t: 'Perfecto, gracias', m: 2 },
          { d: 'out', t: 'A ti. ¡Hasta el jueves!', m: 2 }
        ]
      },
      gimnasio: {
        name: 'Gimnasio Forma', avatar: 'G', brand: 'Gimnasio Forma', where: 'Sevilla · 420 socios',
        views: [
          { tab: 'Leads', kpis: [['Leads esta semana', '31', '+1'], ['Pruebas agendadas', '12', '+1'], ['Altas este mes', '7', '']],
            title: 'Leads de esta semana', when: 'Semana 45', cols: ['Nombre', 'Origen', 'Interés', 'Prueba', 'Estado'], opt: [1, 2],
            rows: [
              ['Diego', 'WhatsApp', 'Funcional', 'Mié 18:30', 'agent', '', true],
              ['Carla Ríos', 'Instagram', 'Spinning', 'Jue 19:30', 'ok', 'Prueba agendada'],
              ['Tomás Vega', 'Web', 'Pesas', '—', 'wait', 'Sin respuesta'],
              ['Nuria Bel', 'WhatsApp', 'Yoga', 'Vie 10:00', 'ok', 'Alta'],
              ['Iván Soto', 'Google', 'Funcional', 'Mar 18:30', 'ok', 'Prueba hecha'],
              ['Sara Núñez', 'Instagram', 'Pilates', '—', 'wait', 'Seguimiento jueves']
            ] },
          { tab: 'Socios', kpis: [['Socios activos', '420', ''], ['Bajas este mes', '1,8 %', ''], ['Reactivados por el agente', '9', '']],
            title: 'Socios', when: 'Asistencia de las últimas 2 semanas', cols: ['Socio', 'Plan', 'Alta', 'Asistencia', 'Estado'], opt: [2],
            rows: [
              ['Nuria Bel', 'Mensual', '28 oct', '3 por semana', 'ok', 'Activo'],
              ['Iván Soto', 'Trimestral', '12 sep', '4 por semana', 'ok', 'Activo'],
              ['Alba Gil', 'Mensual', '14 oct', '0 en 2 semanas', 'agent', 'Reactivación enviada'],
              ['Pau Mas', 'Anual', '3 ene', '1 por semana', 'wait', 'En riesgo'],
              ['Marcos Ruiz', 'Mensual', '2 feb', '2 por semana', 'ok', 'Activo'],
              ['Lola Peña', 'Anual', '9 mar', '5 por semana', 'ok', 'Activo']
            ] },
          { tab: 'Campañas', kpis: [['Altas por campañas este mes', '7', ''], ['Reactivaciones', '9', ''], ['Coste por lead', '1,10 €', '']],
            title: 'Campañas', when: 'Noviembre', cols: ['Campaña', 'Enviados', 'Respuestas', 'Resultado', 'Estado'], opt: [2],
            rows: [
              ['Reactivar socios inactivos (14 días)', '36', '14', '9 han vuelto', 'ok', 'Activa'],
              ['Clase de prueba gratis (Instagram)', '180', '31', '12 pruebas', 'ok', 'Activa'],
              ['Renovación anual con descuento', '54', '27', '21 renovaciones', 'ok', 'Activa'],
              ['Recordatorio de clase reservada', 'Automático', '—', '98 % asisten', 'ok', 'Activa'],
              ['Reto de enero', '—', '—', '—', 'off', 'Borrador']
            ] },
          { tab: 'Agente', kpis: [['Conversaciones hoy', '28', '+1'], ['Resueltas sin intervención', '89 %', ''], ['Tiempo medio de respuesta', '22 s', '']],
            title: 'Conversaciones de hoy', when: 'Última: ahora', cols: ['Hora', 'Contacto', 'Intención', 'Resultado', 'Estado'], opt: [2],
            rows: [
              ['{t}', 'Diego', 'Precio y prueba', 'Funcional el miércoles 18:30', 'agent', 'Resuelto', true],
              ['22:20', 'Alba Gil', 'Volver tras una lesión', 'Pasado al entrenador', 'esc', 'Escalado'],
              ['21:15', 'Marcos Ruiz', 'Horario de spinning', 'Respondido', 'ok', 'Resuelto'],
              ['20:30', 'Sara Núñez', 'Pilates', 'Seguimiento el jueves', 'wait', 'Pendiente'],
              ['19:45', 'Pau Mas', 'Cambiar de plan', 'Pasado a recepción', 'esc', 'Escalado'],
              ['18:50', 'Nuria Bel', 'Reservar clase', 'Yoga el viernes 10:00', 'ok', 'Resuelto']
            ] },
          { tab: 'Ajustes', kpis: [['Horario del agente', '24 h', ''], ['Idiomas', '1', ''], ['Integraciones activas', '3', '']],
            title: 'Cómo atiende el agente', when: 'Gimnasio Forma', settings: [
              ['Horario', 'Responde 24 horas, 7 días', true],
              ['Tono', 'Directo y motivador', true],
              ['Idiomas', 'Español', true],
              ['Pasa a una persona', 'Lesiones y cambios de plan', true],
              ['Recordatorio de clase', '2 horas antes', true],
              ['Reactivar inactivos', 'A los 14 días sin venir', true],
              ['Integraciones', 'WhatsApp Business API · Instagram · Control de acceso', true]
            ] }
        ],
        msgs: [
          { d: 'in', t: 'Hola, ¿cuánto cuesta la mensualidad?', m: 0 },
          { d: 'out', t: '¡Hola! La cuota es 39 € al mes sin permanencia, con acceso a todas las clases. ¿Quieres probar una clase gratis esta semana?', buttons: ['Sí, quiero probar', 'Más información'], tap: 0, m: 0 },
          { d: 'in', t: 'Sí, quiero probar', m: 1, reply: true },
          { d: 'in', t: '¿Puede ser el miércoles por la tarde? Soy Diego', m: 1 },
          { d: 'out', t: 'El miércoles hay funcional a las 18:30 y spinning a las 19:30. ¿Cuál te apunto?', buttons: ['Funcional 18:30', 'Spinning 19:30'], tap: 0, m: 1 },
          { d: 'in', t: 'Funcional 18:30', m: 2, reply: true },
          { d: 'out', t: 'Listo, Diego: funcional el miércoles a las 18:30. Trae ropa cómoda y llega 10 minutos antes. ¡Te esperamos!', m: 2 }
        ]
      }
    },
    en: {
      caption: { night: 'What the agent does at {t}, after you have closed', day: 'What the agent is doing right now, at {t}, while you serve customers' },
      status: { online: 'online', typing: 'typing…' },
      day: 'Today', lock: 'Messages are end-to-end encrypted.', input: 'Message',
      crmTag: 'Tailor-made CRM', updated: 'Updated just now', agentState: 'By the agent', settings: 'Settings',
      onLabel: 'On', offLabel: 'Off',
      restaurante: {
        name: 'La Terraza · Restaurant', avatar: 'L', brand: 'La Terraza', where: 'Madrid · 2 rooms',
        views: [
          { tab: 'Bookings', kpis: [['Bookings for tomorrow', '23', '+1'], ['Occupancy at 21:00', '92 %', ''], ['Handled by the agent', '15', '+1']],
            title: 'Tomorrow’s bookings', when: 'Tuesday', cols: ['Time', 'Name', 'Guests', 'Area', 'Notes', 'Status'], opt: [3, 4],
            rows: [
              ['20:00', 'Ortega family', '6', 'Dining room', 'Birthday', 'ok', 'Confirmed'],
              ['20:30', 'Marc Vidal', '2', 'Terrace', '—', 'ok', 'Confirmed'],
              ['21:00', 'Laura', '4', 'Terrace', 'Gluten free', 'agent', '', true],
              ['21:00', 'Ana Ruiz', '3', 'Dining room', 'High chair', 'wait', 'Pending'],
              ['21:30', 'Pedro Lima', '2', 'Terrace', '—', 'ok', 'Confirmed'],
              ['22:00', 'Sato party', '8', 'Dining room', 'Tasting menu', 'ok', 'Confirmed']
            ] },
          { tab: 'Guests', kpis: [['Guests in the CRM', '1,284', ''], ['Regulars (3+ visits)', '412', ''], ['Return after a reminder', '61 %', '']],
            title: 'Guests', when: 'Last 90 days', cols: ['Name', 'Visits', 'Last', 'Preferences', 'Status'], opt: [3],
            rows: [
              ['Laura', '1', 'Tomorrow', 'Gluten free · Terrace', 'agent', 'New'],
              ['Marc Vidal', '12', 'Tomorrow', 'Terrace · House wine', 'ok', 'Regular'],
              ['Ortega family', '6', 'Tomorrow', 'Dining room · Birthday', 'ok', 'Regular'],
              ['Pedro Lima', '4', 'Tomorrow', 'Terrace', 'ok', 'Regular'],
              ['Ana Ruiz', '2', '3 weeks ago', 'High chair', 'wait', 'Reminder sent'],
              ['Sato party', '3', '2 months ago', 'Tasting menu · Corporate', 'ok', 'Corporate']
            ] },
          { tab: 'Campaigns', kpis: [['Bookings from campaigns this month', '62', ''], ['Reply rate', '14 %', ''], ['Cost per booking', '€0.90', '']],
            title: 'WhatsApp campaigns', when: 'November', cols: ['Campaign', 'Sent', 'Replies', 'Bookings', 'Status'], opt: [2],
            rows: [
              ['Seasonal menu', '620', '84', '37', 'ok', 'Live'],
              ['Win back inactive guests (90 days)', '240', '31', '14', 'ok', 'Live'],
              ['Birthdays this month', '48', '19', '11', 'wait', 'Scheduled'],
              ['Review request after the visit', '310', '92', '—', 'ok', 'Live'],
              ['Corporate Christmas dinners', '—', '—', '—', 'off', 'Draft']
            ] },
          { tab: 'Agent', kpis: [['Conversations today', '31', '+1'], ['Resolved without a human', '94 %', ''], ['Average reply time', '28 s', '']],
            title: 'Today’s conversations', when: 'Last: just now', cols: ['Time', 'Guest', 'Intent', 'Outcome', 'Status'], opt: [2],
            rows: [
              ['{t}', 'Laura', 'Booking', 'Table for 4 tomorrow at 21:00', 'agent', 'Resolved', true],
              ['22:31', 'Javier', 'Opening hours', 'Answered', 'ok', 'Resolved'],
              ['21:57', 'Carmen', 'Cancellation', 'Table released', 'ok', 'Resolved'],
              ['21:10', 'Hugo', 'Allergies and menu', 'Menu sent', 'ok', 'Resolved'],
              ['20:42', 'Marta', 'Event for 20 people', 'Handed to the manager', 'esc', 'Escalated'],
              ['19:30', 'Álvaro', 'Booking', 'Table for 2 on Saturday', 'ok', 'Resolved']
            ] },
          { tab: 'Settings', kpis: [['Agent hours', '24 h', ''], ['Languages', '2', ''], ['Active integrations', '3', '']],
            title: 'How the agent serves', when: 'La Terraza', settings: [
              ['Hours', 'Replies 24 hours, 7 days', true],
              ['Tone', 'Warm and informal, the house voice', true],
              ['Languages', 'Spanish and English', true],
              ['Hands over to a person', 'Events over 12 people and complaints', true],
              ['Booking reminder', '3 hours before, on WhatsApp', true],
              ['Ask for a review after the visit', 'Next day at 12:00', true],
              ['Integrations', 'WhatsApp Business API · Google Calendar · POS', true]
            ] }
        ],
        msgs: [
          { d: 'in', t: 'Hi, do you have a table for 4 tomorrow at 21:00?', m: 0 },
          { d: 'out', t: 'Hi! Yes, we still have a table for 4 at 21:00. Where would you like to sit?', buttons: ['Terrace', 'Dining room'], tap: 0, m: 0 },
          { d: 'in', t: 'Terrace', m: 1, reply: true },
          { d: 'in', t: 'Under Laura.', m: 1 },
          { d: 'out', t: 'Done, Laura: table for 4 tomorrow at 21:00 on the terrace. I will send you a reminder tomorrow at 18:00. Any allergies we should know about?', m: 1 },
          { d: 'in', t: 'Gluten free, thanks', m: 2 },
          { d: 'out', t: 'Noted, we will tell the kitchen. See you tomorrow!', m: 2 }
        ]
      },
      clinica: {
        name: 'Clínica Dental Norte', avatar: 'C', brand: 'Clínica Dental Norte', where: 'Valencia · 3 surgeries',
        views: [
          { tab: 'Schedule', kpis: [['Appointments Thursday', '18', ''], ['Open slots', '3', '+1'], ['Changes made by the agent', '6', '+1']],
            title: 'Thursday schedule · Dr. Ruiz', when: 'Thursday', cols: ['Time', 'Patient', 'Treatment', 'Reminder', 'Status'], opt: [2, 3],
            rows: [
              ['10:00', 'Open', '—', '—', 'off', 'Slot freed'],
              ['10:30', 'Jorge Peña', 'Cleaning', 'Sent', 'ok', 'Confirmed'],
              ['12:30', 'Open', '—', '—', 'off', 'Available'],
              ['16:00', 'Elena Soto', 'Check-up', 'Sent', 'ok', 'Confirmed'],
              ['17:00', 'Marta Gil', 'Check-up', 'Wednesday 17:00', 'agent', '', true],
              ['17:30', 'Luis Mora', 'Filling', 'Sent', 'ok', 'Confirmed']
            ] },
          { tab: 'Patients', kpis: [['Active patients', '2,140', ''], ['Check-ups up to date', '78 %', ''], ['No-shows this month', '4 %', '']],
            title: 'Patients', when: 'With an appointment this month', cols: ['Patient', 'Treatment', 'Last visit', 'Next', 'Status'], opt: [3],
            rows: [
              ['Marta Gil', 'Check-up', '6 months ago', 'Thursday 17:00', 'agent', 'Appointment moved'],
              ['Jorge Peña', 'Cleaning', '1 year ago', 'Thursday 10:30', 'ok', 'Confirmed'],
              ['Elena Soto', 'Check-up', '6 months ago', 'Thursday 16:00', 'ok', 'Confirmed'],
              ['Nerea Díaz', 'Orthodontics', '1 month ago', 'In 4 weeks', 'ok', 'In treatment'],
              ['Pablo Ruiz', 'Implant', '2 weeks ago', '—', 'wait', 'Quote sent'],
              ['Luis Mora', 'Filling', '3 months ago', 'Thursday 17:30', 'ok', 'Confirmed']
            ] },
          { tab: 'Campaigns', kpis: [['Appointments from campaigns', '75', ''], ['Automatic confirmations', '96 %', ''], ['Slots recovered this month', '18', '']],
            title: 'WhatsApp campaigns', when: 'November', cols: ['Campaign', 'Sent', 'Replies', 'Appointments', 'Status'], opt: [2],
            rows: [
              ['Annual check-up due', '180', '71', '52', 'ok', 'Live'],
              ['Confirmation 24 h before', 'Automatic', '—', '96 % confirm', 'ok', 'Live'],
              ['Autumn whitening', '420', '58', '23', 'ok', 'Live'],
              ['Survey after the visit', '140', '97', '4.9 / 5', 'ok', 'Live'],
              ['Invisible orthodontics', '—', '—', '—', 'wait', 'Scheduled']
            ] },
          { tab: 'Agent', kpis: [['Conversations today', '24', '+1'], ['Resolved without a human', '91 %', ''], ['Average reply time', '25 s', '']],
            title: 'Today’s conversations', when: 'Last: just now', cols: ['Time', 'Patient', 'Intent', 'Outcome', 'Status'], opt: [2],
            rows: [
              ['{t}', 'Marta Gil', 'Move an appointment', 'Thursday 17:00 with Dr. Ruiz', 'agent', 'Resolved', true],
              ['21:40', 'Iván', 'Price of a cleaning', 'Answered', 'ok', 'Resolved'],
              ['20:55', 'Rosa', 'Severe pain', 'Handed to the doctor', 'esc', 'Escalated'],
              ['19:20', 'Tomás', 'First visit', 'Friday 10:30 booked', 'ok', 'Resolved'],
              ['18:05', 'Lucía', 'Insurance paperwork', 'Sent', 'ok', 'Resolved'],
              ['17:12', 'Pablo Ruiz', 'Implant quote', 'Quote sent', 'wait', 'Pending']
            ] },
          { tab: 'Settings', kpis: [['Agent hours', '24 h', ''], ['Languages', '2', ''], ['Active integrations', '3', '']],
            title: 'How the agent serves', when: 'Clínica Dental Norte', settings: [
              ['Hours', 'Replies 24 hours, 7 days', true],
              ['Tone', 'Professional and warm', true],
              ['Languages', 'Spanish and English', true],
              ['Hands over to a person', 'Emergencies, pain and quotes', true],
              ['Appointment reminder', '24 hours before, with confirmation', true],
              ['Waiting list', 'Offers freed slots to patients waiting', true],
              ['Integrations', 'WhatsApp Business API · Google Calendar · Practice software', true]
            ] }
        ],
        msgs: [
          { d: 'in', t: 'Good evening, can I move my Thursday appointment? I cannot make 10:00.', m: 0 },
          { d: 'out', t: 'Of course, Marta. Thursday has openings with Dr. Ruiz. Which works better?', buttons: ['Thursday 12:30', 'Thursday 17:00'], tap: 1, m: 0 },
          { d: 'in', t: 'Thursday 17:00', m: 1, reply: true },
          { d: 'out', t: 'Done: Thursday at 17:00 with Dr. Ruiz. I will send a reminder on Wednesday. If you need to move it again, just write here.', m: 1 },
          { d: 'in', t: 'Perfect, thank you', m: 2 },
          { d: 'out', t: 'Thank you. See you Thursday!', m: 2 }
        ]
      },
      gimnasio: {
        name: 'Gimnasio Forma', avatar: 'G', brand: 'Gimnasio Forma', where: 'Seville · 420 members',
        views: [
          { tab: 'Leads', kpis: [['Leads this week', '31', '+1'], ['Trials booked', '12', '+1'], ['Sign-ups this month', '7', '']],
            title: 'This week’s leads', when: 'Week 45', cols: ['Name', 'Source', 'Interest', 'Trial', 'Status'], opt: [1, 2],
            rows: [
              ['Diego', 'WhatsApp', 'Functional', 'Wed 18:30', 'agent', '', true],
              ['Carla Ríos', 'Instagram', 'Spinning', 'Thu 19:30', 'ok', 'Trial booked'],
              ['Tomás Vega', 'Web', 'Weights', '—', 'wait', 'No reply yet'],
              ['Nuria Bel', 'WhatsApp', 'Yoga', 'Fri 10:00', 'ok', 'Signed up'],
              ['Iván Soto', 'Google', 'Functional', 'Tue 18:30', 'ok', 'Trial done'],
              ['Sara Núñez', 'Instagram', 'Pilates', '—', 'wait', 'Follow-up Thursday']
            ] },
          { tab: 'Members', kpis: [['Active members', '420', ''], ['Churn this month', '1.8 %', ''], ['Won back by the agent', '9', '']],
            title: 'Members', when: 'Attendance, last 2 weeks', cols: ['Member', 'Plan', 'Joined', 'Attendance', 'Status'], opt: [2],
            rows: [
              ['Nuria Bel', 'Monthly', '28 Oct', '3 a week', 'ok', 'Active'],
              ['Iván Soto', 'Quarterly', '12 Sep', '4 a week', 'ok', 'Active'],
              ['Alba Gil', 'Monthly', '14 Oct', '0 in 2 weeks', 'agent', 'Win-back sent'],
              ['Pau Mas', 'Annual', '3 Jan', '1 a week', 'wait', 'At risk'],
              ['Marcos Ruiz', 'Monthly', '2 Feb', '2 a week', 'ok', 'Active'],
              ['Lola Peña', 'Annual', '9 Mar', '5 a week', 'ok', 'Active']
            ] },
          { tab: 'Campaigns', kpis: [['Sign-ups from campaigns this month', '7', ''], ['Members won back', '9', ''], ['Cost per lead', '€1.10', '']],
            title: 'Campaigns', when: 'November', cols: ['Campaign', 'Sent', 'Replies', 'Result', 'Status'], opt: [2],
            rows: [
              ['Win back inactive members (14 days)', '36', '14', '9 came back', 'ok', 'Live'],
              ['Free trial class (Instagram)', '180', '31', '12 trials', 'ok', 'Live'],
              ['Annual renewal with a discount', '54', '27', '21 renewals', 'ok', 'Live'],
              ['Reminder for booked classes', 'Automatic', '—', '98 % attend', 'ok', 'Live'],
              ['January challenge', '—', '—', '—', 'off', 'Draft']
            ] },
          { tab: 'Agent', kpis: [['Conversations today', '28', '+1'], ['Resolved without a human', '89 %', ''], ['Average reply time', '22 s', '']],
            title: 'Today’s conversations', when: 'Last: just now', cols: ['Time', 'Contact', 'Intent', 'Outcome', 'Status'], opt: [2],
            rows: [
              ['{t}', 'Diego', 'Price and trial', 'Functional on Wednesday 18:30', 'agent', 'Resolved', true],
              ['22:20', 'Alba Gil', 'Coming back after an injury', 'Handed to the trainer', 'esc', 'Escalated'],
              ['21:15', 'Marcos Ruiz', 'Spinning timetable', 'Answered', 'ok', 'Resolved'],
              ['20:30', 'Sara Núñez', 'Pilates', 'Follow-up on Thursday', 'wait', 'Pending'],
              ['19:45', 'Pau Mas', 'Change of plan', 'Handed to the front desk', 'esc', 'Escalated'],
              ['18:50', 'Nuria Bel', 'Book a class', 'Yoga on Friday 10:00', 'ok', 'Resolved']
            ] },
          { tab: 'Settings', kpis: [['Agent hours', '24 h', ''], ['Languages', '1', ''], ['Active integrations', '3', '']],
            title: 'How the agent serves', when: 'Gimnasio Forma', settings: [
              ['Hours', 'Replies 24 hours, 7 days', true],
              ['Tone', 'Direct and motivating', true],
              ['Languages', 'Spanish', true],
              ['Hands over to a person', 'Injuries and plan changes', true],
              ['Class reminder', '2 hours before', true],
              ['Win back inactive members', 'After 14 days without a visit', true],
              ['Integrations', 'WhatsApp Business API · Instagram · Access control', true]
            ] }
        ],
        msgs: [
          { d: 'in', t: 'Hi, how much is the monthly membership?', m: 0 },
          { d: 'out', t: 'It is 39 € a month with no lock-in, all classes included. Want to try a free class this week?', buttons: ['Yes, I want to try', 'More information'], tap: 0, m: 0 },
          { d: 'in', t: 'Yes, I want to try', m: 1, reply: true },
          { d: 'in', t: 'Could it be Wednesday afternoon? I am Diego', m: 1 },
          { d: 'out', t: 'On Wednesday there is functional at 18:30 and spinning at 19:30. Which one shall I book?', buttons: ['Functional 18:30', 'Spinning 19:30'], tap: 0, m: 1 },
          { d: 'in', t: 'Functional 18:30', m: 2, reply: true },
          { d: 'out', t: 'Done, Diego: functional on Wednesday at 18:30. Bring comfortable clothes and arrive 10 minutes early. See you!', m: 2 }
        ]
      }
    }
  };

  var root = document.getElementById('demoChat');
  if (!root) return;
  var buttons = Array.prototype.slice.call(document.querySelectorAll('.demo-switch button'));
  var body = root.querySelector('.chat-body');
  var head = root.querySelector('.chat-head');
  var avatar = head.querySelector('.chat-avatar');
  var who = head.querySelector('.chat-who strong');
  var status = head.querySelector('.chat-status');
  var input = root.querySelector('.chat-input-field');
  var caption = document.getElementById('demoCaption');
  var clock = document.querySelector('.phone-time');
  var win = document.getElementById('crmWindow');
  var markHTML = (win && win.querySelector('.crm-mark')) ? win.querySelector('.crm-mark').innerHTML : 'Z';
  var timers = [];
  var current = 'restaurante';
  var crm = { view: 0, newShown: false, L: null, d: null };
  var motion = function () {
    return document.documentElement.classList.contains('js') && !window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  };

  function lang() {
    var l = (document.documentElement.lang || 'es').slice(0, 2).toLowerCase();
    return DATA[l] ? l : 'es';
  }
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function hhmm(d) { return pad(d.getHours()) + ':' + pad(d.getMinutes()); }
  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; });
  }
  function later(ms, fn) { timers.push(setTimeout(fn, ms)); }

  function tick() {
    var now = new Date();
    if (clock) clock.textContent = hhmm(now);
    if (caption) {
      var L = DATA[lang()];
      var h = now.getHours();
      caption.textContent = (h >= 20 || h < 8 ? L.caption.night : L.caption.day).replace('{t}', hhmm(now));
    }
  }

  function bubble(m, when) {
    var el = document.createElement('div');
    el.className = 'msg ' + m.d + (m.reply ? ' reply' : '');
    var html = '<span class="msg-text">' + esc(m.t) + '</span><time>' + esc(when) + (m.d === 'out' ? '<i class="ticks" aria-hidden="true"></i>' : '') + '</time>';
    if (m.buttons) {
      html += '<span class="msg-buttons">' + m.buttons.map(function (b) { return '<span>' + esc(b) + '</span>'; }).join('') + '</span>';
    }
    el.innerHTML = html;
    return el;
  }

  // ---- el CRM a medida: la ventana (barra lateral, cabecera) y la vista elegida
  function bump(value) {
    // «23» pasa a «24» cuando la fila nueva ya está dentro; lo que no es un número se queda igual
    var m = /^(\d[\d.,]*)(.*)$/.exec(value);
    if (!m) return value;
    var digits = m[1];
    var n = parseInt(digits.replace(/[.,]/g, ''), 10) + 1;
    var out = String(n);
    if (digits.length > 3 && digits.indexOf('.') >= 0) out = out.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
    else if (digits.length > 3 && digits.indexOf(',') >= 0) out = out.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    return out + m[2];
  }
  function navItem(v, i, cls) {
    var on = i === crm.view;
    return '<button type="button" class="' + cls + (on ? ' on' : '') + '" role="tab" aria-selected="' + (on ? 'true' : 'false') + '" data-view="' + i + '">' + esc(v.tab) + '</button>';
  }
  function renderCRM(L, d) {
    if (!win) return;
    crm.L = L; crm.d = d;
    win.setAttribute('aria-label', L.crmTag + ' · ' + d.brand);
    var side = d.views.map(function (v, i) { return navItem(v, i, 'crm-nav'); }).join('');
    var tabs = d.views.map(function (v, i) { return navItem(v, i, 'crm-tab'); }).join('');
    var html = '<aside class="crm-side"><span class="crm-mark" aria-hidden="true">' + markHTML + '</span><nav role="tablist" aria-label="' + esc(L.crmTag) + '">' + side + '</nav><div class="crm-who"><b>' + esc(d.brand) + '</b>' + esc(d.where) + '</div></aside>';
    html += '<div class="crm-main"><div class="crm-top"><span class="crm-mark" aria-hidden="true">' + markHTML + '</span><span class="crm-brand">' + esc(d.brand) + ' <span>· ' + esc(L.crmTag) + '</span></span><span class="crm-live">' + esc(L.updated) + '</span><div class="crm-tabs" role="tablist">' + tabs + '</div></div><div class="crm-body" role="tabpanel"></div></div>';
    win.innerHTML = html;
    renderView(crm.view, false);
  }
  function renderView(idx, animate) {
    if (!win || !crm.d) return;
    var L = crm.L, v = crm.d.views[idx];
    if (!v) return;
    crm.view = idx;
    var live = crm.newShown;
    win.classList.toggle('updated', live);
    win.querySelectorAll('[data-view]').forEach(function (b) {
      var on = parseInt(b.getAttribute('data-view'), 10) === idx;
      b.classList.toggle('on', on); b.setAttribute('aria-selected', on ? 'true' : 'false');
    });
    var now = hhmm(new Date());
    var html = '<div class="crm-kpis">' + v.kpis.map(function (k) {
      var val = (live && k[2]) ? bump(k[1]) : k[1];
      return '<div class="crm-kpi"><small>' + esc(k[0]) + '</small><strong>' + esc(val) + (k[2] ? '<i>' + esc(k[2]) + '</i>' : '') + '</strong></div>';
    }).join('') + '</div>';
    html += '<div class="crm-title"><b>' + esc(v.title) + '</b><em>' + esc(v.when) + '</em></div>';
    if (v.settings) {
      html += '<div class="crm-settings">' + v.settings.map(function (s) {
        return '<div class="crm-set"><div class="crm-set-text"><b>' + esc(s[0]) + '</b><span>' + esc(s[1]) + '</span></div>' +
          '<button type="button" class="crm-toggle' + (s[2] ? ' on' : '') + '" role="switch" aria-checked="' + (s[2] ? 'true' : 'false') + '" aria-label="' + esc(s[0]) + '"><span class="crm-toggle-label">' + esc(s[2] ? L.onLabel : L.offLabel) + '</span></button></div>';
      }).join('') + '</div>';
    } else {
      html += '<table class="crm"><thead><tr>' + v.cols.map(function (col, i) { return '<th' + (v.opt.indexOf(i) >= 0 ? ' class="opt"' : '') + '>' + esc(col) + '</th>'; }).join('') + '</tr></thead><tbody>';
      v.rows.forEach(function (r) {
        var n = v.cols.length - 1;
        var isNew = r[n + 2] === true;
        html += '<tr' + (isNew ? ' class="crm-row new' + (live ? ' show' : '') + '"' : '') + '>';
        for (var i = 0; i < n; i++) {
          var cls = [];
          if (v.opt.indexOf(i) >= 0) cls.push('opt');
          if (v.opt.indexOf(i) >= 0 && i === v.opt[v.opt.length - 1]) cls.push('dim');
          html += '<td' + (cls.length ? ' class="' + cls.join(' ') + '"' : '') + '>' + esc(String(r[i]).replace('{t}', now)) + '</td>';
        }
        var state = r[n], label = r[n + 1] || L.agentState;
        html += '<td><span class="crm-state ' + esc(state) + '">' + esc(label) + '</span></td></tr>';
      });
      html += '</tbody></table>';
    }
    var panel = win.querySelector('.crm-body');
    panel.innerHTML = html;
    if (animate && motion()) {
      panel.classList.remove('swap'); void panel.offsetWidth; panel.classList.add('swap');
    }
  }
  function showNewRow() {
    if (!win) return;
    crm.newShown = true;
    renderView(crm.view, false);
  }
  if (win) {
    win.addEventListener('click', function (e) {
      var nav = e.target.closest ? e.target.closest('[data-view]') : null;
      if (nav) { renderView(parseInt(nav.getAttribute('data-view'), 10), true); return; }
      var tog = e.target.closest ? e.target.closest('.crm-toggle') : null;
      if (tog) {
        var on = !tog.classList.contains('on');
        tog.classList.toggle('on', on); tog.setAttribute('aria-checked', on ? 'true' : 'false');
        tog.querySelector('.crm-toggle-label').textContent = on ? crm.L.onLabel : crm.L.offLabel;
      }
    });
    // flechas entre pestañas, como en una interfaz de verdad
    win.addEventListener('keydown', function (e) {
      if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft' && e.key !== 'ArrowDown' && e.key !== 'ArrowUp') return;
      var t = e.target.closest ? e.target.closest('[data-view]') : null;
      if (!t) return;
      e.preventDefault();
      var n = crm.d.views.length;
      var next = (crm.view + ((e.key === 'ArrowRight' || e.key === 'ArrowDown') ? 1 : n - 1)) % n;
      renderView(next, true);
      var cls = t.classList.contains('crm-tab') ? '.crm-tab' : '.crm-nav';
      var el = win.querySelector(cls + '[data-view="' + next + '"]');
      if (el) el.focus();
    });
  }

  function render(key) {
    timers.forEach(clearTimeout); timers = [];
    current = key;
    var L = DATA[lang()];
    var d = L[key];
    var now = new Date();
    var base = new Date(now.getTime() - 3 * 60000);
    who.textContent = d.name;
    status.textContent = L.status.online;
    if (avatar) avatar.textContent = d.avatar;
    if (input) input.textContent = L.input;
    tick();
    crm.view = 0; crm.newShown = false;
    renderCRM(L, d);
    body.innerHTML = '<div class="chat-day">' + esc(L.day) + '</div><div class="chat-lock">' + esc(L.lock) + '</div>';
    var t = 300;
    d.msgs.forEach(function (m) {
      var when = hhmm(new Date(base.getTime() + m.m * 60000));
      var el = bubble(m, when);
      if (!motion()) {
        body.appendChild(el); el.classList.add('shown');
        if (m.d === 'out') el.classList.add('read');
        if (m.buttons && typeof m.tap === 'number') el.querySelectorAll('.msg-buttons span')[m.tap].classList.add('tapped');
        return;
      }
      if (m.d === 'out') {
        later(t, function () { status.textContent = L.status.typing; });
        t += 1100;
        later(t, function () { status.textContent = L.status.online; body.appendChild(el); requestAnimationFrame(function () { el.classList.add('shown'); }); });
        t += 650;
        later(t, function () { el.classList.add('read'); });
        if (m.buttons && typeof m.tap === 'number') {
          var idx = m.tap;
          t += 900;
          later(t, function () { el.querySelectorAll('.msg-buttons span')[idx].classList.add('tapped'); });
          t += 250;
        } else {
          t += 500;
        }
      } else {
        later(t, function () { body.appendChild(el); requestAnimationFrame(function () { el.classList.add('shown'); }); });
        t += m.reply ? 500 : 900;
      }
    });
    if (!motion()) { showNewRow(); }
    else { later(t + 400, showNewRow); }
    buttons.forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-sector') === key)); });
  }

  buttons.forEach(function (b) {
    b.addEventListener('click', function () { render(b.getAttribute('data-sector')); });
  });

  // Si la página cambia de idioma (la portada en inglés se traduce en el navegador),
  // la escena se vuelve a pintar en ese idioma.
  if (window.MutationObserver) {
    new MutationObserver(function () { render(current); })
      .observe(document.documentElement, { attributes: true, attributeFilter: ['lang'] });
  }

  // La hora del teléfono sigue la del visitante.
  tick();
  setInterval(tick, 30000);

  // Arranca cuando la escena entra en pantalla, para que la secuencia se vea.
  var started = false;
  function start() { if (started) return; started = true; render(current); }
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      if (entries.some(function (e) { return e.isIntersecting; })) { start(); io.disconnect(); }
    }, { threshold: 0.25 });
    io.observe(root);
  } else {
    start();
  }
})();
