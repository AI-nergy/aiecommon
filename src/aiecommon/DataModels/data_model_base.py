from pydantic import BaseModel
import logging
import json

from aiecommon.FileSystem import LocalDataFiles

class DataModelBase(BaseModel):

    @classmethod
    def _validate(cls, data, key = None):
        """
        DO NOT USE THIS FUNCTION, create a @classmethod override instead.
        Called for validation of the data after loading from file.
        You should raise an exception if validation doesn't pass. Return value of this function is discarded.

        Args:
            data: data to validate
            key: str (None) optional key specified when calling to from_json(), used for loading only one entry from a JSON file with a dictionary 
        Returns:
            None
        """
        logging.info("DataModelBase _validate() called. This function does nothing, implement override in parent class if needed")
        return None
    
    @classmethod
    def from_json(cls, path: str, package = None, key:str = None):
        """
        Loads the data into data class from a JSON file.
        Calls __validate() in which data can be adidtionally checked and anexception thrown.

        Args:
            path: str Path of the file to load
            package: str|Package (None) Package from which to load the file. If not specified, it loads from current project.
            key: str (None) if specified, the data loaded from the file is interpreted as dictionary and the value of the specified key is loaded into the class. 
        Returns:
            class object: object of the class with the data loaded from the file
        """

        # Load the specified JSON file
        data = LocalDataFiles.load_json(path, package)

        # Run validation function on the loaded data
        cls._validate(data, key)

        # Return an instance of class representing data
        if key is None:
            return cls(**data)
        else:
            return cls(**data[key])
        
    @classmethod
    def from_json_string(cls, json_string: str, key:str = None):
        """
        Loads the data into data class from a JSON string.

        Args:
            json_string: string from which to load JSON
            key: str (None) if specified, the data loaded from the string is interpreted as dictionary and the value of the specified key is loaded into the class. 
        Returns:
            class object: object of the class with the data loaded from the file
        """

        # Load the JSON string
        data = json.loads(json_string)

        # Return an instance of class representing data
        if key is None:
            return cls(**data)
        else:
            return cls(**data[key])