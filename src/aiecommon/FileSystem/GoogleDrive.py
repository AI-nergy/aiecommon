import io, os, logging
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from .file_system_base import FileSystemBase

class GoogleDrive(FileSystemBase):
 
    FILESYSTEM_IDENTIFIER = "googledrive"
    # TODO: move these to functions in FileSystemBase
#    CACHE_DIRECTORY = os.path(FileSystemBase.CONFIG_DATA_DIRECTORY, FILEYSTEM_IDENTIFIER)
#    STORAGE_DIRECTORY = os.path(FileSystemBase.CONFIG_STORAGE_DIRECTORY, FILEYSTEM_IDENTIFIER)

    API_KEY = "AIzaSyBhOrmr3zbXxgPun535888qk9Bb0E7Ln5s"  # get from API->Credentials page in console.cloud.googl.com

    def __init__(self):

        self.service = build("drive", "v3", developerKey=GoogleDrive.API_KEY)
        logging.info(f"GoogleDrive constructor")

    def get_file(self, fileId, localFileName = None, usePermanentStorage = False):

        if self.service is None:
            return None

        if usePermanentStorage:
            download_directory = GoogleDrive.get_storage_directory()
        else:
            download_directory = GoogleDrive.get_cache_directory()

        if not os.path.exists(download_directory):
            os.makedirs(download_directory)
            
        #localFileName = fileId

        localFilePath = os.path.join(download_directory, localFileName)

        if os.path.exists(localFilePath):
            logging.info(f"GoogleDrive get from local cache (disk): {localFilePath}")
            return localFilePath
        
        request = self.service.files().get_media(fileId=fileId)

        fh = io.FileIO(localFilePath, "wb")
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            logging.info(f"GoogleDrive download from drive: {localFilePath} {int(status.progress() * 100)}%.")
        fh.close()
        
        return localFilePath
