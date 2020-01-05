import enum

import numpy as np

from OptionPricing.BlackScholes import BS
from OptionPricing import Payoff, Instrument, utils


class Greek(enum.Enum):
    DELTA = 1
    GAMMA = 2
    VEGA = 3
    OMEGA = 4


class Greeks:
    def __init__(self, instrument: BS, payoff: Payoff, method: utils.GreekMethod, n: int):
        self.payoff = payoff
        self.instrument = instrument
        self.method = method
        self.n = n

    def calculate_greeks(self, gr: list):
        data = {}
        for i in range(self.n):
            self.instrument.generate_trajectory(False)
            for greek in gr:
                if greek not in data.keys():
                    data[greek] = [getattr(self.payoff, greek)(self.method)]
                else:
                    data[greek].append(getattr(self.payoff, greek)(self.method))
        greeks = {}
        for greek in gr:
            greeks[greek] = [np.mean(data[greek]), np.std(data[greek])/np.sqrt(self.n)]

        return greeks


if __name__ == '__main__':
    bs = BS(0, 0.2, 0.05, 0, 100, 100, [i/12 for i in range(1, 13)], True)

    greeks = {}
    for k in range(1000, 10000, 1000):
        g = Greeks(bs, Payoff.Asian(bs, True), utils.GreekMethod.TRAJECTORY_DIFFERENTIATION, k)
        greeks[k] = g.calculate_greeks(['delta'])

    print(greeks)
