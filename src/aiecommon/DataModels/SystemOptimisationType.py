from enum import Enum

class SystemOptimisationType(str, Enum):
    SYSTEM_OPTIMISATION_TYPE_PV_ONLY = 'SYSTEM_OPTIMISATION_TYPE_PV_ONLY'
    SYSTEM_OPTIMISATION_TYPE_BATTERY_ONLY = 'SYSTEM_OPTIMISATION_TYPE_BATTERY_ONLY'
    SYSTEM_OPTIMISATION_TYPE_PV_AND_BATTERY = 'SYSTEM_OPTIMISATION_TYPE_PV_AND_BATTERY'

    @staticmethod
    def optimizationOnlyAllowedTypes():
        return [
            SystemOptimisationType.SYSTEM_OPTIMISATION_TYPE_BATTERY_ONLY
        ]