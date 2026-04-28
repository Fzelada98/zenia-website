#!/usr/bin/env python3
"""Merge the 9 Apify CSVs and enrich with email addresses scraped from websites.

Pipeline:
  1. Read all CSVs in C:\\Users\\Usuario\\Downloads\\apify-batch\\
  2. Tag each row with source combo (vertical, city, country)
  3. Deduplicate across combos (same business listed twice)
  4. For each row with website but no email: scrape homepage + contact pages
  5. Write final unified CSV ready for personalize_outreach.py

Output: C:\\Users\\Usuario\\Downloads\\zenia-prospects-enriched.csv
"""
import csv
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlparse

import requests

INPUT_DIR = Path(r"C:\Users\Usuario\Downloads\apify-batch")
OUTPUT = Path(r"C:\Users\Usuario\Downloads\zenia-prospects-enriched.csv")

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
HEADERS = {"User-Agent": UA, "Accept-Language": "es,en;q=0.8"}
TIMEOUT = 8

EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
JUNK_DOMAINS = {
    "example.com", "domain.com", "yourcompany.com", "wordpress.org",
    "wordpress.com", "wixsite.com", "godaddy.com", "sentry-next.wixpress.com",
    "sentry.io", "fonts.gstatic.com", "googleapis.com", "test.com",
}
CONTACT_PATHS = ["", "/contacto", "/contact", "/contact-us", "/contactenos",
                  "/sobre-nosotros", "/about", "/nosotros"]

# Map filename slug → (vertical, city, country)
COMBO_META = {
    "madrid-gimnasios":      ("gimnasios",   "Madrid",      "Espana"),
    "madrid-estetica":       ("estetica",    "Madrid",      "Espana"),
    "madrid-ecommerce":      ("ecommerce",   "Madrid",      "Espana"),
    "bogota-gimnasios":      ("gimnasios",   "Bogota",      "Colombia"),
    "bogota-estetica":       ("estetica",    "Bogota",      "Colombia"),
    "lima-restaurantes":     ("restaurantes","Lima",        "Peru"),
    "barcelona-restaurantes":("restaurantes","Barcelona",   "Espana"),
    "cdmx-estetica":         ("estetica",    "CDMX",        "Mexico"),
    "cdmx-ecommerce":        ("ecommerce",   "CDMX",        "Mexico"),
}


def is_junk_email(email):
    e = email.lower().strip()
    domain = e.split("@")[-1]
    if domain in JUNK_DOMAINS:
        return True
    if any(ext in e for ext in [".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif"]):
        return True
    if re.match(r"^(test|admin|user|demo|info)@(test|demo|example|domain|sample)", e):
        return True
    return False


def normalize_url(url):
    if not url:
        return None
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url


def fetch(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True, verify=False)
        if r.status_code == 200 and "text/html" in r.headers.get("Content-Type", ""):
            return r.text
    except Exception:
        return None
    return None


def extract_emails(html):
    if not html:
        return set()
    emails = set()
    for m in re.finditer(r'mailto:([^"\'?\s>&]+)', html, re.IGNORECASE):
        e = m.group(1).strip().lower()
        if "@" in e and not is_junk_email(e):
            emails.add(e)
    for m in EMAIL_RE.finditer(html):
        e = m.group(0).strip().lower()
        if not is_junk_email(e):
            emails.add(e)
    return emails


def scrape_email(website):
    base = normalize_url(website)
    if not base:
        return ""
    parsed = urlparse(base)
    base = f"{parsed.scheme}://{parsed.netloc}"
    base_domain = parsed.netloc.replace("www.", "")

    found = set()
    for path in CONTACT_PATHS[:4]:
        html = fetch(base + path)
        if html:
            found.update(extract_emails(html))
            if len(found) >= 3:
                break

    # Prefer emails from same domain as website
    same_domain = [e for e in found
                   if base_domain.split(".")[-2] in e.split("@")[-1]]
    if same_domain:
        return sorted(same_domain)[0]
    if found:
        return sorted(found)[0]
    return ""


