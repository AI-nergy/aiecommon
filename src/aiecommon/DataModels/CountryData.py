from pydantic import BaseModel, validator
from typing import Optional
import json
import logging

from ..Models import BiddingRegion, PricesTechnologies
from ..Exceptions import AieException
from .data_model_base import DataModelBase

class CountryData(DataModelBase):
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

    @classmethod
    def _validate(cls, data, key):
        """
        Validate the data after loading from file, raises an exception if validation doesn't pass.

        Args:
            data: dict Data to validate
            key: str Key of the country 
        Returns:
            None
        """

        # Check if input countryCode is present in the loaded data or not.
        if key.upper() not in data:
            # If not raise an AieException.COUNTRY_NOT_SUPPORTED_FOR_OPTIMIZATION exception
            logging.error(f"Country code {key} not supported for optimisation")
            raise AieException(AieException.COUNTRY_NOT_SUPPORTED_FOR_OPTIMIZATION)
