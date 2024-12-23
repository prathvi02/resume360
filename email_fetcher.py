from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def fetch_resumes():
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = build('gmail', 'v1', credentials=creds)

    results = service.users().messages().list(userId='me', q="has:attachment").execute()
    messages = results.get('messages', [])

    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        for part in msg['payload'].get('parts', []):
            if part['filename'] and part['mimeType'] == 'application/pdf':
                with open(part['filename'], 'wb') as f:
                    f.write(part['body'].get('data').encode())
                print(f"Downloaded: {part['filename']}")
