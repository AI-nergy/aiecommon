import pandas as pd
from typing import List
import sys; sys.path.append('../..')
from aiecommon.DataModels import CountryData
from aiecommon.Models import InputData

class GetEmissionsData:
    """
    This class is used to get emissions data 
    """

    def __init__(self, path: str, input_data: InputData, countryData: CountryData) -> None:
        """
        Initializes the GetPowerPricesData class.

        Parameters:
        -----------
        path : str
            The path to the directory where the CSV files are stored.
        input_data : InputData
            An object containing the location data.
        countryData : CountryData
            An object containing the country-specific data.
        """
        self.path = path
        self.location = input_data.location
        self.countryData = countryData
        self.co2_emissions = self._get_emission_coefficients()

    def _get_emission_coefficients(self) -> List[float]:
        """
        Returns a list of emission coefficients for the specified bidding zone.

        Returns:
        --------
        List[float]
            A list of emission coefficients.
        """

        # data is in Kg CO2/kWh
        emissions = pd.read_csv(f"{self.path}/shared/CO2EmissionsHourly.csv", header=0, index_col=0, parse_dates=True)
        # Filter by bidding region and return
        return [e for e in emissions[self.location.biddingZone]]

 

