import numpy as np
import enum
from MonteCarlo import SequenceGenerator
from OptionPricing import Instrument
import matplotlib.pyplot as plt


class RandomVariable(enum.Enum):
    GAUSSIAN = 0
    EXPON = 1


class RandomGeneratorMethod(enum.Enum):
    INVERSION_METHOD = 0
    ACCEPT_REJECT = 1
    BOX_MULLER = 2
    MARSAGLIA_BRAY = 3



class QMC:
    def __init__(self, sequence_type: SequenceGenerator.SequenceGenerator):
        self.sequence_gen = sequence_type

    def generate_rv(self, seq0_gen, seq1_gen, rv: RandomVariable, method: RandomGeneratorMethod, n: int):
        result = []
        seq0 = seq0_gen.generate_sequence(int(n/2) + 1)
        seq1 = seq1_gen.generate_sequence(int(n/2) + 1)
        if method == RandomGeneratorMethod.BOX_MULLER:
            if rv == RandomVariable.GAUSSIAN:
                for i in range(int(np.ceil(n/2))):
                    u, v = seq0[i], seq1[i]
                    r = np.sqrt(-2 * np.log(1 - u))
                    result.append(r * np.cos(2 * np.pi * v))
                    result.append(r * np.sin(2 * np.pi * v))
        return result[:n]

    def generate_multivariate_rv(self):
        pass


class RQMC(QMC):
    def __init__(self, sequence_type: SequenceGenerator.SequenceGenerator):
        super().__init__(sequence_type)


if __name__ == '__main__':
    seq0 = SequenceGenerator.SequenceGenerator(SequenceGenerator.TypeSeq.VAN_DER_CORPUT, 3)
    seq1 = SequenceGenerator.SequenceGenerator(SequenceGenerator.TypeSeq.VAN_DER_CORPUT, 2)
    qmc = QMC(seq0)
    res = qmc.generate_rv(seq0, seq1, RandomVariable.GAUSSIAN, RandomGeneratorMethod.BOX_MULLER, 100000)
    print(np.min(res))
    plt.hist(res)
    plt.show()
