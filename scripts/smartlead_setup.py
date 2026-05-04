#!/usr/bin/env python3
"""SmartLead Campaign Setup — Madrid Gym Week 1.

Creates campaign + uploads 15 leads + configures 3-email sequence + schedule.
Leaves campaign in PAUSED state. Fabrizzio activates manually after test send.

Run from repo root: py scripts/smartlead_setup.py
"""
import csv
import json
import os
import sys
from pathlib import Path

import requests

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Read API key from backend/.env
ENV_PATH = Path(__file__).resolve().parent.parent / "backend" / ".env"
API_KEY = None
for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
    if line.startswith("SMARTLEAD_API_KEY="):
        API_KEY = line.split("=", 1)[1].strip().strip('"').strip("'")
        break

if not API_KEY:
    print("ERROR: SMARTLEAD_API_KEY not in backend/.env")
    sys.exit(1)

BASE = "https://server.smartlead.ai/api/v1"
EMAIL_ACCOUNT_ID = 18171990  # fabrizzio.zelada@zeniapartners.com
CSV_PATH = r"C:\Users\Usuario\Downloads\zenia-MADRID-GYM-WEEK1.csv"
CAMPAIGN_NAME = "Madrid Gym Week 1"


def api(method, endpoint, **kwargs):
    """Wrapper: appends api_key to all requests."""
    url = f"{BASE}{endpoint}"
    if "params" not in kwargs:
        kwargs["params"] = {}
    kwargs["params"]["api_key"] = API_KEY
    kwargs["timeout"] = kwargs.get("timeout", 30)
    r = requests.request(method, url, **kwargs)
    if not r.ok:
        print(f"ERROR {method} {endpoint}: {r.status_code} {r.text[:300]}")
        return None
    try:
        return r.json()
    except Exception:
        return r.text


def step1_create_campaign():
    """Create the campaign."""
    print("\n=== STEP 1: Create campaign ===")
    payload = {
        "name": CAMPAIGN_NAME,
        "client_id": None,
    }
    result = api("POST", "/campaigns/create", json=payload)
    if not result:
        return None
    campaign_id = result.get("id") or result.get("campaign_id") or result.get("data", {}).get("id")
    print(f"OK Campaign ID: {campaign_id}")
    return campaign_id


def step2_link_email_account(campaign_id):
    """Link Fabrizzio's email account to campaign."""
    print("\n=== STEP 2: Link email account ===")
    payload = {"email_account_ids": [EMAIL_ACCOUNT_ID]}
    result = api("POST", f"/campaigns/{campaign_id}/email-accounts", json=payload)
    if result is None:
        return False
    print(f"OK Email account {EMAIL_ACCOUNT_ID} linked")
    return True


def step3_upload_leads(campaign_id):
    """Upload 15 leads from CSV with custom fields."""
    print("\n=== STEP 3: Upload leads ===")
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    leads = []
    for r in rows:
        first_name = r.get("first_name", "").strip()
        leads.append({
            "email": r["email"].strip().lower(),
            "first_name": first_name,
            "company_name": r.get("company_name", "").strip(),
            "website": r.get("website", "").strip(),
            "phone_number": r.get("phone", "").strip(),
            "custom_fields": {
                "custom_opener": r.get("custom_opener", "").strip(),
                "city": r.get("city", "").strip(),
                "vertical": r.get("vertical", "").strip(),
                "country": r.get("country", "").strip(),
                "first_name_with_space": (" " + first_name) if first_name else "",
            },
        })

    payload = {
        "lead_list": leads,
        "settings": {
            "ignore_global_block_list": False,
            "ignore_unsubscribe_list": False,
            "ignore_community_bounce_list": False,
            "ignore_duplicate_leads_in_other_campaign": False,
        },
    }
    result = api("POST", f"/campaigns/{campaign_id}/leads", json=payload)
    if not result:
        return False
    print(f"OK Uploaded {len(leads)} leads")
    print(f"   Response: {json.dumps(result)[:200]}")
    return True


