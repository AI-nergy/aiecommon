from aiecommon.Models import Location
from ..DataModels import TechnicalData, InputData, CountryData 
#from DataModels.CountryData import CountryData 

from ..Interfaces import GetSolarProductionData, GetPowerPricesData, GetDemandData, GetInvestmentData, GetEmissionsData
import pandas as pd
import json
import logging

class Scenario: 
    """
    A class representing a scenario of solar panel production and power consumption data for a given location in a specific country.
    
    Attributes:
        InputData (InputData): The request data to generate the scenario. 
        CountryData (CountryData): The relevant data about the target country.
        Location (LocationData): The data about the requested location.
        RoofTopsides (list): A list of integers representing the sides of rooftops available for installation.
        Demand (DemandData): The data about hourly power demand over one year.
        Production (ProductionData): The data about hourly solar production over one year.
        Prices (PowerPricesData): The data about hourly energy prices over one year.
        TimeWindow (range): A range object representing the time window over which the data is provided.
        TechnicalData (TechnicalData): The technical data about solar panels used in the scenario.
        InvestmentData (InvestmentData): The investment data relevant to the particular scenario.
        DiscardedRooftopSides (list): A list of rooftop sides that cannot be installed on due to capacity limitations.
    """
    
    def __init__(self, request: InputData) -> None:
        """
        Constructs all necessary attributes for the Scenario object.

        Args:
            request (InputData): The request data to generate the scenario.
        """
        self.InputData = request
        #self.CountryData = CountryData.from_json(path = "modules/aiesolar/optimizer/data/CountryData.json", request= request)
        self.CountryData = CountryData.from_json(path="modules/aiesolar/optimizer/data/shared/CountryData.json", key=request.location.countryCode)

        self.Location = request.location
        self.TechnicalData = TechnicalData.from_json(path="modules/aiesolar/optimizer/data/shared/TechnicalData.json")
        self.RoofTopsides = list(range(len(self.InputData.rooftopSummaryTable)))
        self.ConsumptionData = GetDemandData(path="modules/aiesolar/optimizer/data/shared", request= self.InputData, technicalData=self.TechnicalData)
        self.Demand = self.ConsumptionData.Demand
        logging.info(f"starting to get solar production data from external API")
        self.Production = GetSolarProductionData(request= self.InputData).Production
        logging.info(f"finished getting solar production data from external API")
        self.Prices = GetPowerPricesData(path="modules/aiesolar/optimizer/data", requestData=request, countryData = self.CountryData)
        self.co2_emissions = GetEmissionsData(path="modules/aiesolar/optimizer/data", requestData=request, countryData = self.CountryData).co2_emissions
        self.TimeWindow = range(len(self.Demand)) # one year houly data
        self.InvestmentData = GetInvestmentData(
                    countryData=self.CountryData, technicalData=self.TechnicalData
                )
        self.DiscardedRooftopSides = []

            
        
        
    
    