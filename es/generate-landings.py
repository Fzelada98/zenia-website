"""
Zenia Partners — Spanish Landing Page Generator
Generates SEO-optimized landing pages for Spain market
Uses the SAME design system as the main homepage (main.css)
Pricing: €297/€497/€897, Setup €997 (ONLY for /es pages)
"""

import os

# =============================================================================
# VERTICAL DATA
# =============================================================================

VERTICALS = [
    # Tier 1 — GSC already detects
    {
        "slug": "crm-restaurantes",
        "title": "CRM con IA para Restaurantes",
        "meta_title": "CRM para Restaurantes | Reservas y WhatsApp con IA | ZENIA",
        "meta_desc": "CRM con agente de IA para restaurantes. Automatiza reservas por WhatsApp, fideliza clientes y gestiona resenas. Listo en 5 semanas. Desde €297/mes.",
        "badge": "Gastronomia",
        "h1_main": "CRM para Restaurantes.",
        "h1_gradient": "Reservas automaticas. Clientes que vuelven.",
        "lead": "Tu agente de IA contesta reservas por WhatsApp, confirma mesas, envia recordatorios y pide resenas en Google. 24/7. Sin que tu equipo toque el telefono.",
        "pain_title": "restaurantes",
        "pains_without": [
            "Reservas por telefono que se pierden en hora punta",
            "No sabes quien es cliente frecuente y quien nuevo",
            "Resenas negativas sin respuesta en Google",
            "Promociones genericas que nadie abre",
            "Cero datos sobre preferencias de tus comensales"
        ],
        "pains_with": [
            "Reservas automatizadas por WhatsApp e Instagram 24/7",
            "Perfil de cada cliente: visitas, platos favoritos, alergias",
            "Alertas de resenas y respuestas sugeridas por IA",
            "Campanas segmentadas con tasas de apertura del 98%",
            "Dashboard con metricas reales de retencion"
        ],
        "content_blocks": [
            {
                "icon": "shield",
                "h2_main": "Por que los restaurantes necesitan un",
                "h2_gradient": "CRM en 2026",
                "text": "La gastronomia ha cambiado. El cliente de hoy no llama para reservar. Escribe por WhatsApp, mira tu Instagram, lee resenas en Google y decide en 30 segundos si va a tu restaurante o al de al lado. Si no estas preparado para esa realidad, estas perdiendo dinero cada dia. Un CRM para restaurantes no es un software generico. Es un sistema que centraliza todas las interacciones con tus clientes y automatiza todo lo que antes dependia de la memoria de tu equipo."
            },
            {
                "icon": "clock",
                "h2_main": "Reservas automatizadas:",
                "h2_gradient": "nunca pierdas una mesa",
                "text": "El sistema de reservas manual es un cuello de botella. En hora pico nadie contesta el telefono. Los mensajes de WhatsApp se acumulan. Con ZENIA, tu agente de IA recibe la solicitud, verifica disponibilidad, confirma la reserva, envia recordatorio 24h antes y pide resena despues de la visita. Reduce no-shows un 45%."
            },
            {
                "icon": "chart",
                "h2_main": "Fidelizacion de clientes:",
                "h2_gradient": "el verdadero negocio",
                "text": "Adquirir un cliente nuevo cuesta 5 veces mas que retener uno existente. En gastronomia, el margen esta en la recurrencia. Nuestro sistema registra cada visita, detecta cumpleanos y aniversarios, y envia invitaciones personalizadas automaticamente. Tasa de conversion en fechas especiales: 35%+."
            }
        ],
        "results": [
            ("-45%", "Reduccion de no-shows"),
            ("+30%", "Clientes recurrentes"),
            ("98%", "Apertura WhatsApp"),
            ("24/7", "Reservas automaticas"),
            ("5sem", "Implementacion completa"),
            ("+35%", "Conversion en fechas especiales")
        ],
        "faqs": [
            ("Puedo gestionar reservas por WhatsApp de forma automatica?",
             "Si. El agente de IA recibe la solicitud, verifica disponibilidad en tiempo real, confirma la mesa, recoge datos del comensal y envia recordatorio automatico. Todo sin intervencion humana."),
            ("Como funciona el programa de fidelizacion?",
             "El CRM registra cada visita y acumula puntos automaticamente. Cuando el cliente alcanza un umbral, recibe un mensaje por WhatsApp con su recompensa. Sin tarjetas fisicas, sin apps."),
            ("Funciona para restaurantes con varias sedes?",
             "Si. Cada sede tiene su disponibilidad propia, pero los datos de clientes son compartidos. Las campanas pueden segmentarse por sede o enviarse a toda la base."),
            ("Se integra con mi sistema de punto de venta?",
             "Trabajamos para integrar con los principales TPV del mercado. La integracion vincula tickets con perfiles de cliente para alimentar el programa de fidelizacion."),
            ("Cuanto cuesta implementar el CRM?",
             "El plan Starter empieza en €297/mes con un setup de €997. Incluye configuracion completa y entrenamiento de tu agente de IA personalizado. Listo en 5 semanas."),
            ("Necesito conocimientos tecnicos?",
             "No. Nosotros hacemos todo. Tu equipo solo necesita saber usar WhatsApp. En 5 semanas tienes el sistema funcionando."),
            ("Puedo cancelar cuando quiera?",
             "Si. Sin permanencia, sin penalizaciones. Cancelas cuando quieras. Pero el 95% de nuestros clientes se quedan porque los resultados hablan solos."),
            ("Que pasa si un cliente quiere hablar con una persona?",
             "El agente de IA detecta cuando una conversacion requiere atencion humana y transfiere la conversacion a tu equipo automaticamente. Nunca pierde un cliente.")
        ],
        "cta_h2_main": "Deja de depender de la suerte para",
        "cta_h2_gradient": "llenar mesas",
        "cta_text": "Habla con nosotros. Te mostramos como automatizar reservas, fidelizar clientes y hacer crecer tu restaurante con IA. Sin compromiso."
    },
    {
        "slug": "crm-gimnasios",
        "title": "CRM con IA para Gimnasios",
        "meta_title": "CRM para Gimnasios | Retencion de Socios con IA | ZENIA",
        "meta_desc": "CRM con agente de IA para gimnasios y centros deportivos. Retiene socios, automatiza seguimiento y genera leads. Desde €297/mes.",
        "badge": "Fitness",
        "h1_main": "CRM para Gimnasios.",
        "h1_gradient": "Socios que se quedan. Leads que entran.",
        "lead": "Tu agente de IA responde consultas de nuevos leads por WhatsApp, hace seguimiento a socios inactivos y automatiza renovaciones. 24/7.",
        "pain_title": "gimnasios",
        "pains_without": [
            "Leads preguntan horarios y nadie responde en 3 horas",
            "Socios cancelan sin que nadie intente retenerlos",
            "Cero seguimiento a quien deja de venir en 2 semanas",
            "Renovaciones manuales que se te olvidan",
            "No sabes que clases funcionan y cuales no"
        ],
        "pains_with": [
            "Respuesta automatica a leads en menos de 2 minutos",
            "Alerta cuando un socio lleva 7 dias sin venir + mensaje automatico",
            "Renovaciones automaticas con recordatorio por WhatsApp",
            "Seguimiento personalizado por objetivo (perdida de peso, fuerza, etc.)",
            "Dashboard con metricas de retencion, asistencia y conversion"
        ],
        "content_blocks": [
            {
                "icon": "shield",
                "h2_main": "El problema real de los",
                "h2_gradient": "gimnasios en 2026",
                "text": "El 67% de los socios de un gimnasio cancelan en los primeros 90 dias. No porque el gimnasio sea malo, sino porque nadie les hace seguimiento. Nadie les pregunta como va su entrenamiento. Nadie les recuerda que tienen una clase reservada manana. Un CRM para gimnasios resuelve esto automaticamente."
            },
            {
                "icon": "clock",
                "h2_main": "Retencion de socios:",
                "h2_gradient": "donde esta el dinero",
                "text": "Captar un socio nuevo cuesta entre €50 y €200 en publicidad. Retener uno existente cuesta €0 si tienes el sistema adecuado. Nuestro agente de IA detecta patrones de abandono (menos visitas, horarios irregulares) y actua antes de que el socio cancele."
            },
            {
                "icon": "chart",
                "h2_main": "Captacion de leads:",
                "h2_gradient": "convierte curiosos en socios",
                "text": "Cuando alguien pregunta por WhatsApp cuanto cuesta la cuota, tienes 5 minutos para responder. Despues de eso, ya esta mirando al gimnasio de al lado. Tu agente de IA responde al instante con horarios, precios, y agenda una visita guiada. Conversion de lead a socio: +40%."
            }
        ],
        "results": [
            ("-35%", "Reduccion de cancelaciones"),
            ("+40%", "Conversion de leads"),
            ("2min", "Tiempo respuesta leads"),
            ("24/7", "Seguimiento automatico"),
            ("5sem", "Implementacion completa"),
            ("+25%", "Ticket promedio")
        ],
        "faqs": [
            ("Como detecta el sistema que un socio va a cancelar?",
             "Analiza patrones: frecuencia de visitas, horarios, tipo de actividad. Cuando detecta una caida (ej: de 4 visitas/semana a 1), activa un mensaje personalizado antes de que el socio tome la decision de irse."),
            ("Funciona para estudios de yoga, pilates o crossfit?",
             "Si. Adaptamos el sistema a cualquier tipo de centro deportivo. Las automatizaciones se configuran segun tu modelo: clases grupales, entrenamiento personal, mixto."),
            ("Se integra con mi software de gestion actual?",
             "Trabajamos con los principales softwares de gestion de gimnasios. La integracion permite sincronizar socios, pagos y asistencia automaticamente."),
            ("Cuanto cuesta?",
             "Desde €297/mes (plan Starter) con setup de €997. Incluye configuracion completa y entrenamiento de tu agente de IA. Listo en 5 semanas."),
            ("Puedo gestionar multiples sedes?",
             "Si. Dashboard centralizado con datos por sede. Cada sede tiene sus propias automatizaciones pero los reportes se consolidan."),
            ("Necesito conocimientos tecnicos?",
             "No. Nosotros implementamos todo. Tu equipo solo necesita saber usar WhatsApp."),
            ("Cuanto tarda la implementacion?",
             "5 semanas desde la firma. Semana 1: analisis de tu negocio. Semanas 2-4: configuracion y entrenamiento IA. Semana 5: lanzamiento y ajustes."),
            ("Que pasa si un lead quiere hablar con una persona?",
             "El agente transfiere la conversacion a tu equipo automaticamente cuando detecta que se necesita atencion humana.")
        ],
        "cta_h2_main": "Deja de perder socios que podrias",
        "cta_h2_gradient": "retener",
        "cta_text": "Habla con nosotros. Te mostramos como reducir cancelaciones y convertir mas leads en socios. Sin compromiso."
    },
    {
        "slug": "crm-salones-belleza",
        "title": "CRM para Salones de Belleza",
        "meta_title": "CRM para Salones de Belleza | Citas y Fidelizacion con IA | ZENIA",
        "meta_desc": "CRM con agente de IA para salones de belleza y estetica. Automatiza citas por WhatsApp, reduce cancelaciones y fideliza clientes. Desde €297/mes.",
        "badge": "Belleza",
        "h1_main": "CRM para Salones de Belleza.",
        "h1_gradient": "Agenda llena. Clientes fieles.",
        "lead": "Tu agente de IA gestiona citas por WhatsApp, envia recordatorios, reduce cancelaciones y lanza campanas de fidelizacion. Sin que tus estilistas toquen el telefono.",
        "pain_title": "salones de belleza",
        "pains_without": [
            "Citas que se cancelan sin aviso y pierdes huecos",
            "Clientas llaman cuando estas atendiendo y no puedes contestar",
            "No recuerdas preferencias de cada clienta (color, corte, productos)",
            "Tus mejores clientas se van sin que te enteres por que",
            "Promociones por Instagram que no sabes si funcionan"
        ],
        "pains_with": [
            "Citas automatizadas por WhatsApp con confirmacion y recordatorio",
            "Perfil de cada clienta: historial de servicios, productos, frecuencia",
            "Alerta cuando una clienta habitual lleva 6 semanas sin venir",
            "Campanas segmentadas: cumpleanos, nuevos servicios, descuentos VIP",
            "Dashboard con metricas de retencion y ticket promedio"
        ],
        "content_blocks": [
            {
                "icon": "shield",
                "h2_main": "Por que tu salon necesita un",
                "h2_gradient": "CRM en 2026",
                "text": "El salon promedio pierde el 25% de sus citas por cancelaciones de ultimo momento. No porque las clientas no quieran venir, sino porque nadie les recordo. Un simple mensaje por WhatsApp 24 horas antes reduce las cancelaciones un 60%. Eso es un CRM bien configurado."
            },
            {
                "icon": "clock",
                "h2_main": "Gestion de citas:",
                "h2_gradient": "nunca pierdas un hueco",
                "text": "Tu clienta escribe por WhatsApp: 'Quiero tinte y corte el viernes'. El agente de IA verifica disponibilidad de tu estilista, confirma la cita, envia recordatorio y si cancela, ofrece el hueco a la siguiente clienta en lista de espera. Todo automatico."
            },
            {
                "icon": "chart",
                "h2_main": "Fidelizacion:",
                "h2_gradient": "que vuelvan siempre",
                "text": "Cada clienta tiene un perfil con su historial completo: que color usa, cada cuanto viene, que productos compra. Cuando lleva tiempo sin venir, recibe un mensaje personalizado. En su cumpleanos, un descuento especial. El resultado: clientas que se sienten cuidadas y no se van a la competencia."
            }
        ],
        "results": [
            ("-60%", "Cancelaciones"),
            ("+25%", "Retencion de clientas"),
            ("98%", "Apertura WhatsApp"),
            ("24/7", "Gestion de citas"),
            ("5sem", "Implementacion completa"),
            ("+20%", "Ticket promedio")
        ],
        "faqs": [
            ("Puedo gestionar citas por WhatsApp automaticamente?",
             "Si. El agente de IA recibe la solicitud, verifica disponibilidad del estilista, confirma la cita y envia recordatorio 24h antes. Si la clienta cancela, ofrece el hueco a la siguiente en lista de espera."),
            ("Se adapta a diferentes servicios y duraciones?",
             "Si. Configuramos cada servicio con su duracion: corte (30min), tinte (2h), tratamiento (1h). El sistema agenda sin solapamientos."),
            ("Puedo enviar promociones segmentadas?",
             "Si. Segmenta por tipo de servicio, frecuencia de visita, ticket promedio, fecha de ultima visita. Envia campanas por WhatsApp con tasa de apertura del 98%."),
            ("Cuanto cuesta?",
             "Desde €297/mes con setup de €997. Incluye configuracion completa, entrenamiento del agente IA y todas las automatizaciones."),
            ("Funciona para cadenas de salones?",
             "Si. Cada sede gestiona sus citas y estilistas, pero los datos de clientas son compartidos para fidelizacion cruzada."),
            ("Necesito conocimientos tecnicos?",
             "No. Nosotros implementamos todo en 5 semanas. Tu equipo solo usa WhatsApp."),
            ("Que pasa si una clienta quiere hablar con alguien?",
             "El agente transfiere automaticamente a tu equipo cuando detecta que se necesita atencion humana."),
            ("Puedo ver el historial de cada clienta?",
             "Si. Perfil completo: servicios realizados, productos comprados, preferencias, frecuencia, valor total acumulado.")
        ],
        "cta_h2_main": "Deja de perder citas y clientas que podrias",
        "cta_h2_gradient": "fidelizar",
        "cta_text": "Habla con nosotros. Te mostramos como llenar tu agenda, reducir cancelaciones y fidelizar a tus mejores clientas. Sin compromiso."
    },
    # Tier 2 — Verticals
    {
        "slug": "crm-clinicas",
        "title": "CRM con IA para Clinicas y Dentistas",
        "meta_title": "CRM para Clinicas y Dentistas | Citas con IA y WhatsApp | ZENIA",
        "meta_desc": "CRM con agente de IA para clinicas, dentistas y consultorios. Automatiza citas, recordatorios y seguimiento de pacientes. Desde €297/mes.",
        "badge": "Salud",
        "h1_main": "CRM para Clinicas y Dentistas.",
        "h1_gradient": "Citas automaticas. Pacientes que vuelven.",
        "lead": "Tu recepcion pierde 2 horas diarias gestionando citas por telefono. Tu agente de IA lo hace en segundos, 24/7, por WhatsApp.",
        "pain_title": "clinicas",
        "pains_without": [
            "Pacientes llaman 5 veces para confirmar una cita",
            "No-shows que te cuestan horas de profesional parado",
            "Seguimiento post-tratamiento manual e inconsistente",
            "Pacientes se van a otro dentista sin que sepas por que",
            "Recepcion saturada en horas punta"
        ],
        "pains_with": [
            "Citas por WhatsApp con confirmacion y recordatorio automatico",
            "No-shows reducidos un 50% con doble recordatorio",
            "Seguimiento post-tratamiento automatico por WhatsApp",
            "Alerta cuando un paciente no vuelve en el plazo esperado",
            "Recepcion liberada: el agente IA gestiona el 80% de llamadas"
        ],
        "content_blocks": [
            {"icon": "shield", "h2_main": "Clinicas y consultorios en", "h2_gradient": "2026", "text": "El paciente moderno no quiere llamar por telefono. Quiere escribir por WhatsApp, confirmar su cita con un mensaje y recibir recordatorios automaticos. Las clinicas que no se adaptan pierden pacientes frente a las que si lo hacen. Un CRM sanitario con IA resuelve esto sin contratar mas recepcionistas."},
            {"icon": "clock", "h2_main": "Gestion de citas:", "h2_gradient": "sin cuellos de botella", "text": "El agente de IA recibe solicitudes de cita por WhatsApp, verifica disponibilidad del profesional, confirma, envia recordatorio 48h y 2h antes, y si el paciente cancela, rellena el hueco con otro paciente en lista de espera. Reduce no-shows un 50%."},
            {"icon": "chart", "h2_main": "Seguimiento de pacientes:", "h2_gradient": "atencion continua", "text": "Despues de un tratamiento, el sistema envia mensajes de seguimiento automaticos: como se siente el paciente, si necesita revision, recordatorio de proxima cita. Mejora la satisfaccion y la retencion sin esfuerzo manual."}
        ],
        "results": [("-50%", "No-shows"), ("+35%", "Retencion pacientes"), ("80%", "Consultas auto-gestionadas"), ("24/7", "Gestion de citas"), ("5sem", "Implementacion"), ("+40%", "Satisfaccion pacientes")],
        "faqs": [
            ("Es seguro para datos de pacientes?", "Si. Cumplimos con RGPD y las mejores practicas de proteccion de datos sanitarios. Los datos se encriptan en transito y en reposo."),
            ("Se integra con mi software de gestion clinica?", "Trabajamos para integrar con los principales softwares del sector. La sincronizacion permite unificar historiales y agendas."),
            ("Puedo gestionar varios profesionales?", "Si. Cada profesional tiene su agenda propia. El agente de IA gestiona disponibilidad de todos desde un solo canal WhatsApp."),
            ("Cuanto cuesta?", "Desde €297/mes con setup de €997. Implementacion completa en 5 semanas."),
            ("Los pacientes saben que hablan con una IA?", "El agente se presenta de forma transparente. Cuando el paciente necesita hablar con una persona, la transferencia es inmediata."),
            ("Funciona para clinicas con varias sedes?", "Si. Dashboard centralizado, agendas por sede, datos compartidos."),
            ("Cuanto tarda la implementacion?", "5 semanas. Nosotros hacemos todo."),
            ("Puedo enviar recordatorios de revisiones periodicas?", "Si. El sistema programa automaticamente recordatorios de revisiones segun el tipo de tratamiento realizado.")
        ],
        "cta_h2_main": "Deja de perder pacientes por",
        "cta_h2_gradient": "falta de seguimiento",
        "cta_text": "Habla con nosotros. Te mostramos como reducir no-shows y fidelizar pacientes. Sin compromiso."
    },
    {
        "slug": "crm-hoteles",
        "title": "CRM con IA para Hoteles",
        "meta_title": "CRM para Hoteles | Reservas Directas con IA y WhatsApp | ZENIA",
        "meta_desc": "CRM con agente de IA para hoteles y alojamientos. Aumenta reservas directas, reduce dependencia de OTAs y fideliza huespedes. Desde €297/mes.",
        "badge": "Hosteleria",
        "h1_main": "CRM para Hoteles.",
        "h1_gradient": "Mas reservas directas. Menos comisiones.",
        "lead": "Pierdes reservas directas porque no contestas en menos de 1 hora. Tu agente de IA responde al instante por WhatsApp con disponibilidad y precios.",
        "pain_title": "hoteles",
        "pains_without": ["Dependencia de Booking y Expedia (15-25% comision)", "Consultas por WhatsApp sin responder durante horas", "Huespedes que no vuelven porque no les haces seguimiento", "Check-in y check-out generan colas en recepcion", "Sin datos de preferencias de huespedes repetidores"],
        "pains_with": ["Reservas directas por WhatsApp sin comision de OTA", "Respuesta instantanea con disponibilidad y precios", "Mensajes pre-estancia con informacion util del destino", "Check-in digital por WhatsApp antes de llegar", "Perfil de huesped con preferencias y estancias anteriores"],
        "content_blocks": [
            {"icon": "shield", "h2_main": "Hoteles en", "h2_gradient": "2026: menos OTAs, mas directo", "text": "Las OTAs se llevan entre el 15% y el 25% de cada reserva. Un hotel de 50 habitaciones puede estar pagando mas de €100,000 al ano en comisiones. El CRM con IA te ayuda a captar reservas directas por WhatsApp, reduciendo tu dependencia de intermediarios."},
            {"icon": "clock", "h2_main": "Reservas directas:", "h2_gradient": "tu canal mas rentable", "text": "Cuando un cliente potencial te escribe por WhatsApp preguntando disponibilidad, tienes 15 minutos para responder. Despues, reserva en Booking. Tu agente de IA responde al instante con habitaciones disponibles, precios y fotos. Cierra la reserva directa sin comisiones."},
            {"icon": "chart", "h2_main": "Experiencia del huesped:", "h2_gradient": "de reserva a resena", "text": "Antes de llegar: informacion del destino, check-in digital. Durante la estancia: servicio de habitaciones por WhatsApp. Despues: solicitud de resena en Google/TripAdvisor. Todo automatico, todo personalizado."}
        ],
        "results": [("+40%", "Reservas directas"), ("-20%", "Comisiones OTA"), ("15min", "Respuesta a consultas"), ("+4.5", "Rating medio"), ("5sem", "Implementacion"), ("€0", "Comision reserva directa")],
        "faqs": [
            ("Se integra con mi PMS?", "Trabajamos para integrar con los principales PMS del mercado (Opera, Cloudbeds, etc.). La sincronizacion permite gestionar disponibilidad en tiempo real."),
            ("Puedo gestionar reservas de grupo?", "Si. El agente recopila datos del grupo (fechas, numero de habitaciones, necesidades especiales) y los pasa a tu equipo para presupuesto personalizado."),
            ("Funciona en varios idiomas?", "Si. El agente de IA puede atender en español, ingles, frances, aleman y otros idiomas segun tus necesidades."),
            ("Cuanto cuesta?", "Desde €297/mes con setup de €997. Listo en 5 semanas."),
            ("Cuanto ahorro en comisiones?", "Dependiendo de tu volumen, nuestros clientes reducen comisiones OTA entre un 15% y un 30% al captar reservas directas."),
            ("Puedo enviar ofertas a huespedes anteriores?", "Si. El CRM almacena el historial de cada huesped y puedes lanzar campanas segmentadas: repetidores, temporada baja, eventos especiales.")
        ],
        "cta_h2_main": "Deja de pagar comisiones por reservas que podrias",
        "cta_h2_gradient": "captar directamente",
        "cta_text": "Habla con nosotros. Te mostramos como aumentar reservas directas y reducir dependencia de OTAs. Sin compromiso."
    },
    {
        "slug": "crm-inmobiliarias",
        "title": "CRM con IA para Inmobiliarias",
        "meta_title": "CRM para Inmobiliarias | Leads y WhatsApp con IA | ZENIA",
        "meta_desc": "CRM con agente de IA para inmobiliarias. Cualifica leads automaticamente, responde consultas de pisos y agenda visitas por WhatsApp. Desde €297/mes.",
        "badge": "Inmobiliaria",
        "h1_main": "CRM para Inmobiliarias.",
        "h1_gradient": "Leads cualificados. Visitas agendadas.",
        "lead": "Tus leads piden informacion de pisos y se van a la competencia que contesta primero. Tu agente de IA responde al instante con fichas, fotos y agenda visitas.",
        "pain_title": "inmobiliarias",
        "pains_without": ["Leads de portales que se enfrian porque tardas en responder", "Agentes que pierden tiempo con leads no cualificados", "Seguimiento manual de decenas de oportunidades a la vez", "No sabes que propiedades interesan a cada lead", "Visitas que se cancelan sin aviso"],
        "pains_with": ["Respuesta instantanea a leads de portales por WhatsApp", "Cualificacion automatica: presupuesto, zona, tipo de inmueble", "Pipeline visual con cada lead y su estado", "Matching automatico: lead-propiedad segun preferencias", "Confirmacion y recordatorio de visitas por WhatsApp"],
        "content_blocks": [
            {"icon": "shield", "h2_main": "Inmobiliarias en", "h2_gradient": "2026: velocidad gana", "text": "El 78% de los compradores contactan a 3 o mas inmobiliarias. El que responde primero se lleva la visita. Si tardas mas de 30 minutos en responder un lead de Idealista o Fotocasa, ya lo perdiste. Un agente de IA responde en segundos, 24/7."},
            {"icon": "clock", "h2_main": "Cualificacion de leads:", "h2_gradient": "solo los que valen la pena", "text": "El agente de IA pregunta presupuesto, zona preferida, metros cuadrados y plazo de compra. Filtra leads serios de curiosos. Tus agentes humanos solo reciben leads cualificados con toda la informacion lista."},
            {"icon": "chart", "h2_main": "Visitas y seguimiento:", "h2_gradient": "cierra mas operaciones", "text": "Agenda visitas automaticamente, envia recordatorios, y despues de la visita pregunta al lead que le parecio. Si le gusto pero no se decide, el sistema hace seguimiento periodico hasta que cierre o descarte."}
        ],
        "results": [("30seg", "Respuesta a leads"), ("+45%", "Leads cualificados"), ("-30%", "Visitas canceladas"), ("+20%", "Tasa de cierre"), ("5sem", "Implementacion"), ("100%", "Leads registrados")],
        "faqs": [
            ("Se integra con Idealista, Fotocasa, etc.?", "Trabajamos para integrar con los principales portales inmobiliarios. Los leads entran automaticamente al CRM y reciben respuesta inmediata."),
            ("Puede enviar fichas de propiedades por WhatsApp?", "Si. El agente envia fotos, caracteristicas, precio y ubicacion de las propiedades que coinciden con las preferencias del lead."),
            ("Funciona para alquiler y venta?", "Si. Configuramos pipelines separados para cada tipo de operacion con sus propias automatizaciones."),
            ("Cuanto cuesta?", "Desde €297/mes con setup de €997. Implementacion completa en 5 semanas."),
            ("Puedo gestionar un equipo de agentes?", "Si. Cada agente tiene su cartera de leads y propiedades. Los reportes consolidan todo en un dashboard."),
            ("Cuanto tarda la implementacion?", "5 semanas. Nosotros hacemos todo.")
        ],
        "cta_h2_main": "Deja de perder leads que podrias",
        "cta_h2_gradient": "convertir en ventas",
        "cta_text": "Habla con nosotros. Te mostramos como responder mas rapido y cerrar mas operaciones. Sin compromiso."
    },
    {
        "slug": "crm-cafeterias",
        "title": "CRM para Cafeterias y Bares",
        "meta_title": "CRM para Cafeterias y Bares | Fidelizacion con IA | ZENIA",
        "meta_desc": "CRM para cafeterias y bares. Programa de fidelizacion automatico por WhatsApp, campanas segmentadas y gestion de resenas. Desde €297/mes.",
        "badge": "Gastronomia",
        "h1_main": "CRM para Cafeterias y Bares.",
        "h1_gradient": "Clientes habituales. No casualidades.",
        "lead": "Tu competencia ya fideliza con programas de puntos automaticos y tu sigues con tarjetas de papel. Es hora de cambiar.",
        "pain_title": "cafeterias y bares",
        "pains_without": ["Clientes que vienen una vez y no vuelven", "Programa de fidelizacion en papel que nadie llena", "No sabes cuantos clientes habituales tienes realmente", "Promociones que no llegan a quien deberian", "Resenas negativas sin responder"],
        "pains_with": ["Programa de fidelizacion digital por WhatsApp", "Perfil de cada cliente con frecuencia y consumo medio", "Campanas segmentadas: 'No vienes hace 2 semanas'", "Ofertas de cumpleanos automaticas", "Gestion de resenas con respuestas sugeridas por IA"],
        "content_blocks": [
            {"icon": "shield", "h2_main": "Cafeterias y bares en", "h2_gradient": "2026: fidelizar es el juego", "text": "El cafe de la esquina compite con 5 opciones en la misma calle. La diferencia no esta en el cafe, esta en la experiencia. Un CRM que recuerda que tu cliente habitual pide cortado con leche de avena y le manda una oferta en su cumpleanos convierte casualidades en habituales."},
            {"icon": "clock", "h2_main": "Fidelizacion digital:", "h2_gradient": "sin tarjetas de papel", "text": "Tu cliente escanea un QR, se registra por WhatsApp y empieza a acumular puntos automaticamente. Sin apps, sin tarjetas que se pierden. Cuando alcanza el premio, recibe un mensaje por WhatsApp. Simple, efectivo, automatico."},
            {"icon": "chart", "h2_main": "Conoce a tus clientes:", "h2_gradient": "datos que valen oro", "text": "Cuantos clientes habituales tienes? Cuantos vinieron este mes vs el anterior? Cual es tu ticket promedio? Sin un CRM, estas adivinando. Con el, tienes datos reales para tomar decisiones."}
        ],
        "results": [("+30%", "Clientes recurrentes"), ("98%", "Apertura mensajes"), ("€0", "Coste por fidelizacion"), ("24/7", "Programa activo"), ("5sem", "Implementacion"), ("+15%", "Ticket promedio")],
        "faqs": [
            ("Como funciona el programa de puntos?", "El cliente escanea un QR en tu barra. Se registra por WhatsApp (una sola vez). Cada visita acumula puntos automaticamente. Cuando alcanza el premio, recibe un mensaje. Sin apps, sin tarjetas."),
            ("Cuanto cuesta?", "Desde €297/mes con setup de €997. Todo incluido."),
            ("Funciona para bares con terraza y zona interior?", "Si. El sistema se adapta a tu operativa sin importar la distribucion."),
            ("Puedo enviar ofertas de happy hour?", "Si. Campanas programadas: happy hour, nuevos platos, eventos especiales. Segmentadas por tipo de cliente."),
            ("Necesito wifi o hardware especial?", "Solo un codigo QR impreso en tu barra/mesa. El resto funciona por WhatsApp."),
            ("Cuanto tarda la implementacion?", "5 semanas. Nosotros hacemos todo.")
        ],
        "cta_h2_main": "Deja de depender de que el cliente",
        "cta_h2_gradient": "pase por tu puerta",
        "cta_text": "Habla con nosotros. Te mostramos como convertir clientes casuales en habituales. Sin compromiso."
    },
    {
        "slug": "crm-retail",
        "title": "CRM WhatsApp para Tiendas y Retail",
        "meta_title": "CRM para Tiendas y Retail | WhatsApp y IA | ZENIA",
        "meta_desc": "CRM con WhatsApp e IA para tiendas y retail. Fideliza clientes, automatiza comunicaciones y aumenta ventas recurrentes. Desde €297/mes.",
        "badge": "Retail",
        "h1_main": "CRM para Tiendas y Retail.",
        "h1_gradient": "Ventas recurrentes. Clientes conectados.",
        "lead": "Tus clientes preguntan stock por WhatsApp y nadie responde a tiempo. Tu agente de IA contesta al instante con disponibilidad, precios y alternativas.",
        "pain_title": "tiendas y retail",
        "pains_without": ["Clientes preguntan si tienes un producto y nadie contesta", "No sabes que compro cada cliente ni cuando volvera", "Promociones masivas que no segmentan", "Stock bajo sin que nadie avise al cliente interesado", "Competencia online que te come cuota"],
        "pains_with": ["Respuesta instantanea a consultas de stock por WhatsApp", "Historial de compras por cliente: que compra, cada cuanto, ticket medio", "Campanas segmentadas: nuevas colecciones, rebajas VIP, cumpleanos", "Alerta automatica cuando un producto vuelve a tener stock", "Canal directo con tu cliente que Amazon no puede replicar"],
        "content_blocks": [
            {"icon": "shield", "h2_main": "Retail en", "h2_gradient": "2026: la relacion es la ventaja", "text": "Amazon no puede mandarte un WhatsApp para avisarte que llego la nueva coleccion que te gusta. Tu si. La ventaja del retail fisico y local esta en la relacion personal. Un CRM amplifica esa relacion a escala."},
            {"icon": "clock", "h2_main": "Comunicacion directa:", "h2_gradient": "WhatsApp como canal de ventas", "text": "Tu cliente favorito no abre emails. Pero si abre WhatsApp. Tasa de apertura del 98%. Envia nuevas llegadas, ofertas exclusivas, avisos de stock limitado. Directo al bolsillo de tu cliente."},
            {"icon": "chart", "h2_main": "Fidelizacion inteligente:", "h2_gradient": "el cliente que vuelve vale mas", "text": "Un cliente que compra 4 veces al ano vale 10 veces mas que uno que compra una vez. El CRM identifica a tus mejores clientes y los cuida automaticamente: descuentos VIP, acceso anticipado, eventos exclusivos."}
        ],
        "results": [("+25%", "Ventas recurrentes"), ("98%", "Apertura WhatsApp"), ("+40%", "Retencion clientes"), ("24/7", "Atencion automatica"), ("5sem", "Implementacion"), ("+30%", "Recompra clientes")],
        "faqs": [
            ("Se integra con mi TPV?", "Trabajamos para integrar con los principales sistemas de punto de venta. La sincronizacion permite vincular compras con perfiles de cliente."),
            ("Puedo avisar cuando un producto vuelve a tener stock?", "Si. Cuando un cliente pregunta por un producto agotado, el sistema lo registra y le avisa automaticamente cuando vuelve a estar disponible."),
            ("Funciona para tiendas online y fisicas?", "Si. Unificamos el canal online y offline en un solo CRM. El cliente tiene un unico perfil con su historial completo."),
            ("Cuanto cuesta?", "Desde €297/mes con setup de €997. Implementacion en 5 semanas."),
            ("Puedo gestionar varias tiendas?", "Si. Dashboard centralizado con datos por tienda. Cada tienda tiene sus propias campanas pero los clientes son compartidos."),
            ("Necesito conocimientos tecnicos?", "No. Nosotros hacemos todo.")
        ],
        "cta_h2_main": "Deja de competir solo por precio.",
        "cta_h2_gradient": "Compite por relacion.",
        "cta_text": "Habla con nosotros. Te mostramos como fidelizar clientes y aumentar ventas recurrentes. Sin compromiso."
    },
    {
        "slug": "crm-wellness",
        "title": "CRM para Centros de Wellness y Spa",
        "meta_title": "CRM para Centros de Wellness y Spa | Citas con IA | ZENIA",
        "meta_desc": "CRM con IA para centros de wellness, spas y masajes. Automatiza citas, reduce cancelaciones y fideliza clientes. Desde €297/mes.",
        "badge": "Wellness",
        "h1_main": "CRM para Wellness y Spa.",
        "h1_gradient": "Agenda optimizada. Clientes que repiten.",
        "lead": "Tus clientes cancelan citas sin avisar y pierdes el 20% de tu facturacion. El agente de IA reduce cancelaciones con recordatorios inteligentes.",
        "pain_title": "centros de wellness",
        "pains_without": ["Cancelaciones de ultimo momento que dejan huecos vacios", "Terapeutas con tiempo muerto por mala gestion de agenda", "Clientes que vienen una vez y no vuelven a reservar", "Paquetes y bonos que no se renuevan", "No sabes que tratamientos prefiere cada cliente"],
        "pains_with": ["Recordatorios automaticos que reducen cancelaciones un 55%", "Agenda optimizada sin huecos muertos", "Seguimiento post-tratamiento por WhatsApp", "Renovacion automatica de bonos y paquetes", "Perfil de cliente con historial de tratamientos y preferencias"],
        "content_blocks": [
            {"icon": "shield", "h2_main": "Wellness y spa en", "h2_gradient": "2026", "text": "El sector wellness crece un 10% anual en España. Pero la competencia tambien. Los centros que fidelizan con tecnologia retienen el 40% mas de clientes que los que gestionan todo a mano."},
            {"icon": "clock", "h2_main": "Gestion de citas:", "h2_gradient": "cero huecos vacios", "text": "El agente gestiona citas por WhatsApp, confirma 48h y 2h antes, y si alguien cancela, ofrece el hueco a clientes en lista de espera automaticamente."},
            {"icon": "chart", "h2_main": "Experiencia del cliente:", "h2_gradient": "de la cita a la fidelizacion", "text": "Despues del tratamiento, el sistema envia un mensaje de bienestar, recomienda el siguiente tratamiento segun su historial y ofrece paquetes personalizados. La experiencia premium no termina cuando el cliente se va."}
        ],
        "results": [("-55%", "Cancelaciones"), ("+40%", "Retencion"), ("98%", "Apertura mensajes"), ("24/7", "Gestion citas"), ("5sem", "Implementacion"), ("+20%", "Ticket promedio")],
        "faqs": [
            ("Puedo gestionar diferentes terapeutas y tratamientos?", "Si. Cada terapeuta tiene su agenda. Cada tratamiento su duracion. El agente agenda sin solapamientos."),
            ("Funciona con bonos y paquetes?", "Si. El sistema gestiona bonos de sesiones, paquetes y renovaciones automaticas."),
            ("Cuanto cuesta?", "Desde €297/mes con setup de €997."),
            ("Cuanto tarda la implementacion?", "5 semanas. Nosotros hacemos todo."),
            ("Se integra con mi software actual?", "Trabajamos para integrar con los principales softwares de gestion de spas y centros wellness."),
            ("Puedo enviar promociones por temporada?", "Si. Campanas segmentadas por tipo de tratamiento, frecuencia de visita y temporada.")
        ],
        "cta_h2_main": "Deja de perder ingresos por",
        "cta_h2_gradient": "citas canceladas",
        "cta_text": "Habla con nosotros. Te mostramos como optimizar tu agenda y fidelizar clientes. Sin compromiso."
    },
    {
        "slug": "crm-academias",
        "title": "CRM para Academias y Centros de Formacion",
        "meta_title": "CRM para Academias | Matriculas y Seguimiento con IA | ZENIA",
        "meta_desc": "CRM con IA para academias y centros de formacion. Automatiza matriculas, seguimiento de alumnos y comunicacion por WhatsApp. Desde €297/mes.",
        "badge": "Educacion",
        "h1_main": "CRM para Academias.",
        "h1_gradient": "Mas matriculas. Alumnos comprometidos.",
        "lead": "Pierdes matriculas porque tardas 48 horas en responder consultas. Tu agente de IA responde al instante con cursos, horarios y precios.",
        "pain_title": "academias",
        "pains_without": ["Consultas de potenciales alumnos sin responder en 48h", "Alumnos que abandonan sin que nadie les haga seguimiento", "Matriculas manuales con formularios en papel", "No sabes que cursos interesan a cada alumno", "Comunicacion masiva sin segmentar"],
        "pains_with": ["Respuesta instantanea con catalogo de cursos y precios", "Alerta cuando un alumno falta 2 clases consecutivas", "Proceso de matricula digital por WhatsApp", "Recomendaciones de cursos basadas en historial", "Comunicacion segmentada por curso, nivel y horario"],
        "content_blocks": [
            {"icon": "shield", "h2_main": "Academias en", "h2_gradient": "2026", "text": "El mercado de formacion es hipercompetitivo. Cada consulta que no respondes en menos de 1 hora es una matricula que se va a otra academia. Un agente de IA responde al instante con informacion completa y agenda una visita o clase de prueba."},
            {"icon": "clock", "h2_main": "Captacion de alumnos:", "h2_gradient": "responde antes que nadie", "text": "El agente responde consultas por WhatsApp con informacion de cursos, horarios, precios y disponibilidad. Agenda clases de prueba automaticamente. Tasa de conversion de consulta a matricula: +35%."},
            {"icon": "chart", "h2_main": "Retencion de alumnos:", "h2_gradient": "que no abandonen", "text": "El sistema detecta patrones de abandono (faltas consecutivas, bajo engagement) y activa mensajes de seguimiento antes de que el alumno cancele."}
        ],
        "results": [("+35%", "Conversion consulta-matricula"), ("-30%", "Abandonos"), ("1min", "Respuesta a consultas"), ("24/7", "Atencion automatica"), ("5sem", "Implementacion"), ("+15%", "Renovacion matriculas")],
        "faqs": [
            ("Funciona para diferentes tipos de formacion?", "Si. Idiomas, musica, artes marciales, informatica, oposiciones. Configuramos el sistema segun tu modelo."),
            ("Puedo gestionar multiples horarios y grupos?", "Si. El agente gestiona disponibilidad por curso, horario y nivel."),
            ("Cuanto cuesta?", "Desde €297/mes con setup de €997."),
            ("Cuanto tarda la implementacion?", "5 semanas."),
            ("Puedo enviar comunicaciones a padres?", "Si. El sistema gestiona contactos de alumnos y tutores por separado."),
            ("Se integra con plataformas de e-learning?", "Trabajamos para integrar con las principales plataformas de formacion online.")
        ],
        "cta_h2_main": "Deja de perder matriculas por",
        "cta_h2_gradient": "tardar en responder",
        "cta_text": "Habla con nosotros. Te mostramos como captar mas alumnos y retener los que tienes. Sin compromiso."
    },
    {
        "slug": "crm-consultorias",
        "title": "CRM WhatsApp para Consultoras",
        "meta_title": "CRM para Consultoras | Seguimiento de Proyectos con IA | ZENIA",
        "meta_desc": "CRM con IA para consultoras y asesoras. Automatiza seguimiento de clientes, propuestas y facturacion por WhatsApp. Desde €297/mes.",
        "badge": "Consultorias",
        "h1_main": "CRM para Consultoras.",
        "h1_gradient": "Clientes gestionados. Proyectos controlados.",
        "lead": "Tu equipo pierde 3 horas diarias en emails de seguimiento que podrian automatizarse. El agente de IA lo hace por ti.",
        "pain_title": "consultoras",
        "pains_without": ["Seguimiento de propuestas manual y desordenado", "Clientes que no responden y se enfrian", "No sabes en que fase esta cada proyecto", "Facturacion manual con errores", "Informacion dispersa entre email, WhatsApp y Excel"],
        "pains_with": ["Pipeline visual de propuestas y proyectos", "Follow-up automatico a propuestas sin respuesta", "Dashboard de estado de cada proyecto en tiempo real", "Recordatorios de facturacion y cobro automaticos", "Todo centralizado en un solo sistema"],
        "content_blocks": [
            {"icon": "shield", "h2_main": "Consultoras en", "h2_gradient": "2026", "text": "Una consultora tipica maneja entre 10 y 30 proyectos activos simultaneamente. Sin un CRM, la informacion se dispersa entre emails, WhatsApp, carpetas compartidas y la memoria de cada consultor. El resultado: seguimientos que se olvidan, propuestas que se enfrian y facturas que se atrasan."},
            {"icon": "clock", "h2_main": "Pipeline de ventas:", "h2_gradient": "de la propuesta al cierre", "text": "Cada oportunidad se visualiza en un pipeline: contacto inicial, propuesta enviada, negociacion, cierre. El agente hace follow-up automatico si una propuesta lleva 5 dias sin respuesta. Tasa de cierre mejora un 25%."},
            {"icon": "chart", "h2_main": "Gestion de clientes:", "h2_gradient": "todo en un solo lugar", "text": "Cada cliente tiene un perfil con historial completo: proyectos realizados, propuestas pendientes, facturacion, comunicaciones. Tu equipo sabe exactamente donde esta cada cuenta sin preguntar."}
        ],
        "results": [("+25%", "Tasa de cierre"), ("-3h", "Tiempo en follow-ups"), ("100%", "Visibilidad pipeline"), ("24/7", "Seguimiento automatico"), ("5sem", "Implementacion"), ("+30%", "Clientes recurrentes")],
        "faqs": [
            ("Se integra con mi herramienta de gestion de proyectos?", "Trabajamos para integrar con Asana, Monday, Notion y las principales herramientas de PM."),
            ("Puedo gestionar multiples consultores?", "Si. Cada consultor tiene su cartera de clientes y proyectos. Los reportes se consolidan para direccion."),
            ("Cuanto cuesta?", "Desde €297/mes con setup de €997."),
            ("Cuanto tarda la implementacion?", "5 semanas."),
            ("Puedo automatizar propuestas?", "El sistema genera borradores de propuestas basados en templates y datos del cliente."),
            ("Funciona para consultoras de diferentes sectores?", "Si. IT, estrategia, RRHH, legal, financiero. Configuramos segun tu modelo.")
        ],
        "cta_h2_main": "Deja de perder propuestas por",
        "cta_h2_gradient": "falta de seguimiento",
        "cta_text": "Habla con nosotros. Te mostramos como cerrar mas proyectos y gestionar mejor tus clientes. Sin compromiso."
    },
    {
        "slug": "crm-medicos",
        "title": "CRM WhatsApp para Consultas Medicas",
        "meta_title": "CRM para Medicos | Citas y Pacientes con IA | ZENIA",
        "meta_desc": "CRM con IA para consultas medicas. Automatiza citas, recordatorios y seguimiento de pacientes por WhatsApp. Desde €297/mes.",
        "badge": "Salud",
        "h1_main": "CRM para Consultas Medicas.",
        "h1_gradient": "Pacientes atendidos. Agenda optimizada.",
        "lead": "Tus pacientes llaman 5 veces para confirmar una cita que podria ser automatica. Libera a tu recepcion con un agente de IA.",
        "pain_title": "consultas medicas",
        "pains_without": ["Telefono que no para de sonar en recepcion", "No-shows que te cuestan horas de consulta vacia", "Pacientes que no vuelven a revisiones periodicas", "Historiales de comunicacion dispersos", "Recepcionista saturada haciendo trabajo repetitivo"],
        "pains_with": ["El 80% de llamadas resueltas por el agente IA", "No-shows reducidos un 50% con recordatorios WhatsApp", "Seguimiento automatico de revisiones periodicas", "Historial de comunicaciones centralizado", "Recepcion enfocada en atencion presencial"],
        "content_blocks": [
            {"icon": "shield", "h2_main": "Consultas medicas en", "h2_gradient": "2026", "text": "El paciente moderno prefiere WhatsApp al telefono. Quiere confirmar su cita con un mensaje, no esperando 5 minutos en linea. Las consultas que se adaptan retienen mas pacientes y optimizan mejor su agenda."},
            {"icon": "clock", "h2_main": "Gestion de citas:", "h2_gradient": "automatizada por WhatsApp", "text": "El paciente escribe por WhatsApp. El agente verifica disponibilidad, ofrece horarios, confirma la cita y envia recordatorios automaticos. Si el paciente cancela, el hueco se ofrece a otros pacientes en lista de espera."},
            {"icon": "chart", "h2_main": "Seguimiento de pacientes:", "h2_gradient": "atencion continua", "text": "Recordatorios de revisiones periodicas, seguimiento post-consulta, avisos de resultados disponibles. Todo automatico, todo por WhatsApp, todo cumpliendo RGPD."}
        ],
        "results": [("-50%", "No-shows"), ("80%", "Consultas automatizadas"), ("+30%", "Retencion pacientes"), ("24/7", "Gestion citas"), ("5sem", "Implementacion"), ("+25%", "Satisfaccion pacientes")],
        "faqs": [
            ("Es seguro para datos de pacientes?", "Si. Cumplimos RGPD y mejores practicas de proteccion de datos sanitarios."),
            ("Se integra con mi software de gestion clinica?", "Trabajamos para integrar con los principales softwares del sector."),
            ("Cuanto cuesta?", "Desde €297/mes con setup de €997."),
            ("Cuanto tarda?", "5 semanas."),
            ("Los pacientes saben que es una IA?", "Si, transparencia total. Cuando necesitan hablar con una persona, la transferencia es inmediata."),
            ("Puedo gestionar varios doctores?", "Si. Cada doctor tiene su agenda. El agente gestiona todas.")
        ],
        "cta_h2_main": "Deja de saturar tu recepcion con llamadas que",
        "cta_h2_gradient": "una IA puede resolver",
        "cta_text": "Habla con nosotros. Te mostramos como optimizar tu consulta. Sin compromiso."
    },
    {
        "slug": "crm-abogados",
        "title": "CRM WhatsApp para Despachos de Abogados",
        "meta_title": "CRM para Abogados | Leads y Seguimiento con IA | ZENIA",
        "meta_desc": "CRM con IA para despachos de abogados. Cualifica leads, automatiza seguimiento de casos y comunicacion por WhatsApp. Desde €297/mes.",
        "badge": "Legal",
        "h1_main": "CRM para Abogados.",
        "h1_gradient": "Casos organizados. Clientes informados.",
        "lead": "Pierdes clientes porque no respondes consultas iniciales en menos de 2 horas. Tu agente de IA responde al instante y cualifica el caso.",
        "pain_title": "despachos de abogados",
        "pains_without": ["Consultas de potenciales clientes que se enfrian", "Seguimiento de casos manual y desordenado", "Clientes que llaman preguntando estado del caso", "Informacion dispersa entre email y carpetas", "Facturacion por horas que no se registra bien"],
        "pains_with": ["Respuesta instantanea a consultas con cualificacion del caso", "Pipeline visual por estado del caso", "Updates automaticos al cliente sobre su expediente", "Todo centralizado: comunicaciones, documentos, plazos", "Registro automatico de horas y facturacion"],
        "content_blocks": [
            {"icon": "shield", "h2_main": "Despachos de abogados en", "h2_gradient": "2026", "text": "El 70% de los potenciales clientes contactan a 2-3 despachos antes de decidir. El que responde primero con informacion clara tiene el 60% de probabilidad de quedarse con el caso. Un agente de IA responde al instante, 24/7."},
            {"icon": "clock", "h2_main": "Captacion de clientes:", "h2_gradient": "responde antes que nadie", "text": "El agente cualifica la consulta: tipo de caso, urgencia, presupuesto estimado. Filtra consultas serias de curiosos. Tu solo recibes leads cualificados listos para una primera reunion."},
            {"icon": "chart", "h2_main": "Gestion de casos:", "h2_gradient": "todo bajo control", "text": "Cada caso tiene un expediente digital con plazos, documentos, comunicaciones y facturacion. El cliente recibe updates automaticos sobre el estado de su caso sin que tengas que llamarle."}
        ],
        "results": [("2min", "Respuesta a consultas"), ("+40%", "Conversion de leads"), ("100%", "Visibilidad de casos"), ("24/7", "Atencion automatica"), ("5sem", "Implementacion"), ("+30%", "Clientes referidos")],
        "faqs": [
            ("Es seguro para informacion legal confidencial?", "Si. Cumplimos RGPD y protocolos de confidencialidad legal. Encriptacion en transito y en reposo."),
            ("Se integra con software juridico?", "Trabajamos para integrar con los principales softwares de gestion de despachos."),
            ("Cuanto cuesta?", "Desde €297/mes con setup de €997."),
            ("Cuanto tarda?", "5 semanas."),
            ("Puedo gestionar varios abogados?", "Si. Cada abogado tiene su cartera de casos con reportes consolidados."),
            ("El agente da asesoramiento legal?", "No. Solo cualifica consultas, agenda reuniones y gestiona comunicaciones. El asesoramiento lo da siempre el abogado.")
        ],
        "cta_h2_main": "Deja de perder clientes por",
        "cta_h2_gradient": "tardar en responder",
        "cta_text": "Habla con nosotros. Te mostramos como captar mas clientes y gestionar casos mejor. Sin compromiso."
    },
    {
        "slug": "crm-fotografos",
        "title": "CRM para Fotografos y Estudios",
        "meta_title": "CRM para Fotografos | Presupuestos y Citas con IA | ZENIA",
        "meta_desc": "CRM con IA para fotografos y estudios de fotografia. Automatiza presupuestos, citas y seguimiento por WhatsApp. Desde €297/mes.",
        "badge": "Fotografia",
        "h1_main": "CRM para Fotografos.",
        "h1_gradient": "Agenda llena. Presupuestos automaticos.",
        "lead": "Tus clientes piden presupuesto por Instagram y se olvidan porque tardas en responder. El agente de IA envia tarifas al instante.",
        "pain_title": "fotografos",
        "pains_without": ["Presupuestos que tardas horas en preparar", "Clientes de Instagram que preguntan precio y desaparecen", "Agenda desorganizada entre bodas, comuniones y sesiones", "Seguimiento manual de entregas de fotos", "No sabes que tipo de sesion genera mas ingresos"],
        "pains_with": ["Presupuestos automaticos segun tipo de sesion", "Respuesta instantanea a consultas de Instagram y WhatsApp", "Agenda integrada con confirmaciones automaticas", "Recordatorios de entregas y revisiones", "Dashboard con ingresos por tipo de sesion"],
        "content_blocks": [
            {"icon": "shield", "h2_main": "Fotografos en", "h2_gradient": "2026", "text": "El 80% de tus potenciales clientes te descubren por Instagram. Te mandan un DM preguntando precio. Si no respondes en 1 hora, ya contactaron a otro fotografo. Un agente de IA responde al instante con tus tarifas y disponibilidad."},
            {"icon": "clock", "h2_main": "Presupuestos automaticos:", "h2_gradient": "cierra mas sesiones", "text": "El agente pregunta tipo de sesion (boda, comunion, retrato, producto), fecha y ubicacion. Envia un presupuesto personalizado al instante con tus tarifas. Si el cliente acepta, agenda automaticamente."},
            {"icon": "chart", "h2_main": "Gestion de sesiones:", "h2_gradient": "de la reserva a la entrega", "text": "Cada sesion tiene un timeline: reserva, confirmacion, sesion, edicion, entrega. El cliente recibe updates automaticos en cada fase. Nunca mas te preguntan 'cuando estaran mis fotos?'."}
        ],
        "results": [("+50%", "Respuesta a consultas"), ("+30%", "Sesiones cerradas"), ("1min", "Tiempo de presupuesto"), ("24/7", "Atencion Instagram/WA"), ("5sem", "Implementacion"), ("+40%", "Sesiones agendadas")],
        "faqs": [
            ("Puedo personalizar presupuestos por tipo de sesion?", "Si. Configuras tus tarifas base por tipo y el agente genera presupuestos automaticos personalizados."),
            ("Funciona con Instagram DMs?", "Si. El agente gestiona consultas de WhatsApp e Instagram desde un solo panel."),
            ("Cuanto cuesta?", "Desde €297/mes con setup de €997."),
            ("Cuanto tarda?", "5 semanas."),
            ("Puedo gestionar entregas de fotos?", "Si. El sistema programa recordatorios de edicion y avisa al cliente cuando sus fotos estan listas."),
            ("Se adapta a mi estilo de trabajo?", "Si. Configuramos todo segun tu flujo: tipos de sesion, tiempos de entrega, tarifas, zonas de cobertura.")
        ],
        "cta_h2_main": "Deja de perder sesiones por",
        "cta_h2_gradient": "tardar en presupuestar",
        "cta_text": "Habla con nosotros. Te mostramos como cerrar mas sesiones y gestionar tu agenda. Sin compromiso."
    },
    # Tier 3 — Functional keywords
    {
        "slug": "crm-whatsapp",
        "title": "CRM para WhatsApp en España",
        "meta_title": "CRM para WhatsApp en España | Agente IA para Negocios | ZENIA",
        "meta_desc": "CRM con agente de IA para WhatsApp Business. Automatiza atencion al cliente, ventas y seguimiento. Para PYMEs en España. Desde €297/mes.",
        "badge": "WhatsApp",
        "h1_main": "CRM para WhatsApp.",
        "h1_gradient": "Tu negocio en piloto automatico.",
        "lead": "El 98% de tus clientes abren WhatsApp. Solo el 20% abren email. Tu canal de ventas mas potente merece un CRM que lo aproveche.",
        "pain_title": "negocios que usan WhatsApp",
        "pains_without": ["Mensajes acumulados sin responder", "Un solo telefono para todo el equipo", "No sabes que cliente esta en que fase de compra", "Conversaciones importantes perdidas en el historial", "Cero metricas de cuantas ventas genera WhatsApp"],
        "pains_with": ["Respuestas automaticas 24/7 con agente IA", "Multiple agentes en un solo numero de WhatsApp", "Pipeline de ventas integrado con cada conversacion", "Historial completo de cada cliente", "Dashboard con metricas de conversion y respuesta"],
        "content_blocks": [
            {"icon": "shield", "h2_main": "WhatsApp Business en", "h2_gradient": "2026: mas que un chat", "text": "WhatsApp ya no es solo un canal de comunicacion. Es tu canal de ventas mas potente. Pero sin un CRM detras, es un caos: mensajes sin responder, clientes que se pierden, y cero visibilidad de cuanto negocio genera. Un CRM para WhatsApp transforma el caos en sistema."},
            {"icon": "clock", "h2_main": "Agente de IA:", "h2_gradient": "tu mejor vendedor 24/7", "text": "El agente de IA contesta consultas, envia catalogos, toma pedidos, agenda citas y hace seguimiento. Todo por WhatsApp. Todo automatico. Y cuando la conversacion necesita un humano, transfiere al instante."},
            {"icon": "chart", "h2_main": "Para todo tipo de negocio:", "h2_gradient": "restaurantes, tiendas, clinicas y mas", "text": "Sea cual sea tu negocio, si tus clientes te escriben por WhatsApp, necesitas un CRM que gestione esas conversaciones. Restaurantes, gimnasios, clinicas, inmobiliarias, tiendas, consultoras. El sistema se adapta a tu vertical."}
        ],
        "results": [("98%", "Apertura mensajes"), ("+45%", "Conversion ventas"), ("24/7", "Atencion automatica"), ("5sem", "Implementacion"), ("+60%", "Eficiencia equipo")],
        "faqs": [
            ("Que diferencia hay entre WhatsApp Business y un CRM WhatsApp?", "WhatsApp Business es la app. Un CRM WhatsApp es un sistema detras de la app que gestiona contactos, automatiza respuestas, hace seguimiento y te da metricas. Es la diferencia entre tener un telefono y tener un equipo de ventas."),
            ("Necesito la API de WhatsApp?", "Nosotros gestionamos todo. No necesitas conocimientos tecnicos ni tratar con Meta directamente."),
            ("Puede responder en varios idiomas?", "Si. El agente de IA puede atender en español, ingles y otros idiomas segun tus necesidades."),
            ("Cuanto cuesta?", "Desde €297/mes con setup de €997."),
            ("Cuantos agentes pueden usar el mismo numero?", "Dependiendo del plan, desde 1 hasta ilimitados."),
            ("Se integra con mi CRM actual?", "Trabajamos para integrar con los principales CRMs del mercado."),
            ("Puedo enviar mensajes masivos?", "Si, siguiendo las politicas de WhatsApp Business. Campanas segmentadas con tasas de apertura del 98%."),
            ("Cuanto tarda la implementacion?", "5 semanas. Nosotros hacemos todo.")
        ],
        "cta_h2_main": "Deja de perder ventas en el canal que tus clientes",
        "cta_h2_gradient": "mas usan",
        "cta_text": "Habla con nosotros. Te mostramos como convertir WhatsApp en tu maquina de ventas. Sin compromiso."
    },
    {
        "slug": "crm-pymes",
        "title": "CRM con IA para PYMEs en España",
        "meta_title": "CRM para PYMEs en España | IA y WhatsApp | ZENIA",
        "meta_desc": "CRM con agente de IA para PYMEs españolas. Automatiza ventas, atencion al cliente y operaciones. Sin conocimientos tecnicos. Desde €297/mes.",
        "badge": "PYMEs",
        "h1_main": "CRM para PYMEs.",
        "h1_gradient": "Simple. Potente. Automatico.",
        "lead": "El 64% de las PYMEs españolas ya usan IA. Las que no, estan perdiendo clientes frente a las que si. No necesitas ser tecnico. Nosotros hacemos todo.",
        "pain_title": "PYMEs",
        "pains_without": ["Gestion de clientes en Excel o en la cabeza", "Oportunidades que se pierden por falta de seguimiento", "Equipo pequeño haciendo tareas repetitivas", "Sin datos para tomar decisiones de negocio", "Competidores mas grandes con mas recursos tecnologicos"],
        "pains_with": ["CRM con toda la informacion de tus clientes", "Seguimiento automatico de cada oportunidad", "Agente IA que libera a tu equipo de tareas repetitivas", "Dashboard con metricas reales de tu negocio", "Tecnologia de multinacional a precio de PYME"],
        "content_blocks": [
            {"icon": "shield", "h2_main": "PYMEs españolas en", "h2_gradient": "2026", "text": "Las PYMEs representan el 99.8% del tejido empresarial español. Pero solo el 36% tiene un CRM. Las que lo tienen retienen un 27% mas de clientes y cierran un 30% mas de ventas. La diferencia no es el tamaño. Es el sistema."},
            {"icon": "clock", "h2_main": "IA para PYMEs:", "h2_gradient": "no es solo para grandes", "text": "Hace 2 años, un agente de IA costaba €50,000 de desarrollo. Hoy, con Zenia, tienes uno funcionando en 5 semanas por €297/mes. La tecnologia se ha democratizado. La pregunta ya no es si puedes permitirtelo, sino si puedes permitirte no tenerlo."},
            {"icon": "chart", "h2_main": "Done-for-you:", "h2_gradient": "nosotros hacemos todo", "text": "No te vendemos software para que lo configures tu. Nosotros analizamos tu negocio, configuramos el CRM, entrenamos el agente IA con tu catalogo y lo dejamos funcionando. Tu solo sigues atendiendo a tus clientes. En 5 semanas, tu negocio opera en piloto automatico."}
        ],
        "results": [("+30%", "Ventas"), ("+27%", "Retencion"), ("5sem", "Implementacion"), ("€297", "Desde/mes"), ("0", "Conocimientos tecnicos"), ("+60%", "Eficiencia operativa")],
        "faqs": [
            ("Que es un CRM?", "Un sistema que centraliza toda la informacion de tus clientes: contactos, conversaciones, compras, preferencias. Te permite hacer seguimiento automatico y no perder ninguna oportunidad."),
            ("Necesito conocimientos tecnicos?", "No. Nosotros hacemos todo. Tu equipo solo necesita saber usar WhatsApp."),
            ("Cuanto cuesta?", "Desde €297/mes con setup de €997."),
            ("Para que tipo de negocio funciona?", "Restaurantes, gimnasios, clinicas, tiendas, inmobiliarias, consultoras, academias y mas. Configuramos segun tu vertical."),
            ("Cuanto tarda?", "5 semanas desde la firma."),
            ("Puedo cancelar cuando quiera?", "Si. Sin permanencia."),
            ("Que incluye el setup?", "Analisis de tu negocio, configuracion del CRM, entrenamiento del agente IA con tu catalogo/servicios, integracion con WhatsApp y pruebas."),
            ("Es mejor que Hubspot o Salesforce?", "No somos un software generico. Somos un servicio de implementacion completa con agente IA personalizado. Tu no configuras nada. Nosotros hacemos todo.")
        ],
        "cta_h2_main": "Deja de gestionar tu negocio con",
        "cta_h2_gradient": "Excel y memoria",
        "cta_text": "Habla con nosotros. Te mostramos como automatizar tu PYME con IA. Sin compromiso. Sin conocimientos tecnicos."
    },
    {
        "slug": "crm-negocios-pequenos",
        "title": "CRM WhatsApp para Negocios Pequeños",
        "meta_title": "CRM para Negocios Pequeños | WhatsApp con IA | ZENIA",
        "meta_desc": "CRM con WhatsApp e IA para negocios pequeños. Automatiza atencion, ventas y fidelizacion sin conocimientos tecnicos. Desde €297/mes.",
        "badge": "Negocios",
        "h1_main": "CRM para Negocios Pequeños.",
        "h1_gradient": "Grande en resultados. Simple de usar.",
        "lead": "No necesitas un equipo de IT. No necesitas saber de tecnologia. Solo necesitas WhatsApp y 5 semanas. Nosotros hacemos el resto.",
        "pain_title": "negocios pequeños",
        "pains_without": ["Haces todo tu: vendes, atiendes, facturas, cobras", "Pierdes clientes porque no puedes estar en todo", "Tu competencia responde mas rapido", "No tienes tiempo para marketing ni seguimiento", "Trabajas 12 horas y sientes que no avanzas"],
        "pains_with": ["Un agente IA que atiende mientras tu trabajas", "Respuesta instantanea a clientes 24/7", "Seguimiento automatico que no olvida a nadie", "Campanas de fidelizacion que se envian solas", "Mas tiempo para lo que importa: tu negocio"],
        "content_blocks": [
            {"icon": "shield", "h2_main": "Negocios pequeños en", "h2_gradient": "2026", "text": "Si tienes un negocio pequeño, probablemente haces de todo: vendes, atiendes, compras, facturas, limpias. No tienes tiempo para responder WhatsApps a las 11 de la noche. Pero tu cliente espera respuesta. Un agente de IA lo hace por ti mientras duermes."},
            {"icon": "clock", "h2_main": "Tu primer empleado digital:", "h2_gradient": "sin nomina", "text": "Un agente de IA cuesta menos que un empleado a media jornada. Pero trabaja 24/7, no pide vacaciones y no comete errores de seguimiento. Es tu primer empleado digital. Y el mas rentable."},
            {"icon": "chart", "h2_main": "Sin complicaciones:", "h2_gradient": "nosotros hacemos todo", "text": "No necesitas instalar nada. No necesitas saber de CRM ni de IA. Nos cuentas tu negocio, nosotros configuramos todo, y en 5 semanas tienes un sistema que trabaja por ti."}
        ],
        "results": [("24/7", "Atencion automatica"), ("€297", "Desde/mes"), ("5sem", "Listo para usar"), ("0", "Conocimientos tecnicos"), ("+50%", "Tiempo libre"), ("+30%", "Ventas recurrentes")],
        "faqs": [
            ("Que tipo de negocio puede usarlo?", "Cualquiera que reciba consultas o pedidos por WhatsApp: peluquerias, tiendas, restaurantes, talleres, clinicas, estudios, consultoras."),
            ("De verdad no necesito saber nada de tecnologia?", "De verdad. Nosotros hacemos todo. Tu solo nos cuentas como funciona tu negocio y nosotros lo automatizamos."),
            ("Cuanto cuesta?", "Desde €297/mes con setup de €997."),
            ("Es caro para un negocio pequeño?", "Es menos que un empleado a media jornada. Y trabaja 24/7. La pregunta es: cuanto te cuesta NO tenerlo?"),
            ("Cuanto tarda?", "5 semanas."),
            ("Puedo cancelar?", "Si. Sin permanencia."),
            ("Que pasa si no funciona para mi negocio?", "Antes de empezar, analizamos tu negocio para confirmar que el sistema tiene sentido. Si no es para ti, te lo decimos. No vendemos humo."),
            ("Como empiezo?", "Escribenos por WhatsApp. En 30 minutos te explicamos todo y evaluamos si encaja con tu negocio.")
        ],
        "cta_h2_main": "Deja de hacer todo tu solo.",
        "cta_h2_gradient": "Automatiza lo repetitivo.",
        "cta_text": "Habla con nosotros. 30 minutos para evaluar si el sistema funciona para tu negocio. Sin compromiso."
    },
]

