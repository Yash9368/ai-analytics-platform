"""
GA4 Service Account Diagnostic Tool
====================================
Verifies the service account is authentic and can access GA4 correctly.

Run from the backend directory:
    python verify_ga4_access.py

This script performs 5 checks:
    1. JSON key file structure validation
    2. Service account authentication (get access token from Google)
    3. Service account existence check (IAM API)
    4. GA4 Data API enabled check
    5. GA4 property access test
"""

import json
import os
import sys
from pathlib import Path

# ─── Colors for terminal output ───
class C:
    GREEN  = "\033[92m"
    RED    = "\033[91m"
    YELLOW = "\033[93m"
    CYAN   = "\033[96m"
    BOLD   = "\033[1m"
    RESET  = "\033[0m"

def ok(msg):    print(f"  {C.GREEN}✅ PASS{C.RESET}  {msg}")
def fail(msg):  print(f"  {C.RED}❌ FAIL{C.RESET}  {msg}")
def warn(msg):  print(f"  {C.YELLOW}⚠️  WARN{C.RESET}  {msg}")
def info(msg):  print(f"  {C.CYAN}ℹ️  INFO{C.RESET}  {msg}")
def header(n, title):
    print(f"\n{C.BOLD}{'='*60}")
    print(f"  CHECK {n}: {title}")
    print(f"{'='*60}{C.RESET}")


# ──────────────────────────────────────────────────────────────
# CHECK 1: Validate JSON key file structure
# ──────────────────────────────────────────────────────────────
def check_1_json_structure():
    header(1, "JSON Key File Structure")

    cred_path = Path(__file__).parent / "credentials" / "ga4-service-account.json"

    if not cred_path.exists():
        fail(f"File not found: {cred_path}")
        return None

    ok(f"File exists: {cred_path}")
    info(f"File size: {cred_path.stat().st_size} bytes")

    try:
        with open(cred_path) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        fail(f"Invalid JSON: {e}")
        return None

    ok("Valid JSON format")

    # Check required fields
    required_fields = [
        "type", "project_id", "private_key_id", "private_key",
        "client_email", "client_id", "auth_uri", "token_uri",
        "auth_provider_x509_cert_url", "client_x509_cert_url"
    ]
    missing = [f for f in required_fields if f not in data]
    if missing:
        fail(f"Missing fields: {missing}")
        return None

    ok("All required fields present")

    # Verify type
    if data["type"] != "service_account":
        fail(f"Wrong type: '{data['type']}' (expected 'service_account')")
        warn("This might be an OAuth client credential, NOT a service account key.")
        warn("Go to: https://console.cloud.google.com/iam-admin/serviceaccounts")
        warn("Click your service account → Keys → Add Key → Create new key → JSON")
        return None

    ok(f"Type: {data['type']}")
    info(f"Project ID: {data['project_id']}")
    info(f"Client Email: {data['client_email']}")
    info(f"Client ID: {data['client_id']}")
    info(f"Private Key ID: {data['private_key_id'][:8]}...")

    # Verify private key format
    pk = data.get("private_key", "")
    if not (pk.startswith("-----BEGIN RSA PRIVATE KEY-----") or pk.startswith("-----BEGIN PRIVATE KEY-----")):
        fail("Private key has invalid format (doesn't start with RSA header)")
        return None

    ok("Private key format is valid (RSA)")

    return data


# ──────────────────────────────────────────────────────────────
# CHECK 2: Authenticate with Google (get access token)
# ──────────────────────────────────────────────────────────────
def check_2_authentication(cred_data):
    header(2, "Service Account Authentication")

    try:
        from google.oauth2 import service_account
        from google.auth.transport.requests import Request
    except ImportError:
        fail("google-auth not installed. Run: pip install google-auth")
        return None

    cred_path = Path(__file__).parent / "credentials" / "ga4-service-account.json"

    try:
        scopes = ["https://www.googleapis.com/auth/analytics.readonly"]
        credentials = service_account.Credentials.from_service_account_file(
            str(cred_path), scopes=scopes
        )
        ok("Credentials object created from JSON key")
    except Exception as e:
        fail(f"Failed to create credentials: {e}")
        return None

    # Try to get an access token
    try:
        credentials.refresh(Request())
        ok("Successfully obtained access token from Google!")
        info(f"Token expiry: {credentials.expiry}")
        info(f"Service account: {credentials.service_account_email}")
        return credentials
    except Exception as e:
        error_msg = str(e)
        fail(f"Authentication failed: {error_msg}")

        if "invalid_grant" in error_msg.lower():
            warn("The private key may have been revoked or the service account deleted.")
            warn("Go to: https://console.cloud.google.com/iam-admin/serviceaccounts")
            warn("Check if the service account still exists and create a new key if needed.")
        elif "disabled" in error_msg.lower():
            warn("The service account or project might be disabled.")
            warn("Check: https://console.cloud.google.com/iam-admin/serviceaccounts")

        return None


