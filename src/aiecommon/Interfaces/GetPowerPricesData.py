import pandas as pd
from typing import List
import sys; sys.path.append('../..')
from aiecommon.DataModels import RequestData, CountryData

class GetPowerPricesData:
    """
    A class used to get power prices data from CSV files and calculate buying and selling prices based on the input.

    Attributes:
    -----------
    path : str
        The path to the directory where the CSV files are stored.
    location : RequestData
        An object containing the location data.
    countryData : CountryData
        An object containing the country-specific data.

    Methods:
    --------
    _get_nordpool_prices(self) -> List[float]:
        Returns a list of Nordpool prices for the specified bidding zone.
    _get_distribution_prices(self) -> List[float]:
        Returns a list of distribution prices for the specified country.
    _calculate_buying_price(self) -> List[float]:
        Calculates the buying prices based on the country-specific data and returns a list of prices.
    _calculate_selling_price(self) -> List[float]:
        Calculates the selling prices based on the country-specific data and returns a list of prices.
    _buying_price_function_per_country(countryCode: str, countryData: CountryData, powerPrices: List[float], distributionPrices: List[float]) -> List[float]:
        Calculates the buying prices based on the country-specific data and returns a list of prices.

    """

    def __init__(self, path: str, requestData: RequestData, countryData: CountryData) -> None:
        """
        Initializes the GetPowerPricesData class.

        Parameters:
        -----------
        path : str
            The path to the directory where the CSV files are stored.
        requestData : RequestData
            An object containing the location data.
        countryData : CountryData
            An object containing the country-specific data.
        """
        self.path = path
        self.requestData = requestData
        self.location = requestData.location
        self.countryData = countryData
        self.distributionPrices = self._get_distribution_prices()
        self.__powerPrices = self._get_nordpool_prices()
        self.buyingPrices = self._calculate_buying_price()
        self.sellingPrices = self._calculate_selling_price()


    def _get_nordpool_prices(self) -> List[float]:
        """
        Returns a list of Nordpool prices for the specified bidding zone.

        Returns:
        --------
        List[float]
            A list of Nordpool prices.
        """
        # SpotPrices dataset is in euros
        ele_prices = pd.read_csv(f"{self.path}/shared/PowerPrices.csv", header=0, index_col=0, parse_dates=True)
        # Select bidding region
        return [price / 1000 for price in ele_prices[self.location.biddingZone]]

    def _get_distribution_prices(self, suffix: str="") -> List[float]:
        """
        Returns a list of distribution prices for the specified country.

        Returns:
        --------
        List[float]
            A list of distribution prices.
        """
        dist_prices = pd.read_csv(f"{self.path}/{self.location.countryCode.lower()}/DistributionPrice{self.location.countryCode}{'_' + self.requestData.systemType if self.location.countryCode == 'EE' else ''}.csv", header=0, index_col=0, parse_dates=True)
        return [prices.item() for prices in dist_prices.values]

    def _calculate_buying_price(self) -> List[float]:
        """
        Calculates the buying prices based on the country-specific data and returns a list of prices.

        Returns:
        --------
        List[float]
            A list of buying prices.
        """
        return self._buying_price_function_per_country(self.location.countryCode, self.countryData, self.__powerPrices, self.distributionPrices)

    def _calculate_selling_price(self):
        """
        Calculate the selling price for electricity by applying a penalty percentage to the power prices.

        Returns:
            list: A list of selling prices for each hour in the power prices list.
        """
        return [price * (1 - self.countryData.penaltySellingPowerPrice) for price in self.__powerPrices]

    def _buying_price_function_per_country(self, countryCode: str, countryData: CountryData, powerPrices: list, distributionPrices: list):
        """
        Calculate the buying price for electricity based on the country code, country data, power prices, and distribution prices.

        Args:
            countryCode (str): The country code for the country where the electricity is being bought.
            countryData (CountryData): The country data object for the country where the electricity is being bought.
            powerPrices (list): A list of power prices for each hour.
            distributionPrices (list): A list of distribution prices for each hour.

        Returns:
            list: A list of buying prices for each hour.
        """
        if countryCode == "DK":
            return [
                (
                    powerPrices[t] * 1.15
                    + distributionPrices[t]
                    + countryData.transportTariff
                    + countryData.electricityTax
                )
                * (1 + countryData.vat)
                for t in range(len(powerPrices))
            ]
        elif countryCode == "SI":
            return [(price +
                countryData.transportTariff +
                countryData.feeSupportingRES + 
                countryData.feeMarketOperator + 
                countryData.feeExciseDutyOfElectricity) * (countryData.vat + 1) for price in powerPrices]
        elif countryCode == "EE":
            return [
                (
                    powerPrices[t]
                    + distributionPrices[t] # assuming that distribution price includes RES levy and electricity price duty
                )
                *  (1 + (countryData.vat if self.requestData.systemType in ["house", "building"] else 0))
                for t in range(len(powerPrices))
            ]
        else:
            return [price * 1.15 for price in powerPrices]
