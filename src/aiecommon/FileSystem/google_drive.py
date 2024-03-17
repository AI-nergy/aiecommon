import io, os
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from .file_system_base import FileSystemBase
from ..Logger import Logger

class GoogleDrive(FileSystemBase):

    _FILESYSTEM_IDENTIFIER = "google_drive"
    # TODO: move these to functions in FileSystemBase
#    CACHE_DIRECTORY = os.path(FileSystemBase.CONFIG_DATA_DIRECTORY, FILEYSTEM_IDENTIFIER)
#    STORAGE_DIRECTORY = os.path(FileSystemBase.CONFIG_STORAGE_DIRECTORY, FILEYSTEM_IDENTIFIER)


    def __init__(self):
        # get from API->Credentials page in console.cloud.googl.com
        self._API_KEY = os.environ["AINERGY_GOOGLE_DRIVE_API_KEY"]

        self.service = build("drive", "v3", developerKey=self._API_KEY)
        Logger.info(f"GoogleDrive constructor")

    def get_file(self, fileId:str, localFileName:str = None, usePermanentStorage:bool = False):

        if self.service is None:
            return None

        if usePermanentStorage:
            download_directory = GoogleDrive._get_storage_directory()
        else:
            download_directory = GoogleDrive._get_cache_directory()

        if not os.path.exists(download_directory):
            os.makedirs(download_directory)
            
        if localFileName is None:
            localFileName = fileId

        localFilePath = os.path.join(download_directory, localFileName)

        if os.path.exists(localFilePath):
            Logger.info(f"GoogleDrive get from local cache (disk): {localFilePath}")
            return localFilePath
        
        request = self.service.files().get_media(fileId=fileId)

        fh = io.FileIO(localFilePath, "wb")
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            Logger.info(f"GoogleDrive download from drive: {localFilePath} {int(status.progress() * 100)}%.")
        fh.close()
        
        return localFilePath

    @classmethod
    def open_file(cls, fileId:str, localFileName:str = None, usePermanentStorage:bool = False):
        return super().open_file(fileId, "r", localFileName, usePermanentStorage)