# ──────────────────────────────────────────────────────────────
# CHECK 3: Verify service account exists in Google Cloud
# ──────────────────────────────────────────────────────────────
def check_3_service_account_exists(credentials, cred_data):
    header(3, "Service Account Existence (IAM)")

    try:
        from google.auth.transport.requests import AuthorizedSession
    except ImportError:
        fail("google-auth not installed")
        return False

    project_id = cred_data["project_id"]
    email = cred_data["client_email"]

    session = AuthorizedSession(credentials)

    # Check if the service account exists via IAM API
    url = f"https://iam.googleapis.com/v1/projects/{project_id}/serviceAccounts/{email}"
    try:
        resp = session.get(url)
        if resp.status_code == 200:
            sa_info = resp.json()
            ok(f"Service account EXISTS in project '{project_id}'")
            info(f"Display name: {sa_info.get('displayName', '(none)')}")
            info(f"Unique ID: {sa_info.get('uniqueId', 'N/A')}")
            disabled = sa_info.get("disabled", False)
            if disabled:
                fail("Service account is DISABLED!")
                warn("Enable it at: https://console.cloud.google.com/iam-admin/serviceaccounts")
                return False
            else:
                ok("Service account is ENABLED")
            return True
        elif resp.status_code == 404:
            fail(f"Service account NOT FOUND in project '{project_id}'!")
            warn("The service account may have been deleted.")
            warn(f"Go to: https://console.cloud.google.com/iam-admin/serviceaccounts?project={project_id}")
            warn("Create a new service account and download a fresh JSON key.")
            return False
        elif resp.status_code == 403:
            warn(f"Cannot verify via IAM API (403 — insufficient permissions to query IAM)")
            info("This is non-critical. The service account may still work for GA4.")
            info("Moving on to GA4 access check...")
            return True  # non-fatal, continue
        else:
            warn(f"Unexpected IAM response: {resp.status_code} — {resp.text[:200]}")
            return True  # non-fatal, continue
    except Exception as e:
        warn(f"Could not reach IAM API: {e}")
        return True  # non-fatal


# ──────────────────────────────────────────────────────────────
# CHECK 4: GA4 Data API enabled check
# ──────────────────────────────────────────────────────────────
def check_4_api_enabled(credentials, cred_data):
    header(4, "Google Analytics Data API Enabled")

    try:
        from google.auth.transport.requests import AuthorizedSession
    except ImportError:
        fail("google-auth not installed")
        return False

    project_id = cred_data["project_id"]
    session = AuthorizedSession(credentials)

    # Check if the Analytics Data API is enabled
    url = (
        f"https://serviceusage.googleapis.com/v1/"
        f"projects/{project_id}/services/analyticsdata.googleapis.com"
    )
    try:
        resp = session.get(url)
        if resp.status_code == 200:
            state = resp.json().get("state", "UNKNOWN")
            if state == "ENABLED":
                ok("Google Analytics Data API is ENABLED ✅")
                return True
            else:
                fail(f"Google Analytics Data API state: {state}")
                warn(f"Enable it at: https://console.cloud.google.com/apis/library/analyticsdata.googleapis.com?project={project_id}")
                return False
        elif resp.status_code == 403:
            warn("Cannot check API status (403 — no permission to query Service Usage API)")
            info("This is non-critical. Will test directly in Check 5.")
            return True
        else:
            warn(f"Service Usage API response: {resp.status_code}")
            return True
    except Exception as e:
        warn(f"Could not check API status: {e}")
        return True


