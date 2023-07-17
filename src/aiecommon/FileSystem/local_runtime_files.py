import io, os, logging
from .file_system_base import FileSystemBase

class LocalRuntimeFiles(FileSystemBase):
 
    FILESYSTEM_IDENTIFIER = "localRuntimeFiles"

    def __init__(self):
            
        logging.info(f"LocalFile constructor")

    def get_file(self, filePath, usePermanentStorage = True):

        if usePermanentStorage:
            base_directory = LocalRuntimeFiles.get_storage_directory()
        else:
            base_directory = LocalRuntimeFiles.get_cache_directory()

        fullFilePath = os.path.join(base_directory, filePath)
        fullFileDir = os.path.dirname(fullFilePath)

        if not os.path.exists(fullFileDir):
            os.makedirs(fullFileDir, exist_ok = True)

        return fullFilePath
