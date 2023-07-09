from pydantic import BaseModel, validator
from ..Models import BiddingRegion, PricesTechnologies
from typing import Optional
from .RequestData import RequestData
import json
from aiecommon.Exceptions import AieException
import logging

class CountryData(BaseModel):
    investmentSubsidy: float
    biddingRegions: list[BiddingRegion]
    priceTechnology: PricesTechnologies
    labourHourRateEUR: Optional[float]
    permittingCostsEUR: Optional[float]
    materialFixedCost: Optional[float]
    annualizationRate: Optional[float]
    discountCoefficient: Optional[float]
    penaltySellingPowerPrice: Optional[float]
    transportTariff: Optional[float] 
    vat: Optional[float]
    electricityTax: Optional[float]
    limitGridExport: Optional[float] = 1.0 # Percentage of the total capacity
    feeSupportingRES : Optional[float] 
    feeMarketOperator : Optional[float]  
    feeExciseDutyOfElectricity : Optional[float] 
    feeForSupportingEfficencyImprovements : Optional[float]
    feeForAvailablePowerInstallation : Optional[float]
        
    # Define function: from_json
    # This function reads a JSON file and returns an object of CountryData class.

    def from_json(path: str, request: RequestData = None):
        # Open the specified JSON file
        with open(path, 'r') as f:
            # Load the contents of the file into a Python object using json library
            country_data = json.loads(f.read())

        # Check if input countryCode is present in the loaded data or not.
        if request.location.countryCode.upper() not in country_data:
            # If not raise an AieException.COUNTRY_NOT_SUPPORTED_FOR_OPTIMIZATION exception
            logging.error(f"Country code {request.location.countryCode} not supported")
            raise AieException(AieException.COUNTRY_NOT_SUPPORTED_FOR_OPTIMIZATION)
        
        # Return an instance of CountryData class representing data for the input country code
        return CountryData(**country_data[request.location.countryCode])