#!/usr/bin/env python3
"""Run all 9 Apify Google Maps scrapes in sequence for Zenia outreach.

Combos (hottest leads × diversified countries):
  1. Madrid Gimnasios (150)
  2. Madrid Estética (100)
  3. Madrid Ecommerce/luxury (100)
  4. Bogotá Gimnasios (150)
  5. Bogotá Estética (100)
  6. Lima Restaurantes (100)
  7. Barcelona Restaurantes (100)
  8. CDMX Estética (50)
  9. CDMX Ecommerce (50)

Total: 900 prospects, ~$4.50 of $4.75 free credit remaining.

USAGE:
  1. Get your Apify API token: https://console.apify.com/account/integrations
  2. Set env var: APIFY_TOKEN=apify_api_xxxxx
  3. Run: py scripts/apify_batch.py
  4. Wait ~2-3 hours for all 9 to complete.
  5. CSVs land in C:\\Users\\Usuario\\Downloads\\apify-batch\\
"""
import json
import os
import time
from pathlib import Path
import requests

API_TOKEN = os.environ.get("APIFY_TOKEN", "")
if not API_TOKEN:
    print("ERROR: Set APIFY_TOKEN env var first.")
    print("  Get token at: https://console.apify.com/account/integrations")
    print("  Then run: $env:APIFY_TOKEN='apify_api_xxx' (PowerShell)")
    print("  Or:       export APIFY_TOKEN='apify_api_xxx' (bash)")
    exit(1)

ACTOR_ID = "compass~google-maps-extractor"
OUT_DIR = Path(r"C:\Users\Usuario\Downloads\apify-batch")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# 9 combos
COMBOS = [
    # (slug, search_terms, location, language, max_places)
    ("madrid-gimnasios",     "gimnasios",          "Madrid, Spain",       "es", 150),
    ("madrid-estetica",      "centros de estetica", "Madrid, Spain",       "es", 100),
    ("madrid-ecommerce",     "tienda online ropa joyeria", "Madrid, Spain", "es", 100),
    ("bogota-gimnasios",     "gimnasios",          "Bogota, Colombia",    "es", 150),
    ("bogota-estetica",      "centros de estetica", "Bogota, Colombia",    "es", 100),
    ("lima-restaurantes",    "restaurantes",       "Lima, Peru",          "es", 100),
    ("barcelona-restaurantes","restaurantes",      "Barcelona, Spain",    "es", 100),
    ("cdmx-estetica",        "centros de estetica", "Ciudad de Mexico",    "es",  50),
    ("cdmx-ecommerce",       "tienda en linea",    "Ciudad de Mexico",    "es",  50),
]


def run_scrape(slug, search, location, lang, max_places):
    print(f"\n{'='*60}")
    print(f"[{slug}] Starting: {search} @ {location} (max {max_places})")
    print(f"{'='*60}")

    payload = {
        "searchStringsArray": [search],
        "locationQuery": location,
        "language": lang,
        "maxCrawledPlacesPerSearch": max_places,
        "skipClosedPlaces": True,
        "scrapeContacts": False,  # base scrape only, we enrich emails separately
    }

    # Start run
    start_url = f"https://api.apify.com/v2/acts/{ACTOR_ID}/runs?token={API_TOKEN}"
    r = requests.post(start_url, json=payload, timeout=30)
    if r.status_code not in (200, 201):
        print(f"  ERROR starting run: HTTP {r.status_code}: {r.text[:300]}")
        return None
    run_id = r.json()["data"]["id"]
    print(f"  Run started: {run_id}")

    # Poll until finished
    poll_url = f"https://api.apify.com/v2/actor-runs/{run_id}?token={API_TOKEN}"
    last_status = ""
    while True:
        time.sleep(15)
        r = requests.get(poll_url, timeout=30)
        data = r.json()["data"]
        status = data["status"]
        if status != last_status:
            print(f"  Status: {status}")
            last_status = status
        if status in ("SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"):
            break

    if status != "SUCCEEDED":
        print(f"  Run did not succeed (status={status}). Skipping.")
        return None

    # Download dataset as CSV
    dataset_id = data["defaultDatasetId"]
    csv_url = f"https://api.apify.com/v2/datasets/{dataset_id}/items?format=csv&clean=true&token={API_TOKEN}"
    r = requests.get(csv_url, timeout=120)
    out_path = OUT_DIR / f"{slug}.csv"
    with open(out_path, "wb") as f:
        f.write(r.content)
    print(f"  CSV saved: {out_path}")

    cost_used = data.get("usage", {}).get("ACTOR_COMPUTE_UNITS", 0)
    print(f"  Compute units consumed: {cost_used}")
    return out_path


def main():
    started = time.time()
    print(f"Starting Apify batch — 9 combos, ~900 prospects total")
    print(f"Estimated runtime: 2-3 hours\n")

    results = []
    for slug, search, location, lang, max_places in COMBOS:
        out = run_scrape(slug, search, location, lang, max_places)
        results.append((slug, out))

    elapsed = (time.time() - started) / 60
    print(f"\n{'='*60}")
    print(f"BATCH DONE in {elapsed:.1f} minutes")
    print(f"{'='*60}")
    print(f"\nResults:")
    for slug, path in results:
        status = "OK" if path else "FAILED"
        print(f"  {slug}: {status} {path or ''}")
    print(f"\nNext step: run scripts/merge_and_enrich.py to combine CSVs and extract emails.")


if __name__ == "__main__":
    main()