# City pages (Tier 4)
CITIES = [
    {"slug": "crm-madrid", "city": "Madrid", "desc": "Madrid es el centro de negocios de España con mas de 500,000 PYMEs. La competencia es feroz y la atencion al cliente marca la diferencia. Un CRM con IA te da la ventaja de responder primero, fidelizar mejor y vender mas."},
    {"slug": "crm-barcelona", "city": "Barcelona", "desc": "Barcelona combina turismo, gastronomia, retail y tech en una ciudad hipercompetitiva. Las PYMEs catalanas que automatizan su atencion al cliente con IA captan mas clientes y retienen mejor a los existentes."},
    {"slug": "crm-valencia", "city": "Valencia", "desc": "Valencia es la tercera ciudad de España y su tejido de PYMEs crece cada ano. Hosteleria, comercio local y servicios profesionales son los verticales con mayor potencial de automatizacion con IA."},
    {"slug": "crm-sevilla", "city": "Sevilla", "desc": "Sevilla lidera el sur de España en emprendimiento. Restaurantes, hoteles, clinicas y comercios locales pueden multiplicar su eficiencia con un CRM que automatiza la atencion por WhatsApp."},
    {"slug": "crm-malaga", "city": "Malaga", "desc": "Malaga es el hub tecnologico del sur de España. PYMEs de hosteleria, inmobiliaria y servicios profesionales encuentran en la automatizacion con IA su mejor aliada para competir con cadenas mas grandes."},
]

