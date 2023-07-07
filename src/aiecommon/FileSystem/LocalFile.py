import io, os, logging
from .file_system_base import FileSystemBase

class LocalFile(FileSystemBase):
 
    FILESYSTEM_IDENTIFIER = "localfile"
    DATA_DIRECTORY = os.path.join(os.getcwd(), "data")

    def __init__(self):
            
        logging.info(f"LocalFile constructor")

    def get_file(self, filePath):

        return os.path.join(self.DATA_DIRECTORY, filePath)
