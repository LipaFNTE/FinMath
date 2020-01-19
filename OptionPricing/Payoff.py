import numpy as np
from OptionPricing import Instrument, utils


class Payoff:
    def __init__(self, call):
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
    def __init__(self, call):
        super().__init__(call)

    def payoff_function(self, s_T, r, T, K):
        if self.call:
            return np.exp(-r * T) * max(s_T - K, 0)
        else:
            return np.exp(-r * T) * max(K - s_T, 0)


class TrajectoryPayoff(Payoff):
    def __init__(self, call):
        super().__init__(call)

    def payoff_function(self):
        pass


class BarrierOut(TrajectoryPayoff):
    def __init__(self, A, B, call):
        super().__init__(call)
        self.A = A
        self.B = B

    def payoff_function(self, s: list, r, T, K):
        for i in range(len(s)):
            if (s[i] <= self.A) | (s[i] >= self.B):
                return 0
        if self.call:
            return max(s[len(s) - 1] - K, 0) * np.exp(-r * T)
        else:
            return max(K - s[len(s) - 1], 0) * np.exp(-r * T)


class Asian(TrajectoryPayoff):
    def __init__(self, call):
        super().__init__(call)

    def payoff_function(self, s: list, K, r, T: list):
        s_ = np.mean(s)

        if self.call:
            return max(s_ - K, 0) * np.exp(
                -r * T[len(T) - 1])
        else:
            return max(K - s_, 0) * np.exp(
                -r * T[len(T) - 1])

    def delta(self, s: list, K, r, T: list, sigma, Z: list, method: utils.GreekMethod):
        if method == utils.GreekMethod.TRAJECTORY_DIFFERENTIATION:
            ind = self.get_indicator()
            return np.exp(- r * T[len(T) - 1]) * ind * \
                   np.mean(s) / s[0]
        if method == utils.GreekMethod.LIKELIHOOD_RATIO:
            return self.payoff_function(s, K, r, T) * Z[0] / \
                   (s[0] * sigma * np.sqrt(T[0]))

    def vega(self, s, K, r, T, method: utils.GreekMethod):
        if method == utils.GreekMethod.TRAJECTORY_DIFFERENTIATION:
            ind = self.get_indicator()
            sig_diff = self.sigma_diff()
            return np.exp(- r * T[len(T) - 1]) * ind * sig_diff
        if method == utils.GreekMethod.LIKELIHOOD_RATIO:
            return self.payoff_function(s, K, r, K) * self.get_vega_sum()

    def sigma_diff(self, s: list, T: list, sigma, Z: list):
        _s = []
        for i in range(1, len(s)):
            v1 = 0
            for j in range(1, i):
                v1 = v1 + np.sqrt(T[j] - T[j - 1]) * Z[j]
            _s.append(s[i] * (- sigma * T[i] + v1))
        return np.mean(_s)

    def get_indicator(self, s: list, K):
        if self.call:
            return int((np.mean(s) > K) == True)
        else:
            return int((K - np.mean(s)) == True)

    def get_vega_sum(self, T: list, sigma, Z: list):
        v = [(Z[0] ** 2 - 1) / sigma - Z[0] * np.sqrt(
            T[0])]
        for i in range(1, len(T)):
            (Z[i] ** 2 - 1) / sigma - Z[0] * np.sqrt(
                T[i] - T[i - 1])
        return sum(v)


class BasketOption(Payoff):
    def __init__(self):
        pass


class MinOption(BasketOption):
    pass


class MaxOption(BasketOption):
    pass


class Altiplano(BasketOption):
    pass


class Atlas(BasketOption):
    pass


class Himalaya(BasketOption):
    pass