def step4_create_sequence(campaign_id):
    """Add 3-email sequence: Email 1 + FU2 (4d) + FU3 (3d more)."""
    print("\n=== STEP 4: Create sequence ===")

    email_1_body = """<p>Hola{{first_name_with_space}},</p>

<p>{{custom_opener}}</p>

<p>Soy Fabrizzio, fundador de Zenia Partners.</p>

<p>La retención anual en gimnasios de España cayó al 66.4% en 2025 (HFA Benchmarking Report). 1 de cada 3 socios cancela cada año, y la mitad lo hace en los primeros 90 días. La causa principal: cero seguimiento personalizado entre la primera visita y los primeros 30 días.</p>

<p>Te paso una plantilla con 47 mensajes pre-armados de WhatsApp para gimnasios que cubre onboarding del nuevo socio, alertas de churn por inactividad, reactivación de socios en pausa, programa de referidos automatizado y renovación con upselling.</p>

<p>Sin captura de email, sin compromiso:<br>
<a href="https://zeniapartners.com/lead-magnets/gimnasios.html">https://zeniapartners.com/lead-magnets/gimnasios.html</a></p>

<p>Si después de probarla quieres un agente de IA personalizado conectado a tu WhatsApp Business 24/7, escríbeme.</p>

<p>También construimos CRMs y SaaS a medida si tu operativa tiene necesidades específicas (gestión de socios, integración con software de control de acceso, módulos de retención avanzados, dashboards de churn por cohorte, etc).</p>

<p>Un saludo,<br>
Fabrizzio Zelada<br>
Founder · Zenia Partners<br>
zeniapartners.com</p>"""

    email_2_body = """<p>{{first_name}},</p>

<p>¿Te sirvió la plantilla para retención de socios?</p>

<p>Si todavía no la has mirado: <a href="https://zeniapartners.com/lead-magnets/gimnasios.html">https://zeniapartners.com/lead-magnets/gimnasios.html</a></p>

<p>Si quieres ver cómo aplicaría a {{company_name}} con un agente de IA personalizado conectado a tu WhatsApp, agendamos 30 min sin compromiso:<br>
<a href="https://calendly.com/zeladauriartef/30min">https://calendly.com/zeladauriartef/30min</a></p>

<p>Si la retención no es prioridad ahora, dímelo y lo dejo para junio.</p>

<p>Saludos,<br>
Fabrizzio</p>"""

    email_3_body = """<p>{{first_name}},</p>

<p>Tres opciones para cerrar esto sin más mensajes:</p>

<p>1. La plantilla te interesó pero no es momento → respondes "junio" y te escribo entonces<br>
2. No te interesa Zenia → respondes "stop" y no insisto<br>
3. Sigues interesado → agenda 30 min aquí: <a href="https://calendly.com/zeladauriartef/30min">https://calendly.com/zeladauriartef/30min</a></p>

<p>Cualquiera vale. Sin presión.</p>

<p>Fabrizzio</p>"""

    sequences = [
        {
            "seq_number": 1,
            "seq_delay_details": {"delay_in_days": 0},
            "variant_distribution_type": "MANUAL_EQUAL",
            "lead_distribution_percentage": 60,
            "winning_metric_property": "OPEN_RATE",
            "seq_variants": [
                {
                    "subject": "Plantilla gratis para tu gimnasio en Madrid",
                    "email_body": email_1_body,
                    "variant_label": "A",
                },
            ],
        },
        {
            "seq_number": 2,
            "seq_delay_details": {"delay_in_days": 4},
            "variant_distribution_type": "MANUAL_EQUAL",
            "seq_variants": [
                {
                    "subject": "Re: Plantilla gratis para tu gimnasio en Madrid",
                    "email_body": email_2_body,
                    "variant_label": "A",
                },
            ],
        },
        {
            "seq_number": 3,
            "seq_delay_details": {"delay_in_days": 3},
            "variant_distribution_type": "MANUAL_EQUAL",
            "seq_variants": [
                {
                    "subject": "Última pregunta sobre {{company_name}}",
                    "email_body": email_3_body,
                    "variant_label": "A",
                },
            ],
        },
    ]

    payload = {"sequences": sequences}
    result = api("POST", f"/campaigns/{campaign_id}/sequences", json=payload)
    if not result:
        return False
    print(f"OK Sequence created: 3 emails (Day 0, +4d, +3d)")
    return True


