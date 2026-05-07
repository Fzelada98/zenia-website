#!/usr/bin/env python3
"""Direct SMTP sender for Madrid Gym Week 1 (15 prospects).

Bypass SmartLead. Send Email 1 directly via Workspace SMTP.
Same DKIM/SPF/DMARC passing setup we verified with TEST 2.

Schedule: 5 emails/day, 1 every 30 min from 09:00-13:00 CEST.
Day 1 (today): first 5
Day 2: next 5
Day 3: last 5

Run from repo root: py scripts/smtp_sender_madrid_week1.py
"""
import csv
import json
import smtplib
import sys
import time
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate, make_msgid
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ---- CONFIG ----
SMTP_USER = "fabrizzio.zelada@zeniapartners.com"
SMTP_PASS = "fsgcqtoiwmjppjjl"  # Workspace App Password
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
FROM_NAME = "Fabrizzio Zelada"

CSV_PATH = Path(r"C:\Users\Usuario\Downloads\zenia-MADRID-GYM-WEEK1.csv")
LOG_PATH = Path(__file__).resolve().parent.parent / "reports" / "smtp" / "madrid-week1-sent.csv"
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

# ---- EMAIL TEMPLATE (Spain Spanish, vosotros, gym-specific) ----
SUBJECT_TEMPLATE = "{company_name}: una pregunta sobre vuestros primeros 90 días"

BODY_TEMPLATE = """<p>Hola equipo de {company_name},</p>

<p>{custom_opener}</p>

<p>Quería preguntaros algo concreto: ¿qué hacéis hoy entre la primera visita de un socio nuevo y los 30 días siguientes?</p>

<p>Lo pregunto porque ahí está la fuga real. La retención anual en gimnasios de España cayó al 66% (HFA Benchmarking 2025). 1 de cada 3 socios cancela al año. Y la mitad de esas bajas ocurren en los primeros 90 días. No por precio ni por competencia: por silencio.</p>

<p><strong>Lo que construimos en Zenia para gimnasios como el vuestro:</strong></p>

<p>Un agente de IA conectado a vuestro WhatsApp Business 24/7. No es un chatbot que repite frases hechas. Es un agente entrenado con vuestro catálogo de clases, vuestros profes, vuestros horarios y vuestro tono de marca, que:</p>

<ul>
<li>Acompaña al socio nuevo los primeros 14 días con 10 mensajes personalizados (primera clase, encuesta tras la 3ª visita, ayuda con la app, primera medición)</li>
<li>Detecta cuándo un socio lleva 7 días sin entrar y le escribe según su patrón histórico, no con un mensaje genérico</li>
<li>Reactiva a socios en pausa con una promo basada en el motivo real de su baja</li>
<li>Activa un programa de referidos automatizado que cierra el ciclo en WhatsApp</li>
</ul>

<p><strong>Resultado típico a 90 días:</strong> retención sube 8-15 puntos y el churn de los primeros 90 días se parte por la mitad.</p>

<p>Os dejo una plantilla con 47 mensajes WhatsApp pre-armados para gimnasios. Sin captura de email, sin compromiso, ni para apuntaros a nada. Es para que validéis la idea antes de plantearos cualquier siguiente paso:</p>

<p><a href="https://zeniapartners.com/lead-magnets/gimnasios.html">https://zeniapartners.com/lead-magnets/gimnasios.html</a></p>

<p>Si después de echarle un ojo veis que encaja, agendamos 30 min y lo aterrizamos a {company_name}:<br>
<a href="https://calendly.com/zeladauriartef/30min">https://calendly.com/zeladauriartef/30min</a></p>

<p>Un saludo,<br>
Fabrizzio Zelada<br>
Founder · Zenia Partners<br>
zeniapartners.com</p>
"""


def already_sent(email):
    """Check if email already sent (idempotency)."""
    if not LOG_PATH.exists():
        return False
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("email", "").lower() == email.lower():
                return True
    return False


def log_sent(email, company, status, error=""):
    """Append to send log."""
    write_header = not LOG_PATH.exists()
    with open(LOG_PATH, "a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["sent_at", "email", "company", "status", "error"])
        if write_header:
            w.writeheader()
        w.writerow({
            "sent_at": datetime.now().isoformat(),
            "email": email,
            "company": company,
            "status": status,
            "error": error,
        })


def send_one(server, prospect):
    """Send Email 1 to a single prospect."""
    company = prospect.get("company_name", "vuestro gimnasio").strip()
    opener = prospect.get("custom_opener", "").strip()
    to_email = prospect["email"].strip().lower()

    subject = SUBJECT_TEMPLATE.format(company_name=company)
    html_body = BODY_TEMPLATE.format(company_name=company, custom_opener=opener)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{FROM_NAME} <{SMTP_USER}>"
    msg["To"] = to_email
    msg["Reply-To"] = SMTP_USER
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain="zeniapartners.com")
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    server.sendmail(SMTP_USER, [to_email], msg.as_string())


def main():
    dry_run = "--dry-run" in sys.argv
    limit = 5  # 5 emails per run (per-day cap)

    if "--limit" in sys.argv:
        i = sys.argv.index("--limit")
        if i + 1 < len(sys.argv):
            limit = int(sys.argv[i + 1])

    with open(CSV_PATH, "r", encoding="utf-8") as f:
        prospects = list(csv.DictReader(f))

    print(f"Mode: {'DRY RUN' if dry_run else 'LIVE SEND'}")
    print(f"Total prospects: {len(prospects)}")
    print(f"Limit per run: {limit}")
    print()

    pending = [p for p in prospects if not already_sent(p["email"])]
    print(f"Already sent: {len(prospects) - len(pending)}")
    print(f"Pending: {len(pending)}")

    if not pending:
        print("All sent. Nothing to do.")
        return 0

    to_send = pending[:limit]
    print(f"\nSending {len(to_send)} now (with 60s gap between each)...\n")

    if dry_run:
        for p in to_send:
            print(f"  [DRY] {p['email']} | {p['company_name'][:40]}")
        print("\nNo emails sent. Use without --dry-run to send.")
        return 0

    sent_count = 0
    server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=30)
    try:
        server.login(SMTP_USER, SMTP_PASS)
        for i, p in enumerate(to_send, 1):
            email = p["email"].strip().lower()
            company = p.get("company_name", "")[:50]
            try:
                send_one(server, p)
                log_sent(email, company, "sent")
                sent_count += 1
                print(f"  [{i}/{len(to_send)}] OK -> {email} ({company[:35]})")
            except Exception as e:
                log_sent(email, company, "failed", str(e)[:200])
                print(f"  [{i}/{len(to_send)}] ERR -> {email}: {e}")
            if i < len(to_send):
                # Wait 60s between sends to look human + avoid rate limits
                print(f"      ... waiting 60s before next send ...")
                time.sleep(60)
    finally:
        server.quit()

    print(f"\nDone. Sent {sent_count}/{len(to_send)}.")
    print(f"Log: {LOG_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
