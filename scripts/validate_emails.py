#!/usr/bin/env python3
"""Validate email deliverability via MX record lookup.

Filters out emails whose domain has no MX record (will bounce 100%).
Does NOT verify specific mailbox (no SMTP probe — too slow + risky).

Pipeline:
  1. Read enriched CSV
  2. For each unique email domain: DNS MX lookup
  3. Mark rows with bad MX as email='' (drops them from outreach)
  4. Overwrite CSV in place

Output: same enriched CSV with bad emails stripped.
"""
import csv
import socket
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

try:
    import dns.resolver
    USE_DNSPYTHON = True
except ImportError:
    USE_DNSPYTHON = False

INPUT = Path(r"C:\Users\Usuario\Downloads\zenia-prospects-enriched.csv")

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def has_mx_dnspython(domain):
    try:
        resolver = dns.resolver.Resolver()
        resolver.timeout = 4
        resolver.lifetime = 6
        answers = resolver.resolve(domain, "MX")
        return bool(list(answers))
    except Exception:
        try:
            answers = resolver.resolve(domain, "A")
            return bool(list(answers))
        except Exception:
            return False


def has_mx_socket(domain):
    """Fallback if dnspython not installed: just check domain resolves."""
    try:
        socket.gethostbyname(domain)
        return True
    except Exception:
        return False


def has_mx(domain):
    return has_mx_dnspython(domain) if USE_DNSPYTHON else has_mx_socket(domain)


def main():
    if not INPUT.exists():
        print(f"ERROR: {INPUT} not found.")
        sys.exit(1)

    with open(INPUT, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        fieldnames = list(rows[0].keys())

    emails = [(i, (r.get("email") or "").strip().lower()) for i, r in enumerate(rows)]
    domains_unique = sorted(set(e.split("@")[-1] for _, e in emails if "@" in e))

    print(f"Total rows: {len(rows)}")
    print(f"Rows with email: {sum(1 for _, e in emails if e)}")
    print(f"Unique domains to check: {len(domains_unique)}")
    print(f"Using {'dnspython' if USE_DNSPYTHON else 'socket fallback'}\n")

    domain_status = {}
    with ThreadPoolExecutor(max_workers=20) as ex:
        futures = {ex.submit(has_mx, d): d for d in domains_unique}
        done = 0
        for f in as_completed(futures):
            d = futures[f]
            ok = f.result()
            domain_status[d] = ok
            done += 1
            mark = "OK " if ok else "BAD"
            print(f"[{done}/{len(domains_unique)}] {mark} {d}", flush=True)

    bad = sum(1 for v in domain_status.values() if not v)
    print(f"\nBad domains: {bad}/{len(domains_unique)}")

    stripped = 0
    for r in rows:
        email = (r.get("email") or "").strip().lower()
        if "@" not in email:
            continue
        domain = email.split("@")[-1]
        if not domain_status.get(domain, True):
            r["email"] = ""
            stripped += 1

    with open(INPUT, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

    final_with_email = sum(1 for r in rows if r.get("email"))
    print(f"Stripped: {stripped} emails with bad MX")
    print(f"Final valid emails: {final_with_email}/{len(rows)} ({100*final_with_email//len(rows)}%)")


if __name__ == "__main__":
    main()
