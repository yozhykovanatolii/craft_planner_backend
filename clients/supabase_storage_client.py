from datetime import datetime
from supabase import create_client
from config import settings

class SupabaseStorageClient:
    def __init__(self):
        self.__client = create_client(settings.supabase_project_url, settings.supabase_anon_key)
        
    def save_image(self, user_id: int, file: bytes, content_type: str, filename: str):
        extension = filename.split(".")[-1]
        file_name = f"{user_id}/{int(datetime.now().timestamp() * 1000)}.{extension}"
        self.__client.storage.from_('users').upload(file = file, path = file_name, file_options = {"content-type": content_type})
        return self.__client.storage.from_('users').get_public_url(file_name)