# =============================================================================
# SHARED COMPONENTS
# =============================================================================

# SVG icons for tailor-point blocks
ICONS = {
    "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
    "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>',
    "chart": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>',
}

# WhatsApp SVG path (reused across components)
WA_SVG_PATH = 'M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z'

NAV_SVG_LOGO = '<svg class="zenia-mark" viewBox="0 0 140 140" fill="none"><defs><linearGradient id="zg-b" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#2563EB"/><stop offset="100%" stop-color="#3B82F6"/></linearGradient><linearGradient id="zg-v" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#6366F1"/><stop offset="100%" stop-color="#7C3AED"/></linearGradient></defs><rect width="140" height="140" rx="28" fill="#0F172A"/><path d="M 70 18 Q 18 18 18 38 L 18 57 Q 18 63 24 63 L 88 63 Z" fill="url(#zg-b)"/><path d="M 70 122 Q 122 122 122 102 L 122 83 Q 122 77 116 77 L 52 77 Z" fill="url(#zg-v)"/></svg>'

FOOTER_SVG_LOGO = '<svg class="zenia-mark zenia-mark--sm" viewBox="0 0 140 140" fill="none"><defs><linearGradient id="zg2-b" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#2563EB"/><stop offset="100%" stop-color="#3B82F6"/></linearGradient><linearGradient id="zg2-v" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#6366F1"/><stop offset="100%" stop-color="#7C3AED"/></linearGradient></defs><rect width="140" height="140" rx="28" fill="#0F172A"/><path d="M 70 18 Q 18 18 18 38 L 18 57 Q 18 63 24 63 L 88 63 Z" fill="url(#zg2-b)"/><path d="M 70 122 Q 122 122 122 102 L 122 83 Q 122 77 116 77 L 52 77 Z" fill="url(#zg2-v)"/></svg>'


