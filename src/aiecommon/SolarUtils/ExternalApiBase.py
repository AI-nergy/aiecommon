import os
import random
import pandas as pd
import aiecommon.custom_logger as custom_logger
logger = custom_logger.get_logger()

import time
from pvlib import iotools
import numpy as np

from aiecommon.Exceptions import AieException
from aiecommon import SolarUtils
from aiecommon.FileSystem import LocalRuntimeFiles

class ExternalApiBase():
    
    STORAGE_FOLDER = 'ExternalApiBase'
    API_IDENTIFIER = 'NONE'
    USE_PERMANENT_STORAGE = False

    @classmethod
    def _get_cache_file_path(cls, latitude, longitude):
        cache_key = cls._get_cache_key(latitude, longitude)
        return LocalRuntimeFiles.get_file(os.path.join(cls.STORAGE_FOLDER, cache_key), usePermanentStorage=cls.USE_PERMANENT_STORAGE)

    @classmethod
    def _save_cache(cls, latitude, longitude, data):
        cache_file_path = cls._get_cache_file_path(latitude, longitude)
        logger.info(f"ExternalApiBase: Saving {cls.API_IDENTIFIER} data to cache, cache_file_path={cache_file_path}")
        return cls._write_cache(cache_file_path, data)

    @classmethod
    def _get_cache(cls, latitude, longitude):
        full_cache_file_path = cls._get_cache_file_path(latitude, longitude)

        if not os.path.exists(full_cache_file_path):
            logger.info(f"ExternalApiBase: Get {cls.API_IDENTIFIER} cache file doesn't exist, full_cache_file_path={full_cache_file_path}")
            return None
        
        try:
            logger.info(f"ExternalApiBase: Get {cls.API_IDENTIFIER} cache file, full_cache_file_path={full_cache_file_path}")
            return cls._read_cache(full_cache_file_path)
        except Exception as e:
            logger.error(f"ExternalApiBase: Cannot open {cls.API_IDENTIFIER} cache file, full_cache_file_path={full_cache_file_path}, exception={e}")
            return None
