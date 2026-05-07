#!/usr/bin/env python3
"""Programmatic SEO landing generator for ZENIA Partners.

Generates city x vertical landing pages following the established template.
Each landing targets a long-tail local query like "CRM para [vertical] en [city]".

Strategy for May 2026 expansion (~200 new landings):
- Top 7 verticals x 10 NEW cities = 70 landings
- 5 NEW verticals x 15 existing cities = 75 landings
- 13 standalone verticals x 5 top cities = 65 landings
"""
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ES_DIR = ROOT / "es"
SITEMAP = ROOT / "sitemap.xml"

# ---------- Vertical metadata ----------
# Each vertical: slug -> (display_singular, plural_short, intro_benefit, faq_specific, problem_lines, hero_pitch_template)
VERTICALS = {
    "crm-restaurantes": {
        "label": "restaurantes",
        "label_caps": "Restaurantes",
        "intro_benefit": "automatiza reservas, ventas y seguimiento 24/7",
        "h1": "CRM para restaurantes",
        "pains": [
            "Tu restaurante en {city} compite con cientos de opciones. Si no respondes en 5 minutos, el cliente ya agendó con otro.",
            "Los clientes en {city} usan WhatsApp antes que email o llamada. Sin sistema omnicanal, pierdes leads todos los días.",
            "La rotación de clientes en restaurantes de {city} es alta. Sin seguimiento automatizado, el cliente se olvida de ti y vuelve al de siempre.",
        ],
    },
    "crm-gimnasios": {
        "label": "gimnasios",
        "label_caps": "Gimnasios",
        "intro_benefit": "automatiza retención de socios, onboarding y reactivación de bajas",
        "h1": "CRM para gimnasios",
        "pains": [
            "1 de cada 3 socios cancela cada año en gimnasios de {city}. Sin sistema de retención no detectas a tiempo a los que están en riesgo.",
            "Los socios nuevos en {city} suelen abandonar en los primeros 90 días. Sin onboarding automatizado por WhatsApp, pierdes la mitad antes del mes 3.",
            "El equipo de tu gimnasio en {city} no puede contestar 200 mensajes al día. Sin agente de IA, las dudas quedan sin responder y el lead se enfría.",
        ],
    },
    "crm-salones-belleza": {
        "label": "salones de belleza",
        "label_caps": "Salones de Belleza",
        "intro_benefit": "automatiza agendamiento, fidelización y upselling de tratamientos",
        "h1": "CRM para salones de belleza",
        "pains": [
            "Las clientas en {city} reservan por WhatsApp e Instagram. Sin sistema unificado, el agendamiento se cae entre canales.",
            "Captar una clienta nueva en {city} cuesta 5-7 veces más que retener una. Sin programa de fidelización, no rentabilizas la inversión inicial.",
            "Los salones en {city} pierden 15-20% de citas por falta de recordatorios. Sin recordatorios automatizados es ingreso que se evapora.",
        ],
    },
    "crm-clinicas": {
        "label": "clínicas",
        "label_caps": "Clínicas",
        "intro_benefit": "automatiza gestión de citas y seguimiento de pacientes",
        "h1": "CRM para clínicas",
        "pains": [
            "Las clínicas en {city} reciben consultas por WhatsApp 24/7. Sin agente de IA, las nocturnas y de fin de semana se pierden.",
            "El seguimiento post-consulta en {city} suele ser manual. Sin automatización, los pacientes no completan el plan de tratamiento.",
            "Recuperar pacientes inactivos en {city} requiere un protocolo. Sin sistema de reactivación, dejas dinero en la mesa cada mes.",
        ],
    },
    "crm-abogados": {
        "label": "despachos de abogados",
        "label_caps": "Despachos de Abogados",
        "intro_benefit": "automatiza captación de leads, seguimiento de casos y agendamiento de consultas",
        "h1": "CRM para despachos de abogados",
        "pains": [
            "Los leads de despachos en {city} llegan por web, WhatsApp y referidos. Sin CRM unificado, la mitad se pierde por mala asignación.",
            "El primer contacto con un cliente potencial en {city} debe ser en menos de 30 minutos. Sin agente de IA respondiendo 24/7, se va al siguiente despacho.",
            "El seguimiento de casos en {city} consume horas que tu equipo dedica a tareas administrativas en lugar de jurídicas.",
        ],
    },
    "crm-retail": {
        "label": "comercios retail",
        "label_caps": "Retail",
        "intro_benefit": "automatiza ventas, atención al cliente y fidelización",
        "h1": "CRM para retail",
        "pains": [
            "Tu tienda en {city} recibe consultas por WhatsApp, Instagram y web. Sin omnicanalidad, los pedidos se duplican o se pierden.",
            "Los clientes en {city} esperan respuesta inmediata. Sin agente de IA 24/7, el carrito se abandona y la venta se pierde.",
            "Reactivar clientes que compraron una vez es 5x más rentable que captar nuevos. Sin sistema de retención, ese ingreso recurrente no existe.",
        ],
    },
    "crm-cafeterias": {
        "label": "cafeterías",
        "label_caps": "Cafeterías",
        "intro_benefit": "automatiza pedidos, fidelización y programa de puntos",
        "h1": "CRM para cafeterías",
        "pains": [
            "Las cafeterías en {city} compiten en cada esquina. Sin programa de fidelización, el cliente no repite o rota a otra.",
            "Los pedidos por WhatsApp para llevar en {city} suelen perderse en mensajes mezclados. Sin sistema dedicado, errores de pedido y clientes molestos.",
            "Las promociones de cafeterías en {city} se anuncian por redes sin segmentar. Sin CRM, no sabes quién consume qué ni cuándo enviar el mensaje.",
        ],
    },
    "crm-hoteles": {
        "label": "hoteles",
        "label_caps": "Hoteles",
        "intro_benefit": "automatiza reservas, atención a huéspedes y upselling",
        "h1": "CRM para hoteles",
        "pains": [
            "Los huéspedes en {city} consultan por WhatsApp antes de reservar. Sin agente de IA respondiendo 24/7 en varios idiomas, las reservas se van a Booking.",
            "El upselling en {city} (upgrade de habitación, late checkout, spa) se pierde porque nadie pregunta proactivamente al huésped.",
            "La reseña post-estancia en {city} es lo que sube ranking en Google. Sin sistema automatizado de petición, las quedan en silencio.",
        ],
    },
    "crm-academias": {
        "label": "academias",
        "label_caps": "Academias",
        "intro_benefit": "automatiza captación de alumnos, recordatorios de clase y renovaciones",
        "h1": "CRM para academias",
        "pains": [
            "Las academias en {city} reciben consultas por web y WhatsApp todo el día. Sin agente de IA, las dudas sobre horarios y precios quedan sin respuesta.",
            "La inscripción a curso en {city} requiere 3-5 toques antes de cerrar. Sin secuencia automatizada, los leads tibios se enfrían.",
            "Las renovaciones anuales en {city} se trabajan a último momento. Sin recordatorios programados, perdes alumnos que iban a renovar.",
        ],
    },
    "crm-consultorias": {
        "label": "consultorías",
        "label_caps": "Consultorías",
        "intro_benefit": "automatiza captación de leads, agendamiento de calls y seguimiento",
        "h1": "CRM para consultorías",
        "pains": [
            "Las consultorías en {city} captan por LinkedIn y referidos. Sin CRM, el seguimiento se cae entre Slack, email y WhatsApp.",
            "Una propuesta enviada en {city} sin follow-up sistemático cierra al 15%. Con secuencia automatizada cierra al 35%.",
            "El reporte mensual a clientes en {city} consume horas. Sin sistema, tu consultora gasta tiempo en formato en lugar de insight.",
        ],
    },
    "crm-ecommerce": {
        "label": "ecommerce",
        "label_caps": "Ecommerce",
        "intro_benefit": "automatiza recuperación de carritos, atención al cliente y upselling",
        "h1": "CRM para ecommerce",
        "pains": [
            "Tu tienda online recibe consultas en tiempo real. Sin agente de IA respondiendo en menos de 60 segundos, el cliente compra al competidor.",
            "Los carritos abandonados en {city} se recuperan al 30% con secuencia automatizada de WhatsApp + email. Sin sistema, ese ingreso se queda en cero.",
            "El soporte post-compra en {city} (envíos, devoluciones, cambios) consume el 40% del tiempo del equipo. Sin agente de IA es ineficiencia pura.",
        ],
    },
    "crm-fotografos": {
        "label": "fotógrafos profesionales",
        "label_caps": "Fotógrafos",
        "intro_benefit": "automatiza consultas de cotización, agendamiento y entrega de archivos",
        "h1": "CRM para fotógrafos",
        "pains": [
            "Los fotógrafos en {city} reciben 20-50 consultas al mes por Instagram y WhatsApp. Sin sistema, la mitad no se contesta a tiempo.",
            "Las cotizaciones de boda y eventos en {city} requieren follow-up estructurado. Sin CRM, los leads tibios se pierden.",
            "La entrega de fotos editadas y el cobro final en {city} suele ser ad-hoc. Sin proceso automatizado, las galerías y pagos se atrasan.",
        ],
    },
    "crm-inmobiliarias": {
        "label": "inmobiliarias",
        "label_caps": "Inmobiliarias",
        "intro_benefit": "automatiza captación de compradores, seguimiento y cierre",
        "h1": "CRM para inmobiliarias",
        "pains": [
            "Las inmobiliarias en {city} reciben leads de Idealista, Fotocasa y portales propios. Sin CRM unificado, la asignación a agentes se cae.",
            "El seguimiento de visitas en {city} requiere 6-12 toques antes de cerrar. Sin secuencia automatizada por WhatsApp, los compradores se enfrían.",
            "La cualificación de leads en {city} consume horas de los agentes. Con agente de IA pre-cualificas en menos de 2 minutos.",
        ],
    },
    "crm-medicos": {
        "label": "consultas médicas",
        "label_caps": "Médicos",
        "intro_benefit": "automatiza agendamiento, recordatorios y seguimiento de pacientes",
        "h1": "CRM para consultas médicas",
        "pains": [
            "Las consultas médicas en {city} reciben pacientes que reservan por WhatsApp 24/7. Sin agente de IA, las consultas nocturnas se pierden.",
            "Los recordatorios de cita y vacunación en {city} suelen ser manuales. Sin automatización, las faltas suben al 15-20%.",
            "El seguimiento post-consulta en {city} (revisión de tratamiento, próxima visita) consume el tiempo del equipo médico.",
        ],
    },
    "crm-wellness": {
        "label": "centros de wellness",
        "label_caps": "Wellness",
        "intro_benefit": "automatiza reservas de tratamientos, fidelización y programas de membresía",
        "h1": "CRM para centros de wellness",
        "pains": [
            "Los centros de wellness en {city} venden experiencias premium por WhatsApp. Sin agente de IA, las consultas de horarios y disponibilidad se atascan.",
            "El cliente recurrente en {city} es la base del negocio wellness. Sin programa de fidelización automatizado, la frecuencia baja con el tiempo.",
            "El upselling de tratamientos complementarios en {city} se pierde porque nadie sugiere proactivamente al cliente.",
        ],
    },
    # ----- NEW VERTICALS for May 2026 expansion -----
    "crm-veterinarias": {
        "label": "clínicas veterinarias",
        "label_caps": "Veterinarias",
        "intro_benefit": "automatiza agendamiento, recordatorios de vacunación y seguimiento",
        "h1": "CRM para clínicas veterinarias",
        "pains": [
            "Las clínicas veterinarias en {city} reciben consultas urgentes por WhatsApp todo el día. Sin agente de IA filtrando, los casos críticos se mezclan con los rutinarios.",
            "Los recordatorios de vacunación y desparasitación en {city} se hacen a mano. Sin automatización, los dueños olvidan y las mascotas pierden el calendario.",
            "El seguimiento post-cirugía en {city} requiere 3-5 contactos. Sin sistema, la recuperación queda sin monitoreo y los dueños llaman en pánico.",
        ],
    },
    "crm-dentistas": {
        "label": "clínicas dentales",
        "label_caps": "Dentistas",
        "intro_benefit": "automatiza agendamiento, recordatorios de tratamiento y fidelización",
        "h1": "CRM para clínicas dentales",
        "pains": [
            "Las clínicas dentales en {city} pierden 15-20% de citas por falta de recordatorios. Sin recordatorios 24h y 1h, el sillón queda vacío.",
            "Los tratamientos largos en {city} (ortodoncia, implantes) requieren seguimiento mensual. Sin CRM, los pacientes abandonan a la mitad.",
            "La consulta inicial gratuita en {city} es el mayor canal de captación. Sin agente de IA agendando 24/7, los leads se van a la clínica que sí responde.",
        ],
    },
    "crm-fisios": {
        "label": "fisioterapeutas",
        "label_caps": "Fisioterapia",
        "intro_benefit": "automatiza agendamiento, seguimiento de rehabilitación y recordatorios",
        "h1": "CRM para fisioterapeutas",
        "pains": [
            "Los fisioterapeutas en {city} dependen de sesiones recurrentes. Sin recordatorios automáticos, los pacientes faltan y rompen el plan de rehabilitación.",
            "El primer contacto en {city} suele venir por WhatsApp. Sin agente de IA respondiendo en 60 segundos, el lead se va a la siguiente clínica.",
            "El alta del paciente y la recomendación de mantenimiento en {city} no se sistematiza. Sin CRM, la relación se enfría tras el último tratamiento.",
        ],
    },
    "crm-spas": {
        "label": "spas",
        "label_caps": "Spas",
        "intro_benefit": "automatiza reservas, programas de fidelización y eventos VIP",
        "h1": "CRM para spas",
        "pains": [
            "Los spas en {city} venden experiencia y exclusividad. Sin agente de IA respondiendo con tono premium 24/7, la primera impresión se cae.",
            "Las reservas de tratamientos en {city} compiten en horarios. Sin sistema de gestión, doble booking y clientes molestos.",
            "La fidelización en {city} se construye con experiencias periódicas. Sin programa automatizado, el cliente se olvida hasta el siguiente cumpleaños.",
        ],
    },
    "crm-panaderias": {
        "label": "panaderías y obradores",
        "label_caps": "Panaderías",
        "intro_benefit": "automatiza pedidos, programa de fidelización y eventos especiales",
        "h1": "CRM para panaderías",
        "pains": [
            "Las panaderías en {city} reciben pedidos de tartas y catering por WhatsApp. Sin sistema, los pedidos se mezclan y errores de fecha y cantidad son frecuentes.",
            "El programa de cliente recurrente en {city} no existe en la mayoría de panaderías. Sin fidelización digital, todo el negocio depende de tráfico de calle.",
            "Los pedidos de eventos (bodas, comuniones, navidad) en {city} requieren cotización y seguimiento. Sin CRM, el flujo se cae entre llamada y mostrador.",
        ],
    },
}

