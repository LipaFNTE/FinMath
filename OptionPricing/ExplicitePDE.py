import pandas as pd
import numpy as np

class ExplicitePDE:
    def __init__(self, L_m, L_p, N, M, T, sigma, r, K):
        self.L_m = L_m
        self.L_p = L_p
        self.N = N
        self.M = M
        self.T = T
        self.dt = self.T/self.M
        self.ds = (self.L_p - self.L_m)/(self.N + 1)
        self.sigma = sigma
        self.r = r
        self.K = K

    def _generate_grid(self):
        t = [i*self.dt for i in range(self.M)]
        s = [self.L_m + k*self.ds for k in range(1, self.N + 1)]
        return t, s

    def _generate_params(self):
        t, s = self._generate_grid()
        alpha = [0.5*(pow(self.sigma*s[j - 1], 2)/pow(self.ds, 2) - (self.r * s[j - 1])/(self.ds)) for j in range(1, self.N + 1)]
        gamma = [0.5*(pow(self.sigma*s[j - 1], 2)/pow(self.ds, 2) + (self.r * s[j - 1])/(self.ds)) for j in range(1, self.N + 1)]
        beta = [-((pow(self.sigma*s[j - 1], 2)/pow(self.ds, 2)) + self.r) for j in range(1, self.N + 1)]
        return alpha, beta, gamma

    def _generate_boundaries(self):
        t, s = self._generate_grid()
        v_0 = [self.K * np.exp(-self.r * (self.T - t_i)) for t_i in t]
        v_N = []
        return v_0, v_N

    def _explicite_schema(self, f):
        alpha, beta, gamma = self._generate_params()
        v_0, v_N = self._generate_boundaries()
        prev = f
        now = []
        for i in range(self.M - 1, -1, -1):
            term_1 = (1 + self.dt * beta[0]) * prev[0] + self.dt * gamma[0] * prev[1] + self.dt * alpha[0] * v_0[i + 1]
            for j in range(2, self.N - 1):
                pass
            term_N = self.dt * alpha[self.N - 1] * prev[self.N - 2] + (1 + self.dt * beta[self.N - 1]) * prev[self.N - 1] + self.dt * gamma[self.N - 1] * v_N[i + 1]


if __name__ == '__main__':
    pass