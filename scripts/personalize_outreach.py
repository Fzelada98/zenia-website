#!/usr/bin/env python3
"""Generate a unique custom_opener per prospect using Claude Haiku.

Pipeline:
  1. Read enriched CSV (post-Apify + email scrape)
  2. For each prospect with email: scrape website snippets to feed context
  3. Call Claude Haiku to draft a 1-2 sentence opener referencing
     something specific about THAT prospect (not a generic template)
  4. Write final CSV with custom_opener column ready for SmartLead campaign

USAGE:
  Set ANTHROPIC_API_KEY env var, then:
  py scripts/personalize_outreach.py

Cost: ~$0.001/prospect with claude-haiku-4-5. ~$0.50 for 500 prospects.

Output: C:\\Users\\Usuario\\Downloads\\zenia-prospects-FINAL.csv (smartlead ready)
"""
import csv
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests

# Force stdout to UTF-8 with errors='replace' so emojis/special chars don't crash on Windows cp1252
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

INPUT = Path(r"C:\Users\Usuario\Downloads\zenia-prospects-enriched.csv")
OUTPUT = Path(r"C:\Users\Usuario\Downloads\zenia-prospects-FINAL.csv")

API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
if not API_KEY:
    print("ERROR: Set ANTHROPIC_API_KEY env var first.")
    print("  Get it from your Anthropic console.")
    print("  PowerShell: $env:ANTHROPIC_API_KEY = 'sk-ant-xxx'")
    sys.exit(1)

MODEL = "claude-haiku-4-5"
ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_HEADERS = {
    "x-api-key": API_KEY,
    "anthropic-version": "2023-06-01",
    "content-type": "application/json",
}

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
WEB_HEADERS = {"User-Agent": UA}


def fetch_snippet(website, max_chars=2000):
    """Fetch homepage and extract clean text snippet for context."""
    if not website:
        return ""
    try:
        if not website.startswith(("http://", "https://")):
            website = "https://" + website
        r = requests.get(website, headers=WEB_HEADERS, timeout=8, verify=False)
        if r.status_code != 200:
            return ""
        html = r.text
        # Strip scripts/styles
        html = re.sub(r"<script[^>]*>.*?</script>", " ", html, flags=re.DOTALL)
        html = re.sub(r"<style[^>]*>.*?</style>", " ", html, flags=re.DOTALL)
        # Strip tags
        text = re.sub(r"<[^>]+>", " ", html)
        text = re.sub(r"\s+", " ", text).strip()
        return text[:max_chars]
    except Exception:
        return ""


PROMPT_TEMPLATE = """Eres un experto en cold email B2B en español. Te paso datos de UN prospect específico:

- Nombre del negocio: {company}
- Vertical: {vertical}
- Ciudad: {city}
- País: {country}
- Reseñas Google: {rating}/5 con {reviews_count} reseñas
- Categoría: {category}
- Snippet de su web: {snippet}

Tu tarea: escribe UNA frase de apertura (máximo 30 palabras) específica de ESTE prospect que conecte algo concreto y observable de él (su volumen de reseñas, su categoría específica, algo de su web) con un pain point real de su vertical.

Reglas estrictas:
- TUTEAR (usar "tú": tienes, te paso, cuéntame, sabes)
- Tildes correctas (á é í ó ú ñ)
- NO clichés tipo "vi en tu web", "increíble trabajo", "felicitaciones por"
- NO em-dashes (usar comas o puntos)
- NO la palabra "chatbot"
- Tono cercano profesional, no zalamero, sin formalismo distante
- Si no hay info concreta del prospect, di algo específico de su vertical+ciudad

Responde SOLO con la frase de apertura, sin explicaciones, sin comillas."""


def call_claude(prompt, max_retries=3):
    body = {
        "model": MODEL,
        "max_tokens": 150,
        "messages": [{"role": "user", "content": prompt}],
    }
    for attempt in range(max_retries):
        try:
            r = requests.post(ANTHROPIC_URL, headers=ANTHROPIC_HEADERS,
                              json=body, timeout=30)
            if r.status_code == 200:
                data = r.json()
                return data["content"][0]["text"].strip()
            elif r.status_code == 429:
                time.sleep(2 ** attempt)
                continue
            else:
                return ""
        except Exception:
            time.sleep(1)
    return ""


def personalize_one(idx, row, total):
    company = row.get("company_name", "")
    if not row.get("email"):
        return idx, ""

    snippet = fetch_snippet(row.get("website", ""), max_chars=1500)
    prompt = PROMPT_TEMPLATE.format(
        company=company,
        vertical=row.get("vertical", ""),
        city=row.get("city", ""),
        country=row.get("country", ""),
        rating=row.get("rating", "n/a"),
        reviews_count=row.get("reviews_count", "n/a"),
        category=row.get("category", ""),
        snippet=snippet[:1200] if snippet else "(sin info de web)",
    )
    opener = call_claude(prompt)
    # ASCII-safe print: replace any non-encodable chars
    safe_company = company[:35].encode("ascii", "replace").decode("ascii")
    safe_opener = opener[:70].encode("ascii", "replace").decode("ascii")
    print(f"[{idx + 1}/{total}] {safe_company:35} | {safe_opener}", flush=True)
    return idx, opener


def main():
    requests.packages.urllib3.disable_warnings()

    if not INPUT.exists():
        print(f"ERROR: {INPUT} not found. Run merge_and_enrich.py first.")
        sys.exit(1)

    with open(INPUT, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    has_email = [r for r in rows if r.get("email")]
    print(f"Total prospects: {len(rows)}")
    print(f"With email (will personalize): {len(has_email)}")
    print(f"Estimated cost: ${len(has_email) * 0.001:.2f} USD\n")

    # Add custom_opener column
    for r in rows:
        r["custom_opener"] = ""

    to_process = [(i, r) for i, r in enumerate(rows) if r.get("email")]
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(personalize_one, i, r, len(to_process)): i
                    for i, r in to_process}
        for future in as_completed(futures):
            idx, opener = future.result()
            rows[idx]["custom_opener"] = opener

    # Write final CSV with all columns + custom_opener
    fieldnames = list(rows[0].keys()) if rows else []
    if "custom_opener" not in fieldnames:
        fieldnames.append("custom_opener")
    with open(OUTPUT, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

    with_opener = sum(1 for r in rows if r.get("custom_opener"))
    print()
    print("=" * 60)
    print(f"DONE. Output: {OUTPUT}")
    print(f"Total: {len(rows)}")
    print(f"With email: {len(has_email)}")
    print(f"With custom_opener generated: {with_opener}")
    print(f"\nReady to upload to SmartLead.")


if __name__ == "__main__":
    main()
