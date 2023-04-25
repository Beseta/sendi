from __future__ import print_function
import base64
import csv
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.message import EmailMessage

import mimetypes
import os
from email.message import EmailMessage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def gmail_send_message(service):
    with open('blogs2.csv') as blogs:
        reader = csv.DictReader(blogs)
        for row in reader:
            try:
                message = EmailMessage()

                message.set_content(
f"""
Hola, {row['NOMBRE']}!

Pon aqui el contenido de tu correo. Puedes usar enters y todo lo que quieras. 
Sugiero que no pongas acentos porque puede que no se envien bien.

Saludos,
Viana
""")

                # attachment
                attachment_filename = 'foto.png'
                # guessing the MIME type
                type_subtype, _ = mimetypes.guess_type(attachment_filename)
                maintype, subtype = type_subtype.split('/')

                with open(attachment_filename, 'rb') as fp:
                    attachment_data = fp.read()
                message.add_attachment(attachment_data, maintype, subtype)

                message['To'] = row['EMAIL']
                message['From'] = 'gduser2@workspacesamples.dev'
                message['Subject'] = 'ASUNTO DEL CORREO AQUI'
                encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

                create_message = {
                    'raw': encoded_message
                }
                send_message = (service.users().messages().send
                                (userId="me", body=create_message).execute())
                print(F'Message Id: {send_message["id"]}')
            except HttpError as error:
                print(F'An error occurred: {error}')
                send_message = None
    return send_message

def main():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('gmail', 'v1', credentials=creds)
        gmail_send_message(service)

    except HttpError as error:
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()