def render_nav():
    return f'''<nav class="nav scrolled" id="nav">
  <div class="nav-inner">
    <a href="/es/" class="nav-logo">{NAV_SVG_LOGO}<span class="nav-logo-text">ZENIA</span></a>
    <ul class="nav-links">
      <li><a href="/es/">Inicio</a></li>
      <li><a href="#solucion">Solucion</a></li>
      <li><a href="#precios">Precios</a></li>
      <li><a href="#faq">FAQ</a></li>
      <li><a href="/blog/">Blog</a></li>
    </ul>
    <div class="nav-right">
      <div class="nav-cta"><a href="https://wa.me/34677612799" class="btn btn-primary">WhatsApp</a></div>
    </div>
    <button class="nav-mobile-toggle" id="navToggle" aria-label="Toggle menu">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
    </button>
  </div>
</nav>'''


def render_footer():
    return f'''<footer class="footer">
  <div class="container">
    <div class="footer-inner">
      <div class="footer-brand">
        <div class="footer-logo">{FOOTER_SVG_LOGO}<span>ZENIA</span></div>
        <p class="footer-tagline">Go Beyond</p>
        <p>Ayudamos a negocios a automatizar operaciones con agentes de IA y CRM inteligente. Resultados medibles en 5 semanas.</p>
      </div>
      <div class="footer-columns">
        <div class="footer-col">
          <h3 class="footer-heading">Soluciones</h3>
          <ul>
            <li><a href="/es/crm-restaurantes.html">Restaurantes</a></li>
            <li><a href="/es/crm-gimnasios.html">Gimnasios</a></li>
            <li><a href="/es/crm-salones-belleza.html">Belleza</a></li>
            <li><a href="/es/crm-whatsapp.html">WhatsApp CRM</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h3 class="footer-heading">Empresa</h3>
          <ul>
            <li><a href="/es/">Inicio</a></li>
            <li><a href="/blog/">Blog</a></li>
            <li><a href="mailto:fabrizzio.zelada@zeniapartners.com">Contacto</a></li>
            <li><a href="/">English</a></li>
          </ul>
        </div>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; 2026 ZENIA. Todos los derechos reservados.</p>
      <p class="footer-founder">Fundado por <span>Fabrizzio Zelada</span></p>
      <div class="footer-social">
        <a href="https://www.linkedin.com/company/zenia-partners/" target="_blank" rel="noopener" aria-label="LinkedIn"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg></a>
        <a href="https://www.instagram.com/zeniapartners" target="_blank" rel="noopener" aria-label="Instagram"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg></a>
      </div>
    </div>
  </div>
</footer>'''


