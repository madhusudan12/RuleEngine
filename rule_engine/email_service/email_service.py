
from rule_engine.email_service.email_connection import GMailConnection

import base64
from abc import ABC
from email import message_from_bytes

import chardet
from googleapiclient.errors import HttpError


class EmailService(ABC):
    def __init__(self):
        self._connection = None
        self._service = None

    def get_service(self):
        return self._service

    def fetch_emails(self, query=''):
        raise NotImplementedError

    def mark_as_read(self, email):
        pass

    def mark_as_un_read(self, email):
        pass

    def move_message(self, email, label_id):
        pass


class GmailService(EmailService):
    def __init__(self, credentials_file):
        super().__init__()
        self._connection = GMailConnection(credentials_file)
        self._service = self._connection.get_connection()

    def mark_as_read(self, email):
        try:
            self.get_service().users().messages().modify(
                userId='me', id=email.id, body={'removeLabelIds': ['UNREAD']}
            ).execute()
        except HttpError as error:
            print(f'An error occurred: {error}')

    def mark_as_un_read(self, email):
        try:
            self.get_service().users().messages().modify(
                userId='me', id=email.id, body={'addLabelIds': ['UNREAD']}
            ).execute()
        except HttpError as error:
            print(f'An error occurred: {error}')

    def move_message(self, email, label_id):
        try:
            self.get_service().users().messages().modify(
                userId='me', id=email.id, body={'addLabelIds': [label_id]}
            ).execute()
        except HttpError as error:
            print(f'An error occurred: {error}')

    def fetch_emails(self, max_results=100):
        try:
            results = self.get_service().users().messages().list(userId='me', q='', maxResults=max_results).execute()
            messages = results.get('messages', [])
            emails = []
            for msg in messages:
                msg_data = self.get_service().users().messages().get(userId='me', id=msg['id'], format='raw').execute()
                msg_str = base64.urlsafe_b64decode(msg_data['raw'].encode('ASCII'))
                mime_msg = message_from_bytes(msg_str)

                # Extract the message payload
                message = self.get_message_payload(mime_msg)

                email_data = {
                    'id': msg['id'],
                    'from': mime_msg['From'],
                    'to': mime_msg['To'],
                    'subject': mime_msg['Subject'],
                    'message': message,
                    'received_date': msg_data['internalDate']
                }
                emails.append(email_data)

            return emails
        except HttpError as error:
            print(f'An error occurred: {error}')
            return None

    def get_message_payload(self, mime_msg):
        if mime_msg.is_multipart():
            # Iterate over each part and find the text or html part
            for part in mime_msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if "attachment" not in content_disposition:
                    if content_type == "text/plain":
                        return self.decode_payload(part.get_payload(decode=True))  # Return the plain text message
                    elif content_type == "text/html":
                        return self.decode_payload(part.get_payload(decode=True))  # Optionally return the HTML message
        else:
            return self.decode_payload(mime_msg.get_payload(decode=True))  # If not multipart, return the message payload

        return ""  # If no suitable part is found, return an empty string

    def decode_payload(self, payload):
        # Detect encoding using chardet
        result = chardet.detect(payload)
        encoding = result['encoding']

        if encoding:
            try:
                return payload.decode(encoding, errors='replace')
            except Exception as e:
                print(f"Error decoding with detected encoding {encoding}: {e}")
                return payload.decode('utf-8', errors='replace')  # Fallback to utf-8 with error replacement
        else:
            # If encoding is None, fallback to utf-8 with error replacement
            return payload.decode('utf-8', errors='replace')
