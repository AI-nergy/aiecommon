import logging

from .GoogleDrive import GoogleDrive
from .local_runtime_files import LocalRuntimeFiles
from .local_data_files import LocalDataFiles
from .file_system_base import FileSystemBase


class FileSystem:

#    file_system_list = {
#        "googledrive": GoogleDrive    
#    }
    file_system_list = [GoogleDrive, LocalRuntimeFiles, LocalDataFiles]
    GoogleDrive = GoogleDrive
    LocalRuntimeFiles = LocalRuntimeFiles
    LocalDataFiles = LocalDataFiles

    __file_system_objects = {}

    @staticmethod
    def get_file_path(file:str, fileSystemClass:FileSystemBase = LocalRuntimeFiles, init_params = {}, params = {}):
        
#        fileSystemObject = None

#        if file_system_identifier in FileSystem.__file_system_objects:
#            filesystem_object = FileSystem.__file_system_objects[file_system_identifier]
#        else:
#            for file_system_class in FileSystem.file_system_list:
#                if file_system_class.FILESYSTEM_IDENTIFIER == file_system_identifier:
#                    filesystem_object = file_system_class(**init_params)
#                    break

        if fileSystemClass in FileSystem.__file_system_objects:
            filesystem_object = FileSystem.__file_system_objects[fileSystemClass]
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
    def open_file(file:str, fileSystemClass:FileSystemBase = LocalDataFiles, mode:str = "r", init_params:dict = {}, params:dict = {}):
        return fileSystemClass.open_file(FileSystem.get_file_path(file, fileSystemClass, init_params, params), mode)
