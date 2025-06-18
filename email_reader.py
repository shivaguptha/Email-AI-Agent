from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import base64
from nlp import classify_intent

creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/gmail.modify'])

import re

def extract_email(from_string):
    # Pattern to extract email from string like: Name <email@domain.com>
    match = re.search(r'<([^>]+)>', from_string)
    if match:
        return match.group(1)
    return from_string  


def fetch_unread_emails():
    service = build('gmail', 'v1', credentials=creds)
    result = service.users().messages().list(userId='me', labelIds=['INBOX'], q='is:unread').execute()
    messages = result.get('messages', [])
    messages = messages[:10]

    email_data = []
    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        snippet = msg_data['snippet']
        payload = msg_data['payload']

        # Extract headers to get sender's email
        headers = payload.get('headers', [])
        from_email = None
        for header in headers:
            if header['name'].lower() == 'from':
                from_email = header['value']
                break

        # Extract body
        body = ''
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    body_data = part['body'].get('data', '')
                    if body_data:
                        body = base64.urlsafe_b64decode(body_data).decode('utf-8')
        else:
            body_data = payload['body'].get('data', '')
            if body_data:
                body = base64.urlsafe_b64decode(body_data).decode('utf-8')

        from_email=extract_email(from_email)
        if(from_email[:7]!="noreply"):

            email_data.append({
                'id': msg['id'],
                'snippet': snippet,
                'body': body,
                'from':  from_email
            })

    return email_data


# === Sample Usage ===
if __name__ == "__main__":

    emails = fetch_unread_emails()
    # for email in emails:
    #     print(f"From: {email['from']}")
    #     print(f"Body: {email['body'][:100]}...")  # Print first 100 chars of body
    #     print("-" * 40)
    intent, confidance=classify_intent(emails[0]['body'])
    print(intent, confidance)