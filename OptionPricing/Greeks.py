import numpy as np
import enum
from OptionPricing import Payoff, Instrument, utils





class Greeks:
    def __init__(self, instrument: Instrument, payoff: Payoff, method: utils.GreekMethod, n: int):
        self.payoff = payoff
        self.instrument = instrument
        self.method = method
        self.n = n

    def calculate_greeks(self, gr: list):
        for i in range(len(self.n)):
            s_ = self._generate_trajectory()
            d = self.payoff.delta()
            g = self.payoff.gamma()
            v = self.payoff.vega()
            o = self.payoff.omega()

    def _generate_trajectory(self):
        pass


