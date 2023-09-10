from pydantic import BaseModel, validator
from typing import Optional
import json
import logging

from .BiddingRegion import BiddingRegion
from .PricesTechnologies import PricesTechnologies
from ..Exceptions import AieException
from .data_model_base import DataModelBase

class CountryData(DataModelBase):
    investmentSubsidy: float
    biddingRegions: list[BiddingRegion]
    priceTechnology: PricesTechnologies
    labourHourRateEUR: Optional[float] = None
    permittingCostsEUR: Optional[float] = None
    materialFixedCost: Optional[float] = None
    annualizationRate: Optional[float] = None
    discountCoefficient: Optional[float] = None
    penaltySellingPowerPrice: Optional[float] = None
    transportTariff: Optional[float] = None
    vat: Optional[float] = None
    electricityTax: Optional[float] = None
    limitGridExport: Optional[float] = 1.0 # Percentage of the total capacity
    feeSupportingRES : Optional[float] = None
    feeMarketOperator : Optional[float] = None
    feeExciseDutyOfElectricity : Optional[float] = None
    feeForSupportingEfficencyImprovements : Optional[float] = None
    feeForAvailablePowerInstallation : Optional[float] = None
    feeSupportingRES : Optional[float] 
    feeMarketOperator : Optional[float]  
    feeExciseDutyOfElectricity : Optional[float] 
    feeForSupportingEfficencyImprovements : Optional[float]
    feeForAvailablePowerInstallation : Optional[float]
    renewableEnergyLevy : Optional[float]
    electricityExerciseDuty : Optional[float]
    connectionFeeMonthly: Optional[dict]
    peakConsumptionFeeMonthlyPerKw: Optional[dict]
    deliveryCostPeak: Optional[float]
    deliveryCostOffPeak: Optional[float]
    feedInTariffPeak: Optional[float]
    feedInTariffOffPeak: Optional[float]
    electricityTax: Optional[float]
    fixedDeliveryCost: Optional[float]
    gridManagementCost: Optional[float]
    reductionEnergyTax: Optional[float]
    feedInFactor: Optional[float]

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