def render_wa_float():
    return f'''<a href="https://wa.me/34677612799?text=Hola%2C%20me%20interesa%20saber%20mas%20sobre%20Zenia" class="wa-float" aria-label="WhatsApp" title="Escribenos por WhatsApp" style="position:fixed;bottom:24px;right:24px;width:56px;height:56px;background:#25D366;border-radius:50%;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 12px rgba(0,0,0,0.3);z-index:9998;transition:transform 0.2s">
  <svg viewBox="0 0 24 24" width="28" height="28"><path fill="#fff" d="{WA_SVG_PATH}"/></svg>
</a>'''


def render_mobile_nav_js():
    """Minimal JS for mobile nav toggle + FAQ accordion + smooth scroll."""
    return '''<script>
// Mobile nav toggle
var navToggle = document.getElementById('navToggle');
var navLinks = document.querySelector('.nav-links');
var navRight = document.querySelector('.nav-right');
if (navToggle) {
  navToggle.addEventListener('click', function() {
    var isOpen = navLinks.classList.toggle('nav-open');
    navRight.classList.toggle('nav-open');
    document.body.classList.toggle('nav-menu-open', isOpen);
    navToggle.setAttribute('aria-expanded', String(isOpen));
  });
  document.querySelectorAll('.nav-links a').forEach(function(a) {
    a.addEventListener('click', function() {
      navLinks.classList.remove('nav-open');
      navRight.classList.remove('nav-open');
      document.body.classList.remove('nav-menu-open');
      navToggle.setAttribute('aria-expanded', 'false');
    });
  });
}
// FAQ accordion
document.querySelectorAll('.faq-item').forEach(function(item) {
  item.querySelector('h3').style.cursor = 'pointer';
  item.querySelector('p').style.display = 'none';
  item.querySelector('h3').addEventListener('click', function() {
    var p = item.querySelector('p');
    var isOpen = p.style.display === 'block';
    // Close all
    document.querySelectorAll('.faq-item p').forEach(function(pp) { pp.style.display = 'none'; });
    document.querySelectorAll('.faq-item').forEach(function(fi) { fi.style.borderColor = ''; });
    if (!isOpen) {
      p.style.display = 'block';
      item.style.borderColor = 'var(--border-hover)';
    }
  });
});
// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(function(a) {
  a.addEventListener('click', function(e) {
    var target = document.querySelector(a.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});
</script>'''


