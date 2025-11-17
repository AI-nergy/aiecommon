import io
import json
import os
from urllib.error import HTTPError
import pandas as pd
import time
import numpy as np
import requests
from requests import Request
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

import aiecommon.custom_logger as custom_logger
logger = custom_logger.get_logger()
from aiecommon import SolarUtils
from aiecommon.SolarUtils.ExternalApiBase import ExternalApiBase
from aiecommon.Exceptions import AieException

class GoogleSolarApi(ExternalApiBase):
    
    STORAGE_FOLDER = 'googlesolarapi'
    API_IDENTIFIER = 'GoogleSolarApi'
    USE_PERMANENT_STORAGE = 'True'

    COORDINATES_DECIMAL_PLACES = 4

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
        min_result_size - if the downloaded data is smaller, it won't count as successful download
        ignore_cache - whether to make the API call regardless of the existence of cache
        """
        self.API_KEY = os.getenv("AIENERGY_GOOGLE_API_KEY")

        super().__init__(max_retries, min_retry_delay, min_result_size, ignore_cache)


    @staticmethod
    def _get_cache_key(params: dict):
        return f"{params['endpoint_identifier']}_{params['radius_meters']}_{np.round(params['latitude'], GoogleSolarApi.COORDINATES_DECIMAL_PLACES):.3f}_{np.round(params['longitude'], GoogleSolarApi.COORDINATES_DECIMAL_PLACES):.3f}"

    @staticmethod
    def _read_cache(cache_file_path: str, params) -> pd.DataFrame:
        match params["endpoint_identifier"]:
            case GoogleSolarApi.ENDPOINT_IDENTIFIER_DATALAYERS:
                with open(cache_file_path) as file:
                    return json.load(file)
            case (GoogleSolarApi.ENDPOINT_IDENTIFIER_DSM |
            GoogleSolarApi.ENDPOINT_IDENTIFIER_MASK):
                with open(cache_file_path, "rb") as file:
                    return file.read()
            case _:
                logger.error(f"GoogleSolarApi._read_cache: invalid endpoint_identifier, endpoint_identifier={params['endpoint_identifier']}")

    @staticmethod
    def _write_cache(cache_file_path: str, data, params):
        match params["endpoint_identifier"]:
            case GoogleSolarApi.ENDPOINT_IDENTIFIER_DATALAYERS:
                with open(cache_file_path, "w") as file:
                    return json.dump(data, file)
            case (GoogleSolarApi.ENDPOINT_IDENTIFIER_DSM | 
            GoogleSolarApi.ENDPOINT_IDENTIFIER_MASK):
                with open(cache_file_path, "bw") as file:
                    return file.write(data)
            case _:
                logger.error(f"GoogleSolarApi._write_cache: invalid endpoint_identifier, endpoint_identifier={params['endpoint_identifier']}")

    @staticmethod
    def _check_cache(cached_result, params):
        match params["endpoint_identifier"]:
            case GoogleSolarApi.ENDPOINT_IDENTIFIER_DATALAYERS:
                if isinstance(cached_result, dict):
                    return True
                else:
                    logger.warning(f"GoogleSolarApi._check_cache/{params['endpoint_identifier']}: cached data exsist but it's not a valid JSON, params={params}")
                    return False
            case (GoogleSolarApi.ENDPOINT_IDENTIFIER_MASK |
            GoogleSolarApi.ENDPOINT_IDENTIFIER_DSM):
                try:
                    image_stream = io.BytesIO(cached_result)
                    with Image.open(image_stream) as img:
                        img.verify()
                    return True
                except (IOError, SyntaxError) as exception:
                    logger.warning(f"GoogleSolarApi._check_cache/{params['endpoint_identifier']}: cached data exsist but it's not a valid TIFF, params={params}, exception={exception}")
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

    def _fetch_data_layers(self, max_retries, retry_count, endpoint_identifier, latitude, longitude, radius_meters, use_google_experimental):
        
        if use_google_experimental == True:
            query_params = {
                'location.latitude': latitude,
                'location.longitude': longitude,
                'view': 'IMAGERY_LAYERS',
                'radiusMeters': radius_meters,  # optional, you can change this, CHRISTIAN TODO
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
                'radiusMeters': radius_meters, # optional, you can change this, CHRISTIAN TODO
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

    # def _fetch_dsm(self, max_retries, retry_count, endpoint_identifier, latitude, longitude, radius_meters, url):
        
    #     response = requests.get(url=url, params={"key": self.API_KEY})
    #     if response.status_code == 200:
    #         logger.info(f'GoogleSolarApi {retry_count}/{max_retries}: Successfully fetched tiff data')
    #         return response.content
    #     else:
    #         raise AieException(AieException.EXTERNAL_API_FAILED, f"GoogleSolarApi._fetch_tiff {retry_count}/{max_retries}: API call failed, response.status_code={response.status_code}, response.text={response.text}", {"api": self.API_IDENTIFIER, "status_code": response.status_code})

    # def _fetch_mask(self, max_retries, retry_count, endpoint_identifier, latitude, longitude, radius_meters, url):
        
    #     response = requests.get(url=url, params={"key": self.API_KEY})
    #     if response.status_code == 200:
    #         logger.info(f'GoogleSolarApi {retry_count}/{max_retries}: Successfully fetched tiff data')
    #         return response.content
    #     else:
    #         raise AieException(AieException.EXTERNAL_API_FAILED, f"GoogleSolarApi._fetch_tiff {retry_count}/{max_retries}: API call failed, response.status_code={response.status_code}, response.text={response.text}", {"api": self.API_IDENTIFIER, "status_code": response.status_code})

    def _fetch_tiff(self, max_retries, retry_count, endpoint_identifier, latitude, longitude, radius_meters, url):
        
        response = requests.get(url=url, params={"key": self.API_KEY})
        if response.status_code == 200:
            logger.info(f'GoogleSolarApi {retry_count}/{max_retries}: Successfully fetched tiff data')
            return response.content
        else:
            raise AieException(AieException.EXTERNAL_API_FAILED, f"GoogleSolarApi._fetch_tiff {retry_count}/{max_retries}: API call failed, response.status_code={response.status_code}, response.text={response.text}", {"api": self.API_IDENTIFIER, "status_code": response.status_code})

    def _get_tiff(
        self,
        api_call_params,
        max_retries : int | None = None,
        min_retry_delay : int | None = None,
        min_result_size : int = 1024,
        ignore_cache : bool | None = None,
    ) -> pd.DataFrame | None:
        """
        Retrieve Google Solar API tiff for given api_call_params
        """

        return self.call_api(
            api_call_function=self. _fetch_tiff,
            api_call_params=api_call_params,
            get_result_size_function=self._get_result_size,
            max_retries=max_retries,
            min_retry_delay=min_retry_delay,
            min_result_size=min_result_size,
            ignore_cache=ignore_cache,
        )
    
    def get_layers_info(
        self,
        latitude, longitude,
        radius_meters,
        use_google_experimental,
        max_retries : int | None = None,
        min_retry_delay : int | None = None,
        min_result_size : int = 64,
        ignore_cache : bool | None = True,
    ) -> pd.DataFrame | None:
        """
        Retrieve Google Solar API layer info for given coordinates
        """

        return self.call_api(
            api_call_function=self. _fetch_data_layers,
            api_call_params={
                "latitude": latitude,
                "longitude": longitude,
                "radius_meters": radius_meters,
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


    def get_tiff(
        self,
        latitude, longitude,
        radius_meters,
        url,
        max_retries : int | None = None,
        min_retry_delay : int | None = None,
        min_result_size : int = 1024,
        ignore_cache : bool | None = None,
    ) -> pd.DataFrame | None:
        """
        Retrieve Google Solar API tiff for given url
        """

        return self._get_tiff(
            api_call_params={
                "latitude": latitude,
                "longitude": longitude,
                "radius_meters": radius_meters,
                "url": url,
                "endpoint_identifier": GoogleSolarApi.ENDPOINT_IDENTIFIER_DSM,
            },
            max_retries=max_retries,
            min_retry_delay=min_retry_delay,
            min_result_size=min_result_size,
            ignore_cache=ignore_cache,
        )

    def get_data(
        self,
        latitude: float,
        longitude: float,
        radius_meters: float,
        use_google_experimental: bool,
        endpoint_identifiers: list = [ENDPOINT_IDENTIFIER_DSM, ENDPOINT_IDENTIFIER_MASK],
        max_retries : int | None = None,
        min_retry_delay : int | None = None,
        ignore_cache : bool | None = None,
    ) -> pd.DataFrame | None:
        """
        Retrieve Google Solar API dsm and mask for given latitude and lognitude
        This function majes three calls:
            - to data layer to retreive dsm url and mask url - JSON response
            - to the dsm url retreived from the data layer response - TIFF response
            - to the mask url retreived from the data layer response - TIFF response
        """

        endpoint_identifiers_set = set(endpoint_identifiers)
        api_call_params = {}

        api_call_params[GoogleSolarApi.ENDPOINT_IDENTIFIER_DSM] = {
                "latitude": latitude,
                "longitude": longitude,
                "radius_meters": radius_meters,
                "endpoint_identifier": GoogleSolarApi.ENDPOINT_IDENTIFIER_DSM,
        }

        api_call_params[GoogleSolarApi.ENDPOINT_IDENTIFIER_MASK] = {
            "latitude": latitude,
            "longitude": longitude,
            "radius_meters": radius_meters,
            "endpoint_identifier": GoogleSolarApi.ENDPOINT_IDENTIFIER_MASK,
        }

        cached_dsm_data = None
        cached_mask_data = None

        if ignore_cache:
            endpoint_identifiers_set.add(GoogleSolarApi.ENDPOINT_IDENTIFIER_DATALAYERS)
            logger.info(f"GoogleSolarApi: ignore cache is on, will not check cache before calling data layers endpoint, ignore_cache={ignore_cache}")
        else: 
            if GoogleSolarApi.ENDPOINT_IDENTIFIER_DSM in endpoint_identifiers_set:
                cached_dsm_data = self._get_result_from_cache(ignore_cache=ignore_cache, api_call_params=api_call_params[GoogleSolarApi.ENDPOINT_IDENTIFIER_DSM]) 
                if cached_dsm_data is None:
                    endpoint_identifiers_set.add(GoogleSolarApi.ENDPOINT_IDENTIFIER_DATALAYERS)
            if GoogleSolarApi.ENDPOINT_IDENTIFIER_MASK in endpoint_identifiers_set:
                cached_mask_data = self._get_result_from_cache(ignore_cache=ignore_cache, api_call_params=api_call_params[GoogleSolarApi.ENDPOINT_IDENTIFIER_MASK])
                if cached_mask_data is None:
                    endpoint_identifiers_set.add(GoogleSolarApi.ENDPOINT_IDENTIFIER_DATALAYERS)
        
        if GoogleSolarApi.ENDPOINT_IDENTIFIER_DATALAYERS in endpoint_identifiers_set:
            layers_info = self.get_layers_info(
                latitude=latitude,
                longitude=longitude,
                radius_meters=radius_meters,
                use_google_experimental=use_google_experimental,
                max_retries = max_retries,
                min_retry_delay = max_retries,
                ignore_cache = ignore_cache if len(endpoint_identifiers_set) == 0 else True,
            )
            logger.info(f"GoogleSolarApi: got data layers info, layers_info={layers_info}")

            if layers_info:
                api_call_params[GoogleSolarApi.ENDPOINT_IDENTIFIER_DSM]["url"] = layers_info.get('dsmUrl')
                api_call_params[GoogleSolarApi.ENDPOINT_IDENTIFIER_MASK]["url"] = layers_info.get('maskUrl')
                cached_dsm_data = None
                cached_mask_data = None
        else:
            layers_info = None

        # Initialize data with any cached values
        dsm_data = cached_dsm_data if cached_dsm_data else None
        mask_data = cached_mask_data if cached_mask_data else None

        # Download DSM and mask in parallel if they are requested and not in cache
        futures = {}
        with ThreadPoolExecutor(max_workers=2) as executor:
            if GoogleSolarApi.ENDPOINT_IDENTIFIER_DSM in endpoint_identifiers_set and dsm_data is None:
                futures["dsm"] = executor.submit(
                    self._get_tiff,
                    api_call_params=api_call_params[GoogleSolarApi.ENDPOINT_IDENTIFIER_DSM],
                    max_retries=max_retries,
                    min_retry_delay=min_retry_delay,
                    ignore_cache=ignore_cache,
                )
            if GoogleSolarApi.ENDPOINT_IDENTIFIER_MASK in endpoint_identifiers_set and mask_data is None:
                futures["mask"] = executor.submit(
                    self._get_tiff,
                    api_call_params=api_call_params[GoogleSolarApi.ENDPOINT_IDENTIFIER_MASK],
                    max_retries=max_retries,
                    min_retry_delay=min_retry_delay,
                    ignore_cache=ignore_cache,
                )

            # Collect results
            for key, future in futures.items():
                if key == "dsm":
                    dsm_data = future.result()
                elif key == "mask":
                    mask_data = future.result()

        return dict(layers_info=layers_info, mask_data=mask_data, dsm_data=dsm_data)


    