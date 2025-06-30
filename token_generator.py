from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os
import json

# Broader scopes: read, send, modify emails
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.modify'
]

def regenerate_token():
    creds = None
    token_path = 'token.json'
    creds_path = 'credentials.json'  # Your OAuth client secrets from Google Cloud Console

    # Run OAuth flow
    flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
    creds = flow.run_local_server(port=0)

    # Save token as JSON (compatible with google.oauth2.credentials.Credentials.from_authorized_user_file)
    with open(token_path, 'w') as token:
        token.write(creds.to_json())

    print("✅ token.json regenerated successfully.")

if __name__ == '__main__':
    regenerate_token()