# =============================================================================
# HTML TEMPLATE — VERTICAL PAGES
# =============================================================================

def generate_landing(v):
    """Generate a complete landing page HTML from vertical data."""

    wa_link = f"https://wa.me/34677612799?text=Hola%2C%20me%20interesa%20el%20{v['slug'].replace('-','%20')}"

    # FAQ Schema JSON-LD
    faq_schema = ',\n    '.join([
        '{{"@type":"Question","name":"{}","acceptedAnswer":{{"@type":"Answer","text":"{}"}}}}'.format(
            q.replace('"', '\\"'), a.replace('"', '\\"')
        )
        for q, a in v["faqs"]
    ])

    # FAQ HTML
    faq_html = '\n'.join([
        f'      <div class="faq-item"><h3>{q}</h3><p>{a}</p></div>'
        for q, a in v["faqs"]
    ])

    # Pain points — opp-card style (before/after grid)
    pains_without_html = '\n'.join([
        f'          <li>{p}</li>' for p in v["pains_without"]
    ])
    pains_with_html = '\n'.join([
        f'          <li>{p}</li>' for p in v["pains_with"]
    ])

    # Content blocks — tailor-point style
    content_html = '\n'.join([
        f'''      <div class="tailor-point">
        <div class="tailor-point-icon">{ICONS.get(b.get("icon", "shield"), ICONS["shield"])}</div>
        <div>
          <h3 class="h4-style">{b["h2_main"]} <span class="text-gradient">{b["h2_gradient"]}</span></h3>
          <p>{b["text"]}</p>
        </div>
      </div>''' for b in v["content_blocks"]
    ])

    # Results — impact-card style
    results_html = '\n'.join([
        f'      <div class="impact-card"><div class="impact-number text-gradient">{val}</div><h3 class="h4-style">{label}</h3></div>'
        for val, label in v["results"]
    ])

    # Footer verticals
    all_slugs = [vv["slug"] for vv in VERTICALS] + [c["slug"] for c in CITIES]
    footer_links = '\n'.join([
        f'    <a href="/es/{s}.html" style="color:var(--text-muted);font-size:13px;text-decoration:none;transition:color 0.2s">{s.replace("crm-","").replace("-"," ").title()}</a>'
        for s in all_slugs if s != v["slug"]
    ])

    return f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<!-- Google Analytics 4 -->
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('consent', 'default', {{ analytics_storage: 'denied' }});
</script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-HP0VQSEL68"></script>
<script>
  gtag('js', new Date());
  gtag('config', 'G-HP0VQSEL68', {{ send_page_view: true }});
</script>

<title>{v["meta_title"]}</title>
<meta name="description" content="{v["meta_desc"]}">
<link rel="canonical" href="https://zeniapartners.com/es/{v["slug"]}.html">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
<meta name="author" content="ZENIA">
<meta name="theme-color" content="#0A0F1C">
<link rel="icon" type="image/svg+xml" href="/assets/icons/favicon.svg">
<link rel="apple-touch-icon" href="/assets/icons/favicon.svg">

<link rel="alternate" hreflang="es" href="https://zeniapartners.com/es/{v["slug"]}.html">
<link rel="alternate" hreflang="en" href="https://zeniapartners.com/">
<link rel="alternate" hreflang="x-default" href="https://zeniapartners.com/">

<meta property="og:type" content="website">
<meta property="og:title" content="{v["meta_title"]}">
<meta property="og:description" content="{v["meta_desc"]}">
<meta property="og:url" content="https://zeniapartners.com/es/{v["slug"]}.html">
<meta property="og:site_name" content="ZENIA">
<meta property="og:image" content="https://zeniapartners.com/assets/images/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="es_ES">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{v["meta_title"]}">
<meta name="twitter:description" content="{v["meta_desc"]}">
<meta name="twitter:image" content="https://zeniapartners.com/assets/images/og-image.png">

<script type="application/ld+json">
{{
  "@context":"https://schema.org",
  "@type":"Service",
  "name":"{v["title"]}",
  "provider":{{"@type":"Organization","name":"ZENIA","url":"https://zeniapartners.com"}},
  "description":"{v["meta_desc"]}",
  "areaServed":{{"@type":"Country","name":"Spain"}},
  "offers":{{"@type":"Offer","priceCurrency":"EUR","price":"297","priceSpecification":{{"@type":"UnitPriceSpecification","price":"297","priceCurrency":"EUR","unitText":"mes"}},"description":"Plan Starter — 1 canal + 1 agente IA","url":"https://zeniapartners.com/es/{v["slug"]}.html"}}
}}
</script>

