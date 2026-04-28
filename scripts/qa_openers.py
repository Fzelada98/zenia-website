#!/usr/bin/env python3
"""QA review of generated openers + fill fallback for empty ones."""
import csv
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

INPUT = Path(r"C:\Users\Usuario\Downloads\zenia-prospects-FINAL.csv")

# Generic fallback per vertical (used when web scrape failed)
FALLBACK = {
    "restaurantes": "Veo que tienes presencia activa en {city}, una zona competitiva para hostelería. ¿Cómo gestionas las reservas y los no-shows por WhatsApp?",
    "gimnasios":    "En {city} la competencia entre gimnasios es brutal y la retención cae al 66%. ¿Cómo gestionas hoy el seguimiento de socios nuevos en sus primeros 30 días?",
    "estetica":     "El sector de estética en {city} mueve mucho volumen, pero captar nuevas clientas cuesta 5-7x más que retener. ¿Cómo trabajas la fidelización con tus clientas actuales?",
    "ecommerce":    "Las tiendas online en {city} pierden entre 70-78% de los carritos iniciados. ¿Cómo gestionas hoy la recuperación de carritos y el seguimiento post-venta?",
}

CLICHES = ["felicitaciones", "increíble trabajo", "vi en tu web", "te felicito"]


def main():
    with open(INPUT, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        fieldnames = list(rows[0].keys())

    no_opener_with_email = [r for r in rows if r.get("email") and not r.get("custom_opener")]
    print(f"Filling fallback for {len(no_opener_with_email)} prospects with email but no opener\n")

    filled = 0
    for r in rows:
        if not r.get("email") or r.get("custom_opener"):
            continue
        vertical = r.get("vertical", "")
        city = r.get("city", "")
        template = FALLBACK.get(vertical)
        if template:
            r["custom_opener"] = template.format(city=city)
            filled += 1

    cliche_hits = []
    for r in rows:
        opener = (r.get("custom_opener") or "").lower()
        for c in CLICHES:
            if c in opener:
                cliche_hits.append((r.get("company_name", ""), c, r.get("custom_opener", "")[:80]))

    with open(INPUT, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

    final = sum(1 for r in rows if r.get("email") and r.get("custom_opener"))
    print(f"Fallback filled: {filled}")
    print(f"Final prospects with email + opener: {final}/{sum(1 for r in rows if r.get('email'))}")
    print()

    if cliche_hits:
        print(f"WARNING: {len(cliche_hits)} openers with banned cliches:")
        for c, kw, text in cliche_hits[:10]:
            print(f"  [{kw}] {c}: {text}")
    else:
        print("No banned cliches detected.")

    print("\n=== SAMPLE 15 OPENERS BY VERTICAL ===")
    by_vertical = {}
    for r in rows:
        if r.get("custom_opener"):
            v = r.get("vertical", "?")
            by_vertical.setdefault(v, []).append(r)
    for v, lst in sorted(by_vertical.items()):
        print(f"\n--- {v.upper()} (showing 4 of {len(lst)}) ---")
        for r in lst[:4]:
            print(f"  [{r.get('company_name', '')[:35]}] ({r.get('city', '')})")
            print(f"     {r.get('custom_opener', '')}")


if __name__ == "__main__":
    main()
