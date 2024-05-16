import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from requests import HTTPError
import os
from client_communication.email.email_template_builder import get_bot_ready_template

SCOPES = [
        "https://www.googleapis.com/auth/gmail.send"
    ]
PORT = int(os.environ.get('GMAIL_API_PORT'))


flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)

creds = flow.run_local_server(port=PORT)

service = build('gmail','v1',credentials=creds)

def send_email_with_template(receiver, subject, html_content):
    message = MIMEMultipart('alternative')
    message['to'] = receiver
    message['subject'] = subject

    decoration = MIMEText(html_content,'html')
    message.attach(decoration)
    send_mail(message)

def send_raw_email(receiver, subject, body=''):
    message = MIMEText(body)
    message['to'] = receiver
    message['subject'] = subject
    send_mail(message)

def send_mail(mail):
    create_message = {'raw': base64.urlsafe_b64encode(mail.as_bytes()).decode()}
    try:
        message = (
            service.users().messages().send(
                userId="me", body=create_message
            ).execute()
        )
        print("EMAIL SENT")
    except HTTPError as error:
        print(f"Error occured sending mail {error}")
