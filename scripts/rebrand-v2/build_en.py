#!/usr/bin/env python3
"""ZENIA v2 · portada en INGLÉS (index.html en la raíz), mismo sistema que la española (build.py).

Uso: python3 scripts/rebrand-v2/build_en.py <raíz_del_sitio> [--preview]
  --preview  escribe <raíz>/v2/index.html con noindex
Reutiliza piezas de build.py (logo, iconos, integraciones, versión de la hoja). Mantiene la redirección
de la portada inglesa: quien navega en español (o eligió español) va a /es/; ?lang=en fuerza el inglés.
El formulario manda el sector con el valor interno en español (Clínica/Taller/Autoescuela/Otro) para que
el aviso de leads lo entienda igual; locale = en."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as B  # noqa: E402  (no ejecuta nada al importarse)

E, MARK, MARK_SOLO, WA_ICO, PLAY, ICO, INTEG, wa = B.E, B.MARK, B.MARK_SOLO, B.WA_ICO, B.PLAY, B.ICO, B.INTEG, B.wa
PREVIEW, RAIZ, V, CF, CALENDLY = B.PREVIEW, B.RAIZ, B.V, B.CF, B.CALENDLY
SECTOR_EN = {'clinica': 'Clinic', 'taller': 'Auto shop', 'autoescuela': 'Driving school'}
WA_INFO = "Hi, I'm coming from the Zenia website and would like more information"

NEGOCIOS = {
    'clinica': {'nombre': 'Dental clinic · example', 'inicial': 'C', 'vertical': 'clinica',
                'saludo': "Hi! I'm the clinic's assistant. I can help with appointments, prices and opening hours. What do you need?",
                'cita': {'chip': 'Book an appointment', 'p': "Hi, I'd like to book a teeth cleaning",
                         'intro': 'Of course! These are the next free slots for a cleaning:', 'servicio': 'teeth cleaning'},
                'preguntas': [
                    {'p': 'Is the first visit free?', 'r': 'Yes, the first visit is free: the dentist checks you and you leave with a written quote. Shall I find you a slot?'},
                    {'p': 'Are you open on Saturdays?', 'r': 'Yes, Saturdays from 10 am to 2 pm. Weekdays from 9:30 am to 8:30 pm, no lunch break.'},
                    {'p': 'Can I pay for braces in installments?', 'r': "Yes, you can pay monthly. We'll go through the details at your first visit, quote in hand."},
                    {'p': 'I have a really bad toothache', 'r': "Sorry to hear that. I'm letting reception know right now so they call you and give you the first free slot today."}]},
    'taller': {'nombre': 'Auto repair shop · example', 'inicial': 'T', 'vertical': 'taller',
               'saludo': "Hi! I'm the shop's assistant. I can give you prices, book you in and tell you how your car is doing. How can I help?",
               'cita': {'chip': 'Book a service', 'p': "I'd like to bring my car in for a service this week",
                        'intro': 'Sure, these are the next free slots for a service:', 'servicio': 'car service'},
               'preguntas': [
                   {'p': 'How much is an oil change?', 'r': "It depends on the engine and the oil it takes. Send me make, model and year and I'll give you the exact price."},
                   {'p': 'Do you have courtesy cars?', 'r': 'Yes, for repairs longer than a day, subject to availability. I can book one with your appointment if you need it.'},
                   {'p': 'Can you do a pre-inspection check?', 'r': 'Yes: we check it before your inspection and tell you what needs fixing. Want me to book you in?'},
                   {'p': 'Is my car ready? Plate 7ABC123', 'r': "I'm passing your plate to the shop manager to confirm. As soon as he replies, I'll message you here."}]},
    'autoescuela': {'nombre': 'Driving school · example', 'inicial': 'A', 'vertical': 'autoescuela',
                    'saludo': "Hi! I'm the driving school's assistant. I can tell you prices, packages and how to sign up. What do you need?",
                    'cita': {'chip': 'I want to sign up', 'p': 'Hi, I want to get my driving licence',
                             'intro': "Great! Let's book a visit to sign you up. These slots are free:", 'servicio': 'sign-up visit'},
                    'preguntas': [
                        {'p': 'How much does the licence cost?', 'r': "We have packages with theory and driving lessons. I'll send you the price of each one and what it includes."},
                        {'p': 'Can I do the theory online?', 'r': 'Yes: practice tests on your phone and, if you like, classes at the school in the afternoon.'},
                        {'p': 'How many lessons will I need?', 'r': 'It depends on each student. We assess it in your first lesson and tell you how many we recommend.'},
                        {'p': 'I need to change my test date', 'r': "The office handles that with the testing authority. I'm passing them your name so they call you today."}]},
}

GUION = {'nombre': 'Dental clinic · example', 'pasos': [
    ('The patient messages on WhatsApp', 'Any time. Even at 11:40 pm, after you have closed.'),
    ('The agent answers with your information', 'Treatments, prices, hours and locations from your website, in your tone.'),
    ('It offers real slots from your calendar', 'It reads your calendar and only offers free times.'),
    ('It books and logs it in your CRM', 'The appointment lands in the calendar and the patient record, no typing.'),
    ('It sends a reminder the day before', "And if the patient can't make it, it reschedules in the same chat."),
    ('Clinical questions go to your team', 'Pain, emergencies or medical doubts: reception gets the whole conversation.')],
    'mensajes': [
        {'dir': 'tag', 't': 'Monday · 11:40 pm', 'paso': 0},
        {'dir': 'in', 't': 'Hi, do you have an appointment for a cleaning this week?', 'paso': 0},
        {'dir': 'out', 't': 'Hi! Yes. A cleaning takes about 30 minutes and the first visit is free. Mornings or afternoons?', 'paso': 1},
        {'dir': 'in', 't': 'Afternoon', 'paso': 1},
        {'dir': 'out', 't': 'These are free at our Midtown clinic:', 'botones': ['Thursday 5:00 pm', 'Thursday 6:30 pm', 'Friday 5:30 pm'], 'elegido': 0, 'paso': 2},
        {'dir': 'in', 't': 'Thursday 5 pm. Laura Gomez', 'paso': 2},
        {'dir': 'out', 't': "Done, Laura: cleaning on Thursday at 5:00 pm at Midtown. It's in the calendar.", 'paso': 3},
        {'dir': 'tag', 't': 'Wednesday · 6:00 pm', 'paso': 4},
        {'dir': 'out', 't': 'Hi Laura, a reminder of your appointment tomorrow at 5:00 pm. Reply "yes" to confirm or tell me if you need to change it.', 'paso': 4},
        {'dir': 'in', 't': 'Yes. By the way, my gums bleed a little, is that normal?', 'paso': 5},
        {'dir': 'out', 't': "Best to have the hygienist look at it tomorrow. I'm passing your message on so they know before your visit.", 'paso': 5}]}
CRM_PASOS = [(0, 'New contact: Laura Gomez · WhatsApp'), (2, 'Interest: cleaning · afternoon'), (3, 'Appointment created: Thursday 5:00 pm · Midtown'),
             (4, 'Reminder sent · appointment confirmed'), (5, 'Reception alerted: question about gums')]

PANELES = {
    'clinica': {
        'marca': 'Your clinic', 'barra': 'your clinic', 'fichas': 'Patients', 'agenda': 'Calendar',
        'convs': [('Anna P.', 'esc', 'To your team', 'My tooth really hurts…'), ('Laura Gomez', 'cita', 'Booked', 'Thursday 5 pm · cleaning'),
                  ('Mark R.', 'ok', 'Answered', 'Braces in installments?'), ('+1 ••• ••• 4128', 'ok', 'Answered', 'Open on Saturdays?'),
                  ('Peter L.', 'cita', 'Booked', 'Moved his visit to Friday')],
        'hilo': [('in', 'Hi, do you have an appointment for a cleaning this week?'), ('out', 'Hi! Yes. The first visit is free. Mornings or afternoons?'),
                 ('in', 'Afternoon'), ('out', 'I have Thursday at 5:00 pm or 6:30 pm, or Friday at 5:30 pm.'),
                 ('in', 'Thursday 5 pm. Laura Gomez'), ('out', "Done, Laura: Thursday at 5:00 pm at Midtown. I'll remind you the day before.")],
        'tag': 'Appointment created in the Midtown calendar · 11:44 pm',
        'kpis': [('Appointments this week', '38'), ('Booked by the agent', '21'), ('Confirmed by reminder', '33'), ('Rescheduled by chat', '4')],
        'agenda_cols': ['When', 'Patient', 'Treatment', 'Location', 'Clinician', 'Status'],
        'agenda_rows': [['Thu 5:00 pm', 'Laura Gomez', 'Cleaning', 'Midtown', 'Hygienist', ('cita', 'By the agent')],
                        ['Thu 6:30 pm', 'David Marin', 'Check-up', 'Midtown', 'Dr. Ruiz', ('ok', 'Confirmed')],
                        ['Fri 10:00 am', 'Carmen Vidal', 'First visit', 'Uptown', 'Dr. Soto', ('cita', 'By the agent')],
                        ['Fri 12:00 pm', 'Peter Lima', 'Braces', 'Uptown', 'Dr. Ruiz', ('ok', 'Confirmed')],
                        ['Fri 5:30 pm', 'Anna Perez', 'Emergency', 'Midtown', 'Dr. Soto', ('esc', 'By reception')]],
        'fichas_cols': ['Patient', 'Last contact', 'Interested in', 'Next visit', 'Location', 'Source'],
        'fichas_rows': [['Laura Gomez', 'Today, 11:44 pm', 'Cleaning', 'Thursday 5:00 pm', 'Midtown', 'WhatsApp'],
                        ['Mark Ruiz', 'Today, 7:10 pm', 'Clear aligners', 'Not booked', 'Uptown', 'Google'],
                        ['Carmen Vidal', 'Yesterday', 'Implants', 'Friday 10:00 am', 'Uptown', 'Instagram'],
                        ['Peter Lima', 'Monday', 'Braces', 'Friday 12:00 pm', 'Uptown', 'WhatsApp']],
        'toggles': [('Reply after hours', 'Nights, weekends and holidays.', 1),
                    ("Book in each location's calendar", 'Only free slots of the right clinician.', 1),
                    ('Reminder the day before', 'With the option to confirm or reschedule.', 1),
                    ('Send clinical questions to reception', 'Pain, emergencies and medical doubts.', 1),
                    ('Ask for a review after the visit', 'Only if the visit went well.', 0)]},
    'taller': {
        'marca': 'Your shop', 'barra': 'your shop', 'fichas': 'Vehicles', 'agenda': 'Workshop',
        'convs': [('James M.', 'ok', 'Quote sent', 'Brake pads?'), ('Lucy R.', 'cita', 'Ready', 'Is my car ready?'),
                  ('Peter S.', 'esc', 'Shop manager', 'Strange noise in the steering'), ('+1 ••• ••• 2083', 'ok', 'Answered', 'Open on Saturday?'),
                  ('Anna T.', 'cita', 'Booked', 'Inspection check on Wednesday')],
        'hilo': [('in', 'Hi, how much do you charge to replace brake pads?'), ('out', "Hi! What's the make, model and year of the car?"),
                 ('in', '2019 Honda Civic'), ('out', "I'll send you the quote with front pads and labor. Shall I book you in?"),
                 ('in', 'Wednesday at 9. Plate 7ABC123'), ('out', 'Booked: Wednesday 9:00 am, Honda Civic 7ABC123.')],
        'tag': 'Quote and booking created · Honda Civic 7ABC123',
        'kpis': [('Cars in the shop today', '14'), ('Booked by the agent', '9'), ('Quotes sent', '17'), ('“Car ready” alerts', '11')],
        'agenda_cols': ['Drop-off', 'Customer', 'Vehicle', 'Job', 'Location', 'Status'],
        'agenda_rows': [['Wed 9:00 am', 'James Martin', 'Honda Civic · 7ABC123', 'Brake pads', 'North', ('cita', 'By the agent')],
                        ['Wed 9:30 am', 'Anna Torres', 'Toyota Corolla · 8DEF456', 'Inspection check', 'North', ('ok', 'In the shop')],
                        ['Wed 10:00 am', 'Lucy Romero', 'VW Golf · 9GHJ789', 'Service', 'South', ('ok', 'Ready for pick-up')],
                        ['Wed 11:30 am', 'Peter Sanz', 'Kia Forte · 6KLM012', 'Steering', 'South', ('esc', 'Diagnosis')],
                        ['Wed 4:30 pm', 'Ray Gil', 'Ford Focus · 5NPQ345', 'Tires', 'North', ('cita', 'By the agent')]],
        'fichas_cols': ['Plate', 'Vehicle', 'Customer', 'Last job', 'Next inspection', 'Source'],
        'fichas_rows': [['7ABC123', 'Honda Civic 2019', 'James Martin', 'Brake pads (today)', 'Mar 2027', 'WhatsApp'],
                        ['8DEF456', 'Toyota Corolla 2016', 'Anna Torres', 'Inspection check (today)', 'Nov 2026', 'Google'],
                        ['9GHJ789', 'VW Golf 2021', 'Lucy Romero', '30,000-mile service', 'May 2027', 'WhatsApp'],
                        ['6KLM012', 'Kia Forte 2018', 'Peter Sanz', 'Steering (in progress)', 'Jan 2027', 'Referral']],
        'toggles': [('Ask for make, model and plate', 'Before giving any price.', 1),
                    ("Book in each location's calendar", 'By type of job.', 1),
                    ('Tell customers when the car is ready', 'As soon as your team marks it done.', 1),
                    ('Inspection and service reminders', 'A month before, with a slot to book.', 1),
                    ('Ask for a review at pick-up', 'Only if the job went well.', 0)]},
    'autoescuela': {
        'marca': 'Your school', 'barra': 'your school', 'fichas': 'Students', 'agenda': 'Lessons',
        'convs': [('Martha R.', 'cita', 'Sign-up', '15-lesson package'), ('Evan G.', 'ok', 'Answered', 'Motorcycle licence price?'),
                  ('Sara L.', 'cita', 'Moved', "Move Tuesday's lesson"), ('+1 ••• ••• 7315', 'ok', 'Answered', 'Is the theory online?'),
                  ('Diego P.', 'esc', 'Office', 'Test date')],
        'hilo': [('in', 'Hi! How much is it to get a licence with you?'), ('out', "Hi! We have three packages with theory and lessons. I'll send you the price of each."),
                 ('in', 'I like the 15-lesson one'), ('out', 'To sign up, drop by with your ID. Does Friday at 6:00 pm work?'),
                 ('in', "Yes. I'm Martha Ruiz"), ('out', "You're in, Martha: Friday 6:00 pm at the office, 15-lesson package.")],
        'tag': 'Student created · 15-lesson package · source: Instagram',
        'kpis': [('Lessons this week', '64'), ('Booked or moved by chat', '18'), ('Sign-ups this week', '7'), ('In follow-up', '12')],
        'agenda_cols': ['When', 'Student', 'Type', 'Instructor', 'Vehicle', 'Status'],
        'agenda_rows': [['Mon 8:00 am', 'Sara Lopez', 'Driving lesson', 'John', 'Clio · 2233', ('cita', 'Moved by chat')],
                        ['Mon 9:00 am', 'Evan Garcia', 'Motorcycle lesson', 'Rose', 'MT-07', ('ok', 'Confirmed')],
                        ['Mon 6:00 pm', 'Martha Ruiz', 'Sign-up', 'Office', 'Not needed', ('cita', 'By the agent')],
                        ['Tue 10:00 am', 'Diego Pena', 'Driving test', 'John', 'Clio · 2233', ('esc', 'Office')],
                        ['Tue 5:00 pm', 'Lara Gil', 'Driving lesson', 'Rose', 'Ibiza · 4455', ('ok', 'Confirmed')]],
        'fichas_cols': ['Student', 'Package', 'Lessons done', 'Theory', 'Test', 'Source'],
        'fichas_rows': [['Martha Ruiz', '15 lessons', '0 / 15', 'Pending', 'Not set', 'Instagram'],
                        ['Sara Lopez', '20 lessons', '12 / 20', 'Passed', 'Dec 2026', 'WhatsApp'],
                        ['Evan Garcia', 'Motorcycle', '5 / 10', 'Passed', 'Not set', 'Google'],
                        ['Diego Pena', '15 lessons', '15 / 15', 'Passed', 'Tuesday', 'Referral']],
        'toggles': [('Answer prices and packages', 'With what each one includes.', 1),
                    ('Book the sign-up visit', "In the office's free slots.", 1),
                    ('Move lessons by chat', "Only with 24 hours' notice.", 1),
                    ('Follow up with people who did not sign up', 'After 3 days, with what they asked.', 1),
                    ('Test reminders', 'The day before, with time and place.', 0)]},
}

NICHOS = {
    'clinica': ('Dental and aesthetic clinics', 'Appointments, first visits, quotes and reminders, without leaving patients on read.',
                ['Booking by location and specialty', 'Reminder the day before', 'Clinical questions, always to your team'],
                'Do you have a cleaning slot this week?', 'Yes, Thursday at 5:00 pm at Midtown. Shall I book it?', 'Get a demo for your clinic'),
    'taller': ('Auto repair and tire shops', 'Quotes, service bookings and “your car is ready” alerts.',
               ['Asks for make, model and plate', 'Workshop slots by location', 'Alert when the car is ready'],
               'How much for brake pads?', "What's the make, model and year? I'll give you the exact price.", 'Get a demo for your shop'),
    'autoescuela': ('Driving schools', 'Sign-ups, licence prices and lessons, answered on the spot.',
                    ['Prices and packages from your site', 'Sign-up and lesson booking', 'Follow-up with people who did not sign up'],
                    'How much is the licence?', 'We have three packages. Here is the price of each 👇', 'Get a demo for your school'),
}

FAQ = [
    ('Does the agent replace my team?', 'No. It handles the repetitive questions, books and reminds. Anything that needs a person (complaints, special cases, emergencies) goes to your team with the whole conversation, and your team can step into any chat at any time.'),
    ('Where does it get its information?', 'From your website, your prices and your rules. You review it before it goes live. What it does not know, it does not make up: it passes it to your team.'),
    ('Do I need a new WhatsApp number?', 'We work with the official WhatsApp Business API. You can use your current number or a new one; on the call we explain the options and what each one involves.'),
    ('What does it connect to?', 'WhatsApp Business API, Google Calendar, Calendly, HubSpot, Zoho CRM and Odoo, among others. If you use something else, we will look at it in the demo.'),
    ('How much does it cost?', 'It depends on your conversation volume and what needs connecting. After showing you the demo with your business, we send you a fixed proposal with the monthly price.'),
    ('How does the 48-hour demo work?', 'You leave us your website and we set up an agent with your public information. We send you a link to try it as if you were a customer, nothing to install.'),
]

MAS = [
    ('Client cases', [('/cases/global-watch-buyers-ai-acquisition.html', 'Global Watch Buyers'), ('/cases/throwin-salt-gaia-ebay-whatsapp.html', 'Throwin’ Salt Co.'),
                      ('/cases/croian-hein-private-cellar-switzerland.html', 'Croian & Hein'), ('/cases/cicero-public-affairs-spain-italy.html', 'Cicero'),
                      ('/cases/boutique-law-firm-latam.html', 'Boutique law firm'), ('/cases/', 'All cases')]),
    ('Resources', [('/blog/', 'Blog'), ('/en/ai-bookkeeping-importer-chicago.html', 'AI bookkeeping for importers: Chicago'),
                   ('/en/ai-bookkeeping-importer-dallas.html', 'Dallas'), ('/en/ai-bookkeeping-importer-atlanta.html', 'Atlanta'),
                   ('/en/ai-bookkeeping-importer-doral.html', 'Doral'), ('/about.html', 'About Zenia')]),
    ('En español', [('/es/', 'Inicio'), ('/es/clinicas/', 'Clínicas'), ('/es/talleres/', 'Talleres'), ('/es/autoescuelas/', 'Autoescuelas'),
                    ('/es/cobertura.html', 'Sectores y ciudades')]),
]

REDIRECT = ('<script>(function(){try{var q=new URLSearchParams(location.search).get("lang");if(q==="en")return;'
            'var s=localStorage.getItem("zenia-lang-v2");var n=(navigator.languages&&navigator.languages[0])||navigator.language||"";'
            'if(q==="es"||s==="es"||(!s&&/^es/i.test(n))){location.replace("/es/"+location.hash);}}catch(e){}})();</script>')


def head():
    title = 'AI agent for WhatsApp with calendar and custom CRM | Zenia'
    desc = 'Zenia puts an AI agent on your business WhatsApp: it replies instantly, books into your calendar and logs every chat in your CRM. Your demo in 48 h.'
    canon, og = 'https://zeniapartners.com/', 'og-z2-home-en.jpg'
    robots = '<meta name="robots" content="noindex,nofollow">' if PREVIEW else '<meta name="robots" content="index,follow">'
    org = json.dumps({'@context': 'https://schema.org', '@type': ['Organization', 'ProfessionalService'], '@id': 'https://zeniapartners.com/#organization',
                      'name': 'Zenia Partners', 'url': 'https://zeniapartners.com/', 'logo': 'https://zeniapartners.com/assets/logos/zenia-logo.png',
                      'email': 'fabrizzio.zelada@zeniapartners.com', 'description': 'AI agents for business WhatsApp, with calendar and a custom CRM.'}, ensure_ascii=False)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
{REDIRECT}
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
{robots}
<link rel="canonical" href="{canon}">
<link rel="alternate" hreflang="en" href="https://zeniapartners.com/">
<link rel="alternate" hreflang="es" href="https://zeniapartners.com/es/">
<link rel="alternate" hreflang="x-default" href="https://zeniapartners.com/">
<link rel="icon" type="image/svg+xml" href="/assets/icons/favicon.svg">
<meta name="theme-color" content="#070B13">
<meta property="og:type" content="website">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="https://zeniapartners.com/assets/images/{og}">
<meta property="og:image:secure_url" content="https://zeniapartners.com/assets/images/{og}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="en_US">
<meta property="og:site_name" content="Zenia Partners">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://zeniapartners.com/assets/images/{og}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="/assets/z2/z2.css?v={V}">
{'' if PREVIEW else B.GA}
<script type="application/ld+json">{org}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
'''


def nav():
    links = [('How it works', '#how-it-works'), ('Solutions', '#solutions'), ('Product', '#product'), ('Cases', '#cases'), ('FAQ', '#faq')]
    li = ''.join(f'<a href="{u}">{E(t)}</a>' for t, u in links)
    w = E(wa(WA_INFO))
    return f'''<header class="nav"><div class="wrap">
<a class="brand" href="/" aria-label="Zenia, home">{MARK}<span>Zenia</span></a>
<nav class="nav-links" aria-label="Main">{li}</nav>
<div class="nav-cta"><a class="nav-wa" href="{w}" target="_blank" rel="noopener">WhatsApp</a><a class="btn btn-white" href="#demo">Get your demo</a></div>
<details class="menu"><summary aria-label="Open menu"><span></span></summary>
<div class="menu-panel">{li}<a href="{w}" target="_blank" rel="noopener">Message us on WhatsApp</a><a class="btn btn-white" href="#demo">Get your demo</a></div></details>
</div></header>
'''


def phone(kind, nombre='', inicial=''):
    return f'''<div class="phone" data-chat="{kind}">
<div class="phone-status" aria-hidden="true"><span>9:41</span><span><svg viewBox="0 0 16 12"><path fill="currentColor" d="M0 9h2v3H0zM4 6h2v6H4zM8 3h2v9H8zM12 0h2v12h-2z"/></svg><svg viewBox="0 0 24 12"><rect x=".5" y=".5" width="20" height="11" rx="2.5" fill="none" stroke="currentColor"/><rect x="2" y="2" width="16" height="8" rx="1.5" fill="currentColor"/></svg></span></div>
<div class="chat"><div class="chat-head"><span class="chat-avatar" aria-hidden="true">{E(inicial)}</span><div class="chat-who"><strong>{E(nombre)}</strong><span class="chat-status">online</span></div></div>
<div class="chat-body" aria-live="polite"><div class="chat-day">Today</div></div>
{'<div class="chips" role="group" aria-label="Example questions"></div>' if kind == 'live' else ''}
<div class="chat-input" aria-hidden="true"><span>Message</span><i></i></div></div></div>'''


def hero():
    seg = '<div class="seg" role="group" aria-label="Try it as a customer of">' + ''.join(
        f'<button type="button" data-k="{k}" aria-pressed="false">{E(SECTOR_EN[k])}</button>' for k in NEGOCIOS) + '</div>'
    integ = ''.join(f'<span><i>{s}</i>{E(n)}</span>' for n, s in INTEG[:3])
    n = NEGOCIOS['clinica']['nombre']
    return f'''<section class="hero"><div class="hero-bg" style="background-image:url(/assets/images/hero-madrid.webp)"></div><div class="hero-glow"></div><div class="wrap">
<div><span class="label">AI agents for WhatsApp</span>
<h1>Your WhatsApp answers, books and <span class="hl">sells 24/7</span></h1>
<p class="lead">Zenia puts an AI agent on your business WhatsApp. It replies in seconds with your information, books into your calendar and logs every conversation in your CRM. Whatever needs a person, it hands over to you.</p>
<div class="btns"><a class="btn btn-white" href="#demo">Get your free demo</a><a class="btn btn-ghost" href="#how-it-works">{PLAY}See how it works</a></div>
<p class="check">Your demo with your business information in 48 h · No commitment</p>
<div class="trust"><small>Works with</small><div class="trust-row">{integ}</div></div></div>
<div class="hero-phone">{seg}{phone('live', n, n[0])}<p class="seg-note">Tap a question like a customer would. Example business.</p></div>
</div></section>
'''


def logos():
    t = [('Global Watch Buyers', '/cases/img/gwb-emblem.png', 'Luxury Watch Buyers · 33 countries', '/cases/global-watch-buyers-ai-acquisition.html'),
         ('Croian & Hein', '/cases/img/croian-mark.svg', 'Rare wines · Switzerland', '/cases/croian-hein-private-cellar-switzerland.html'),
         ('Migrafácil', '/cases/img/migrafacil-mark.png', 'Work and study in Europe', None),
         ('Throwin’ Salt Co.', '/cases/img/ts-mark.png', 'Luxury Timepieces · USA', '/cases/throwin-salt-gaia-ebay-whatsapp.html'),
         ('Cicero', '/cases/img/cicero-mark.svg', 'Public affairs with AI', '/cases/cicero-public-affairs-spain-italy.html')]
    tiles = ''
    for n, src, d, u in t:
        dentro = f'<img src="{src}" alt="" loading="lazy"><span>{E(n)}<em>{E(d)}</em></span>'
        tiles += f'<a class="logo-tile" href="{u}">{dentro}</a>' if u else f'<div class="logo-tile">{dentro}</div>'
    return f'<section class="logos"><div class="wrap"><small>Businesses already working with Zenia</small><div class="logo-row">{tiles}</div></div></section>\n'


def cards_producto():
    return '''<section class="band"><div class="wrap">
<div class="head"><span class="label">Agent + calendar + CRM</span>
<h2>Sell where your customers already message you. <span class="muted">On WhatsApp, with your calendar and CRM up to date.</span></h2></div>
<div class="cards3">
<div class="card"><div class="mini" aria-hidden="true"><div class="b in">Hi, how much is teeth whitening?</div><div class="b out">Hi! It depends on the type: let me explain both options and what each includes.</div><div class="b in">Do you have anything on Saturday?</div><div class="b out">Yes, at 11:00 am or 12:30 pm. Which one works?</div></div>
<span class="label">WhatsApp + AI</span><h3>Your agent replies in seconds</h3><p>With your information and your tone, nights and weekends too.</p></div>
<div class="card"><div class="mini" aria-hidden="true"><div class="slot"><span><b>Thu 5:00 pm</b> · Cleaning</span><span class="state cita">Booked by the agent</span></div><div class="slot"><span><b>Thu 6:30 pm</b> · Check-up</span><span class="state ok">Confirmed</span></div><div class="slot on"><span><b>Fri 10:00 am</b> · Free</span><span class="muted">Offered</span></div><div class="slot"><span><b>Fri 12:00 pm</b> · Braces</span><span class="state ok">Confirmed</span></div></div>
<span class="label">Calendar</span><h3>Books into your calendar</h3><p>Offers only free slots, confirms and reminds the day before.</p></div>
<div class="card"><div class="mini" aria-hidden="true"><table><tr><td>Laura G.</td><td>Thursday visit</td><td><span class="state cita">Booked</span></td></tr><tr><td>Mark R.</td><td>Braces price</td><td><span class="state ok">Answered</span></td></tr><tr><td>Anna P.</td><td>Toothache</td><td><span class="state esc">To your team</span></td></tr><tr><td>Peter L.</td><td>Reschedule</td><td><span class="state cita">Booked</span></td></tr></table></div>
<span class="label">Custom CRM</span><h3>Every conversation, logged</h3><p>Who wrote, what they wanted and how it ended, no typing.</p></div>
</div></div></section>
'''


def soluciones():
    out = ''
    for k, (t, p, lis, q, a, go) in NICHOS.items():
        out += f'''<a class="niche" href="#demo"><div class="niche-top"><span class="niche-ico">{ICO[k]}</span><h3>{E(t)}</h3><p>{E(p)}</p>
<ul>{''.join(f'<li>{E(x)}</li>' for x in lis)}</ul></div>
<div class="niche-a" aria-hidden="true">{E(q)}</div><div class="niche-q" aria-hidden="true">{E(a)}</div>
<div class="niche-go">{E(go)} <span>→</span></div></a>'''
    return f'''<section class="band alt" id="solutions"><div class="wrap"><div class="head"><span class="label">Solutions by sector</span>
<h2>Built for businesses that live on WhatsApp</h2><p class="lead">Every sector asks different things. The agent arrives knowing yours.</p></div>
<div class="niches">{out}</div>
<p class="other">Another sector? Restaurants, real estate, gyms or law firms: <a href="{E(wa('Hi, I would like to know if Zenia fits my sector'))}" target="_blank" rel="noopener">message us and we will take a look</a>.</p></div></section>
'''


def como_funciona():
    pasos = ''.join(f'<li><div><b>{E(a)}</b><span>{E(b)}</span></div></li>' for a, b in GUION['pasos'])
    feed = ''.join(f'<li data-paso="{n}" hidden>{E(t)}</li>' for n, t in CRM_PASOS)
    return f'''<section class="band" id="how-it-works"><div class="wrap">
<div class="head"><span class="label">How it works</span><h2>A full booking, without touching your phone</h2>
<p class="lead">Watch a complete conversation: the agent answers, books, reminds and knows when to hand the chat to a person.</p></div>
<div class="how"><div><ol class="steps">{pasos}</ol>
<div class="crm-feed" aria-live="polite"><p><b>In your CRM</b><span class="crm-dot">live</span></p><ul>{feed}</ul></div>
<button class="replay" type="button">Play again</button></div>
{phone('auto', GUION['nombre'], 'C')}</div>
</div></section>
'''


def _app(k, idx):
    P = PANELES[k]
    pid = lambda t: f'p-en-{k}-{t}'
    ON = ' class="on"'
    side = (f'<span data-tab="{pid("conv")}" class="on">Conversations</span><span data-tab="{pid("agenda")}">{E(P["agenda"])}</span>'
            f'<span data-tab="{pid("fichas")}">{E(P["fichas"])}</span><span>Campaigns</span><span data-tab="{pid("agente")}">Agent</span>')
    convs = ''.join(f'<div{ON if i == 1 else ""}><b>{E(n)} <span class="state {c}">{E(s)}</span></b>{E(t)}</div>' for i, (n, c, s, t) in enumerate(P['convs']))
    hilo = ''.join(f'<div class="b {"in" if d == "in" else "out"}">{E(t)}</div>' for d, t in P['hilo'])
    kp = ''.join(f'<div class="kpi"><small>{E(a)}</small><strong>{E(b)}</strong></div>' for a, b in P['kpis'])

    def tabla(cols, rows):
        th = ''.join(f'<th>{E(c)}</th>' for c in cols)
        tr = ''
        for r in rows:
            celdas = ''
            for j, c in enumerate(r):
                if isinstance(c, tuple):
                    celdas += f'<td><span class="state {c[0]}">{E(c[1])}</span></td>'
                else:
                    celdas += f'<td>{"<b>" + E(c) + "</b>" if j == 0 else E(c)}</td>'
            tr += f'<tr>{celdas}</tr>'
        return f'<div class="tbl-wrap"><table class="tbl"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'
    tog = ''.join(f'<div class="toggle"><span><b>{E(a)}</b>{E(b)}</span><i class="sw{"" if on else " off"}"></i></div>' for a, b, on in P['toggles'])
    tabs = (f'<div class="tabs" role="tablist"><button role="tab" aria-selected="true" aria-controls="{pid("conv")}">Conversations</button>'
            f'<button role="tab" aria-selected="false" aria-controls="{pid("agenda")}">{E(P["agenda"])}</button>'
            f'<button role="tab" aria-selected="false" aria-controls="{pid("fichas")}">{E(P["fichas"])}</button>'
            f'<button role="tab" aria-selected="false" aria-controls="{pid("agente")}">Agent</button></div>')
    return f'''<div class="app-wrap" data-panel="{k}"{"" if idx == 0 else " hidden"}>{tabs}
<div class="app"><div class="app-bar"><i></i><i></i><i></i><span>CRM for {E(P["barra"])} · built by Zenia</span></div>
<div class="app-body"><div class="app-side"><b>{MARK}{E(P["marca"])}</b>{side}</div>
<div class="app-main">
<div class="app-panel" id="{pid("conv")}" role="tabpanel"><div class="convs"><div class="convs-list">{convs}</div><div class="thread">{hilo}<span class="tag">{E(P["tag"])}</span></div></div></div>
<div class="app-panel" id="{pid("agenda")}" role="tabpanel" hidden><div class="kpis">{kp}</div>{tabla(P["agenda_cols"], P["agenda_rows"])}</div>
<div class="app-panel" id="{pid("fichas")}" role="tabpanel" hidden>{tabla(P["fichas_cols"], P["fichas_rows"])}</div>
<div class="app-panel" id="{pid("agente")}" role="tabpanel" hidden><div class="toggles">{tog}</div></div>
</div></div></div></div>'''


def producto():
    seg = '<div class="seg seg-panel" role="group" aria-label="See the CRM for">' + ''.join(
        f'<button type="button" data-panel="{k}" aria-pressed="{"true" if i == 0 else "false"}">{E(SECTOR_EN[k])}</button>' for i, k in enumerate(PANELES)) + '</div>'
    apps = ''.join(_app(k, i) for i, k in enumerate(PANELES))
    return f'''<section class="band" id="product"><div class="wrap">
<div class="head center"><span class="label">Integrated, custom CRM</span><h2>Your CRM, built for your business and connected to your WhatsApp</h2>
<p class="lead">Every business gets its own CRM: with the fields, statuses and views of its sector, connected to its WhatsApp and calendar. Switch sector and see how it changes.</p></div>
{seg}{apps}
<div class="crm-points">
<div><b>Made to measure</b><span>Your fields (treatment, plate, package), your statuses and your views. Not a template.</span></div>
<div><b>Integrated</b><span>WhatsApp, calendar and your current software: every conversation, booking and alert flows in on its own.</span></div>
<div><b>Yours</b><span>Your team can step into any chat and see the full history, and the data belongs to your business.</span></div></div>
<p class="app-note">Panel with example data.</p>
</div></section>
'''


def cifras():
    return '''<section class="band alt"><div class="wrap">
<div class="head center"><h2>What changes from day one</h2></div>
<div class="stats">
<div class="stat"><small>Availability</small><strong>24/7</strong><span>your agent never closes, not even on holidays</span></div>
<div class="stat"><small>First reply</small><strong>&lt;1 min</strong><span>customers do not wait while you finish with someone else</span></div>
<div class="stat"><small>Your demo</small><strong>48 h</strong><span>to try it with your business information</span></div>
<div class="stat"><small>Real case</small><strong>831</strong><span>WhatsApp conversations handled for Global Watch Buyers</span></div>
</div></div></section>
'''


def casos():
    return '''<section class="band" id="cases"><div class="wrap">
<div class="head"><span class="label">Cases</span><h2>Already working for real businesses</h2></div>
<div class="cases">
<a class="case" href="/cases/global-watch-buyers-ai-acquisition.html"><div class="case-img" style="background-image:url(/cases/img/gwb-agente-poster.webp)" role="img" aria-label="The Global Watch Buyers agent answering on WhatsApp"></div>
<div class="case-txt"><span class="label">Global Watch Buyers</span><h3>Luxury watch sellers from 33 countries, handled on WhatsApp</h3>
<p>Pages in 13 languages, WhatsApp with qualification and an AI agent that answers, qualifies and books.</p>
<div class="case-nums"><div><b>831</b><span>conversations</span></div><div><b>33</b><span>countries</span></div><div><b>10 of 12</b><span>ad contacts with a premium watch</span></div></div>
<div class="case-go">Read the case →</div></div></a>
<a class="case" href="/cases/throwin-salt-gaia-ebay-whatsapp.html"><div class="case-img" style="background-image:url(/cases/img/ts-gaia-chat.webp)" role="img" aria-label="Gaia, the Throwin' Salt agent, on WhatsApp"></div>
<div class="case-txt"><span class="label">Throwin’ Salt Co.</span><h3>High-end watches listed on eBay from WhatsApp</h3>
<p>Gaia prepares each listing with title, photos and price, and publishes it when the team says “publish”.</p>
<div class="case-nums"><div><b>54</b><span>watches in 4 weeks</span></div><div><b>23</b><span>in a single day</span></div><div><b>$2M</b><span>of inventory on eBay</span></div></div>
<div class="case-go">Read the case →</div></div></a>
</div></div></section>
'''


def integraciones():
    ico = {n: s for n, s in INTEG}
    nodo = lambda n, s=None: f'<div class="hub-node"><i>{s or ico.get(n, "")}</i>{E(n)}</div>'
    cal = '<svg viewBox="0 0 24 24" fill="none" stroke="#006BFF" stroke-width="2.4"><circle cx="12" cy="12" r="8"/><path d="M15.5 9a4.5 4.5 0 1 0 0 6"/></svg>'
    return f'''<section class="band alt"><div class="wrap">
<div class="head center"><span class="label">Integrations</span><h2>Connects to what you already use</h2>
<p class="lead">No need to switch software: the agent works on top of your WhatsApp, your calendar and your CRM. If you use another tool, we will look at it.</p></div>
<div class="hub"><div class="hub-col">{nodo('WhatsApp Business API')}{nodo('Google Calendar')}{nodo('Calendly', cal)}</div><div><div class="hub-core">{MARK_SOLO}</div><p class="hub-cap">Zenia</p></div><div class="hub-col">{nodo('HubSpot')}{nodo('Zoho CRM')}{nodo('Odoo')}</div></div>
</div></section>
'''


def precio():
    return f'''<section class="band" id="pricing"><div class="wrap"><div class="price">
<div><span class="label">Custom pricing</span><h2>Every business is different. So is your price.</h2>
<p class="lead">We do not sell fixed plans. First we show you the demo with your business; then we send you a fixed proposal: what the agent does, what it connects to and the monthly cost.</p>
<div class="btns"><a class="btn btn-white" href="#demo">Get your demo</a><a class="btn btn-wa" href="{E(wa('Hi, I would like a Zenia proposal for my business'))}" target="_blank" rel="noopener">{WA_ICO}Message us on WhatsApp</a></div>
<p class="check">We reply within 24 hours · No commitment</p></div>
<ul><li><span><b>Based on your volume</b>You pay for what your business needs, not for a plan that does not fit.</span></li>
<li><span><b>Built with your information</b>Prices, hours and rules of your business, reviewed by you before going live.</span></li>
<li><span><b>Hands-on support</b>On WhatsApp, with someone who knows your case.</span></li></ul>
</div></div></section>
'''


def form_demo():
    opts = ''.join(f'<option value="{v}">{t}</option>' for v, t in [('Clínica', 'Clinic'), ('Taller', 'Auto shop'), ('Autoescuela', 'Driving school'), ('Otro', 'Other')])
    return f'''<section class="band alt" id="demo"><div class="wrap"><div class="demo-box">
<div><span class="label">Your demo in 48 h</span><h2>Try it with your business before deciding anything</h2>
<p class="lead">Leave us your website and contact. We set up the agent with your business's public information and send you a link to try it the way your customers would.</p>
<ol class="how-demo"><li><i>1</i><span><b>You send us your website</b>One minute, no calls.</span></li>
<li><i>2</i><span><b>We build your demo</b>With your services, hours and locations, public data only.</span></li>
<li><i>3</i><span><b>You try it on your phone</b>And if it fits, we spend 30 minutes on your real questions.</span></li></ol></div>
<form class="form" novalidate>
<div class="f" style="display:grid;gap:14px">
<label>Your business website<input name="web" type="text" inputmode="url" autocomplete="url" placeholder="www.yourbusiness.com" required></label>
<label>Your name<input name="nombre" type="text" autocomplete="given-name" placeholder="Name"></label>
<label>WhatsApp or email<input name="contacto" type="text" autocomplete="tel" placeholder="+1 555 000 0000" required></label>
<label>Sector<select name="sector">{opts}</select></label>
<button class="btn btn-white" type="submit">Get my demo</button>
<small>We only use this to send you the demo. See our <a href="/privacy/">privacy policy</a>.</small></div>
<div class="ok" role="status"><b>Received.</b> We will message you within 24 hours with your demo link. If you prefer, <a href="{E(wa('Hi, I just asked for my demo on the Zenia website'))}" target="_blank" rel="noopener">message us on WhatsApp</a>.</div>
</form></div></div></section>
'''


def faq():
    det = ''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in FAQ)
    ld = json.dumps({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ]}, ensure_ascii=False)
    return f'''<section class="band" id="faq"><div class="wrap">
<div class="head center"><span class="label">FAQ</span><h2>Frequently asked questions</h2>
<p class="lead">Anything else? <a href="{E(wa('Hi, I have a question about Zenia'))}" target="_blank" rel="noopener" style="color:var(--accent)">Message us on WhatsApp</a>.</p></div>
<div class="faq">{det}</div></div></section>
<script type="application/ld+json">{ld}</script>
'''


def final():
    return f'''<section class="wrap"><div class="final">
<h2>Shall we look at it with your business?</h2><p class="lead">We show you the demo with your information in 48 hours. No commitment.</p>
<div class="btns"><a class="btn btn-white" href="#demo">Get your demo</a><a class="btn btn-ghost" href="{CALENDLY}" target="_blank" rel="noopener">Book 30 minutes</a></div>
</div></section>
'''


def mas():
    DL = ' data-lang="es"'
    cols = ''.join(f'<div><b>{E(t)}</b><p>' + ' · '.join(f'<a href="{u}"{DL if u.startswith("/es/") else ""}>{E(n)}</a>' for u, n in ls) + '</p></div>' for t, ls in MAS)
    return f'<section class="band mas"><div class="wrap"><h2 class="mas-h">More from Zenia</h2><div class="mas-cols">{cols}</div></div></section>\n'


def footer():
    w = E(wa(WA_INFO))
    return f'''<footer><div class="wrap">
<div class="foot"><div><a class="brand" href="/">{MARK}<span>Zenia</span></a><p>AI agents for your business WhatsApp, with your calendar and a custom CRM.</p></div>
<div><b>Product</b><a href="#how-it-works">How it works</a><a href="#product">Custom CRM</a><a href="#pricing">Pricing</a><a href="#demo">Get your demo</a></div>
<div><b>Zenia</b><a href="/cases/">Cases</a><a href="/blog/">Blog</a><a href="/about.html">About</a><a href="/es/" data-lang="es">Español</a></div>
<div><b>Contact</b><a href="mailto:fabrizzio.zelada@zeniapartners.com">fabrizzio.zelada@zeniapartners.com</a><a href="{w}" target="_blank" rel="noopener">WhatsApp +34 677 612 799</a><a href="{CALENDLY}" target="_blank" rel="noopener">Book a call</a></div></div>
<div class="foot-bottom"><span>© 2026 Zenia Partners · Madrid</span><span><a href="/privacy/" style="text-decoration:none">Privacy</a> · <a href="/es/" data-lang="es" style="text-decoration:none">Español</a></span></div>
</div></footer>
<a class="wa-float" href="{w}" target="_blank" rel="noopener" aria-label="Message us on WhatsApp" data-directo>{WA_ICO}</a>
'''


def scripts():
    datos = {'negocios': NEGOCIOS, 'guion': GUION}
    js = json.dumps(datos, ensure_ascii=False).replace('</', '<\\/')
    return f'''<script type="application/json" id="z2-data">{js}</script>
<script src="/assets/z2/z2.js?v={V}" defer></script>
<script>document.addEventListener("click",function(e){{var t=e.target,a=t.closest?t.closest('a[href*="wa.me"]'):null;if(!a)return;try{{navigator.sendBeacon("https://gaia-relojes.onrender.com/gwb/lead",JSON.stringify({{site:"zenia",path:location.pathname+location.search,ref:document.referrer||""}}))}}catch(r){{}}}},true);</script>
<script src="/assets/qualify.js?v=4" defer></script>
<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{{"token": "{CF}"}}'></script>
</body>
</html>
'''


def pagina():
    return (head() + nav() + '<main id="main">' + hero() + logos() + cards_producto() + soluciones() + como_funciona()
            + producto() + cifras() + casos() + integraciones() + precio() + form_demo() + faq() + final() + mas()
            + '</main>' + footer() + scripts())


if __name__ == '__main__':
    destino = os.path.join(RAIZ, 'v2', 'index.html') if PREVIEW else os.path.join(RAIZ, 'index.html')
    B.escribir(destino, pagina())
