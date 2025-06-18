from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import base64
from email.mime.text import MIMEText

creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/gmail.send'])

def send_email(email_data, message_text):
    service = build('gmail', 'v1', credentials=creds)

    # Build message
    message = MIMEText(message_text)
    message['to'] = email_data['from']  # You should extract this dynamically
    message['subject'] = 'Sent Through Automation'  # Optional: extract from original
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    message = {
        'raw': raw_message
    }

    service.users().messages().send(userId='me', body=message).execute()