# ---------- City metadata ----------
# Each city: slug -> (display_name, country, locale, hero_intro_template)
CITIES = {
    # España existentes (algunos faltantes en algunos verticales)
    "madrid": ("Madrid", "España", "es_ES", "Madrid mueve más de 600.000 PYMEs y un poder adquisitivo alto. {label_caps} en Madrid compiten por velocidad de respuesta y profesionalidad digital."),
    "barcelona": ("Barcelona", "España", "es_ES", "Barcelona es la capital fintech y tecnológica de España. {label_caps} en Barcelona necesitan herramientas a la altura del cliente exigente local."),
    "valencia": ("Valencia", "España", "es_ES", "Valencia crece en turismo, tecnología y comercio. {label_caps} en Valencia que automatizan WhatsApp captan más clientes y los retienen mejor."),
    "sevilla": ("Sevilla", "España", "es_ES", "Sevilla es el motor económico del sur. {label_caps} en Sevilla que digitalizan operaciones se diferencian rápido del resto."),
    "malaga": ("Málaga", "España", "es_ES", "Málaga es el polo tecnológico Costa del Sol. {label_caps} en Málaga atienden cliente nacional e internacional, y necesitan respuesta multilingüe 24/7."),
    "bilbao": ("Bilbao", "España", "es_ES", "Bilbao concentra industria, finanzas y turismo. {label_caps} en Bilbao se benefician de procesos digitales que marcan diferencia frente a competencia tradicional."),
    "zaragoza": ("Zaragoza", "España", "es_ES", "Zaragoza es nodo logístico clave del valle del Ebro. {label_caps} en Zaragoza con operaciones digitalizadas escalan más rápido."),
    "murcia": ("Murcia", "España", "es_ES", "Murcia tiene mercado local fuerte y conexión con Levante. {label_caps} en Murcia que respondan primero capturan más cuota."),
    "palma": ("Palma de Mallorca", "España", "es_ES", "Palma vive de turismo y servicios premium. {label_caps} en Palma necesitan agente multilingüe y respuesta en tiempo real."),
    "las-palmas": ("Las Palmas", "España", "es_ES", "Las Palmas combina turismo internacional y mercado local. {label_caps} en Las Palmas con agente de IA en varios idiomas convierten más."),
    # Nuevas España
    "granada": ("Granada", "España", "es_ES", "Granada vive de turismo, hostelería y universidad. {label_caps} en Granada necesitan respuesta inmediata por WhatsApp para no perder oportunidades."),
    "alicante": ("Alicante", "España", "es_ES", "Alicante crece en tecnología, turismo y servicios. {label_caps} en Alicante que automatizan operaciones se diferencian del competidor tradicional."),
    "san-sebastian": ("San Sebastián", "España", "es_ES", "San Sebastián concentra turismo premium y gastronomía top. {label_caps} en San Sebastián necesitan procesos a la altura del cliente exigente."),
    "vigo": ("Vigo", "España", "es_ES", "Vigo es motor industrial gallego con vocación atlántica. {label_caps} en Vigo se benefician de digitalización para escalar a mercado nacional."),
    "a-coruna": ("A Coruña", "España", "es_ES", "A Coruña combina industria, retail y servicios. {label_caps} en A Coruña que respondan rápido por WhatsApp captan más clientes locales y de la zona."),
    "vitoria": ("Vitoria-Gasteiz", "España", "es_ES", "Vitoria es capital del País Vasco con mercado solvente. {label_caps} en Vitoria necesitan eficiencia operativa para mantener márgenes."),
    "pamplona": ("Pamplona", "España", "es_ES", "Pamplona tiene economía estable y cliente fiel. {label_caps} en Pamplona ganan ventaja siendo los primeros en digitalizar contacto y seguimiento."),
    "cordoba": ("Córdoba", "España", "es_ES", "Córdoba combina patrimonio, turismo y servicios locales. {label_caps} en Córdoba con respuesta inmediata captan turistas y residentes por igual."),
    "toledo": ("Toledo", "España", "es_ES", "Toledo concentra turismo cultural y comercio local. {label_caps} en Toledo que digitalicen atención multiplican retención."),
    "salamanca": ("Salamanca", "España", "es_ES", "Salamanca tiene flujo constante de estudiantes y turistas. {label_caps} en Salamanca con sistema de fidelización capturan recurrencia que otros pierden."),
    # LATAM existentes
    "lima": ("Lima", "Perú", "es_PE", "Lima concentra el 30% del PBI peruano y mercado SMB activo. {label_caps} en Lima con WhatsApp + IA capturan ventaja competitiva masiva."),
    "bogota": ("Bogotá", "Colombia", "es_CO", "Bogotá tiene 600.000 PYMEs activas. {label_caps} en Bogotá que respondan primero por WhatsApp y automaticen seguimiento captan más clientes y retienen mejor."),
    "cdmx": ("Ciudad de México", "México", "es_MX", "CDMX concentra el mercado SMB más grande de habla hispana. {label_caps} en CDMX necesitan agente de IA 24/7 para competir en velocidad de respuesta."),
    "santiago": ("Santiago", "Chile", "es_CL", "Santiago es capital económica andina. {label_caps} en Santiago que digitalizan operación se diferencian rápido del competidor tradicional."),
    "buenos-aires": ("Buenos Aires", "Argentina", "es_AR", "Buenos Aires concentra el mercado SMB argentino. {label_caps} en Buenos Aires con sistema digitalizado capturan más cuota frente a competencia tradicional."),
    # Nuevas LATAM
    "quito": ("Quito", "Ecuador", "es_EC", "Quito es capital política y económica de Ecuador. {label_caps} en Quito con WhatsApp + IA atienden mercado local y cuentas internacionales con misma calidad."),
    "guayaquil": ("Guayaquil", "Ecuador", "es_EC", "Guayaquil es polo comercial y portuario. {label_caps} en Guayaquil que automaticen captación capturan más cuota en mercado dinámico."),
    "medellin": ("Medellín", "Colombia", "es_CO", "Medellín lidera transformación digital en Colombia. {label_caps} en Medellín con agente de IA 24/7 marcan diferencia frente a competencia tradicional."),
    "cali": ("Cali", "Colombia", "es_CO", "Cali concentra industria, comercio y servicios del sur colombiano. {label_caps} en Cali con respuesta automatizada por WhatsApp escalan sin contratar más personal."),
    "cartagena": ("Cartagena", "Colombia", "es_CO", "Cartagena combina turismo internacional y comercio. {label_caps} en Cartagena necesitan agente multilingüe y respuesta 24/7."),
    "monterrey": ("Monterrey", "México", "es_MX", "Monterrey es capital industrial y financiera del norte mexicano. {label_caps} en Monterrey con CRM digitalizado escalan a mercado nacional con eficiencia."),
    "guadalajara": ("Guadalajara", "México", "es_MX", "Guadalajara es polo tecnológico y financiero. {label_caps} en Guadalajara que automatizan operaciones reducen costo y mejoran experiencia."),
    "panama-city": ("Panamá", "Panamá", "es_PA", "Panamá es hub financiero y logístico de Centroamérica. {label_caps} en Panamá necesitan respuesta multilingüe para mercado local e internacional."),
    "san-jose-cr": ("San José", "Costa Rica", "es_CR", "San José concentra mercado SMB centroamericano más estable. {label_caps} en San José que automaticen ganan ventaja sostenible."),
    "montevideo": ("Montevideo", "Uruguay", "es_UY", "Montevideo es capital económica y digital del Cono Sur. {label_caps} en Montevideo con CRM moderno capturan cuota antes que la competencia."),
    # USA Hispanic
    "miami": ("Miami", "Estados Unidos", "es_US", "Miami concentra el mayor mercado hispano de USA. {label_caps} en Miami necesitan agente bilingüe (inglés + español) que atienda cliente local e internacional 24/7."),
}


