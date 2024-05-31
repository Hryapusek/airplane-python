from enum import Enum


# This class represents the different states of the system
class State(Enum):
    # The system is in the first distance state
    DISTANCE_1 = 1
    # The system is in the second distance state
    DISTANCE_2 = 2
    # The system is in the third distance state
    DISTANCE_3 = 3
    # The system is in the safe distance state
    SAFE_DISTANCE = 4