<script type="application/ld+json">
{{
  "@context":"https://schema.org",
  "@type":"FAQPage",
  "mainEntity":[
    {faq_schema}
  ]
}}
</script>

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Space+Grotesk:wght@700&display=swap" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Space+Grotesk:wght@700&display=swap" rel="stylesheet"></noscript>

<link rel="stylesheet" href="/styles/main.css?v=4">
</head>
<body>

<!-- NAV -->
{render_nav()}

<!-- HERO -->
<section class="hero" id="hero" style="padding-top:120px">
  <div class="hero-bg"><canvas id="glsl-canvas"></canvas><div class="hero-bg-top"></div></div>
  <div class="container">
    <div class="hero-badge">{v["badge"]}</div>
    <h1>{v["h1_main"]}<br><span class="text-gradient">{v["h1_gradient"]}</span></h1>
    <p class="hero-subtitle">{v["lead"]}</p>
    <div class="hero-actions">
      <a href="{wa_link}" class="btn btn-primary btn-arrow">Hablar por WhatsApp</a>
      <a href="#solucion" class="btn btn-secondary">Ver como funciona</a>
    </div>
    <p class="hero-micro">Implementacion completa en 5 semanas. Desde €297/mes.</p>
  </div>
</section>

<!-- PAIN POINTS -->
<section class="section" id="solucion">
  <div class="container">
    <div class="text-center">
      <span class="section-label">El Problema</span>
      <h2 class="section-title">Lo que pasa en los <span class="text-gradient">{v["pain_title"]}</span> hoy</h2>
      <p class="section-desc">La diferencia entre perder clientes y fidelizarlos es un sistema.</p>
    </div>
    <div class="opp-grid" style="grid-template-columns:repeat(2,1fr);margin-top:48px">
      <div class="opp-card">
        <span class="opp-card-number">Sin CRM</span>
        <h3>El problema</h3>
        <ul style="color:var(--text-secondary);padding-left:18px;font-size:14px;line-height:2.2;list-style:disc">
{pains_without_html}
        </ul>
      </div>
      <div class="opp-card" style="border-color:var(--border-hover)">
        <span class="opp-card-number" style="color:var(--primary)">Con ZENIA</span>
        <h3>La solucion</h3>
        <ul style="color:var(--text-secondary);padding-left:18px;font-size:14px;line-height:2.2;list-style:disc">
{pains_with_html}
        </ul>
      </div>
    </div>
  </div>
</section>

<hr class="section-divider">

<!-- CONTENT BLOCKS -->
<section class="section">
  <div class="container">
    <div class="text-center">
      <span class="section-label">Por Que ZENIA</span>
      <h2 class="section-title">La solucion <span class="text-gradient">explicada</span></h2>
    </div>
    <div class="tailor-points" style="max-width:800px;margin:48px auto 0">
{content_html}
    </div>
  </div>
</section>

<hr class="section-divider">

<!-- RESULTS -->
<section class="section">
  <div class="container text-center">
    <div>
      <span class="section-label">Resultados</span>
      <h2 class="section-title">Impacto <span class="text-gradient">medible</span></h2>
      <p class="section-desc">Numeros reales de negocios que usan ZENIA.</p>
    </div>
    <div class="impact-grid" style="margin-top:48px">
{results_html}
    </div>
  </div>
</section>

<hr class="section-divider">

<!-- PROCESS -->
<section class="section">
  <div class="container text-center">
    <div>
      <span class="section-label">Proceso</span>
      <h2 class="section-title">Como <span class="text-gradient">funciona</span></h2>
      <p class="section-desc">De la primera llamada a tu negocio en piloto automatico. 5 semanas.</p>
    </div>
    <div class="process-steps" style="grid-template-columns:repeat(3,1fr);margin-top:60px">
      <div class="process-step">
        <div class="step-number">01</div>
        <h3>Nos cuentas tu negocio</h3>
        <p>Llamada de 30 minutos. Entendemos tus procesos, clientes y objetivos.</p>
      </div>
      <div class="process-step">
        <div class="step-number">02</div>
        <h3>Configuramos todo</h3>
        <p>En 5 semanas montamos tu CRM, entrenamos tu agente de IA personalizado y conectamos WhatsApp.</p>
      </div>
      <div class="process-step">
        <div class="step-number">03</div>
        <h3>Piloto automatico</h3>
        <p>El agente atiende, vende y fideliza. Tu te enfocas en lo que importa.</p>
      </div>
    </div>
  </div>
</section>

<hr class="section-divider">

<!-- PRICING -->
<section class="section" id="precios">
  <div class="container">
    <div class="text-center">
      <span class="section-label">Precios</span>
      <h2 class="section-title">Planes y <span class="text-gradient">precios</span></h2>
      <p class="section-desc">Sin permanencia. Sin sorpresas. Setup incluye configuracion completa + entrenamiento de tu agente de IA personalizado.</p>
    </div>
    <div class="services-grid" style="grid-template-columns:repeat(3,1fr);margin-top:48px">
      <div class="service-card" style="text-align:center">
        <h3>Starter</h3>
        <div class="impact-number text-gradient" style="margin:16px 0 8px">€297<span style="font-size:16px;font-weight:400">/mes</span></div>
        <p style="color:var(--text-muted);font-size:13px;margin-bottom:20px">1 canal + 1 agente IA</p>
        <ul style="list-style:none;text-align:left;font-size:14px;color:var(--text-secondary);line-height:2.2">
          <li>WhatsApp o Instagram</li>
          <li>Agente IA entrenado con tu catalogo</li>
          <li>Respuestas automaticas 24/7</li>
          <li>Dashboard de metricas</li>
        </ul>
      </div>
      <div class="service-card" style="text-align:center;border-color:var(--primary)">
        <div style="font-size:11px;text-transform:uppercase;letter-spacing:1px;color:var(--primary);font-weight:600;margin-bottom:8px">Recomendado</div>
        <h3>Growth</h3>
        <div class="impact-number" style="color:#22c55e;margin:16px 0 8px">€497<span style="font-size:16px;font-weight:400">/mes</span></div>
        <p style="color:var(--text-muted);font-size:13px;margin-bottom:20px">Multicanal + CRM completo</p>
        <ul style="list-style:none;text-align:left;font-size:14px;color:var(--text-secondary);line-height:2.2">
          <li>WhatsApp + Instagram + Web</li>
          <li>CRM con pipeline de ventas</li>
          <li>Automatizaciones avanzadas</li>
          <li>Reportes y analitica</li>
          <li>Soporte prioritario</li>
        </ul>
      </div>
      <div class="service-card" style="text-align:center">
        <h3>Enterprise</h3>
        <div class="impact-number text-gradient" style="margin:16px 0 8px">€897+<span style="font-size:16px;font-weight:400">/mes</span></div>
        <p style="color:var(--text-muted);font-size:13px;margin-bottom:20px">Solucion a medida</p>
        <ul style="list-style:none;text-align:left;font-size:14px;color:var(--text-secondary);line-height:2.2">
          <li>Todos los canales</li>
          <li>Integraciones custom</li>
          <li>Multiples agentes IA</li>
          <li>SLA dedicado</li>
          <li>Account manager</li>
        </ul>
      </div>
    </div>
    <p style="text-align:center;margin-top:32px;font-size:14px;color:var(--text-muted)">Setup desde €997 (configuracion + training IA) · Validez: 7 dias · <strong style="color:var(--text-secondary)">Menos que un empleado a media jornada</strong></p>
  </div>
</section>

<hr class="section-divider">

<!-- FAQ -->
<section class="faq-section" id="faq">
  <div class="container">
    <div class="text-center">
      <span class="section-label">FAQ</span>
      <h2 class="section-title">Preguntas frecuentes sobre<br><span class="text-gradient">{v["title"].lower()}</span></h2>
    </div>
    <div class="faq-grid">
{faq_html}
    </div>
  </div>
</section>

<!-- CTA -->
<section class="cta-section">
  <div class="container">
    <div class="cta-box">
      <span class="section-label">Siguiente Paso</span>
      <h2>{v["cta_h2_main"]} <span class="text-gradient">{v["cta_h2_gradient"]}</span></h2>
      <p>{v["cta_text"]}</p>
      <div class="cta-actions">
        <a href="{wa_link}" class="btn btn-primary btn-arrow">Hablar por WhatsApp</a>
        <a href="#precios" class="btn btn-secondary">Ver precios</a>
      </div>
    </div>
  </div>
</section>

<!-- EXPLORE MORE -->
<section class="section">
  <div class="container text-center">
    <span class="section-label">Mas Soluciones</span>
    <h2 class="section-title">Explora mas <span class="text-gradient">verticales</span></h2>
    <div style="display:flex;flex-wrap:wrap;gap:8px 16px;justify-content:center;margin-top:32px">
{footer_links}
    </div>
  </div>
</section>

<!-- FOOTER -->
{render_footer()}

<!-- WhatsApp Float -->
{render_wa_float()}

<!-- Scripts -->
{render_mobile_nav_js()}

<!-- Cookie Consent -->
<div id="cookieBanner" style="display:none;position:fixed;bottom:0;left:0;right:0;background:#111827;color:#f9fafb;padding:16px 24px;z-index:9999;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;font-size:13px;box-shadow:0 -2px 12px rgba(0,0,0,0.2);align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;">
  <p style="margin:0;flex:1;min-width:240px;line-height:1.5;">Usamos cookies para analitica (Google Analytics) y mejorar tu experiencia. <a href="/privacy" style="color:#818cf8;text-decoration:underline;">Politica de privacidad</a></p>
  <div style="display:flex;gap:8px;flex-shrink:0;">
    <button onclick="acceptCookies()" style="background:#6366f1;color:white;border:none;padding:8px 20px;border-radius:6px;font-size:13px;font-weight:600;cursor:pointer;">Aceptar</button>
    <button onclick="rejectCookies()" style="background:transparent;color:#d1d5db;border:1px solid #4b5563;padding:8px 16px;border-radius:6px;font-size:13px;cursor:pointer;">Rechazar</button>
  </div>
</div>
<script>
(function(){{
  var consent = localStorage.getItem('cookie_consent');
  if (consent === null) {{
    document.getElementById('cookieBanner').style.display = 'flex';
    window['ga-disable-G-HP0VQSEL68'] = true;
  }} else if (consent === 'rejected') {{
    window['ga-disable-G-HP0VQSEL68'] = true;
  }}
}})();
function acceptCookies() {{
  localStorage.setItem('cookie_consent', 'accepted');
  document.getElementById('cookieBanner').style.display = 'none';
  window['ga-disable-G-HP0VQSEL68'] = false;
  gtag('consent', 'update', {{ analytics_storage: 'granted' }});
}}
function rejectCookies() {{
  localStorage.setItem('cookie_consent', 'rejected');
  document.getElementById('cookieBanner').style.display = 'none';
  window['ga-disable-G-HP0VQSEL68'] = true;
}}
</script>

