import numpy as np
import enum
from MonteCarlo import SequenceGenerator
from OptionPricing import Instrument


class RandomVariable(enum.Enum):
    GAUSSIAN = 1
    EXPON = 2


class QMC:
    def __init__(self, sequence_type: SequenceGenerator.TypeSeq):
        self.sequence_type = sequence_type

    def generate_rv(self, instrument: Instrument, n: int):
        pass

    def generate_multivariate_rv(self):
        pass


class RQMC(QMC):
    def __init__(self, sequence_type: SequenceGenerator.TypeSeq):
        super().__init__(sequence_type)