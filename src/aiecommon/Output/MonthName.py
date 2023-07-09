# TODO: switch to enum module when we move to python 3.11
#from enum import StrEnum
from enum import Enum

# make MonthName an enum class that returns the name of the month as string
class MonthName(Enum):
    Jan = 0
    Feb = 1
    Mar = 2
    Apr = 3
    May = 4
    Jun = 5
    Jul = 6
    Aug = 7
    Sep = 8
    Oct = 9
    Nov = 10
    Dec = 11
