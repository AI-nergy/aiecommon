import io, os, logging
from .file_system_base import FileSystemBase

class LocalRuntimeFiles(FileSystemBase):
 
    _FILESYSTEM_IDENTIFIER = "local_runtime_files"

    def __init__(self):
            
        logging.info(f"LocalFile constructor")

    def get_file(self, filePath, usePermanentStorage = False):

        if usePermanentStorage:
            base_directory = LocalRuntimeFiles._get_storage_directory()
        else:
            base_directory = LocalRuntimeFiles._get_cache_directory()

        fullFilePath = os.path.join(base_directory, filePath)
        fullFileDir = os.path.dirname(fullFilePath)

        if not os.path.exists(fullFileDir):
            os.makedirs(fullFileDir, exist_ok = True)

        return fullFilePath

    @classmethod
    def open_file(cls, filePath, mode = "r", usePermanentStorage = False):
        return super().open_file(filePath, mode, usePermanentStorage)

    @classmethod
    def load_json(cls, filePath, usePermanentStorage = False):
        return super().load_json(filePath, "r", usePermanentStorage = usePermanentStorage)

#    @classmethod
#    def save_json(cls, filePath, usePermanentStorage = False):
#        return super().load_json(filePath, "r", usePermanentStorage = usePermanentStorage)
