import numpy as np
import scipy.stats as sts

from OptionPricing.Instrument import Instrument
from MonteCarlo import QuasiMonteCarlo as qmc


class BS(Instrument):
    def __init__(self, s_0, K, T, r, mu, sigma, q, monte_carlo: bool, quasi: qmc.QMC = None):
        super().__init__(s_0, K, T, r, mu, sigma)
        self.q = q
        if ~monte_carlo:
            quasi = False
        if monte_carlo:
            self.quasi = quasi
            self.n = len(self.T)
            self.Z = []
            self.s = self.generate_trajectory(True)

    def instr_price(self):
        return self.s_0 * np.exp((self.r - 0.5 * (self.sigma ** 2)) * self.T + self.sigma * np.sqrt(self.T) * np.random.normal())

    def option_price(self, is_call: bool):
        if is_call:
            d1 = (np.log(self.s_0 / self.K) + (self.r - self.q + 0.5 * self.sigma ** 2) * self.T) / (
                    self.sigma * np.sqrt(self.T))
            d2 = (np.log(self.s_0 / self.K) + (self.r - self.q - 0.5 * self.sigma ** 2) * self.T) / (
                    self.sigma * np.sqrt(self.T))
            v1 = self.s_0 * np.exp(-self.q * self.T) * sts.norm.cdf(d1, 0.0, 1.0)
            v2 = self.K * np.exp(-self.r * self.T) * sts.norm.cdf(d2, 0.0, 1.0)
            return v1 - v2
        else:
            d1 = (np.log(self.s_0 / self.K) + (self.r - self.q + 0.5 * self.sigma ** 2) * self.T) / (
                    self.sigma * np.sqrt(self.T))
            d2 = (np.log(self.s_0 / self.K) + (self.r - self.q - 0.5 * self.sigma ** 2) * self.T) / (
                    self.sigma * np.sqrt(self.T))
            v1 = self.K * np.exp(-self.r * self.T) * sts.norm.cdf(-d2, 0.0, 1.0)
            v2 = self.s_0 * np.exp(-self.q * self.T) * sts.norm.cdf(-d1, 0.0, 1.0)
            return v1 - v2

    def generate_trajectory(self, ret_value: bool):
        _z = list(np.random.normal(size=self.n))
        self.Z = _z
        _s = [self.s_0 * np.exp((self.r - 0.5 * self.sigma ** 2) * (self.T[1] - self.T[0]) +
                                self.sigma * np.sqrt(self.T[1] - self.T[0]) * self.Z[0])]
        for i in range(1, self.n):
            _s.append(_s[i - 1] * np.exp((self.r - 0.5 * self.sigma ** 2) * (self.T[i] - self.T[i - 1]) +
                                         self.sigma * np.sqrt(self.T[i] - self.T[i - 1]) * self.Z[i]))
        if ret_value:
            return _s
        else:
            self.s = _s

    def generate_price(self, n: int = 1):
        pass


    def generate_multivariate_price(self, dimension: int, cov_matrix, n: int = 1):
        pass