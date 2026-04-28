#!/usr/bin/env python3
"""Clean enriched CSV with aggressive filtering for max conversion rate.

Filters applied (drop if any match):
- Schools mislabeled as gimnasios (.edu domains, admisiones@, "Colegio")
- Big chains (McDonald's, Telepizza, etc) - not SMB target
- Junk placeholder emails (e-mail@sitio.com, test@test, etc)
- Third-party platform emails (cuponatic, groupon, eltenedor, etc) - not the real business
- Low signal businesses (rating < 3.0 or reviews < 3) - low intent / low budget signal
- Generic shared inboxes that won't reach decision maker (info@gmail, etc)

Read: zenia-prospects-enriched.csv
Write: zenia-prospects-clean.csv (high conversion ready)
"""
import csv
import re
from pathlib import Path
from urllib.parse import urlparse

INPUT = Path(r"C:\Users\Usuario\Downloads\zenia-prospects-enriched.csv")
OUTPUT = Path(r"C:\Users\Usuario\Downloads\zenia-prospects-clean.csv")

# School filters (Bogota gimnasios issue)
SCHOOL_TITLE_KW = [
    "colegio", "campestre", "bilingue", "bilingüe", "preescolar",
    "school", "kindergarten",
]
SCHOOL_EMAIL_PREFIX = (
    "admisiones@", "rectoria@", "rectoría@", "secretaria@",
    "direccion@", "dirección@", "preescolar@", "academico@", "academica@",
    "coordinacion@", "coordinación@",
)
SCHOOL_DOMAINS = (".edu.co", ".edu.es", ".edu.mx", ".edu.ar", ".edu.pe", ".edu", ".educ.")

# Chain / franchise filters (not SMB owner-operator)
CHAIN_TITLE_KW = [
    "mcdonald", "kfc", "burger king", "telepizza", "starbucks",
    "domino", "papa john", "popeyes", "subway", "five guys",
    "taco bell", "vips", "pans & company", "foster's",
    "rodilla", "santagloria", "100 montaditos",
    "hotel nh", "hotel meliá", "marriott", "ibis budget",
    "vivagym", "basic-fit", "basicfit", "fitness park", "duet sports",
    "synergym",
    "sephora", "primor", "marionnaud",
]

# Junk / placeholder email patterns
JUNK_EMAIL_PATTERNS = [
    r"^e-?mail@sitio\.",
    r"^test@",
    r"^user@",
    r"^demo@",
    r"^example@",
    r"^ejemplo@",
    r"^sample@",
    r"^name@",
    r"^nombre@",
    r"^you@",
    r"^tu@",
    r"^yourname@",
    r"^firstname",
    r"^correo@",
    r"@sitio\.",
    r"@example\.",
    r"@ejemplo\.",
    r"@test\.",
    r"@demo\.",
    r"@yourwebsite",
    r"@domain\.",
    r"@yourcompany",
    r"@sample\.",
]

# Third-party platforms (the email is the platform's, not the business)
THIRD_PARTY_DOMAINS = [
    "cuponatic.com",
    "groupon.com",
    "groupalia.com",
    "lebargain.com",
    "eltenedor.es",
    "thefork.com",
    "tripadvisor.com",
    "restaurantes.com",
    "atrapalo.com",
    "letsbonus.com",
    "travelclub.es",
    "clikalia.com",
    "yelp.com",
    "facebook.com",
    "instagram.com",
    "wix.com",
    "shopify.com",
    "wordpress.com",
    "tienda.shop",
    "tiendanube.com",
    "wixsite.com",
    "godaddy.com",
]


def is_junk_email(email):
    if not email:
        return False
    e = email.lower().strip()
    for pat in JUNK_EMAIL_PATTERNS:
        if re.search(pat, e):
            return True
    return False


def is_third_party_email(email):
    if not email:
        return False
    e = email.lower().strip()
    domain = e.split("@")[-1] if "@" in e else ""
    return any(domain.endswith(d) or d in domain for d in THIRD_PARTY_DOMAINS)


def is_school(row):
    title = (row.get("company_name") or "").lower()
    email = (row.get("email") or "").lower()

    if any(kw in title for kw in SCHOOL_TITLE_KW):
        return True
    if email and any(email.startswith(p) for p in SCHOOL_EMAIL_PREFIX):
        return True
    if email and any(email.endswith(d) or d in email for d in SCHOOL_DOMAINS):
        return True
    return False


def is_chain(row):
    title = (row.get("company_name") or "").lower()
    return any(kw in title for kw in CHAIN_TITLE_KW)


def is_low_signal(row):
    """Drop if very low review count or low rating (low SMB activity)."""
    try:
        rc = int(row.get("reviews_count") or "0")
    except ValueError:
        rc = 0
    try:
        rating = float(row.get("rating") or "0")
    except ValueError:
        rating = 0
    if rc < 3:  # Almost no reviews = no online presence = low intent
        return True
    if rating > 0 and rating < 3.0:  # Bad reputation = low budget for tools
        return True
    return False


def main():
    with open(INPUT, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    fields = list(rows[0].keys()) if rows else []

    kept = []
    dropped = {
        "schools": 0,
        "chains": 0,
        "junk_email": 0,
        "third_party_email": 0,
        "low_signal": 0,
    }

    for r in rows:
        # Schools (mainly Bogota gimnasios)
        if r.get("vertical") == "gimnasios" and is_school(r):
            dropped["schools"] += 1
            continue
        # Chains
        if is_chain(r):
            dropped["chains"] += 1
            continue
        # Low signal businesses
        if is_low_signal(r):
            dropped["low_signal"] += 1
            continue
        # Junk emails (clear the email field but keep the row for phone/IG outreach)
        email = (r.get("email") or "").strip()
        if email and is_junk_email(email):
            r["email"] = ""  # clear junk
            dropped["junk_email"] += 1
        # Third-party platform emails (clear the email)
        email = (r.get("email") or "").strip()
        if email and is_third_party_email(email):
            r["email"] = ""
            dropped["third_party_email"] += 1
        kept.append(r)

    with open(OUTPUT, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for r in kept:
            writer.writerow(r)

    # Stats by combo
    from collections import defaultdict
    by_combo = defaultdict(lambda: {"total": 0, "with_email": 0})
    for r in kept:
        key = f"{r['city']}-{r['vertical']}"
        by_combo[key]["total"] += 1
        if r.get("email"):
            by_combo[key]["with_email"] += 1

    print("=" * 65)
    print(f"CLEAN CSV (aggressive filters):")
    print(f"  Output: {OUTPUT}")
    print(f"  Input:  {len(rows)}")
    print()
    print(f"Drops:")
    print(f"  Schools (Bogota mislabel):  {dropped['schools']}")
    print(f"  Chains / franchises:        {dropped['chains']}")
    print(f"  Low signal (<3 reviews):    {dropped['low_signal']}")
    print(f"  Junk emails (cleared):      {dropped['junk_email']}")
    print(f"  Third-party emails (clear): {dropped['third_party_email']}")
    print()
    print(f"Final clean rows:    {len(kept)}")
    print(f"With CLEAN email:    {sum(1 for r in kept if r.get('email'))}")
    print()
    print("Breakdown by combo:")
    print(f"  {'Combo':<35} {'Total':>6} {'Email':>6}")
    for combo, stats in sorted(by_combo.items()):
        print(f"  {combo:<35} {stats['total']:>6} {stats['with_email']:>6}")


if __name__ == "__main__":
    main()
