import numpy as np
from OptionPricing import Instrument, utils

class Payoff:
    def __init__(self, instrument: Instrument, call):
        self.instrument = instrument
        self.call = call

    def payoff_function(self):
        pass

    def delta(self, method: utils.GreekMethod):
        pass

    def gamma(self, method: utils.GreekMethod):
        pass

    def vega(self, method: utils.GreekMethod):
        pass

    def omega(self, method: utils.GreekMethod):
        pass


class ClassicPayoff(Payoff):
    def __init__(self, instrument: Instrument, call):
        super().__init__(instrument, call)


class TrajectoryPayoff(Payoff):
    def __init__(self, instrument: Instrument, call):
        super().__init__(instrument, call)

    def payoff_function(self):
        pass


class BarrierOut(TrajectoryPayoff):
    def __init__(self, A, B, instrument: Instrument, call):
        super().__init__(instrument, call)
        self.A = A
        self.B = B

    def payoff_function(self):
        for i in range(len(self.s)):
            if (self.s[i] <= self.A) | (self.s[i] >= self.B):
                return 0
        if self.call:
            return max(self.s[len(self.s) - 1] - self.K, 0) * np.exp(-self.r * self.T)
        else:
            return max(self.K - self.s[len(self.s) - 1], 0) * np.exp(-self.r * self.T)


class Asian(TrajectoryPayoff):
    def __init__(self, instrument: Instrument, call):
        super().__init__(instrument, call)
        self.t = instrument.T

    def payoff_function(self):
        s_ = np.mean(self.instrument.s)

        if self.call:
            return max(s_ - self.instrument.K, 0) * np.exp(-self.instrument.r * self.instrument.T)
        else:
            return max(self.instrument.K - s_, 0) * np.exp(-self.instrument.r * self.instrument.T)

    def delta(self, method: utils.GreekMethod):
        if method == utils.GreekMethod.TRAJECTORY_DIFFERENTIATION:
            ind = self.get_indicator()
            return np.exp(- self.instrument.r * self.instrument.T) * ind *\
                   np.mean(self.instrument.s) / self.instrument.s[0]
        if method == utils.GreekMethod.LIKELIHOOD_RATIO:
            pass

    def vega(self, method: utils.GreekMethod):
        if method == utils.GreekMethod.LIKELIHOOD_RATIO:
            ind = self.get_indicator()
            sig_diff = self.sigma_diff()
            return np.exp(- self.instrument.r * self.instrument.T) * ind * sig_diff
        if method == utils.GreekMethod.LIKELIHOOD_RATIO:
            pass

    def sigma_diff(self):
        _s = []
        for i in range(1, len(self.instrument.s)):
            v1 = 0
            for j in range(1, i):
                v1 = v1 + np.sqrt(self.t[j] - self.t[j - 1]) * np.random.normal()
            _s.append(self.instrument.s[i] * (- self.instrument.sigma * self.t[i] + v1))
        return np.mean(_s)

    def get_indicator(self):
        if self.call:
            return np.mean(self.instrument.s) > self.instrument.K
        else:
            return self.instrument.K - np.mean(self.instrument.s)
