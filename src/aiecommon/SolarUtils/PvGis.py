import random
import pandas as pd
import aiecommon.custom_logger as custom_logger
logger = custom_logger.get_logger()

import time
from pvlib import iotools
import numpy as np

from aiecommon.Exceptions import AieException
from aiecommon import SolarUtils

class PvGis():
    
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
        
        self.TYPICAL_YEAR_START_DATE = '2018-01-01 00:00'
        self.TYPICAL_YEAR_END_DATE = '2018-12-31 23:00'



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
    ):
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

        attempt = 0
        year = int(self.TYPICAL_YEAR_START_DATE.split('-')[0])
        while attempt <= self.max_retries:
            try:
                start = pd.Timestamp(self.TYPICAL_YEAR_START_DATE)
                end = pd.Timestamp(self.TYPICAL_YEAR_END_DATE)
                logger.info(f"Fetching PVGIS TMY for ({latitude},{longitude})")
                start_api = time.perf_counter()
                tmy_data = iotools.get_pvgis_tmy(
                    np.round(latitude, 3),
                    np.round(longitude, 3),
                    url='https://re.jrc.ec.europa.eu/api/v5_3/',
                    usehorizon=True,
                    startyear=2013,
                    endyear=2023,
                    coerce_year=year
                )
                elapsed_api = time.perf_counter() - start_api
                logger.info(f"PVGIS TMY fetch took {elapsed_api:.2f} seconds")

                df = tmy_data[0]
                delays = PvGis.get_tmy_minute_offsets(latitude, longitude, tmy_data[1])
                df.index = df.index.tz_convert(tz)
                full = pd.date_range(start=start, end=end, freq='h', tz=tz)
                df = df.reindex(full)
                df.index = df.index + pd.to_timedelta(delays, unit='min')
                df = df.bfill().ffill().interpolate(method='nearest')
                logger.info("TMY data received; proceeding with geometry cache and production computation.")
                final_data = df[~df.index.duplicated()]
                return final_data
            
            except Exception as e:
                logger.warning(f"{attempt}/{self.max_retries} Caught excepption while getting pvgis data")
                logger.warning(e)
                raise e
                attempt += 1
                if attempt > self.max_retries:
                    raise AieException(AieException.EXTERNAL_API_FAILED)
                time.sleep(self.min_retry_delay * 2**(attempt - 1) + random.random())


    @staticmethod
    def get_tmy_minute_offsets(latitude, longitude, month_year_dict):
        """
        Return a fixed array of minute offsets (8760 entries) for aligning PVGIS TMY timestamps.
        """
        return np.full(8760, 10, dtype=np.float64)