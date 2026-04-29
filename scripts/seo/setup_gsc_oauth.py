"""Interactive OAuth setup for Google Search Console API.

Run once, locally, by Fabrizzio. Generates token.json which is then committed
to GitHub Actions secrets (base64-encoded) as GSC_TOKEN_JSON.

Usage:
    python scripts/seo/setup_gsc_oauth.py
"""
from __future__ import annotations

import base64
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
TOKEN_PATH = REPO_ROOT / "backend" / "token.json"
SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]


PRINT_BANNER = """
================================================================
Zenia GSC OAuth Setup
================================================================

This script authenticates the SEO Operating System against Google
Search Console. You only run this once.

PREREQUISITES (do these in your browser first):

  1. Go to https://console.cloud.google.com/
  2. Create or select a project (e.g. "zenia-seo")
  3. Enable "Google Search Console API"
     -> APIs & Services > Library > search "Search Console"
  4. Configure OAuth consent screen:
     -> APIs & Services > OAuth consent screen
     -> User Type: External, Publishing status: Testing
     -> Add yourself as a test user (zeladauriartef@gmail.com)
  5. Create OAuth Client ID:
     -> APIs & Services > Credentials > Create Credentials
     -> OAuth client ID > Application type: Desktop app
     -> Name: "Zenia SEO Bot"
     -> Download the JSON file (client_secret_xxxx.json)

You'll need that downloaded JSON file path in a moment.

================================================================
"""


def main() -> int:
    print(PRINT_BANNER)

    try:
        from google_auth_oauthlib.flow import InstalledAppFlow  # type: ignore
        from googleapiclient.discovery import build  # type: ignore
    except ImportError:
        print("ERROR: google-auth-oauthlib not installed.")
        print("Run: pip install -r scripts/seo/requirements.txt")
        return 1

    # 1. Find client_secret.json
    default_paths = [
        REPO_ROOT / "backend" / "client_secret.json",
        Path.home() / "Downloads",
    ]
    print("Where is your downloaded client_secret JSON?")
    print(f"(Press Enter to use default: {default_paths[0]})")
    user_path = input("Path: ").strip()

    if not user_path:
        client_secret_path = default_paths[0]
    else:
        client_secret_path = Path(user_path).expanduser()

    if not client_secret_path.exists():
        # try to find in Downloads
        downloads = Path.home() / "Downloads"
        if downloads.exists():
            candidates = sorted(downloads.glob("client_secret*.json"))
            if candidates:
                print(f"Found in Downloads: {candidates[-1]}")
                client_secret_path = candidates[-1]

    if not client_secret_path.exists():
        print(f"ERROR: file not found: {client_secret_path}")
        print("Download client_secret.json from Google Cloud Console first.")
        return 1

    print(f"Using credentials: {client_secret_path}")

    # 2. Run OAuth flow
    print("\nLaunching browser for OAuth consent...")
    print("Sign in with the Google account that has access to zeniapartners.com")
    print("in Search Console (zeladauriartef@gmail.com).\n")

    flow = InstalledAppFlow.from_client_secrets_file(
        str(client_secret_path), scopes=SCOPES
    )
    creds = flow.run_local_server(port=0, prompt="consent")

    # 3. Save token.json
    token_data = {
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": creds.scopes,
    }
    TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)
    TOKEN_PATH.write_text(json.dumps(token_data, indent=2), encoding="utf-8")
    print(f"\nToken saved: {TOKEN_PATH}")

    # 4. Test query
    print("\nTesting GSC connection...")
    try:
        service = build("searchconsole", "v1", credentials=creds, cache_discovery=False)
        sites = service.sites().list().execute()
        site_entries = sites.get("siteEntry", [])
        print(f"Connection OK. Sites accessible: {len(site_entries)}")
        for site in site_entries:
            print(f"  - {site.get('siteUrl')} ({site.get('permissionLevel')})")

        target = "sc-domain:zeniapartners.com"
        if any(s.get("siteUrl") == target for s in site_entries):
            print(f"\nFound target site: {target}")
        else:
            print(
                f"\nWARNING: target site '{target}' not in list."
                " Make sure the Google account is added as user/owner in GSC."
            )
    except Exception as exc:
        print(f"GSC test query FAILED: {exc}")
        return 1

    # 5. Print base64 for GitHub Secrets
    token_b64 = base64.b64encode(TOKEN_PATH.read_bytes()).decode("ascii")
    creds_b64 = base64.b64encode(client_secret_path.read_bytes()).decode("ascii")

    print("\n================================================================")
    print("NEXT STEPS — paste these into GitHub Secrets")
    print("================================================================")
    print("Repo settings: https://github.com/zelada-uriarte/zenia-website/settings/secrets/actions\n")
    print("Secret name:  GSC_TOKEN_JSON")
    print("Secret value (copy the entire base64 string below):\n")
    print(token_b64)
    print("\n" + "-" * 64 + "\n")
    print("Secret name:  GSC_CREDENTIALS_JSON")
    print("Secret value:\n")
    print(creds_b64)
    print("\n================================================================")
    print("Done. After adding secrets, trigger workflow_dispatch on")
    print(".github/workflows/seo-agents.yml to verify end-to-end.")
    print("================================================================")
    return 0


if __name__ == "__main__":
    sys.exit(main())
