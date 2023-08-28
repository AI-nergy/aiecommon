import pandas as pd
import json
import logging

from ..DataModels import CountryData 
from .Location import Location
from .TechnicalData import TechnicalData
from .InputData import InputData
from ..Interfaces import GetSolarProductionData, GetPowerPricesData, GetDemandData, GetInvestmentData, GetEmissionsData

class Scenario: 
    """
    A class representing a scenario of solar panel production and power consumption data for a given location in a specific country.
    
    Attributes:
        InputData (InputData): The input data to generate the scenario. 
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
    
    def __init__(self, input_data: InputData) -> None:
        """
        Constructs all necessary attributes for the Scenario object.

        Args:
            input_data (InputData): The input data to generate the scenario.
        """
        self.InputData = input_data
        #logging.info(self.InputData)
        #self.CountryData = CountryData.from_json(path = "modules/aiesolar/optimizer/data/CountryData.json", input_data=input_data)
        self.CountryData = CountryData.from_json(path="modules/aiesolar/optimizer/data/shared/CountryData.json", key=self.InputData.location.countryCode)

        self.Location = input_data.location
        self.TechnicalData = TechnicalData.from_json(path="modules/aiesolar/optimizer/data/shared/TechnicalData.json")
        self.RoofTopsides = list(range(len(self.InputData.rooftopResult.rooftopSummaryTable)))
        self.ConsumptionData = GetDemandData(path="modules/aiesolar/optimizer/data/shared", input_data= self.InputData, technicalData=self.TechnicalData)
        self.Demand = self.ConsumptionData.Demand
        logging.info(f"starting to get solar production data from external API")
        self.Production = GetSolarProductionData(input_data= self.InputData).Production
        logging.info(f"finished getting solar production data from external API")
        self.Prices = GetPowerPricesData(path="modules/aiesolar/optimizer/data", input_data=input_data, countryData = self.CountryData)
        self.co2_emissions = GetEmissionsData(path="modules/aiesolar/optimizer/data", input_data=input_data, countryData = self.CountryData).co2_emissions
        self.TimeWindow = range(len(self.Demand)) # one year houly data
        self.InvestmentData = GetInvestmentData(
                    countryData=self.CountryData, technicalData=self.TechnicalData
                )
        self.DiscardedRooftopSides = []

            
        
        
    
    