import os, logging
import importlib.resources

from .file_system_base import FileSystemBase
from aiecommon.Exceptions import AieException

class LocalDataFiles(FileSystemBase):

    def __init__(self):
            
        logging.info(f"LocalFile constructor")

    def get_file(self, filePath, package = None):

        suggestedPackages = ["aiecommon"]
        suggestedFiles = []

        if package:
            path = importlib.resources.files(package).joinpath(filePath)
            if (os.path.exists(path) and os.path.isfile(path) ):
                return path
        else:  
            path = filePath
            if (os.path.exists(path) and os.path.isfile(path) ):
                return path

        path = filePath
        if (os.path.exists(path) and os.path.isfile(path) ):
            suggestedFiles.append(f"{path} (project root)")

        for suggestedPackage in suggestedPackages:
            path = importlib.resources.files(suggestedPackage).joinpath(filePath)
            if (os.path.exists(path) and os.path.isfile(path) ):
                suggestedFiles.append(f"{str(filePath)} ({str(suggestedPackage)})")

        if suggestedFiles:
            logging.error(f"File {filePath} ({package if package else 'project root'}) not found, suggested alternatives:")
            for suggestedFile in suggestedFiles:
                logging.error(suggestedFile)

        raise AieException(AieException.GENERIC_PYTHON_ERROR, f"LocalDataFiles, file not found filePath={filePath}, package={package} suggestedFiles={suggestedFiles}")

    @classmethod
    def open_file(cls, filePath, package = None):
        return super().open_file(filePath, "r", package = package)

    @classmethod
    def load_json(cls, filePath, package = None):
        return super().load_json(filePath, package = package)
