
import os
from abc import ABC, abstractmethod

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class MailConnection(ABC):
    def __init__(self, credentials_file):
        self._connection = self._create_connection(credentials_file)

    @abstractmethod
    def _create_connection(self, credentials_file):
        pass

    def get_connection(self):
        return self._connection


class GMailConnection(MailConnection):
    def __init__(self, credentials_file, token_path='token.pickle'):
        self.token_path = token_path
        self.creds = None
        super().__init__(credentials_file)

    def _create_connection(self, credentials_file):
        SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
        if os.path.exists(self.token_path):
            self.creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
                self.creds = flow.run_local_server(port=0)
                with open(self.token_path, 'w') as token:
                    token.write(self.creds.to_json())

        return build('gmail', 'v1', credentials=self.creds)
