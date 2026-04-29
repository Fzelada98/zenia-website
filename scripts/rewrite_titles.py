#!/usr/bin/env python3
"""Rewrite truncated/buggy title tags + meta descriptions for top SEO URLs.

Each entry in REPLACEMENTS has:
  file: path relative to repo root
  old_title: regex pattern to find current <title>
  new_title: new title content (must be <60 chars to avoid Google truncation)
  old_desc: regex pattern for current meta description
  new_desc: new description (140-155 chars ideal)

Run from repo root: py scripts/rewrite_titles.py
"""
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

REPO = Path(__file__).resolve().parent.parent

REPLACEMENTS = [
    {
        "file": "index.html",
        "new_title": "Zenia: CRM con IA + WhatsApp para PyMEs en España y LATAM",
        "new_desc": "CRM con IA + automatización WhatsApp para restaurantes, gimnasios, estética y ecommerce. Setup en 2-3 semanas. Demo gratuita.",
    },
    {
        "file": "services/ai-agents.html",
        "new_title": "Custom AI Agents for Business · Setup in 2-3 Weeks | Zenia",
        "new_desc": "Custom AI agents that handle sales, customer support, and operations 24/7. Setup in 2-3 weeks. Built for SMBs in retail, fitness and hospitality.",
    },
    {
        "file": "services/ai-retail-ecommerce.html",
        "new_title": "AI Automation for Retail & Ecommerce Brands 2026 | Zenia",
        "new_desc": "AI automation for retail, ecommerce, fitness and beauty businesses. Automate sales, bookings, customer engagement and recovery flows. Free demo.",
    },
    {
        "file": "services/crm-omnichannel.html",
        "new_title": "Omnichannel CRM with AI for SMBs · WhatsApp Built-in | Zenia",
        "new_desc": "Unify WhatsApp, Instagram, email and web in one AI-powered CRM. Automate lead capture, follow-ups and customer journeys. Setup in 2-3 weeks.",
    },
    {
        "file": "blog/crm-beauty-salons-guide.html",
        "new_title": "CRM for Beauty Salons 2026: +35% Rebooking, -50% No-Shows",
        "new_desc": "CRM for beauty salons, hair salons and spas with AI. +35% rebooking rate, -50% no-shows, automated WhatsApp client communication. 2026 guide.",
    },
    {
        "file": "blog/crm-belleza-salon-estetica.html",
        "new_title": "CRM para Estética y Belleza 2026: Guía Completa | Zenia",
        "new_desc": "CRM para salones de belleza, peluquerías y estética con IA. +35% rebooking, -50% no-shows, WhatsApp automatizado. Guía completa 2026.",
    },
    {
        "file": "blog/crm-gimnasio-guia.html",
        "new_title": "CRM para Gimnasios 2026: Reduce Bajas 30% y Fideliza | Zenia",
        "new_desc": "Guía completa CRM para gimnasios 2026. Reduce bajas de socios 30%, automatiza seguimiento WhatsApp, fideliza con IA. Software de gestión gym.",
    },
    {
        "file": "blog/crm-gimnasios-fitness.html",
        "new_title": "CRM Gimnasios Fitness 2026: Retención con IA · Zenia",
        "new_desc": "CRM para gimnasios fitness 2026 con IA. Retén socios, automatiza onboarding, reactiva inactivos por WhatsApp. Demo gratuita 30 min.",
    },
    {
        "file": "blog/crm-peluqueria-software-gestion.html",
        "new_title": "CRM Peluquería 2026: Software de Gestión + WhatsApp | Zenia",
        "new_desc": "CRM peluquería 2026 con software de gestión integral: agenda, fichas, WhatsApp y fidelización. +29% ventas y ahorra 14h/semana. Demo gratis.",
    },
    {
        "file": "blog/crm-restaurantes-guia-completa.html",
        "new_title": "CRM para Restaurantes 2026: Reservas + Fidelización IA",
        "new_desc": "CRM para restaurantes con IA: automatiza reservas, fideliza por WhatsApp y aumenta ticket promedio +40%. Guía completa 2026.",
    },
    {
        "file": "blog/crm-restaurants-complete-guide.html",
        "new_title": "CRM for Restaurants 2026: Bookings + Retention with AI",
        "new_desc": "CRM for restaurants with AI: automate bookings, retain guests via WhatsApp, increase average ticket +40%. Complete 2026 guide.",
    },
    {
        "file": "blog/whatsapp-automation-business-guide.html",
        "new_title": "WhatsApp Automation for Business: 2026 Complete Guide",
        "new_desc": "How to automate WhatsApp Business in 2026: API setup, AI agents, lead qualification, ROI examples. Complete guide for SMBs.",
    },
    {
        "file": "blog/whatsapp-crm-pymes-guia.html",
        "new_title": "WhatsApp como CRM para PyMEs: Guía Completa 2026 | Zenia",
        "new_desc": "Guía completa WhatsApp como CRM 2026: organiza contactos, automatiza seguimientos, califica leads y cierra más ventas con IA.",
    },
    {
        "file": "blog/whatsapp-crm-small-business.html",
        "new_title": "WhatsApp as a CRM 2026: Convert Chats Into Sales | Zenia",
        "new_desc": "Use WhatsApp as a CRM in 2026: organize contacts, automate follow-ups, qualify leads and close more deals with AI. Complete guide.",
    },
    {
        "file": "blog/automatizacion-ecommerce-ia.html",
        "new_title": "Automatización Ecommerce 2026: 7 Procesos con IA | Zenia",
        "new_desc": "7 procesos de ecommerce que puedes automatizar con IA en 2026: carritos abandonados, email flows, pricing, soporte, post-venta. Guía práctica.",
    },
    {
        "file": "blog/automatizacion-ia-pymes.html",
        "new_title": "Automatización IA para PyMEs 2026: Guía Práctica | Zenia",
        "new_desc": "Guía práctica de automatización con IA para pymes 2026. Qué procesos automatizar, cuánto cuesta, cómo empezar. Casos reales.",
    },
    {
        "file": "blog/automatizacion-retail-tiendas-ia.html",
        "new_title": "Automatización IA Retail y Tiendas 2026: Guía | Zenia",
        "new_desc": "Automatización con IA para retail y tiendas: predicción de inventario, campañas WhatsApp, CRM omnicanal, retención de clientes 2026.",
    },
    {
        "file": "blog/agente-ia-ventas-ecommerce.html",
        "new_title": "Agentes IA para Ventas Ecommerce 2026: Guía Completa | Zenia",
        "new_desc": "Cómo usar agentes de IA para multiplicar ventas en ecommerce sin contratar: atención 24/7, recovery carritos, escalado online 2026.",
    },
]


