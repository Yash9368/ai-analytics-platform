"""
OAuth2 Authentication Script for GA4
====================================
This script uses your client_secret.json to open a browser window
where you can log in with your Google Account. It will then save
a token.json file containing a refresh token so the backend can
access GA4 automatically.

Run this script:
    python auth_ga4_oauth.py
"""

import os
import sys
try:
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
except ImportError:
    print("Missing dependencies. Installing them now...")
    os.system(f"{sys.executable} -m pip install google-auth-oauthlib")
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials

# The scope for reading GA4 data
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']

def main():
    creds = None
    
    # Path to the client secrets file you will download
    client_secret_path = os.path.join(os.path.dirname(__file__), 'credentials', 'client_secret.json')
    token_path = os.path.join(os.path.dirname(__file__), 'credentials', 'token.json')

    if not os.path.exists(client_secret_path):
        print(f"\n❌ ERROR: Could not find {client_secret_path}")
        print("Please download your OAuth client ID JSON file, rename it to 'client_secret.json',")
        print("and place it in the backend/credentials/ folder.\n")
        sys.exit(1)

    print(f"\n🔍 Found client_secret.json. Checking for existing tokens...")
    
    # The file token.json stores the user's access and refresh tokens
    if os.path.exists(token_path):
        print("Found existing token.json, loading...")
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired token...")
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Failed to refresh token: {e}")
                creds = None

        if not creds:
            print("Opening browser for Google Login...")
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_path, SCOPES)
            creds = flow.run_local_server(port=0)
            
        # Save the credentials for the next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
            print(f"\n✅ SUCCESS! Generated token.json at:\n{token_path}")
            print("\nThe backend will now use this file to authenticate.")

if __name__ == '__main__':
    main()