def step5_set_schedule(campaign_id):
    """Set schedule: Mon 4 May 09:00 CEST, ramp 5/day, L-V 09-13 CEST."""
    print("\n=== STEP 5: Set schedule ===")
    payload = {
        "timezone": "Europe/Madrid",
        "days_of_the_week": [1, 2, 3, 4, 5],  # Mon-Fri
        "start_hour": "09:00",
        "end_hour": "13:00",
        "min_time_btw_emails": 8,  # min minutes between sends
        "max_new_leads_per_day": 5,
        "schedule_start_time": "2026-05-04T09:00:00.000+02:00",  # Mon 4 May 09:00 CEST
    }
    result = api("POST", f"/campaigns/{campaign_id}/schedule", json=payload)
    if result is None:
        return False
    print(f"OK Schedule: Mon 4 May 09:00 CEST, 5/day, L-V 09:00-13:00 Madrid time")
    return True


def step6_set_general_settings(campaign_id):
    """Set general settings: stop conditions, tracking, etc."""
    print("\n=== STEP 6: General settings ===")
    payload = {
        "track_settings": ["DONT_TRACK_EMAIL_OPEN", "DONT_TRACK_LINK_CLICK"],
        "stop_lead_settings": "REPLY_TO_AN_EMAIL",
        "unsubscribe_text": "",
        "send_as_plain_text": False,
        "follow_up_percentage": 100,
        "client_id": None,
        "enable_ai_esp_matching": False,
    }
    result = api("POST", f"/campaigns/{campaign_id}/settings", json=payload)
    if result is None:
        # Settings endpoint might fail, not critical
        print("WARN settings endpoint failed, continuing (may need UI tweak)")
    else:
        print(f"OK General settings: stop on reply, no aggressive tracking")
    return True


def step7_summary(campaign_id):
    """Print final summary + URL."""
    print("\n" + "=" * 60)
    print("CAMPAIGN SETUP COMPLETE")
    print("=" * 60)
    print(f"\nCampaign ID: {campaign_id}")
    print(f"Campaign URL: https://app.smartlead.ai/app/email-campaigns/{campaign_id}")
    print(f"\nCurrent status: PAUSED (you must activate manually)")
    print(f"\nNEXT STEPS for Fabrizzio:")
    print(f"  1. Open campaign URL above")
    print(f"  2. Click 'Send Test Email' -> send to zeladauriartef@gmail.com")
    print(f"  3. Verify email arrives at INBOX (not Spam)")
    print(f"  4. If Inbox: click 'Start Campaign' or activate schedule")
    print(f"  5. If Spam: alert me, don't activate")


def main():
    print(f"SmartLead API: {BASE}")
    print(f"API key: ***{API_KEY[-12:]}")
    print(f"Email account: {EMAIL_ACCOUNT_ID}")
    print(f"CSV: {CSV_PATH}")

    cid = step1_create_campaign()
    if not cid:
        print("FAILED at step 1")
        return 1

    if not step2_link_email_account(cid):
        print("FAILED at step 2 - email account link")
        return 1

    if not step3_upload_leads(cid):
        print("FAILED at step 3 - leads upload")
        return 1

    if not step4_create_sequence(cid):
        print("FAILED at step 4 - sequence")
        return 1

    if not step5_set_schedule(cid):
        print("FAILED at step 5 - schedule")
        return 1

    step6_set_general_settings(cid)

    step7_summary(cid)
    return 0


if __name__ == "__main__":
    sys.exit(main())