TITLE_RE = re.compile(r"<title>.*?</title>", re.DOTALL)
DESC_RE = re.compile(r'<meta\s+name="description"\s+content="[^"]*"\s*/?>', re.IGNORECASE)


def main():
    total = 0
    failed = 0
    for entry in REPLACEMENTS:
        path = REPO / entry["file"]
        if not path.exists():
            print(f"SKIP (not found): {entry['file']}")
            failed += 1
            continue
        content = path.read_text(encoding="utf-8")
        new_content = content
        # Replace title
        new_title_tag = f"<title>{entry['new_title']}</title>"
        new_content, n_title = TITLE_RE.subn(new_title_tag, new_content, count=1)
        # Replace meta description
        new_desc_tag = f'<meta name="description" content="{entry["new_desc"]}">'
        new_content, n_desc = DESC_RE.subn(new_desc_tag, new_content, count=1)
        if n_title > 0 or n_desc > 0:
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(new_content)
            print(f"OK   [{n_title}t,{n_desc}d] {entry['file']} -> {entry['new_title'][:50]}")
            total += 1
        else:
            print(f"NOOP {entry['file']} (no title or meta found)")
            failed += 1

    print(f"\nDone. {total} files updated, {failed} skipped.")


if __name__ == "__main__":
    main()
