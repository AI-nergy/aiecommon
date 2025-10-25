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
    ):
        pass
        self.tz = SolarUtils.get_timezone_from_country_code(country_code)
        


    def get_solar_components(
        latitude, longitude, start_date, end_date, tz2,
        max_retries=3, initial_delay=1
    ):
        """
        Retrieve PVGIS TMY data for the given coordinates and date range,
        retrying on failure, and process it into an hourly DataFrame
        in the target timezone.

        Logs the duration of the external API fetch before proceeding.
        """
        attempt = 0
        year = int(start_date.split('-')[0])
        while attempt <= max_retries:
            try:
                start = pd.Timestamp(start_date)
                end = pd.Timestamp(end_date)
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
                delays = SolarUtils.get_tmy_minute_offsets(latitude, longitude, tmy_data[1])
                df.index = df.index.tz_convert(tz2)
                full = pd.date_range(start=start, end=end, freq='h', tz=tz2)
                df = df.reindex(full)
                df.index = df.index + pd.to_timedelta(delays, unit='min')
                df = df.bfill().ffill().interpolate(method='nearest')
                logger.info("TMY data received; proceeding with geometry cache and production computation.")
                return df[~df.index.duplicated()]
            except Exception:
                attempt += 1
                if attempt > max_retries:
                    raise AieException(AieException.EXTERNAL_API_FAILED)
                time.sleep(initial_delay * 2**(attempt - 1))

