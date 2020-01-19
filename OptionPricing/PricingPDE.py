import numpy as np
import enum
from OptionPricing import Payoff
from numpy import matrix
import numpy as np


class MethodPDE(enum.Enum):
    EXPLICITE = 1
    IMPLICIT = 2
    IMEX = 3


class PricingPDE:
    def __init__(self, method: MethodPDE):
        self.method = MethodPDE

    def pricing_european_option(self, sigma, r, K, T, L, M, N, theta, payoff: Payoff.ClassicPayoff):
        t, s = self._generate_grid(T, L, M, N)
        dt, ds = self._generate_deltas(T, L, M, N)
        alpha, beta, gamma = self._generate_params(sigma, r, T, L, M, N)
        A = self.create_A_matrix(sigma, r, T, L, M, N)
        prev = [payoff.payoff_function(i, r, T, K) for i in s]
        T_calc = self._calculate_T(dt, theta, A, N)
        v = []
        for i in range(M - 2, -1, -1):
            d_i = [alpha[0]*payoff.payoff_function(s[0], r, t[i], K)] + [0 for _ in range(N - 2)] + [gamma[len(gamma) - 1]*payoff.payoff_function(s[len(s) - 1], r, t[i], K)]
            d_i1 = [alpha[0] * ds * payoff.payoff_function(s[0], r, t[i], K)] + [0 for _ in range(N - 2)] + [
                gamma[len(gamma) - 1] * ds * payoff.payoff_function(s[len(s) - 1], r, t[i], K)]
            v1 = np.dot((np.identity(N) + dt * (1 - theta) * A), prev)
            v2 = [dt * w for w in [sum(x) for x in zip([theta * i for i in d_i], [(1 - theta) * s for s in d_i1])]]
            fin_b = [sum(x) for x in zip(v1, v2)]
            v.append(np.linalg.solve(T_calc, np.transpose(fin_b[0])))

        return v[len(v) - 1]

    def _calculate_T(self, dt, theta, A, N):
        return np.identity(N) - dt * theta * A

    def _generate_deltas(self, T, L, M, N):
        return T / M, L / (N + 1)

    def _generate_grid(self, T, L, M, N):
        dt, ds = self._generate_deltas(T, L, M, N)
        t = [i * dt for i in range(M)]
        s = [0 + k * ds for k in range(1, N + 1)]
        return t, s

    def _generate_params(self, sigma, r, T, L, M, N):
        t, s = self._generate_grid(T, L, M, N)
        dt, ds = self._generate_deltas(T, L, M, N)
        alpha = [0.5 * ((pow(sigma * s[j - 1], 2) / pow(ds, 2)) - ((r * s[j - 1]) / ds)) for j in
                 range(1, N + 1)]
        gamma = [0.5 * ((pow(sigma * s[j - 1], 2) / pow(ds, 2)) + ((r * s[j - 1]) / ds)) for j in
                 range(1, N + 1)]
        beta = [-((pow(sigma * s[j - 1], 2) / pow(ds, 2)) + r) for j in range(1, N + 1)]
        return alpha, beta, gamma

    def _generate_boundaries(self, r, K, T, L, M, N):
        t, s = self._generate_grid(T, L, M, N)
        v_0 = [K * np.exp(-r * (T - t_i)) for t_i in t]
        v_N = []
        return v_0, v_N

    def create_A_matrix(self, sigma, r, T, L, M, N):
        alpha, beta, gamma = self._generate_params(sigma, r, T, L, M, N)
        res = [[beta[0], gamma[0]] + [0 for _ in range(N - 2)]]
        for i in range(1, N - 2):
            if i == 1:
                res.append([alpha[i], beta[i], gamma[i]] + [0 for _ in range(N - 3)])
            else:
                res.append([0 for _ in range(i - 1)] + [alpha[i], beta[i], gamma[i]] + [0 for _ in range(N - 2 - i)])
        res.append([0 for _ in range(N - 3)] + [alpha[N - 2], beta[N - 2], gamma[N - 2]])
        res.append([0 for _ in range(N - 2)] + [alpha[N - 1], beta[N - 1]])
        return matrix(res)

    def create_d_vector(self):
        pass


if __name__ == '__main__':
    pricing = PricingPDE(MethodPDE.IMEX)
    v = pricing.pricing_european_option(0.2, 0.02, 100, 1, 160, 5000, 750, 0.5, Payoff.ClassicPayoff(True))
    print(v)
