#!/usr/bin/env python3
"""Filter top 15 Madrid gimnasios for SmartLead Week 1 launch (lunes 4 mayo).

Criteria:
- vertical = gimnasios
- city = Madrid
- email + opener present
- Email NOT broken (no %20, no obvious URL encoding)
- Email NOT shared with another vertical/city (cross-prospect spam risk)
- Dedupe: 1 prospect per unique email (keep highest reviews_count)
- Top 15 by reviews_count desc
"""
import csv
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

INPUT = Path(r"C:\Users\Usuario\Downloads\zenia-prospects-FINAL.csv")
OUTPUT = Path(r"C:\Users\Usuario\Downloads\zenia-MADRID-GYM-WEEK1.csv")

EMAIL_BAD_RE = re.compile(r"[%\s]|^\.|\.\.|@\.|@-")

# Emails to exclude (cross-city or generic chain hubs that fake-match Madrid)
EXCLUDE_EMAILS = {
    "boutique.barcelona@o2centrowellness.com",  # Barcelona inbox para Madrid biz
}


def safe_int(s):
    try:
        return int(str(s).replace(",", "").strip() or 0)
    except Exception:
        return 0


def main():
    with open(INPUT, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        fieldnames = list(rows[0].keys())

    # Filter Madrid gimnasios
    candidates = []
    for r in rows:
        if r.get("city") != "Madrid":
            continue
        if r.get("vertical") != "gimnasios":
            continue
        email = (r.get("email") or "").strip().lower()
        if not email or "@" not in email:
            continue
        if EMAIL_BAD_RE.search(email):
            continue
        if email in EXCLUDE_EMAILS:
            continue
        if not r.get("custom_opener"):
            continue
        candidates.append(r)

    print(f"Madrid gimnasios candidates: {len(candidates)}")

    # Dedupe by email: keep one with highest reviews
    by_email = {}
    for r in candidates:
        email = r["email"].lower().strip()
        if email not in by_email or safe_int(r.get("reviews_count")) > safe_int(by_email[email].get("reviews_count")):
            by_email[email] = r

    unique = sorted(by_email.values(), key=lambda r: safe_int(r.get("reviews_count")), reverse=True)
    print(f"Unique emails: {len(unique)}")

    # Take top 15
    top15 = unique[:15]

    # Write
    with open(OUTPUT, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(top15)

    print(f"\nSaved {len(top15)} prospects to:")
    print(f"  {OUTPUT}")
    print(f"\nList:")
    for i, r in enumerate(top15, 1):
        name = (r["company_name"] or "")[:45]
        print(f"  {i:2d}. {name:45} | {r['reviews_count']:>5} rev | {r['email']}")


if __name__ == "__main__":
    main()
