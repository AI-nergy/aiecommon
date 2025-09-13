import io, os
import random
import time
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from .file_system_base import FileSystemBase
from aiecommon import custom_logger
logger = custom_logger.get_logger()

class GoogleDrive(FileSystemBase):

    _FILESYSTEM_IDENTIFIER = "google_drive"
    _MIN_DOWNLOADED_FILE_SIZE = 80
    _DOWNLOAD_RETRY_DELAY = 3
    # TODO: move these to functions in FileSystemBase
#    CACHE_DIRECTORY = os.path(FileSystemBase.CONFIG_DATA_DIRECTORY, FILEYSTEM_IDENTIFIER)
#    STORAGE_DIRECTORY = os.path(FileSystemBase.CONFIG_STORAGE_DIRECTORY, FILEYSTEM_IDENTIFIER)


    def __init__(self):
        # get from API->Credentials page in console.cloud.googl.com
        self._API_KEY = os.environ["AINERGY_GOOGLE_DRIVE_API_KEY"]

        self.service = build("drive", "v3", developerKey=self._API_KEY)
        logger.info(f"GoogleDrive constructor")

    def download_google_drive_file(self, localFilePath:str, fileId:str):
        logger.info(f"GoogleDrive start download from drive: {localFilePath}.")

        try:
            request = self.service.files().get_media(fileId=fileId)

            fh = io.FileIO(localFilePath, "wb")
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                logger.info(f"GoogleDrive downloading from drive: localFilePath={localFilePath}, progress={int(status.progress() * 100)}%, size={os.path.getsize(localFilePath)}...")
            fh.close()
            logger.info(f"GoogleDrive download from drive DONE: localFilePath={localFilePath}, progress={int(status.progress() * 100)}%, size={os.path.getsize(localFilePath)}.")
        except Exception as e:
            try:
                os.unlink(localFilePath)
            except:
                pass
            logger.error(f"GoogleDrive download from drive FAILED: localFilePath={localFilePath}, error={e}")

    @staticmethod
    def is_downloaded_file_valid(localFilePath:str):
        if not os.path.exists(localFilePath):
            logger.info(f"GoogleDrive downloaded file doesn't exist, localFilePath={localFilePath}")
            return False
        size = os.path.getsize(localFilePath)
        if size < GoogleDrive._MIN_DOWNLOADED_FILE_SIZE:
            logger.info(f"GoogleDrive downloaded file is too small, localFilePath={localFilePath}, size={size}, _MIN_DOWNLOADED_FILE_SIZE={GoogleDrive._MIN_DOWNLOADED_FILE_SIZE}")
            return False
        return True
    
    def get_file(self, fileId:str, localFileName:str = None, usePermanentStorage:bool = False, force_download:bool = False):

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
            if not GoogleDrive.is_downloaded_file_valid(localFilePath):
                logger.info(f"GoogleDrive file is not valid, not getting from local path: localFilePath={localFilePath}, size={os.path.getsize(localFilePath)}")
            elif force_download:
                logger.info(f"GoogleDrive file is valid, but forceDownload is true, not getting from local path: localFilePath={localFilePath}, size={os.path.getsize(localFilePath)}")
            else:
                logger.info(f"GoogleDrive get from local cache (disk): {localFilePath}, size={os.path.getsize(localFilePath)}")
                return localFilePath
        
        self.download_google_drive_file(localFilePath, fileId)

        if not GoogleDrive.is_downloaded_file_valid(localFilePath):
            sleep_delay = GoogleDrive._DOWNLOAD_RETRY_DELAY + random.random()
            logger.info(f"GoogleDrive downloaded file is invalid, retry after sleep, localFilePath={localFilePath}, sleep_delay={sleep_delay}...")
            time.sleep(sleep_delay)
            self.download_google_drive_file(localFilePath, fileId)
        
        return localFilePath

    @classmethod
    def open_file(cls, fileId:str, localFileName:str = None, usePermanentStorage:bool = False):
        return super().open_file(fileId, "r", localFileName, usePermanentStorage)
