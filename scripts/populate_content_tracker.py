#!/usr/bin/env python3
"""Populate blog/content-tracker.json with 90+ pending posts for May 2026
aggressive SEO push (3 posts/day target)."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRACKER = ROOT / "blog" / "content-tracker.json"


def to_slug(s):
    s = s.lower()
    s = re.sub(r"[áàä]", "a", s)
    s = re.sub(r"[éèë]", "e", s)
    s = re.sub(r"[íìï]", "i", s)
    s = re.sub(r"[óòö]", "o", s)
    s = re.sub(r"[úùü]", "u", s)
    s = re.sub(r"[ñ]", "n", s)
    s = re.sub(r"[^a-z0-9 -]", "", s)
    s = re.sub(r"\s+", "-", s).strip("-")
    return s


# ---------- Tier 1 remaining ----------
TIER_1 = [
    ("whatsapp business para restaurantes guia", "restaurantes"),
    ("crm peluqueria software gestion", "belleza"),
    ("marketing salon de unas redes sociales", "belleza"),
]

# ---------- Tier 2 (expansion) ----------
TIER_2 = [
    ("crm para tiendas retail", "retail"),
    ("recuperar carritos abandonados whatsapp", "ecommerce"),
    ("upselling automatico ecommerce ia", "ecommerce"),
    ("atencion al cliente ecommerce ia", "ecommerce"),
    ("automatizar postventa online", "ecommerce"),
    ("crm clinica dental", "clinicas"),
    ("gestion pacientes ia", "clinicas"),
    ("recordatorios citas medicas whatsapp", "clinicas"),
    ("crm centro wellness spa", "wellness"),
    ("crm para abogados gestion clientes", "abogados"),
    ("crm inmobiliarias leads", "inmobiliarias"),
    ("automatizacion academia formacion", "academias"),
]

# ---------- Tier 3 long-tail ----------
TIER_3 = [
    ("por que mis clientes no vuelven restaurante", "restaurantes"),
    ("como responder whatsapp rapido siendo autonomo", "general"),
    ("automatizar negocio pequeno sin programar", "general"),
    ("cuanto cuesta un crm para pymes", "general"),
    ("whatsapp business vs crm profesional diferencias", "general"),
    ("como digitalizar restaurante familiar", "restaurantes"),
    ("perder clientes por no contestar whatsapp", "general"),
    ("herramientas automatizacion pymes 2026", "general"),
    ("como elegir crm para pyme", "general"),
    ("crm vs hoja de calculo cuando migrar", "general"),
    ("integracion whatsapp business api espana", "general"),
    ("agente ia personalizado vs chatbot generico", "general"),
]

# ---------- New Tier 1 deepening (more specific) ----------
TIER_1_DEEP = [
    ("aumentar reservas restaurante 30 dias", "restaurantes"),
    ("reducir no-shows restaurante whatsapp", "restaurantes"),
    ("calcular roi crm restaurante", "restaurantes"),
    ("plantilla bienvenida nuevo socio gimnasio", "gimnasios"),
    ("alertas churn gimnasio detectar a tiempo", "gimnasios"),
    ("upselling tratamientos peluqueria", "belleza"),
    ("programa fidelizacion centro estetica puntos", "belleza"),
    ("gestion citas spa whatsapp automatico", "belleza"),
]

# ---------- Tier 4 City × Vertical (programmatic SEO) ----------
TIER_4_VERTICALS = ["restaurantes", "gimnasios", "belleza"]
TIER_4_CITIES = ["Madrid", "Barcelona", "Valencia", "Sevilla", "Malaga", "Bilbao",
                  "Lima", "Bogota", "CDMX", "Santiago"]
TIER_4_TEMPLATES = [
    "mejor crm para {vertical} en {city}",
    "automatizar whatsapp {vertical} {city}",
    "fidelizar clientes {vertical} {city}",
]


def all_keywords():
    out = []
    for kw, cluster in TIER_1:
        out.append({"keyword": kw, "cluster": cluster, "tier": 1})
    for kw, cluster in TIER_1_DEEP:
        out.append({"keyword": kw, "cluster": cluster, "tier": 1})
    for kw, cluster in TIER_2:
        out.append({"keyword": kw, "cluster": cluster, "tier": 2})
    for kw, cluster in TIER_3:
        out.append({"keyword": kw, "cluster": cluster, "tier": 3})

    # Tier 4: city x vertical (only 1 template per combo to avoid spam)
    for vertical in TIER_4_VERTICALS:
        for city in TIER_4_CITIES:
            kw = TIER_4_TEMPLATES[0].format(vertical=vertical, city=city.lower())
            out.append({"keyword": kw, "cluster": vertical, "tier": 4})
    return out


def main():
    with open(TRACKER, "r", encoding="utf-8") as f:
        data = json.load(f)

    existing_slugs = {p["slug"] for p in data["posts"]}
    existing_keywords = {p["keyword"].lower() for p in data["posts"]}

    new_posts = []
    for entry in all_keywords():
        kw = entry["keyword"]
        slug = to_slug(kw)
        if slug in existing_slugs or kw.lower() in existing_keywords:
            continue
        new_posts.append({
            "slug": slug,
            "keyword": kw,
            "tier": entry["tier"],
            "cluster": entry["cluster"],
            "status": "pending",
            "date": None
        })
        existing_slugs.add(slug)
        existing_keywords.add(kw.lower())

    # Sort: tier 1 first, then 2, 3, 4
    new_posts.sort(key=lambda p: (p["tier"], p["cluster"], p["slug"]))

    data["posts"].extend(new_posts)

    with open(TRACKER, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Added {len(new_posts)} pending posts.")
    print(f"\nTier breakdown of pending:")
    from collections import Counter
    tiers = Counter(p["tier"] for p in new_posts)
    for t in sorted(tiers.keys()):
        print(f"  Tier {t}: {tiers[t]}")
    print(f"\nTotal posts in tracker now: {len(data['posts'])}")
    print(f"  Published: {sum(1 for p in data['posts'] if p['status'] == 'published')}")
    print(f"  Pending: {sum(1 for p in data['posts'] if p['status'] == 'pending')}")


if __name__ == "__main__":
    main()
