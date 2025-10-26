import os
import random
import pandas as pd
from  typing import Callable
import time

import aiecommon.custom_logger as custom_logger
logger = custom_logger.get_logger()

from aiecommon.Exceptions import AieException
from aiecommon.FileSystem import LocalRuntimeFiles

class ExternalApiBase():
    
    STORAGE_FOLDER = 'ExternalApiBase'
    API_IDENTIFIER = 'NONE'
    USE_PERMANENT_STORAGE = False

    def __init__(self,
        max_retries: int = 3,
        min_retry_delay: int = 2,
        min_result_size: int = 1024,
        ignore_cache: bool = False,
    ):
        """
        max_retries - how many times to retry if the API call fails
        min_retry_delay - minimal delay between retries
        min_result_size - if the downloaded data is smaller, it won’t count as successful download
        ignore_cache - whether to make the API call regardless of the existence of cache
        """
        pass

        self.max_retries = max_retries
        self.min_retry_delay = min_retry_delay
        self.min_result_size = min_result_size
        self.ignore_cache = ignore_cache
        
        os.makedirs(LocalRuntimeFiles.get_file(self.STORAGE_FOLDER, usePermanentStorage=self.USE_PERMANENT_STORAGE), exist_ok=True)

    @classmethod
    def _get_cache_file_path(cls, params: dict):
        cache_key = cls._get_cache_key(params)
        return LocalRuntimeFiles.get_file(os.path.join(cls.STORAGE_FOLDER, cache_key), usePermanentStorage=cls.USE_PERMANENT_STORAGE)

    @classmethod
    def _save_cache(cls, params: dict, data):
        cache_file_path = cls._get_cache_file_path(params)
        logger.info(f"ExternalApiBase/{cls.API_IDENTIFIER}: Saving {cls.API_IDENTIFIER} data to cache, cache_file_path={cache_file_path}")
        return cls._write_cache(cache_file_path, data)

    @classmethod
    def _get_cache(cls, params: dict):
        full_cache_file_path = cls._get_cache_file_path(params)

        if not os.path.exists(full_cache_file_path):
            logger.info(f"ExternalApiBase/{cls.API_IDENTIFIER}: Get {cls.API_IDENTIFIER} cache file doesn't exist, full_cache_file_path={full_cache_file_path}")
            return None
        
        try:
            logger.info(f"ExternalApiBase/{cls.API_IDENTIFIER}: Get {cls.API_IDENTIFIER} cache file, full_cache_file_path={full_cache_file_path}")
            return cls._read_cache(full_cache_file_path)
        except Exception as e:
            logger.error(f"ExternalApiBase/{cls.API_IDENTIFIER}: Cannot open {cls.API_IDENTIFIER} cache file, full_cache_file_path={full_cache_file_path}, exception={e}")
            return None

    def call_api(
        self,
        api_call_function: Callable,
        api_call_params: dict,
        get_result_size_function: Callable,
        max_retries: int | None = None,
        min_retry_delay: int | None = None,
        min_result_size: int | None = None,
        ignore_cache: bool | None = None,
    ) -> pd.DataFrame | None:
        """
        Call external api with caching and retry
        """

        max_retries = max_retries if max_retries is not None else self.max_retries
        min_retry_delay = min_retry_delay if min_retry_delay is not None else self.min_retry_delay
        min_result_size = min_result_size if min_result_size is not None else self.min_result_size
        ignore_cache = ignore_cache if ignore_cache is not None else self.ignore_cache

        retry_count = 0

        logger.info(f"ExternalApiBase/{self.API_IDENTIFIER}: Try to get result from cache, api_call_params={api_call_params}")
        cached_result = self._get_cache(api_call_params)
        if cached_result is not None:
            logger.info(f"ExternalApiBase/{self.API_IDENTIFIER}: Got result from cache, api_call_params={api_call_params}")
            if self._check_cache(cached_result, api_call_params):
                return cached_result
            else:
                logger.warning(f"ExternalApiBase/{self.API_IDENTIFIER}: cached data exsist but it didn't pass cache check, api_call_params={api_call_params}")
        else:
            logger.info(f"ExternalApiBase/{self.API_IDENTIFIER}: no cached data, proceeding with api request, api_call_params={api_call_params}")

        while retry_count <= max_retries:
            try:
                result_data = api_call_function(max_retries, retry_count, **api_call_params)
                result_size = get_result_size_function(result_data)

                if  result_size < min_result_size:
                    raise Exception(f"The result size is smaller than limit, result_size={result_size}, min_result_size={min_result_size}")

                logger.info(f"ExternalApiBase/{self.API_IDENTIFIER} {retry_count}/{max_retries}: Saving result to cache, api_call_params={api_call_params}")
                self._save_cache(api_call_params, result_data)

                return result_data

            except Exception as e:
                logger.warning(f"ExternalApiBase/{self.API_IDENTIFIER} {retry_count}/{max_retries}: Caught excepption while getting data")
                logger.warning(e)
                retry_count += 1
                sleep_interval = self.min_retry_delay * 2**(retry_count - 1) + random.random()
                logger.info(f"ExternalApiBase/{self.API_IDENTIFIER} {retry_count}/{max_retries}: Sleeping for {sleep_interval} seconds before retry")
                time.sleep(sleep_interval)

        raise AieException(AieException.EXTERNAL_API_FAILED, f"ExternalApiBase/{self.API_IDENTIFIER} failed after {retry_count} retries", {"api": self.API_IDENTIFIER})
