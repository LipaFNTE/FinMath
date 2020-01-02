import enum
import numpy as np

class GreekMethod(enum.Enum):
    TRAJECTORY_DIFFERENTIATION = 1
    LIKELIHOOD_RATIO = 2