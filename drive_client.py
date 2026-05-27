import os
import io

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/drive']


class GoogleDriveClient:

    def __init__(self):

        self.service = self.authenticate()

    def authenticate(self):

        creds = None

        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file(
                "token.json",
                SCOPES
            )

        if not creds or not creds.valid:

            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())

            else:

                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json",
                    SCOPES
                )

                creds = flow.run_local_server(port=0)

            with open("token.json", "w") as token:
                token.write(creds.to_json())

        return build('drive', 'v3', credentials=creds)

    def search_file(self, filename, folder_id):

        query = (
            f"name='{filename}' and "
            f"'{folder_id}' in parents and "
            f"trashed=false"
        )

        response = self.service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name)'
        ).execute()

        files = response.get('files', [])

        return files[0] if files else None

    def upload_file(
        self,
        local_file,
        folder_id,
        overwrite=True
    ):

        filename = os.path.basename(local_file)

        existing = self.search_file(
            filename,
            folder_id
        )

        if existing:

            if overwrite:

                media = MediaFileUpload(local_file)

                updated = self.service.files().update(
                    fileId=existing['id'],
                    media_body=media
                ).execute()

                return updated

            else:
                raise Exception(
                    "File già esistente su Google Drive"
                )

        metadata = {
            'name': filename,
            'parents': [folder_id]
        }

        media = MediaFileUpload(local_file)

        uploaded = self.service.files().create(
            body=metadata,
            media_body=media,
            fields='id'
        ).execute()

        return uploaded