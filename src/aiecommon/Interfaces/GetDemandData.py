import pandas as pd
import numpy as np

import sys; sys.path.append('../..')
from ..DataModels import RequestData


class GetDemandData:
    def __init__(self, path, request: RequestData) -> None:
        self.path = path
        self.dataRequest = request
        # Read demand data
        self._demand_data = pd.read_csv(f"{path}/PowerConsumption.csv", sep=';')
        # Calculate total ev and heat pump consumption
        # if ev exists or is planned but there is no data on km per day, assign 35 km per day
        self.dataRequest.kilometersPerDayPlanned = 35 if self.dataRequest.electricVehiclePlanned and self.dataRequest.kilometersPerDayPlanned is None else self.dataRequest.kilometersPerDayPlanned
        self.dataRequest.kilometersPerDayExists = 35 if self.dataRequest.electricVehicleExists and self.dataRequest.kilometersPerDayExists is None else self.dataRequest.kilometersPerDayExists
        self.total_ev_consumption_planned = self._get_total_ev_consumption_planned() if self.dataRequest.electricVehiclePlanned else None
        self.total_ev_consumption_exists = self._get_total_ev_consumption_exists() if self.dataRequest.electricVehicleExists else None
        self.total_heat_pump_consumption_planned = self._get_total_heat_pump_consumption() if self.dataRequest.heatPumpPlanned else None
        self.total_heat_pump_consumption_exists = self._get_total_heat_pump_consumption() if self.dataRequest.heatPumpExists else None
        # Return hourly demand data
        self.Demand = self._return_hourly_demand_data(self)
        
    def _return_hourly_demand_data(self, path):
        '''
        Here we return the hourly demand data, taking into account possible PLANNED ev and heat pump consumption
        As well as HP and EV consumption that already exists
        - if planned, we ADD the consumption with corresponding profile to the general electricity consumption
        - if exists, we DEDUCT the specific consumption from the total consumption that the user enter,
        assign the specific HP and EV consumption to the correct profile
        - and finally we sum up all three possible consumption profiles (general, HP, EV) to get the total demand profile
        '''
        return self.sum_lists(self._returnGenericElectricityConsumptionData(), self._returnElectricVehicleDemandData(), self._returnHeatPumpDemandData())
        
        
    def _returnElectricVehicleDemandData(self):
        '''
        this function returns hourly demand data for electric vehicle
        it works both for planned and existing ev, as well as the combination of the two
        it returns ABSOLUTE hourly values, not normalized
        '''
        if self.total_ev_consumption_planned is not None:
            # Read ev demand data
            self._ev_demand_data_planned = pd.read_csv(f"{self.path}/PowerConsumptionElectricVehicleOnly.csv", delimiter=";")
            # normalize ev consumption data and multiply with total ev consumption
            self._ev_demand_data_planned = self._normalise_ev_consumption_data(self._ev_demand_data_planned, self.total_ev_consumption_planned)
        else: #assign zeros to ev demand data
            self._ev_demand_data_planned = list(np.zeros(8760))
        #
        if self.total_ev_consumption_exists is not None:
            #Read ev demand data
            self._ev_demand_data_exists = pd.read_csv(f"{self.path}/PowerConsumptionElectricVehicleOnly.csv", delimiter=";")
            # normalize ev consumption data and multiply with total ev consumption
            self._ev_demand_data_exists = self._normalise_ev_consumption_data(self._ev_demand_data_exists, self.total_ev_consumption_exists)
        else: #assign zeros to ev demand data
            self._ev_demand_data_exists = list(np.zeros(8760))
        # return the sum of the two ev demand data
        return self._ev_demand_data_planned + self._ev_demand_data_exists
    
    def _returnHeatPumpDemandData(self):
        '''
        this function returns hourly demand data for heat pump
        it works both for planned and existing heat pump, as well as the combination of the two
        it returns ABSOLUTE hourly values, not normalized
        '''
        if self.total_heat_pump_consumption_planned is not None:
            # Read heat pump demand data
            self._heat_pump_demand_data_planned = pd.read_csv(f"{self.path}/PowerConsumptionHeatPumpOnly.csv", delimiter=";")
            # normalize heat pump consumption data and multiply with total heat pump consumption
            self._heat_pump_demand_data_planned = self._normalise_heat_pump_consumption_data(self._heat_pump_demand_data_planned, self.total_heat_pump_consumption_planned) 
        else: #assign zeros to heat pump demand data
            self._heat_pump_demand_data_planned = list(np.zeros(8760))
        #
        if self.total_heat_pump_consumption_exists is not None:
            # Read heat pump demand data
            self._heat_pump_demand_data_exists = pd.read_csv(f"{self.path}/PowerConsumptionHeatPumpOnly.csv", delimiter=";")
            # normalize heat pump consumption data and multiply with total heat pump consumption
            self._heat_pump_demand_data_exists = self._normalise_heat_pump_consumption_data(self._heat_pump_demand_data_exists, self.total_heat_pump_consumption_exists)
        else: #assign zeros to heat pump demand data
            self._heat_pump_demand_data_exists = list(np.zeros(8760))
        # return the sum of the two heat pump demand data
        return self._heat_pump_demand_data_planned + self._heat_pump_demand_data_exists
    
    def _returnGenericElectricityConsumptionData(self):
        '''
        Here we return the hourly electricity demand of the generic consumption only
        '''
        totalConsumption = float(self.dataRequest.yearConsumptionKwh)
        # if total_ev_consumption_exists is not None we deduct it from the total consumption
        if self.total_ev_consumption_exists is not None:
            totalConsumption -= self.total_ev_consumption_exists
        # if total_heat_pump_consumption_exists is not None we deduct it from the total consumption
        if self.total_heat_pump_consumption_exists is not None:
            totalConsumption -= self.total_heat_pump_consumption_exists
        # we need to catch the exception if totalConsumption is negative now
        if totalConsumption < 0:
            totalConsumption = 500
        # return normalized generic consumption
        return self._normalise_consumption_data(totalConsumption)
            

    def _normalise_consumption_data(self, consumption):
        """REturn yearly consumption data

        Returns:
            list: Consumption Data
        """
        return list(
            self.aboslute_normalize_data(self._demand_data.iloc[:, 2])
            * float(consumption)
        )
        
    def _normalise_ev_consumption_data(self, EV_load_profile, EVconsumption):
        """Return yearly consumption data for electric vehicle

        Returns:
            list: Consumption Data
        """
        return list(
            self.aboslute_normalize_data(EV_load_profile.iloc[:, 2])
            * float(EVconsumption)) 
        
    def _normalise_heat_pump_consumption_data(self, HP_load_profile, HPconsumption):
        """Return yearly consumption data for heat pump

        Returns:
            list: Consumption Data
        """
        # Calculate total heat pump consumption in a year
        return list(
            self.aboslute_normalize_data(HP_load_profile.iloc[:, 2])
            * float(HPconsumption)) 
        
    def _sum_demand_profiles_and_normalize(self, demand_profile1, demand_profile2):
        """Sum two demand profiles and normalize

        Args:
            demand_profile1 (list): Demand profile 1
            demand_profile2 (list): Demand profile 2

        Returns:
            list: Sum of demand profiles
        """
        return list(
            self.aboslute_normalize_data(
                np.array(demand_profile1) + np.array(demand_profile2)
            )
        )

    def _get_total_ev_consumption_planned(self) -> float:
        return self.dataRequest.kilometersPerDayPlanned * 365 * 18 / 100 # (365 days * average km per day consumption of electric vehicle is 18 kWh/100km)
    
    def _get_total_ev_consumption_exists(self) -> float:
        return self.dataRequest.kilometersPerDayExists * 365 * 18 / 100 # (365 days * average km per day consumption of electric vehicle is 18 kWh/100km)
    
    def _get_total_heat_pump_consumption(self) -> float:
        return 6500 # TODO: Calculate this value from the heat pump data as a function of rooftop size
        
    @staticmethod
    def aboslute_normalize_data(column):
        return column / column.sum()

    @staticmethod
    def sum_lists(list1, list2, list3) -> list:
        return [x + y + z for x, y, z in zip(list1, list2, list3)]