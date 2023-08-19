from typing import Optional
import sys; sys.path.append('../..')
from aiecommon.DataModels import CountryData
from aiecommon.Models import TechnicalData


class GetInvestmentData:

    def __init__(self, countryData: CountryData, technicalData: TechnicalData) -> None:
        self.countryData = countryData
        self.technicalData = technicalData
        self.annualised_fixed_term_pv = self._calculate_annualised_fixed_term_pv()
        self.annualised_fixed_term_inverter = self._calculate_annualised_fixed_term_inverter()
        self.annualised_fixed_term_battery = self._calculate_annualised_fixed_term_battery()
        self.annualised_variable_term_pv = self._calculate_annualised_variable_term_pv()
        self.annualised_variable_term_inverter = self._calculate_annualised_variable_term_inverter()
        self.annualised_variable_term_battery = self._calculate_annualised_variable_term_battery()

    def _annualise(self, cost: float, lifetime: float) -> float:
        """Calculates the annualised cost of an investment."""
        if self.countryData.discountCoefficient > 0:
            annualizationRate = 1/(((1+self.countryData.discountCoefficient)**lifetime - 1)/
                (self.countryData.discountCoefficient * (1 + self.countryData.discountCoefficient)**lifetime))
        if self.countryData.discountCoefficient == 0:
            annualizationRate = 1 / lifetime
        return cost * annualizationRate


    def _calculate_annualised_fixed_term_pv(self) -> float:
        """Capacity-independent PV investment cost."""

        base_cost = self.countryData.priceTechnology.fixTerm.pvPanels + self.countryData.materialFixedCost + \
            self.countryData.permittingCostsEUR + self.countryData.labourHourRateEUR * \
            self.technicalData.Photovoltaic.labourHours

        return self._annualise(
            cost=base_cost, lifetime=self.technicalData.Photovoltaic.lifetime)

    def _calculate_annualised_fixed_term_inverter(self) -> float:
        """Capacity-independent inverter investment cost."""
        base_cost = self.countryData.priceTechnology.fixTerm.inverters
        return self._annualise(
            cost=base_cost, lifetime=self.technicalData.Inverter.lifetime)

    def _calculate_annualised_fixed_term_battery(self) -> float:
        """Capacity-independent battery investment cost."""
        base_cost = self.countryData.priceTechnology.fixTerm.batteries
        return self._annualise(
            cost=base_cost, lifetime=self.technicalData.Battery.lifetime)

    def _calculate_annualised_variable_term_pv(self) -> float:
        """Capacity-dependent PV investment cost."""
        base_cost = self.countryData.priceTechnology.variableTerm.pvPanels
        return self._annualise(
            cost=base_cost, lifetime=self.technicalData.Photovoltaic.lifetime)

    def _calculate_annualised_variable_term_inverter(self) -> float:
        """Capacity-dependent inverter investment cost."""
        base_cost = self.countryData.priceTechnology.variableTerm.inverters
        return self._annualise(
            cost=base_cost, lifetime=self.technicalData.Inverter.lifetime)

    def _calculate_annualised_variable_term_battery(self) -> float:
        """Capacity-dependent battery investment cost."""
        base_cost = self.countryData.priceTechnology.variableTerm.batteries
        return self._annualise(
            cost=base_cost, lifetime=self.technicalData.Battery.lifetime)
