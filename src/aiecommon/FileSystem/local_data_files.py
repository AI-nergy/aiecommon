import os, logging
import json
import importlib.resources

from .file_system_base import FileSystemBase
import aiecommon

class LocalDataFiles(FileSystemBase):

    DATA_SUB_DIRECTORY = "data" 
    APP_DATA_DIRECTORY = os.path.join(os.getcwd(), DATA_SUB_DIRECTORY)

    def __init__(self):
            
        logging.info(f"LocalFile constructor")

    def get_file(self, filePath):

        path = os.path.join(LocalDataFiles.APP_DATA_DIRECTORY, filePath)
        if (os.path.exists(path) and os.path.isfile(path) ):
           return path
# "data/biddingZonesPolygonsFiltered.json"
        path = importlib.resources.files("aiecommon").joinpath(LocalDataFiles.DATA_SUB_DIRECTORY, filePath)
        if (os.path.exists(path) and os.path.isfile(path) ):
           return path

        path = filePath
        if (os.path.exists(path) and os.path.isfile(path) ):
           return path

        return None
#        self.polygons = json.load(importlib.resources.files("aiecommon").joinpath("data/biddingZonesPolygonsFiltered.json").open())

