import logging

from .GoogleDrive import GoogleDrive
from .LocalFile import LocalFile
from .file_system_base import FileSystemBase


class FileSystem:

#    file_system_list = {
#        "googledrive": GoogleDrive    
#    }
    file_system_list = [GoogleDrive, LocalFile]
    GoogleDrive = GoogleDrive
    LocalFile = LocalFile

    __file_system_objects = {}

    @staticmethod
    def get_file_path(file:str, fileSystemClass:FileSystemBase = LocalFile, init_params = {}, params = {}):
        
#        fileSystemObject = None

#        if file_system_identifier in FileSystem.__file_system_objects:
#            filesystem_object = FileSystem.__file_system_objects[file_system_identifier]
#        else:
#            for file_system_class in FileSystem.file_system_list:
#                if file_system_class.FILESYSTEM_IDENTIFIER == file_system_identifier:
#                    filesystem_object = file_system_class(**init_params)
#                    break

        if fileSystemClass in FileSystem.__file_system_objects:
            filesystem_object = FileSystem.__file_system_objects[file_system_identifier]
        else:
            try:
                filesystem_object = fileSystemClass(**init_params)
            except:
                filesystem_object = None
        
        if not filesystem_object:
            logging.info(f"Filesystem {fileSystemClass} doesn't exist")
            return None

#        FileSystem.__file_system_objects[fileSystemClass] = fileSystemObject

        logging.info(f"Getting file: {fileSystemClass}:{file}")
        
        return filesystem_object.get_file(file, **params)

    @staticmethod
    def open_file(file:str, file_system_identifier:str = "localfile", mode:str = "r", init_params:dict = {}, params:dict = {}):
        return open(FileSystem.get_file_path(file, file_system_identifier, init_params, params), mode)