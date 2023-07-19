import os
import logging
import json

class FileSystemBase:

    __object_list = {}

    _FILESYSTEM_IDENTIFIER = None
    # TODO: get directories from config
    __DATA_DIRECTORY = os.path.join(os.getcwd(), "runtimedata")
    __STORAGE_DIRECTORY = os.path.join(__DATA_DIRECTORY, "storage")
    __CACHE_DIRECTORY = os.path.join(__DATA_DIRECTORY, "cache")

    @classmethod
    def _get_cache_directory(cls):
        return os.path.join(cls.__CACHE_DIRECTORY, cls._FILESYSTEM_IDENTIFIER)
    
    @classmethod
    def _get_storage_directory(cls):
        return os.path.join(cls.__STORAGE_DIRECTORY, cls._FILESYSTEM_IDENTIFIER)
        

    @classmethod
    def open_file(cls, filePath, mode = "r", *args, **kwargs):
        
        if cls in FileSystemBase.__object_list:
            object = FileSystemBase.__object_list[cls]
        else:
            object = cls()        
            FileSystemBase.__object_list[cls] = object

        resolvedFilePath = object.get_file(filePath, *args, **kwargs)

        if (resolvedFilePath):
            fullFileDir = os.path.dirname(resolvedFilePath)
            if not os.path.exists(fullFileDir):
                os.makedirs(fullFileDir, exist_ok = True)

            return open(resolvedFilePath, mode)
        else:
            return None

    @classmethod
    def load_json(cls, filePath, *args, **kwargs):
        return json.load(cls.open_file(filePath, *args, **kwargs))