def load_combo(slug):
    """Load a single CSV file and tag rows with combo metadata."""
    path = INPUT_DIR / f"{slug}.csv"
    if not path.exists():
        print(f"  WARN: {slug}.csv not found, skipping")
        return []
    vertical, city, country = COMBO_META[slug]
    with open(path, "r", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["__vertical"] = vertical
        r["__city"] = city
        r["__country"] = country
        r["__combo"] = slug
    return rows


def dedupe(all_rows):
    """Deduplicate by phone OR website (whichever exists)."""
    seen_phone = set()
    seen_web = set()
    unique = []
    for r in all_rows:
        phone = (r.get("phone") or "").strip()
        web = (r.get("website") or "").strip().lower().rstrip("/")
        key_phone = phone if phone else None
        key_web = web if web else None
        if key_phone and key_phone in seen_phone:
            continue
        if key_web and key_web in seen_web:
            continue
        if key_phone:
            seen_phone.add(key_phone)
        if key_web:
            seen_web.add(key_web)
        unique.append(r)
    return unique


def process_row(idx, row, total):
    title = (row.get("title") or "").strip()
    website = (row.get("website") or "").strip()
    if not website:
        return idx, ""
    try:
        email = scrape_email(website)
        status = "OK" if email else "no-email"
        # Use ASCII-safe printing
        print(f"[{idx + 1}/{total}] {title[:40]:40} | {status:9} | {email}", flush=True)
        return idx, email
    except Exception as e:
        return idx, ""


def main():
    requests.packages.urllib3.disable_warnings()

    print("Loading 9 Apify CSVs...")
    all_rows = []
    for slug in COMBO_META.keys():
        rows = load_combo(slug)
        print(f"  {slug}: {len(rows)} rows")
        all_rows.extend(rows)

    print(f"\nTotal raw rows: {len(all_rows)}")

    unique = dedupe(all_rows)
    print(f"After dedupe: {len(unique)}")

    # Enrich missing emails (concurrent scraping)
    to_scrape = [(i, r) for i, r in enumerate(unique) if not r.get("email") and r.get("website")]
    print(f"\nWebsites to scrape for emails: {len(to_scrape)}")

    if to_scrape:
        with ThreadPoolExecutor(max_workers=12) as executor:
            futures = {executor.submit(process_row, i, r, len(to_scrape)): i for i, r in to_scrape}
            for future in as_completed(futures):
                idx, email = future.result()
                unique[idx]["email"] = email

    # Write final CSV (SmartLead-friendly columns)
    out_columns = [
        "email", "first_name", "company_name", "vertical", "city", "country",
        "website", "phone", "category", "rating", "reviews_count", "google_url",
        "instagram_url",
    ]

    with open(OUTPUT, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=out_columns)
        writer.writeheader()
        for r in unique:
            writer.writerow({
                "email": (r.get("email") or "").strip().lower(),
                "first_name": "",  # filled later if owner name available
                "company_name": (r.get("title") or "").strip(),
                "vertical": r["__vertical"],
                "city": r["__city"],
                "country": r["__country"],
                "website": (r.get("website") or "").strip(),
                "phone": (r.get("phone") or "").strip(),
                "category": (r.get("categoryName") or "").strip(),
                "rating": (r.get("totalScore") or "").strip(),
                "reviews_count": (r.get("reviewsCount") or "").strip(),
                "google_url": (r.get("url") or "").strip(),
                "instagram_url": (r.get("instagrams") or "").split(",")[0].strip() if r.get("instagrams") else "",
            })

    with_email = sum(1 for r in unique if r.get("email"))
    print()
    print("=" * 60)
    print(f"DONE. Output saved to:\n  {OUTPUT}")
    print(f"\nStats:")
    print(f"  Total prospects: {len(unique)}")
    print(f"  With email: {with_email} ({100 * with_email // len(unique) if unique else 0}%)")
    print(f"\nBreakdown by combo:")
    from collections import Counter
    by_combo = Counter(r["__combo"] for r in unique)
    for combo, n in sorted(by_combo.items()):
        n_email = sum(1 for r in unique if r["__combo"] == combo and r.get("email"))
        print(f"  {combo}: {n} prospects, {n_email} with email")


if __name__ == "__main__":
    main()
