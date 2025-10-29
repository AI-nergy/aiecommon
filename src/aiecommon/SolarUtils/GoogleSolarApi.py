import json
import pandas as pd
import time
import numpy as np

import aiecommon.custom_logger as custom_logger
logger = custom_logger.get_logger()
from aiecommon import SolarUtils
from aiecommon.SolarUtils.ExternalApiBase import ExternalApiBase

class GoogleSolarApi(ExternalApiBase):
    
    STORAGE_FOLDER = 'googlesolarapi'
    API_IDENTIFIER = 'GoogleSolarApi'
    USE_PERMANENT_STORAGE = 'True'

    COORDINATES_DECIMAL_PLACES = 3
    RADIUS_METERS = 150

    ENDPOINT_IDENTIFIER_DATALAYERS = "ENDPOINT_IDENTIFIER_DATALAYERS"
    ENDPOINT_IDENTIFIER_DSM = "ENDPOINT_IDENTIFIER_DSM"
    ENDPOINT_IDENTIFIER_MASK = "ENDPOINT_IDENTIFIER_MASK"

    def __init__(self,
        max_retries : int = 3,
        min_retry_delay : int = 2,
        min_result_size : int = 1024,
        ignore_cache : bool = False,
    ):
        """
        max_retries - how many times to retry if the API call fails
        min_retry_delay - minimal delay between retries
        min_result_size - if the downloaded data is smaller, it won’t count as successful download
        ignore_cache - whether to make the API call regardless of the existence of cache
        """
        super().__init__(max_retries, min_retry_delay, min_result_size, ignore_cache)


    @staticmethod
    def _get_cache_key(params: dict):
        return f"{params['endpoint_identifier']}_{GoogleSolarApi.RADIUS_METERS}_{np.round(params['latitude'], GoogleSolarApi.COORDINATES_DECIMAL_PLACES):.3f}_{np.round(params['longitude'], GoogleSolarApi.COORDINATES_DECIMAL_PLACES):.3f}"

    @staticmethod
    def _read_cache(cache_file_path: str, params) -> pd.DataFrame:
        match params["endpoint_identifier"]:
            case GoogleSolarApi.ENDPOINT_IDENTIFIER_DATALAYERS:
                return json.load(cache_file_path)
            case GoogleSolarApi.ENDPOINT_IDENTIFIER_DSM:
                return json.load(cache_file_path)
            case GoogleSolarApi.ENDPOINT_IDENTIFIER_MASK:
                return json.load(cache_file_path)
            case _:
                logger.error(f"GoogleSolarApi._read_cache: invalid endpoint_identifier, endpoint_identifier={params['endpoint_identifier']}")

    @staticmethod
    def _write_cache(cache_file_path: str, data: pd.DataFrame, params):
        match params["endpoint_identifier"]:
            case "dataLayers:get":
                return json.dump(cache_file_path)
            case GoogleSolarApi.ENDPOINT_IDENTIFIER_DSM:
                return json.dump(cache_file_path)
            case GoogleSolarApi.ENDPOINT_IDENTIFIER_MASK:
                return json.dump(cache_file_path)
            case _:
                logger.error(f"GoogleSolarApi._write_cache: invalid endpoint_identifier, endpoint_identifier={params['endpoint_identifier']}")

    @staticmethod
    def _check_cache(cached_result, params):
        match params["endpoint_identifier"]:
            case "dataLayers:get":
                try:
                    json.loads(cached_result)
                    return True
                except Exception as e:
                    logger.warning(f"GoogleSolarApi: cached data exsist but it's not a valis JSON, params={params}")
                return False
            case GoogleSolarApi.ENDPOINT_IDENTIFIER_DSM:
                return False
            case GoogleSolarApi.ENDPOINT_IDENTIFIER_MASK:
                return False
            case _:
                logger.error(f"GoogleSolarApi._check_cache: invalid endpoint_identifier, endpoint_identifier={params['endpoint_identifier']}")


    @staticmethod
    def _get_result_size(result_data, params):
        match params["endpoint_identifier"]:
            case "dataLayers:get":
                return len(json.loads(result_data))
            case GoogleSolarApi.ENDPOINT_IDENTIFIER_DSM:
                return 0
            case GoogleSolarApi.ENDPOINT_IDENTIFIER_MASK:
                return 0
            case _:
                logger.error(f"GoogleSolarApi._get_result_size: invalid endpoint_identifier, endpoint_identifier={params['endpoint_identifier']}")

    def _fetch(self, max_retries, retry_count, latitude, longitude, endpoint_identifier, url):

        return None

    def get_solar_components(
        self,
        latitude, longitude,
        country_code : str | None = None,
        max_retries : int | None = None,
        min_retry_delay : int | None = None,
        min_result_size : int | None = None,
        ignore_cache : bool | None = None,
    ) -> pd.DataFrame | None:
        """
        Retrieve PVGIS TMY data for the given coordinates and date range,
        retrying on failure, and process it into an hourly DataFrame
        in the target timezone.

        Logs the duration of the external API fetch before proceeding.
        """

        country_code = country_code if country_code is not None else self.country_code

        return self.call_api(
            api_call_function=self._fetch,
            api_call_params={
                "latitude": latitude,
                "longitude": longitude,
                "endpoint_identifier": "dataLayers:get",
            },
            get_result_size_function=lambda result_data: result_data.size,
            max_retries=max_retries,
            min_retry_delay=min_retry_delay,
            min_result_size=min_result_size,
            ignore_cache=ignore_cache,
        )
