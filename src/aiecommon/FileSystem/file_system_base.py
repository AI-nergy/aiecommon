import os
import logging

class FileSystemBase:


    FILESYSTEM_IDENTIFIER = None
    # TODO: get directories from config
    DATA_DIRECTORY = os.path.join(os.getcwd(), "runtimedata")
    STORAGE_DIRECTORY = os.path.join(DATA_DIRECTORY, "storage")
    CACHE_DIRECTORY = os.path.join(DATA_DIRECTORY, "cache")

    @classmethod
    def get_cache_directory(cls):
        return os.path.join(cls.CACHE_DIRECTORY, cls.FILESYSTEM_IDENTIFIER)
    
    @classmethod
    def get_storage_directory(cls):
        return os.path.join(cls.STORAGE_DIRECTORY, cls.FILESYSTEM_IDENTIFIER)
    
    #@classmethod
    def open_file(filePath, mode):
        return open(filePath, mode)