# ──────────────────────────────────────────────────────────────
# CHECK 5: GA4 Property Access
# ──────────────────────────────────────────────────────────────
def check_5_ga4_access(cred_data):
    header(5, "GA4 Property Access (Data API)")

    try:
        from google.analytics.data_v1beta import BetaAnalyticsDataClient
        from google.analytics.data_v1beta.types import (
            RunReportRequest, DateRange, Metric
        )
    except ImportError:
        fail("google-analytics-data not installed. Run: pip install google-analytics-data")
        return False

    cred_path = Path(__file__).parent / "credentials" / "ga4-service-account.json"

    # Load property ID from .env
    property_id = None
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                if line.strip().startswith("GA4_PROPERTY_ID"):
                    property_id = line.strip().split("=", 1)[1].strip()
                    break

    if not property_id:
        fail("GA4_PROPERTY_ID not found in .env file")
        warn("Add it to your .env: GA4_PROPERTY_ID=537962525")
        return False

    info(f"GA4 Property ID: {property_id}")
    info(f"Service Account: {cred_data['client_email']}")

    # Create client
    try:
        client = BetaAnalyticsDataClient.from_service_account_json(str(cred_path))
        ok("GA4 Data API client created")
    except Exception as e:
        fail(f"Failed to create GA4 client: {e}")
        return False

    # Run a minimal test query
    info("Running test query: activeUsers for last 7 days...")
    try:
        request = RunReportRequest(
            property=f"properties/{property_id}",
            date_ranges=[DateRange(start_date="7daysAgo", end_date="today")],
            metrics=[Metric(name="activeUsers")],
        )
        response = client.run_report(request)

        # Parse response
        if response.row_count is not None:
            value = "0"
            if response.rows:
                value = response.rows[0].metric_values[0].value
            ok(f"GA4 DATA RECEIVED! Active Users (7d): {value}")
            ok("Service account has FULL ACCESS to your GA4 property! 🎉")
            return True
        else:
            warn("Query returned but with no row_count — property may be empty")
            ok("Access is working (property just has no data yet)")
            return True

    except Exception as e:
        error_msg = str(e)
        fail(f"GA4 query failed: {error_msg[:300]}")

        if "403" in error_msg or "PERMISSION_DENIED" in error_msg.upper():
            print(f"\n{C.RED}{C.BOLD}{'─'*60}")
            print("  ROOT CAUSE: PERMISSION DENIED (403)")
            print(f"{'─'*60}{C.RESET}")
            print(f"""
  The service account is AUTHENTIC (it can authenticate with Google),
  but it does NOT have permission to read GA4 Property {property_id}.

  {C.BOLD}GA4 is rejecting the email because Google has changed how
  service accounts are added to GA4 properties.{C.RESET}

  {C.YELLOW}━━━ SOLUTION (Use Google Analytics Admin API instead) ━━━{C.RESET}

  {C.BOLD}Option A: Use the GA4 Admin UI with your PERSONAL email{C.RESET}
  
    The error "This email doesn't match a Google Account" happens
    because GA4's UI sometimes blocks service account emails.
    
    Try these workarounds:
    
    1. Open GA4 → Admin → Property Access Management
    2. Click "+" → "Add users"  
    3. Paste the EXACT email (copy from below, no extra spaces):
    
       {C.CYAN}{cred_data['client_email']}{C.RESET}
    
    4. If it still fails, try the Google Analytics Admin API method below.

  {C.BOLD}Option B: Add via Google Analytics Admin API (Python){C.RESET}
  
    Run this command (we'll create the script for you):
    
       python grant_ga4_access.py

  {C.BOLD}Option C: Use OAuth2 instead of Service Account{C.RESET}
  
    If neither works, we can switch to OAuth2 flow where YOU
    authenticate with your own Google account (no service account needed).
""")
        elif "NOT_FOUND" in error_msg.upper():
            warn(f"Property {property_id} was not found.")
            warn("Double-check the property ID in your GA4 Admin → Property Settings.")
        elif "API_DISABLED" in error_msg.upper() or "has not been used" in error_msg:
            warn("The Google Analytics Data API is not enabled for this project.")
            warn(f"Enable it at: https://console.cloud.google.com/apis/library/analyticsdata.googleapis.com?project={cred_data['project_id']}")

        return False


# ──────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────
def main():
    print(f"\n{C.BOLD}{C.CYAN}{'═'*60}")
    print("  🔍 GA4 Service Account Diagnostic Tool")
    print(f"{'═'*60}{C.RESET}")

    # Check 1
    cred_data = check_1_json_structure()
    if not cred_data:
        print(f"\n{C.RED}Stopped at Check 1. Fix the JSON file first.{C.RESET}\n")
        sys.exit(1)

    # Check 2
    credentials = check_2_authentication(cred_data)
    if not credentials:
        print(f"\n{C.RED}Stopped at Check 2. The service account cannot authenticate.{C.RESET}")
        print(f"The key may be revoked. Create a new key at:")
        print(f"  https://console.cloud.google.com/iam-admin/serviceaccounts?project={cred_data['project_id']}\n")
        sys.exit(1)

    # Check 3
    check_3_service_account_exists(credentials, cred_data)

    # Check 4
    check_4_api_enabled(credentials, cred_data)

    # Check 5
    success = check_5_ga4_access(cred_data)

    # Summary
    print(f"\n{C.BOLD}{'═'*60}")
    if success:
        print(f"  {C.GREEN}ALL CHECKS PASSED — GA4 is fully accessible! 🎉{C.RESET}")
    else:
        print(f"  {C.RED}GA4 ACCESS FAILED — See details above for the fix.{C.RESET}")
    print(f"{'═'*60}\n")

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