<script>
if (window.innerWidth > 768) {{
  window.addEventListener('load', function() {{
    setTimeout(function() {{
      var s1 = document.createElement('script');
      s1.src = 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js';
      s1.onload = function() {{
        setTimeout(function() {{
          var s2 = document.createElement('script');
          s2.src = '/js/animation.js';
          document.body.appendChild(s2);
        }}, 100);
      }};
      document.body.appendChild(s1);
    }}, 1000);
  }});
}}
</script>
</body>
</html>'''


# =============================================================================
# HTML TEMPLATE — CITY PAGES
# =============================================================================

def generate_city_page(city_data):
    """Generate a city-specific landing page."""
    c = city_data
    wa_link = f"https://wa.me/34677612799?text=Hola%2C%20tengo%20un%20negocio%20en%20{c['city']}%20y%20me%20interesa%20Zenia"

    all_verticals = [v for v in VERTICALS if not v["slug"].startswith("crm-whatsapp") and not v["slug"].startswith("crm-pymes") and not v["slug"].startswith("crm-negocios")]

    vertical_grid = '\n'.join([
        f'      <div class="opp-card" style="cursor:pointer" onclick="location.href=\'/es/{v["slug"]}.html\'"><span class="opp-card-number">{v["badge"]}</span><h3>{v["title"].replace("CRM con IA para ","").replace("CRM para ","").replace("CRM WhatsApp para ","")}</h3><p>{v["lead"][:120]}...</p></div>'
        for v in all_verticals[:12]
    ])

    all_slugs = [v["slug"] for v in VERTICALS] + [cc["slug"] for cc in CITIES]
    footer_links = '\n'.join([
        f'    <a href="/es/{s}.html" style="color:var(--text-muted);font-size:13px;text-decoration:none;transition:color 0.2s">{s.replace("crm-","").replace("-"," ").title()}</a>'
        for s in all_slugs if s != c["slug"]
    ])

    faq_items = [
        (f"Que tipo de negocios en {c['city']} pueden usar Zenia?", f"Restaurantes, gimnasios, clinicas, salones de belleza, tiendas, inmobiliarias, hoteles, academias, consultoras y cualquier negocio en {c['city']} que reciba consultas por WhatsApp."),
        ("Cuanto cuesta?", "Desde €297/mes con setup de €997. Implementacion completa en 5 semanas."),
        ("Necesito conocimientos tecnicos?", "No. Nosotros hacemos todo. Tu equipo solo necesita saber usar WhatsApp."),
        (f"Tienen oficina en {c['city']}?", f"Trabajamos de forma remota con clientes en toda España, incluyendo {c['city']}. La implementacion es 100% digital."),
        ("Cuanto tarda la implementacion?", "5 semanas desde la firma."),
        ("Puedo cancelar cuando quiera?", "Si. Sin permanencia, sin penalizaciones."),
    ]

    faq_schema = ',\n    '.join([
        '{{"@type":"Question","name":"{}","acceptedAnswer":{{"@type":"Answer","text":"{}"}}}}'.format(
            q.replace('"', '\\"'), a.replace('"', '\\"')
        )
        for q, a in faq_items
    ])
    faq_html = '\n'.join([
        f'      <div class="faq-item"><h3>{q}</h3><p>{a}</p></div>'
        for q, a in faq_items
    ])

    return f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<!-- Google Analytics 4 -->
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('consent', 'default', {{ analytics_storage: 'denied' }});
</script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-HP0VQSEL68"></script>
<script>
  gtag('js', new Date());
  gtag('config', 'G-HP0VQSEL68', {{ send_page_view: true }});
</script>

<title>CRM con IA para Negocios en {c["city"]} | ZENIA</title>
<meta name="description" content="CRM con agente de IA y WhatsApp para negocios en {c["city"]}. Automatiza atencion, ventas y fidelizacion. Implementacion completa en 5 semanas. Desde €297/mes.">
<link rel="canonical" href="https://zeniapartners.com/es/{c["slug"]}.html">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
<meta name="author" content="ZENIA">
<meta name="theme-color" content="#0A0F1C">
<link rel="icon" type="image/svg+xml" href="/assets/icons/favicon.svg">
<link rel="apple-touch-icon" href="/assets/icons/favicon.svg">

<link rel="alternate" hreflang="es" href="https://zeniapartners.com/es/{c["slug"]}.html">
<link rel="alternate" hreflang="en" href="https://zeniapartners.com/">
<link rel="alternate" hreflang="x-default" href="https://zeniapartners.com/">

<meta property="og:type" content="website">
<meta property="og:title" content="CRM con IA para Negocios en {c["city"]} | ZENIA">
<meta property="og:description" content="Automatiza tu negocio en {c["city"]} con agente de IA y WhatsApp. Desde €297/mes.">
<meta property="og:url" content="https://zeniapartners.com/es/{c["slug"]}.html">
<meta property="og:site_name" content="ZENIA">
<meta property="og:image" content="https://zeniapartners.com/assets/images/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="es_ES">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="CRM con IA para Negocios en {c["city"]} | ZENIA">
<meta name="twitter:description" content="Automatiza tu negocio en {c["city"]} con agente de IA y WhatsApp. Desde €297/mes.">
<meta name="twitter:image" content="https://zeniapartners.com/assets/images/og-image.png">

<script type="application/ld+json">
{{
  "@context":"https://schema.org",
  "@type":"LocalBusiness",
  "name":"Zenia Partners",
  "description":"Agentes de IA y CRM para negocios en {c["city"]}",
  "areaServed":{{"@type":"City","name":"{c["city"]}"}},
  "url":"https://zeniapartners.com/es/{c["slug"]}.html"
}}
</script>

<script type="application/ld+json">
{{
  "@context":"https://schema.org",
  "@type":"FAQPage",
  "mainEntity":[
    {faq_schema}
  ]
}}
</script>

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Space+Grotesk:wght@700&display=swap" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Space+Grotesk:wght@700&display=swap" rel="stylesheet"></noscript>

<link rel="stylesheet" href="/styles/main.css?v=4">
</head>
<body>

<!-- NAV -->
{render_nav()}

<!-- HERO -->
<section class="hero" id="hero" style="padding-top:120px">
  <div class="hero-bg"><canvas id="glsl-canvas"></canvas><div class="hero-bg-top"></div></div>
  <div class="container">
    <div class="hero-badge">{c["city"]}</div>
    <h1>CRM con IA para Negocios en {c["city"]}.<br><span class="text-gradient">Automatiza. Vende mas. Fideliza.</span></h1>
    <p class="hero-subtitle">{c["desc"]}</p>
    <div class="hero-actions">
      <a href="{wa_link}" class="btn btn-primary btn-arrow">Hablar por WhatsApp</a>
      <a href="#verticales" class="btn btn-secondary">Ver soluciones</a>
    </div>
    <p class="hero-micro">Implementacion completa en 5 semanas. Desde €297/mes.</p>
  </div>
</section>

<!-- VERTICALS -->
<section class="section" id="verticales">
  <div class="container">
    <div class="text-center">
      <span class="section-label">Soluciones</span>
      <h2 class="section-title">CRM por <span class="text-gradient">vertical</span> en {c["city"]}</h2>
      <p class="section-desc">Cada negocio es diferente. Cada agente de IA se entrena especificamente para tu vertical.</p>
    </div>
    <div class="opp-grid" style="margin-top:48px">
{vertical_grid}
    </div>
  </div>
</section>

<hr class="section-divider">

<!-- PROCESS -->
<section class="section">
  <div class="container text-center">
    <div>
      <span class="section-label">Proceso</span>
      <h2 class="section-title">Como <span class="text-gradient">funciona</span></h2>
      <p class="section-desc">De la primera llamada a tu negocio en piloto automatico.</p>
    </div>
    <div class="process-steps" style="grid-template-columns:repeat(3,1fr);margin-top:60px">
      <div class="process-step">
        <div class="step-number">01</div>
        <h3>Nos cuentas tu negocio</h3>
        <p>Llamada de 30 min. Entendemos tus procesos y objetivos.</p>
      </div>
      <div class="process-step">
        <div class="step-number">02</div>
        <h3>Configuramos todo</h3>
        <p>En 5 semanas montamos tu CRM y entrenamos tu agente IA.</p>
      </div>
      <div class="process-step">
        <div class="step-number">03</div>
        <h3>Piloto automatico</h3>
        <p>El agente atiende, vende y fideliza 24/7.</p>
      </div>
    </div>
  </div>
</section>

<hr class="section-divider">

<!-- PRICING -->
<section class="section" id="precios">
  <div class="container">
    <div class="text-center">
      <span class="section-label">Precios</span>
      <h2 class="section-title">Planes y <span class="text-gradient">precios</span></h2>
      <p class="section-desc">Sin permanencia. Setup incluye configuracion completa + training IA.</p>
    </div>
    <div class="services-grid" style="grid-template-columns:repeat(3,1fr);margin-top:48px">
      <div class="service-card" style="text-align:center">
        <h3>Starter</h3>
        <div class="impact-number text-gradient" style="margin:16px 0 8px">€297<span style="font-size:16px;font-weight:400">/mes</span></div>
        <p style="color:var(--text-muted);font-size:13px;margin-bottom:20px">1 canal + 1 agente IA</p>
        <ul style="list-style:none;text-align:left;font-size:14px;color:var(--text-secondary);line-height:2.2">
          <li>WhatsApp o Instagram</li>
          <li>Agente IA personalizado</li>
          <li>24/7 automatico</li>
          <li>Dashboard</li>
        </ul>
      </div>
      <div class="service-card" style="text-align:center;border-color:var(--primary)">
        <div style="font-size:11px;text-transform:uppercase;letter-spacing:1px;color:var(--primary);font-weight:600;margin-bottom:8px">Recomendado</div>
        <h3>Growth</h3>
        <div class="impact-number" style="color:#22c55e;margin:16px 0 8px">€497<span style="font-size:16px;font-weight:400">/mes</span></div>
        <p style="color:var(--text-muted);font-size:13px;margin-bottom:20px">Multicanal + CRM</p>
        <ul style="list-style:none;text-align:left;font-size:14px;color:var(--text-secondary);line-height:2.2">
          <li>WhatsApp + Instagram + Web</li>
          <li>Pipeline de ventas</li>
          <li>Automatizaciones</li>
          <li>Reportes</li>
          <li>Soporte prioritario</li>
        </ul>
      </div>
      <div class="service-card" style="text-align:center">
        <h3>Enterprise</h3>
        <div class="impact-number text-gradient" style="margin:16px 0 8px">€897+<span style="font-size:16px;font-weight:400">/mes</span></div>
        <p style="color:var(--text-muted);font-size:13px;margin-bottom:20px">A medida</p>
        <ul style="list-style:none;text-align:left;font-size:14px;color:var(--text-secondary);line-height:2.2">
          <li>Todos los canales</li>
          <li>Integraciones custom</li>
          <li>Multiples agentes</li>
          <li>SLA dedicado</li>
        </ul>
      </div>
    </div>
    <p style="text-align:center;margin-top:32px;font-size:14px;color:var(--text-muted)">Setup desde €997 · Validez: 7 dias · <strong style="color:var(--text-secondary)">Menos que un empleado a media jornada</strong></p>
  </div>
</section>

<hr class="section-divider">

<!-- FAQ -->
<section class="faq-section" id="faq">
  <div class="container">
    <div class="text-center">
      <span class="section-label">FAQ</span>
      <h2 class="section-title">Preguntas frecuentes<br><span class="text-gradient">{c["city"]}</span></h2>
    </div>
    <div class="faq-grid">
{faq_html}
    </div>
  </div>
</section>

<!-- CTA -->
<section class="cta-section">
  <div class="container">
    <div class="cta-box">
      <span class="section-label">Siguiente Paso</span>
      <h2>Tu negocio en {c["city"]} merece <span class="text-gradient">funcionar mejor</span></h2>
      <p>Habla con nosotros. 30 minutos para evaluar si Zenia encaja con tu negocio. Sin compromiso.</p>
      <div class="cta-actions">
        <a href="{wa_link}" class="btn btn-primary btn-arrow">Hablar por WhatsApp</a>
        <a href="#precios" class="btn btn-secondary">Ver precios</a>
      </div>
    </div>
  </div>
</section>

<!-- EXPLORE MORE -->
<section class="section">
  <div class="container text-center">
    <span class="section-label">Mas Soluciones</span>
    <h2 class="section-title">Explora mas <span class="text-gradient">verticales</span></h2>
    <div style="display:flex;flex-wrap:wrap;gap:8px 16px;justify-content:center;margin-top:32px">
{footer_links}
    </div>
  </div>
</section>

<!-- FOOTER -->
{render_footer()}

<!-- WhatsApp Float -->
{render_wa_float()}

<!-- Scripts -->
{render_mobile_nav_js()}

<!-- Cookie Consent -->
<div id="cookieBanner" style="display:none;position:fixed;bottom:0;left:0;right:0;background:#111827;color:#f9fafb;padding:16px 24px;z-index:9999;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;font-size:13px;box-shadow:0 -2px 12px rgba(0,0,0,0.2);align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;">
  <p style="margin:0;flex:1;min-width:240px;line-height:1.5;">Usamos cookies para analitica (Google Analytics) y mejorar tu experiencia. <a href="/privacy" style="color:#818cf8;text-decoration:underline;">Politica de privacidad</a></p>
  <div style="display:flex;gap:8px;flex-shrink:0;">
    <button onclick="acceptCookies()" style="background:#6366f1;color:white;border:none;padding:8px 20px;border-radius:6px;font-size:13px;font-weight:600;cursor:pointer;">Aceptar</button>
    <button onclick="rejectCookies()" style="background:transparent;color:#d1d5db;border:1px solid #4b5563;padding:8px 16px;border-radius:6px;font-size:13px;cursor:pointer;">Rechazar</button>
  </div>
</div>
<script>
(function(){{
  var consent = localStorage.getItem('cookie_consent');
  if (consent === null) {{
    document.getElementById('cookieBanner').style.display = 'flex';
    window['ga-disable-G-HP0VQSEL68'] = true;
  }} else if (consent === 'rejected') {{
    window['ga-disable-G-HP0VQSEL68'] = true;
  }}
}})();
function acceptCookies() {{
  localStorage.setItem('cookie_consent', 'accepted');
  document.getElementById('cookieBanner').style.display = 'none';
  window['ga-disable-G-HP0VQSEL68'] = false;
  gtag('consent', 'update', {{ analytics_storage: 'granted' }});
}}
function rejectCookies() {{
  localStorage.setItem('cookie_consent', 'rejected');
  document.getElementById('cookieBanner').style.display = 'none';
  window['ga-disable-G-HP0VQSEL68'] = true;
}}
</script>

<script>
if (window.innerWidth > 768) {{
  window.addEventListener('load', function() {{
    setTimeout(function() {{
      var s1 = document.createElement('script');
      s1.src = 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js';
      s1.onload = function() {{
        setTimeout(function() {{
          var s2 = document.createElement('script');
          s2.src = '/js/animation.js';
          document.body.appendChild(s2);
        }}, 100);
      }};
      document.body.appendChild(s1);
    }}, 1000);
  }});
}}
</script>
</body>
</html>'''


# =============================================================================
# GENERATE ALL PAGES
# =============================================================================

if __name__ == "__main__":
    output_dir = os.path.dirname(os.path.abspath(__file__))

    # Generate vertical pages
    for v in VERTICALS:
        filepath = os.path.join(output_dir, f"{v['slug']}.html")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(generate_landing(v))
        print(f"  Created: es/{v['slug']}.html")

    # Generate city pages
    for c in CITIES:
        filepath = os.path.join(output_dir, f"{c['slug']}.html")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(generate_city_page(c))
        print(f"  Created: es/{c['slug']}.html")

    print(f"\nTotal: {len(VERTICALS) + len(CITIES)} landing pages generated")
