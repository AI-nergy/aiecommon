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

class PvGis():
    
    STORAGE_FOLDER = 'pvgis'
    PVGIS_START_YEAR = '2013'
    PVGIS_END_YEAR = '2023'
    TYPICAL_YEAR_START_DATE = '2018-01-01 00:00'
    TYPICAL_YEAR_END_DATE = '2018-12-31 23:00'
    TYPICAL_YEAR = int(TYPICAL_YEAR_START_DATE.split('-')[0])
    COORDINATES_DECIMAL_PLACES = 3

    def __init__(self,
        country_code : str,
        max_retries : int = 3,
        min_retry_delay : int = 2,
        min_file_size : int = 1024,
        ignore_cache : bool = False,
    ):
        """
        max_retries=3
        min_retry_delay=2
        min_file_size (optional, with default) - if the downloaded files is smaller, it won’t count as successful download
        ignore_cache (optional, default False) - whether to download regardless of the existence of cache
        """
        pass

        self.country_code = country_code
        self.max_retries = max_retries
        self.min_retry_delay = min_retry_delay
        self.min_file_size = min_file_size
        self.ignore_cache = ignore_cache
        
        os.makedirs(LocalRuntimeFiles.get_file(PvGis.STORAGE_FOLDER, usePermanentStorage=True), exist_ok=True)


    @staticmethod
    def _get_cache_key(latitude, longitude):
        return f"{PvGis.PVGIS_START_YEAR}_{PvGis.PVGIS_END_YEAR}_{np.round(latitude, PvGis.COORDINATES_DECIMAL_PLACES):.3f}_{np.round(longitude, PvGis.COORDINATES_DECIMAL_PLACES):.3f}"

    @staticmethod
    def _get_cache_file_path(latitude, longitude):
        cache_key = PvGis._get_cache_key(latitude, longitude)
        return LocalRuntimeFiles.get_file(os.path.join(PvGis.STORAGE_FOLDER, cache_key), usePermanentStorage=True)


    @staticmethod
    def _save_cache(latitude, longitude, data: pd.DataFrame):
        cache_file_path = PvGis._get_cache_file_path(latitude, longitude)
        logger.info(f"PvGis: Saving data cache as pickle, cache_file_path={cache_file_path}")
        data.to_pickle(cache_file_path)

    @staticmethod
    def _get_cache(latitude, longitude) -> pd.DataFrame:
        full_cache_file_path = PvGis._get_cache_file_path(latitude, longitude)

        if not os.path.exists(full_cache_file_path):
            return None
        
        try:
            logger.info(f"Get PvGis cache file, full_cache_file_path={full_cache_file_path}")
            return pd.read_pickle(full_cache_file_path)
        except Exception as e:
            logger.error(f"Cannot open PvGis cache file, full_cache_file_path={full_cache_file_path}, exception={e}")
            return None


    def get_solar_components(
        self,
        latitude, longitude,
        country_code : str | None = None,
        max_retries : int | None = None,
        min_retry_delay : int | None = None,
        min_file_size : int | None = None,
        ignore_cache : bool | None = None,
        # start_date, end_date, tz2,
        # max_retries=3, initial_delay=1
    ) -> pd.DataFrame | None:
        """
        Retrieve PVGIS TMY data for the given coordinates and date range,
        retrying on failure, and process it into an hourly DataFrame
        in the target timezone.

        Logs the duration of the external API fetch before proceeding.
        """

        country_code = country_code if country_code is not None else self.country_code
        max_retries = max_retries if max_retries is not None else self.max_retries
        min_retry_delay = min_retry_delay if min_retry_delay is not None else self.min_retry_delay
        min_file_size = min_file_size if min_file_size is not None else self.min_file_size
        ignore_cache = ignore_cache if ignore_cache is not None else self.ignore_cache
        tz = SolarUtils.get_timezone_from_country_code(country_code)

        retry_count = 0

        logger.info(f"PvGis: Try to get PvGis result from cache as pickle, latitude={latitude}, longitude={longitude}")
        cached_result = PvGis._get_cache(latitude, longitude)
        if cached_result is not None:
            logger.info(f"PvGis: Got PvGis result from cache as pickle, latitude={latitude}, longitude={longitude}")
            if isinstance(cached_result, pd.DataFrame) and not cached_result.empty:
                return cached_result
            else:
                logger.warning(f"PvGis: cached data exsist but it's not a pd.DataFrame or is empty, latitude={latitude}, longitude={longitude}")
        else:
            logger.info(f"PvGis: no cached data proceeding with pvgis rwequest, latitude={latitude}, longitude={longitude}")

        while retry_count <= self.max_retries:
            try:
                start = pd.Timestamp(PvGis.TYPICAL_YEAR_START_DATE)
                end = pd.Timestamp(PvGis.TYPICAL_YEAR_END_DATE)
                logger.info(f"PvGis {retry_count}/{self.max_retries}: Fetching PVGIS TMY for ({latitude},{longitude})")
                start_api = time.perf_counter()
                tmy_data = iotools.get_pvgis_tmy(
                    np.round(latitude, PvGis.COORDINATES_DECIMAL_PLACES),
                    np.round(longitude, PvGis.COORDINATES_DECIMAL_PLACES),
                    url='https://re.jrc.ec.europa.eu/api/v5_3/',
                    usehorizon=True,
                    startyear=PvGis.PVGIS_START_YEAR,
                    endyear=PvGis.PVGIS_END_YEAR,
                    coerce_year=PvGis.TYPICAL_YEAR
                )
                elapsed_api = time.perf_counter() - start_api
                logger.info(f"PvGis {retry_count}/{self.max_retries}: PVGIS TMY fetch took {elapsed_api:.2f} seconds")

                df = tmy_data[0]
                delays = PvGis.get_tmy_minute_offsets(latitude, longitude, tmy_data[1])
                df.index = df.index.tz_convert(tz)
                full = pd.date_range(start=start, end=end, freq='h', tz=tz)
                df = df.reindex(full)
                df.index = df.index + pd.to_timedelta(delays, unit='min')
                df = df.bfill().ffill().interpolate(method='nearest')
                logger.info(f"PvGis {retry_count}/{self.max_retries}: TMY data received; proceeding with geometry cache and production computation.")
                final_data = df[~df.index.duplicated()]

                logger.info(f"PvGis {retry_count}/{self.max_retries}: Saving result to cache as pickle, latitude={latitude}, longitude={longitude}")
                PvGis._save_cache(latitude, longitude, final_data)

                return final_data
            
            except Exception as e:
                logger.warning(f"PvGis {retry_count}/{self.max_retries}: Caught excepption while getting pvgis data")
                logger.warning(e)
                retry_count += 1
                time.sleep(self.min_retry_delay * 2**(retry_count - 1) + random.random())

        raise AieException(AieException.EXTERNAL_API_FAILED, f"PvGis failed after {retry_count} retries", {"api": "pvgis"})


    @staticmethod
    def get_tmy_minute_offsets(latitude, longitude, month_year_dict):
        """
        Return a fixed array of minute offsets (8760 entries) for aligning PVGIS TMY timestamps.
        """
        return np.full(8760, 10, dtype=np.float64)