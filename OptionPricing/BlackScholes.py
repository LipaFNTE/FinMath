import numpy as np
import scipy.stats as sts


class BS:
    def __init__(self, mu, sigma, r, q, S_0, K, T):
        self.mu = mu
        self.sigma = sigma
        self.r = r
        self.q = q
        self.S_0 = S_0
        self.K = K
        self.T = T

    def instr_price(self):
        return self.S_0*np.exp((self.mu - self.sigma**2)*self.T + self.sigma*np.random.normal())

    def option_price(self, is_call: bool):
        if is_call:
            d1 = (np.log(self.S_0 / self.K) + (self.r - self.q + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))
            d2 = (np.log(self.S_0 / self.K) + (self.r - self.q - 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))
            v1 = self.S_0 * np.exp(-self.q * self.T) * sts.norm.cdf(d1, 0.0, 1.0)
            v2 = self.K * np.exp(-self.r * self.T) * sts.norm.cdf(d2, 0.0, 1.0)
            return v1 - v2
        else:
            d1 = (np.log(self.S_0 / self.K) + (self.r - self.q + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))
            d2 = (np.log(self.S_0 / self.K) + (self.r - self.q - 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))
            v1 = self.K * np.exp(-self.r * self.T) * sts.norm.cdf(-d2, 0.0, 1.0)
            v2 = self.S_0 * np.exp(-self.q * self.T) * sts.norm.cdf(-d1, 0.0, 1.0)
            return v1 - v2