# ---------- Plan: which combinations to generate ----------

# Top 7 verticals × 11 NEW cities (not yet covered for these verticals)
# Existing 7: crm-restaurantes, crm-gimnasios, crm-salones-belleza, crm-clinicas, crm-abogados, crm-retail
# (some lack full coverage)
TOP_VERTICALS = [
    "crm-restaurantes", "crm-gimnasios", "crm-salones-belleza",
    "crm-clinicas", "crm-abogados", "crm-retail", "crm-cafeterias",
]
NEW_CITIES_FOR_TOP = [
    "granada", "alicante", "san-sebastian", "vigo", "a-coruna",
    "quito", "guayaquil", "medellin", "cali", "cartagena",
    "monterrey", "guadalajara", "miami", "montevideo",
]

# 5 NEW verticals × top 15 cities (existing + a few new key ones)
NEW_VERTICALS = [
    "crm-veterinarias", "crm-dentistas", "crm-fisios",
    "crm-spas", "crm-panaderias",
]
TOP_CITIES_FOR_NEW = [
    "madrid", "barcelona", "valencia", "sevilla", "malaga", "bilbao", "palma",
    "lima", "bogota", "cdmx", "santiago", "buenos-aires",
    "medellin", "monterrey", "miami",
    "guadalajara", "quito", "guayaquil", "cali", "cartagena",
    "montevideo", "panama-city", "san-jose-cr",
]

