from __future__ import print_function
import os.path
import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from googleapiclient.errors import HttpError

# OAuth 2.0 클라이언트 ID로 인증 설정
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'path/to/credentials.json'  # 다운로드한 인증 파일의 경로

credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Google Drive API 서비스 생성
service = build('drive', 'v3', credentials=credentials)

def upload_image(file_path, folder_id=None):
    try:
        file_metadata = {'name': os.path.basename(file_path)}
        if folder_id:
            file_metadata['parents'] = [folder_id]

        media = MediaFileUpload(file_path, mimetype='image/jpeg')  # 이미지 파일의 MIME 타입 설정
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f'파일이 업로드되었습니다. 파일 ID: {file.get("id")}')
        return file.get('id')
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

def create_shareable_link(file_id):
    try:
        # 파일을 공개적으로 공유하도록 권한 설정
        permission = {
            'type': 'anyone',
            'role': 'reader',
        }
        service.permissions().create(fileId=file_id, body=permission).execute()

        # 공유 가능한 링크 생성
        link = f'https://drive.google.com/uc?export=view&id={file_id}'
        print(f'공유 가능한 링크: {link}')
        return link
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

if __name__ == '__main__':
    image_path = 'path/to/your/image.jpg'  # 업로드할 이미지 파일의 경로
    folder_id = 'your_folder_id'  # 업로드할 Google Drive 폴더의 ID (선택 사항)

    file_id = upload_image(image_path, folder_id)
    if file_id:
        create_shareable_link(file_id)
