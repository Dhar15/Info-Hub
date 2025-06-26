#This is a script to obtain a refresh token for Gmail API using OAuth 2.0.
#Only needs to be run once to get the refresh token.
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from dotenv import load_dotenv

load_dotenv()

# OAuth 2.0 Scopes for Gmail read-only
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_refresh_token():
    flow = InstalledAppFlow.from_client_config(
        {
            "installed": {
                "client_id": os.getenv("GMAIL_CLIENT_ID"),
                "client_secret": os.getenv("GMAIL_CLIENT_SECRET"),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        },
        SCOPES
    )

    creds = flow.run_local_server(port=0)
    print(f"\nAccess Token: {creds.token}")
    print(f"Refresh Token: {creds.refresh_token}")
    print(f"Token Expiry: {creds.expiry}")
    print("\n✅ Paste the above refresh token into your .env file as GMAIL_REFRESH_TOKEN")

if __name__ == '__main__':
    get_refresh_token()