# Existing standalone-only verticals × 5 top cities
STANDALONE_VERTICALS = [
    "crm-academias", "crm-consultorias", "crm-ecommerce",
    "crm-fotografos", "crm-inmobiliarias", "crm-medicos",
    "crm-wellness", "crm-hoteles",
]
TOP_5_CITIES = ["madrid", "barcelona", "lima", "bogota", "cdmx"]


def slug(vertical, city):
    return f"{vertical}-{city}"


def build_combinations():
    combos = []
    for v in TOP_VERTICALS:
        for c in NEW_CITIES_FOR_TOP:
            combos.append((v, c))
    for v in NEW_VERTICALS:
        for c in TOP_CITIES_FOR_NEW:
            combos.append((v, c))
    for v in STANDALONE_VERTICALS:
        for c in TOP_5_CITIES:
            combos.append((v, c))
    # De-duplicate against existing files
    existing = set(f.replace(".html", "") for f in os.listdir(ES_DIR) if f.endswith(".html"))
    combos = [(v, c) for v, c in combos if slug(v, c) not in existing]
    return combos


# ---------- HTML template ----------
TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="es" href="{canonical}">
<link rel="alternate" hreflang="x-default" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="ZENIA">
<meta property="og:locale" content="{locale}">
<meta property="og:image" content="https://zeniapartners.com/assets/images/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="https://zeniapartners.com/assets/images/og-image.png">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<meta name="author" content="ZENIA">
<meta name="theme-color" content="#0A0F1C">
<link rel="icon" type="image/svg+xml" href="../assets/icons/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/styles/main.css">

