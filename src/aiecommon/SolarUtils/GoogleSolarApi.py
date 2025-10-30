import json
import os
from urllib.error import HTTPError
import pandas as pd
import time
import numpy as np
import requests
from requests import Request

import aiecommon.custom_logger as custom_logger
logger = custom_logger.get_logger()
from aiecommon import SolarUtils
from aiecommon.SolarUtils.ExternalApiBase import ExternalApiBase
from aiecommon.Exceptions import AieException

class GoogleSolarApi(ExternalApiBase):
    
    STORAGE_FOLDER = 'googlesolarapi'
    API_IDENTIFIER = 'GoogleSolarApi'
    USE_PERMANENT_STORAGE = 'True'

    COORDINATES_DECIMAL_PLACES = 3

    RADIUS_METERS = 150
    PIXEL_SIZE_METERS = 0.25
    DATALAYERS_BASE_URL = "https://solar.googleapis.com/v1/dataLayers:get"
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
        This class gets google solar data
        
        max_retries - how many times to retry if the API call fails
        min_retry_delay - minimal delay between retries
        min_result_size - if the downloaded data is smaller, it won’t count as successful download
        ignore_cache - whether to make the API call regardless of the existence of cache
        """
        self.API_KEY = os.getenv("AIENERGY_GOOGLE_API_KEY")

        super().__init__(max_retries, min_retry_delay, min_result_size, ignore_cache)


    @staticmethod
    def _get_cache_key(params: dict):
        return f"{params['endpoint_identifier']}_{GoogleSolarApi.RADIUS_METERS}_{np.round(params['latitude'], GoogleSolarApi.COORDINATES_DECIMAL_PLACES):.3f}_{np.round(params['longitude'], GoogleSolarApi.COORDINATES_DECIMAL_PLACES):.3f}"

    @staticmethod
    def _read_cache(cache_file_path: str, params) -> pd.DataFrame:
        match params["endpoint_identifier"]:
            case GoogleSolarApi.ENDPOINT_IDENTIFIER_DATALAYERS:
                with open(cache_file_path) as file:
                    return json.load(file)
            case GoogleSolarApi.ENDPOINT_IDENTIFIER_DSM:
                return None
            case GoogleSolarApi.ENDPOINT_IDENTIFIER_MASK:
                return None
            case _:
                logger.error(f"GoogleSolarApi._read_cache: invalid endpoint_identifier, endpoint_identifier={params['endpoint_identifier']}")

    @staticmethod
    def _write_cache(cache_file_path: str, data: pd.DataFrame, params):
        match params["endpoint_identifier"]:
            case GoogleSolarApi.ENDPOINT_IDENTIFIER_DATALAYERS:
                with open(cache_file_path, "w") as file:
                    return json.dump(data, file)
            case GoogleSolarApi.ENDPOINT_IDENTIFIER_DSM:
                return None
            case GoogleSolarApi.ENDPOINT_IDENTIFIER_MASK:
                return None
            case _:
                logger.error(f"GoogleSolarApi._write_cache: invalid endpoint_identifier, endpoint_identifier={params['endpoint_identifier']}")

    @staticmethod
    def _check_cache(cached_result, params):
        match params["endpoint_identifier"]:
            case GoogleSolarApi.ENDPOINT_IDENTIFIER_DATALAYERS:
                if isinstance(cached_result, dict):
                    return True
                else:
                    logger.warning(f"GoogleSolarApi: cached data exsist but it's not a valid JSON, params={params}, exception={exception }")
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
            case GoogleSolarApi.ENDPOINT_IDENTIFIER_DATALAYERS:
                return len(json.dumps(result_data))
            case GoogleSolarApi.ENDPOINT_IDENTIFIER_DSM:
                return len(result_data)
            case GoogleSolarApi.ENDPOINT_IDENTIFIER_MASK:
                return len(result_data)
            case _:
                logger.error(f"GoogleSolarApi._get_result_size: invalid endpoint_identifier, endpoint_identifier={params['endpoint_identifier']}")

    def _fetch_data_layers(self, max_retries, retry_count, endpoint_identifier, latitude, longitude, use_google_experimental):
        
        if use_google_experimental == True:
            query_params = {
                'location.latitude': latitude,
                'location.longitude': longitude,
                'view': 'IMAGERY_LAYERS',
                'radiusMeters': self.RADIUS_METERS,  # optional, you can change this, CHRISTIAN TODO
                'pixelSizeMeters': self.PIXEL_SIZE_METERS,
                'requiredQuality': 'BASE',  # optional, you can change this
                'experiments': 'EXPANDED_COVERAGE',
                'key': self.API_KEY
            }
        else:
            query_params = {
                'location.latitude': latitude,
                'location.longitude': longitude,
                'view': 'IMAGERY_LAYERS',
                'radiusMeters': self.RADIUS_METERS,  # optional, you can change this, CHRISTIAN TODO
                'pixelSizeMeters': self.PIXEL_SIZE_METERS,
                'requiredQuality': 'MEDIUM',  # optional, you can change this
                'key': self.API_KEY
            }
        # parameters: https://developers.google.com/maps/documentation/solar/reference/rest/v1/dataLayers/get#query-parameters
        logger.info(f"Map resolution is set to {query_params['pixelSizeMeters']} meters, this is google data")

        response = requests.get(url=self.DATALAYERS_BASE_URL, params=query_params)
        if response.status_code == 200:
            logger.info(f'GoogleSolarApi {retry_count}/{max_retries}: Successfully fetched datalayer JSON')
            data = response.json()
            return data
        else:
            raise AieException(AieException.EXTERNAL_API_FAILED, f"GoogleSolarApi {retry_count}/{max_retries}: API call failed, response.status_code={response.status_code}, response.text={response.text}", {"api": self.API_IDENTIFIER, "status_code": response.status_code})


        # try:
        # except HTTPError as e:
        #     if e.code == 404:
        #         logger.error(f'Internal exception: EXTERNAL_API_FAILED. Error code received is {e.code}.')
        #         logger.error('There is no DSM data for the location you requested.')
        #         raise AieException(AieException.HOUSE_NOT_LOCATED)
        #     else:
        #         logger.error(f'Internal exception: EXTERNAL_API_FAILED. Error code received is {e.code}.')
        #         logger.error(f'Failed to fetch DSM URL: {response.read().decode()}')
        #         raise AieException(AieException.HOUSE_NOT_LOCATED)


    def _fetch_dsm(self, max_retries, retry_count, endpoint_identifier, latitude, longitude, dsm_url):
        
        response = requests.get(url=dsm_url, params={"key": self.API_KEY})
        if response.status_code == 200:
            logger.info(f'GoogleSolarApi {retry_count}/{max_retries}: Successfully fetched dsm data')
            return response.content
        else:
            raise AieException(AieException.EXTERNAL_API_FAILED, f"GoogleSolarApi._fetch_dsm {retry_count}/{max_retries}: API call failed, response.status_code={response.status_code}, response.text={response.text}", {"api": self.API_IDENTIFIER, "status_code": response.status_code})

    def _fetch_mask(self, max_retries, retry_count, endpoint_identifier, latitude, longitude, mask_url):
        
        response = requests.get(url=mask_url, params={"key": self.API_KEY})
        if response.status_code == 200:
            logger.info(f'GoogleSolarApi {retry_count}/{max_retries}: Successfully fetched mask data')
            return response.content
        else:
            raise AieException(AieException.EXTERNAL_API_FAILED, f"GoogleSolarApi._fetch_mask {retry_count}/{max_retries}: API call failed, response.status_code={response.status_code}, response.text={response.text}", {"api": self.API_IDENTIFIER, "status_code": response.status_code})

    def get_layers_info(
        self,
        latitude, longitude,
        use_google_experimental,
        max_retries : int | None = None,
        min_retry_delay : int | None = None,
        min_result_size : int = 64,
        ignore_cache : bool | None = None,
    ) -> pd.DataFrame | None:
        """
        Retrieve Google Solar API layer info for given coordinates
        """

        return self.call_api(
            api_call_function=self. _fetch_data_layers,
            api_call_params={
                "latitude": latitude,
                "longitude": longitude,
                "endpoint_identifier": GoogleSolarApi.ENDPOINT_IDENTIFIER_DATALAYERS,
                # "url": "https://solar.googleapis.com/v1/dataLayers:get",
                "use_google_experimental": use_google_experimental
            },
            get_result_size_function=self._get_result_size,
            max_retries=max_retries,
            min_retry_delay=min_retry_delay,
            min_result_size=min_result_size,
            ignore_cache=ignore_cache,
        )

    def get_dsm(
        self,
        latitude, longitude,
        dsm_url,
        max_retries : int | None = None,
        min_retry_delay : int | None = None,
        min_result_size : int = 64,
        ignore_cache : bool | None = None,
    ) -> pd.DataFrame | None:
        """
        Retrieve Google Solar API dsm for given dsm url
        """

        return self.call_api(
            api_call_function=self. _fetch_dsm,
            api_call_params={
                "latitude": latitude,
                "longitude": longitude,
                "dsm_url": dsm_url,
                "endpoint_identifier": GoogleSolarApi.ENDPOINT_IDENTIFIER_DSM,
            },
            get_result_size_function=self._get_result_size,
            max_retries=max_retries,
            min_retry_delay=min_retry_delay,
            min_result_size=min_result_size,
            ignore_cache=ignore_cache,
        )

    def get_mask(
        self,
        latitude, longitude,
        mask_url,
        max_retries : int | None = None,
        min_retry_delay : int | None = None,
        min_result_size : int = 64,
        ignore_cache : bool | None = None,
    ) -> pd.DataFrame | None:
        """
        Retrieve Google Solar API mask for given mask url
        """

        return self.call_api(
            api_call_function=self. _fetch_mask,
            api_call_params={
                "latitude": latitude,
                "longitude": longitude,
                "mask_url": mask_url,
                "endpoint_identifier": GoogleSolarApi.ENDPOINT_IDENTIFIER_MASK,
            },
            get_result_size_function=self._get_result_size,
            max_retries=max_retries,
            min_retry_delay=min_retry_delay,
            min_result_size=min_result_size,
            ignore_cache=ignore_cache,
        )





