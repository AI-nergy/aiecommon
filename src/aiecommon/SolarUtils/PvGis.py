import pandas as pd
import time
from pvlib import iotools
import numpy as np

import aiecommon.custom_logger as custom_logger
logger = custom_logger.get_logger()
from aiecommon import SolarUtils
from aiecommon.SolarUtils.ExternalApiBase import ExternalApiBase

class PvGis(ExternalApiBase):
    
    STORAGE_FOLDER = 'pvgis'
    API_IDENTIFIER = 'PvGis'
    USE_PERMANENT_STORAGE = 'True'

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
        min_result_size : int = 1024,
        ignore_cache : bool = False,
    ):
        """
        max_retries - how many times to retry if the API call fails
        min_retry_delay - minimal delay between retries
        min_result_size - if the downloaded data is smaller, it won't count as successful download
        ignore_cache - whether to make the API call regardless of the existence of cache
        """
        self.country_code = country_code
        super().__init__(max_retries, min_retry_delay, min_result_size, ignore_cache)


    @staticmethod
    def _get_cache_key(params: dict):
        return f"{PvGis.PVGIS_START_YEAR}_{PvGis.PVGIS_END_YEAR}_{np.round(params['latitude'], PvGis.COORDINATES_DECIMAL_PLACES):.3f}_{np.round(params['longitude'], PvGis.COORDINATES_DECIMAL_PLACES):.3f}"

    @staticmethod
    def _read_cache(cache_file_path: str, params: dict) -> pd.DataFrame:
        return pd.read_pickle(cache_file_path)

    @staticmethod
    def _write_cache(cache_file_path: str, data: pd.DataFrame, params: dict):
        return data.to_pickle(cache_file_path)

    @staticmethod
    def _check_cache(cached_result, params: dict):
        if isinstance(cached_result, pd.DataFrame) and not cached_result.empty:
            return True
        else:
            logger.warning(f"PvGis: cached data exsist but it's not a pd.DataFrame or is empty, params={params}")
            return False

    def _fetch(self, max_retries, retry_count, latitude, longitude, country_code):
        latitude_truncated = np.round(latitude, PvGis.COORDINATES_DECIMAL_PLACES)
        longitude_truncated = np.round(longitude, PvGis.COORDINATES_DECIMAL_PLACES)
        tz = SolarUtils.get_timezone_from_country_code(country_code)

        start = pd.Timestamp(PvGis.TYPICAL_YEAR_START_DATE)
        end = pd.Timestamp(PvGis.TYPICAL_YEAR_END_DATE)
        logger.info(f"PvGis {retry_count}/{max_retries}: Fetching PVGIS TMY for ({latitude},{longitude}) -> ({latitude_truncated}, {longitude_truncated})")
        start_api = time.perf_counter()
        tmy_data = iotools.get_pvgis_tmy(
            latitude_truncated,
            longitude_truncated,
            url='https://re.jrc.ec.europa.eu/api/v5_3/',
            usehorizon=True,
            startyear=PvGis.PVGIS_START_YEAR,
            endyear=PvGis.PVGIS_END_YEAR,
            coerce_year=PvGis.TYPICAL_YEAR
        )
        elapsed_api = time.perf_counter() - start_api
        logger.info(f"PvGis {retry_count}/{max_retries}: PVGIS TMY fetch took {elapsed_api:.2f} seconds")

        df = tmy_data[0]
        delays = PvGis.get_tmy_minute_offsets(latitude, longitude, tmy_data[1])
        df.index = df.index.tz_convert(tz)
        full = pd.date_range(start=start, end=end, freq='h', tz=tz)
        df = df.reindex(full)
        df.index = df.index + pd.to_timedelta(delays, unit='min')
        df = df.bfill().ffill().interpolate(method='nearest')
        logger.info(f"PvGis {retry_count}/{max_retries}: TMY data received; proceeding with geometry cache and production computation.")
        final_data = df[~df.index.duplicated()]

        return final_data

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
                "country_code": country_code,
            },
            get_result_size_function=lambda result_data, params: result_data.size,
            max_retries=max_retries,
            min_retry_delay=min_retry_delay,
            min_result_size=min_result_size,
            ignore_cache=ignore_cache,
        )


    @staticmethod
    def get_tmy_minute_offsets(latitude, longitude, month_year_dict):
        """
        Return a fixed array of minute offsets (8760 entries) for aligning PVGIS TMY timestamps.
        """
        return np.full(8760, 10, dtype=np.float64)