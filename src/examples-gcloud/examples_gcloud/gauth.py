import os
from enum import Enum
from logging import getLogger

from google.auth import default
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

logger = getLogger(__name__)

# use creds to create a client to interact with the Google Drive API.
__SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/gmail.compose",
]


class AuthAccount(Enum):
    user = 0
    service = 1
    unknown = 2

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def from_string(s: str) -> "AuthAccount":
        try:
            return AuthAccount[s]
        except KeyError:
            raise ValueError()


def __get_service_account_credentials():
    # --- use google.oauth2 with GCP service accound.
    credentials = service_account.Credentials.from_service_account_file("service_account.json")
    creds = credentials.with_scopes(__SCOPES)

    logger.debug(creds)
    return creds


def __get_user_account_credentials():
    # --- use google.oauth2 with user accound.
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", __SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", __SCOPES)
            creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

    return creds


def get_credentials(auth_type: AuthAccount | None) -> Credentials:
    match auth_type:
        case AuthAccount.user:
            creds = __get_user_account_credentials()

        case AuthAccount.service:
            creds = __get_service_account_credentials()

        case _:
            creds, _ = default()

    return creds