<script type="application/ld+json">{service_jsonld}</script>
<script type="application/ld+json">{faq_jsonld}</script>

<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('consent', 'default', {{'analytics_storage': 'denied','ad_storage': 'denied','wait_for_update': 500}});
</script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-HP0VQSEL68"></script>
<script>
  gtag('js', new Date());
  gtag('config', 'G-HP0VQSEL68');
</script>

<style>
  .city-badge {{ display: inline-block; padding: 6px 14px; background: rgba(59, 130, 246, 0.1); border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 999px; color: #60A5FA; font-size: 0.85rem; font-weight: 600; margin-bottom: 20px; }}
  .local-pains {{ background: rgba(239, 68, 68, 0.05); border-left: 3px solid #EF4444; padding: 24px 28px; border-radius: 0 12px 12px 0; margin: 40px 0; }}
  .local-pains h3 {{ color: #F87171; font-size: 1.1rem; margin-bottom: 16px; }}
  .local-pains ul {{ list-style: none; padding: 0; }}
  .local-pains li {{ padding: 10px 0 10px 28px; position: relative; color: #CBD5E1; }}
  .local-pains li:before {{ content: "✗"; position: absolute; left: 0; color: #EF4444; font-weight: bold; }}
  .related-links {{ display: flex; flex-wrap: wrap; gap: 12px; margin: 40px 0; }}
  .related-link {{ padding: 10px 16px; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; color: #94A3B8; text-decoration: none; font-size: 0.9rem; transition: all 0.3s; }}
  .related-link:hover {{ border-color: #3B82F6; color: #F1F5F9; }}
  .faq-grid {{ max-width: 800px; margin: 0 auto; }}
  .faq-item {{ background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px 24px; margin-bottom: 12px; }}
  .faq-q {{ font-weight: 600; color: #F1F5F9; cursor: pointer; }}
  .faq-a {{ color: #94A3B8; margin-top: 12px; line-height: 1.7; }}
</style>
</head>
<body>

<nav class="nav scrolled" id="nav">
  <div class="nav-inner">
    <a href="/es/" class="nav-logo"><svg class="zenia-mark" viewBox="0 0 140 140" fill="none"><defs><linearGradient id="zg-b" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#2563EB"/><stop offset="100%" stop-color="#3B82F6"/></linearGradient><linearGradient id="zg-v" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#6366F1"/><stop offset="100%" stop-color="#7C3AED"/></linearGradient></defs><rect width="140" height="140" rx="28" fill="#0F172A"/><path d="M 70 18 Q 18 18 18 38 L 18 57 Q 18 63 24 63 L 88 63 Z" fill="url(#zg-b)"/><path d="M 70 122 Q 122 122 122 102 L 122 83 Q 122 77 116 77 L 52 77 Z" fill="url(#zg-v)"/></svg><span class="nav-logo-text">ZENIA</span></a>
    <ul class="nav-links">
      <li><a href="/es/">Inicio</a></li>
      <li><a href="#solucion">Solución</a></li>
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
</nav>

<section class="hero" id="hero" data-hero-fixed="true">
  <div class="hero-bg"><canvas id="glsl-canvas"></canvas><div class="hero-bg-top"></div></div>
  <div class="container" style="position: relative; z-index: 2; text-align: center;">
    <span class="city-badge">📍 {city_display}, {country}</span>
    <h1 class="section-title" style="font-size: clamp(2rem, 5vw, 3.5rem);">
      <span class="text-gradient">{vertical_h1}</span> en {city_display}
    </h1>
    <p class="hero-lead" style="font-size: 1.15rem; color: #94A3B8; max-width: 720px; line-height: 1.7; margin: 20px auto 32px;">
      {hero_intro} ZENIA despliega ese sistema en 5 semanas.
    </p>
    <div class="hero-ctas" style="display: flex; gap: 12px; flex-wrap: wrap; justify-content: center;">
      <a href="https://wa.me/34677612799" class="btn btn-primary">Habla con nosotros por WhatsApp</a>
      <a href="/es/#precios" class="btn btn-secondary">Ver precios</a>
    </div>
  </div>
</section>

<section class="section" style="padding: 60px 24px;">
  <div class="container">
    <div class="local-pains">
      <h3>El problema real en {city_display}</h3>
      <ul>
        {pains_html}
      </ul>
    </div>

    <h2 class="section-title" style="margin-top: 60px;" id="solucion">Cómo ZENIA resuelve esto en {city_display}</h2>
    <p style="color: #94A3B8; line-height: 1.8; max-width: 720px;">
      Desplegamos un agente de IA personalizado para tu negocio que responde por WhatsApp 24/7 con el tono y procesos de tu empresa. Gestiona consultas, agendamiento y seguimiento sin que tengas que contratar más personal. Se integra con tus herramientas actuales y se entrena con tu catálogo, horarios y reglas operativas.
    </p>

    <h3 style="margin-top: 40px; color: #F1F5F9;">Implementación en 5 semanas</h3>
    <ul style="color: #94A3B8; line-height: 1.8; padding-left: 24px;">
      <li><strong style="color: #F1F5F9;">Semana 1-2:</strong> Diagnóstico de tu operativa actual en {city_display}, mapeo de procesos, conexión de canales.</li>
      <li><strong style="color: #F1F5F9;">Semana 3-4:</strong> Entrenamiento del agente con tu catálogo, tono de marca, FAQs y reglas de negocio.</li>
      <li><strong style="color: #F1F5F9;">Semana 5:</strong> Lanzamiento, monitoreo 24/7, ajustes finos según data real.</li>
    </ul>
  </div>
</section>

<section class="section" style="padding: 60px 24px; background: rgba(255,255,255,0.02);">
  <div class="container">
    <h2 class="section-title" id="faq">Preguntas frecuentes</h2>
    <div class="faq-grid">
      {faq_html}
    </div>
  </div>
</section>

<section class="section" style="padding: 60px 24px;">
  <div class="container" style="text-align: center;">
    <h2 class="section-title">¿Listo para automatizar tu {vertical_label_singular} en {city_display}?</h2>
    <p style="color: #94A3B8; font-size: 1.1rem; margin: 20px 0 32px;">
      Habla con nosotros por WhatsApp y te mostramos cómo sería tu agente de IA en acción.
    </p>
    <a href="https://wa.me/34677612799" class="btn btn-primary" style="font-size: 1.05rem;">Empezar por WhatsApp</a>
  </div>
</section>

<section class="section" style="padding: 40px 24px;">
  <div class="container">
    <h3 style="color: #F1F5F9; margin-bottom: 20px;">Otras ciudades</h3>
    <div class="related-links">
      {related_html}
    </div>
  </div>
</section>

<!-- Three.js animated hero background (desktop only, loads 3s after pageload) -->
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
    }}, 3000);
  }});
}}
</script>

<footer class="footer">
  <div class="container">
    <div class="footer-inner">
      <div class="footer-brand">
        <div class="footer-logo"><svg class="zenia-mark zenia-mark--sm" viewBox="0 0 140 140" fill="none"><defs><linearGradient id="zg2-b" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#2563EB"/><stop offset="100%" stop-color="#3B82F6"/></linearGradient><linearGradient id="zg2-v" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#6366F1"/><stop offset="100%" stop-color="#7C3AED"/></linearGradient></defs><rect width="140" height="140" rx="28" fill="#0F172A"/><path d="M 70 18 Q 18 18 18 38 L 18 57 Q 18 63 24 63 L 88 63 Z" fill="url(#zg2-b)"/><path d="M 70 122 Q 122 122 122 102 L 122 83 Q 122 77 116 77 L 52 77 Z" fill="url(#zg2-v)"/></svg><span>ZENIA</span></div>
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
</footer>

</body>
</html>
"""


def render(vertical, city):
    v = VERTICALS[vertical]
    city_name, country, locale, hero_intro_tpl = CITIES[city]
    label_caps = v["label_caps"]
    label = v["label"]

    # Singular form for CTA section ("automatizar tu restaurante" rather than "tus restaurantes")
    label_singular = {
        "restaurantes": "restaurante",
        "gimnasios": "gimnasio",
        "salones de belleza": "salón de belleza",
        "clínicas": "clínica",
        "despachos de abogados": "despacho",
        "comercios retail": "comercio",
        "cafeterías": "cafetería",
        "hoteles": "hotel",
        "academias": "academia",
        "consultorías": "consultoría",
        "ecommerce": "ecommerce",
        "fotógrafos profesionales": "negocio de fotografía",
        "inmobiliarias": "inmobiliaria",
        "consultas médicas": "consulta médica",
        "centros de wellness": "centro de wellness",
        "clínicas veterinarias": "clínica veterinaria",
        "clínicas dentales": "clínica dental",
        "fisioterapeutas": "consulta de fisioterapia",
        "spas": "spa",
        "panaderías y obradores": "panadería",
    }.get(label, label)

    title = f"{v['h1']} en {city_name} | IA y WhatsApp | ZENIA"
    description = f"{v['h1']} en {city_name}. Agente de IA para WhatsApp que {v['intro_benefit']}. Implementación en 5 semanas. ZENIA."
    canonical = f"https://zeniapartners.com/es/{slug(vertical, city)}.html"

    # Hero intro: customize template with vars
    hero_intro = hero_intro_tpl.format(label=label, label_caps=label_caps)

    # Pains
    pains_html = "\n        ".join(f"<li>{p.format(city=city_name)}</li>" for p in v["pains"])

    # FAQ
    faqs = [
        (f"¿ZENIA funciona para {label} en {city_name}?",
         f"Sí. Operamos con {label} en {country}, incluida {city_name}. El agente se adapta al contexto local: horarios, idioma, canales usados por tus clientes, integraciones con plataformas locales."),
        (f"¿Cuánto cuesta implementar ZENIA para mi {label_singular} en {city_name}?",
         "Plan Starter desde 297€/mes + 997€ setup único. Plan Growth 497€/mes recomendado para negocios con alto volumen. Plan Enterprise a medida para cadenas con múltiples localizaciones."),
        ("¿En cuánto tiempo está operativo?",
         "5 semanas desde la firma. Semana 1-2: diagnóstico y configuración. Semana 3-4: entrenamiento del agente con tu catálogo y procesos. Semana 5: lanzamiento y ajustes."),
        ("¿Se integra con mi herramienta actual?",
         "Sí. Conectamos con WhatsApp Business API, Instagram, calendarios, CRMs existentes, sistemas POS, plataformas de reservas y herramientas más usadas en el sector. Si tienes un caso específico, lo validamos en el diagnóstico."),
        (f"¿Mis datos de clientes en {city_name} están seguros?",
         "Sí. Cumplimos GDPR y normativa local de protección de datos. Los datos se alojan en infraestructura europea, encriptación end-to-end, y tú eres el propietario de la base de datos."),
        ("¿Necesito conocimientos técnicos para usar ZENIA?",
         "No. Nosotros configuramos, entrenamos al agente con tu operativa y te entregamos un panel simple para ver conversaciones, métricas y ajustar plantillas si quieres."),
    ]

    faq_html = "\n      ".join(
        f'<details class="faq-item">\n          <summary class="faq-q">{q}</summary>\n          <div class="faq-a">{a}</div>\n        </details>'
        for q, a in faqs
    )

    faq_jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faqs
        ],
    }, ensure_ascii=False)

    service_jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "Service",
        "name": f"ZENIA {v['h1']} en {city_name}",
        "provider": {"@type": "Organization", "name": "ZENIA", "url": "https://zeniapartners.com"},
        "areaServed": {"@type": "City", "name": city_name},
        "serviceType": v["h1"],
        "description": description,
    }, ensure_ascii=False)

    # Related cities (4 from same vertical)
    related = []
    for other_city in list(CITIES.keys()):
        if other_city == city:
            continue
        other_path = ES_DIR / f"{slug(vertical, other_city)}.html"
        if other_path.exists() or (vertical, other_city) in [(v_, c_) for v_, c_ in build_combinations()]:
            other_name = CITIES[other_city][0]
            related.append((other_city, other_name))
            if len(related) >= 3:
                break

    related_html_parts = [
        f'<a href="/es/{slug(vertical, c)}.html" class="related-link">{v["h1"]} en {n}</a>'
        for c, n in related
    ]
    # Plus link to national page
    related_html_parts.append(f'<a href="/es/{vertical}.html" class="related-link">{v["h1"]} (guía nacional)</a>')
    related_html = "\n      ".join(related_html_parts)

    return TEMPLATE.format(
        title=title,
        description=description,
        canonical=canonical,
        locale=locale,
        service_jsonld=service_jsonld,
        faq_jsonld=faq_jsonld,
        city_display=city_name,
        country=country,
        vertical_h1=v["h1"],
        hero_intro=hero_intro,
        pains_html=pains_html,
        faq_html=faq_html,
        vertical_label_singular=label_singular,
        related_html=related_html,
    )


def update_sitemap(new_paths):
    """Append new URLs to sitemap.xml before </urlset>."""
    with open(SITEMAP, "r", encoding="utf-8") as f:
        content = f.read()
    today = "2026-04-27"
    entries = []
    for path in new_paths:
        entries.append(
            f'  <url>\n    <loc>https://zeniapartners.com/{path}</loc>\n'
            f'    <lastmod>{today}</lastmod>\n    <changefreq>monthly</changefreq>\n'
            f'    <priority>0.8</priority>\n  </url>'
        )
    block = "\n".join(entries) + "\n</urlset>"
    content = content.replace("</urlset>", block)
    with open(SITEMAP, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    combos = build_combinations()
    print(f"Generating {len(combos)} new landings...")

    new_paths = []
    for vertical, city in combos:
        html = render(vertical, city)
        path = ES_DIR / f"{slug(vertical, city)}.html"
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        new_paths.append(f"es/{slug(vertical, city)}.html")
        print(f"  + {path.name}")

    update_sitemap(new_paths)
    print(f"\nDone. {len(new_paths)} new landings + sitemap updated.")


if __name__ == "__main__":
    main()
