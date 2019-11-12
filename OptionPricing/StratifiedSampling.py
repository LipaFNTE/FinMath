import numpy as np
from scipy.stats import norm
import OptionPricing.Payoff

import pandas as pd


class StratifiedSampling:
    def __init__(self, n, k, T, r, mu, sigma, s_0, K, m=0):
        self.n = n
        self.k = k
        self.T = T
        self.r = r
        self.mu = mu,
        self.sigma = sigma
        self.s_0 = s_0
        self.K = K
        self.M = m

    def run(self, trajectory: bool, payoff: OptionPricing.Payoff, call: bool):
        if trajectory:
            return self.trajectory_ss(self.generate_u(), payoff, call)
        else:
            return self.bs_ss(self.generate_u())

    def generate_u(self):
        u = []
        for i in range(self.k):
            temp_u = []
            for j in range(int(self.n / self.k)):
                temp_u.append(np.random.rand())
            u.append(temp_u)
        return u

    def bs_ss(self, u):
        y_i_j = []
        y_i = []
        for i in range(self.k):
            u_i: list = u[i]
            for j in range(int(self.n / self.k)):
                temp_v = (i - 1 + u_i[j]) / self.k
                temp_w = np.sqrt(self.T) * norm.ppf(temp_v)
            y_i.append(np.mean(y_i_j))
        y_ss = (1/self.n) * np.mean(y_i)
        return y_ss

    def trajectory_ss(self, u, payoff: OptionPricing.Payoff.TrajectoryPayoff, call: bool):
        var_y_i = []
        y_i = []
        t = self.generate_time(True)
        for i in range(1, self.k):
            y_temp = []
            u_i: list = u[i]
            for j in range(int(self.n / self.k)):
                temp_v = (i - 1 + u_i[j]) / self.k
                w_T = np.sqrt(self.T) * norm.ppf(temp_v)
                w_t = self.generate_brownian_bridge(w_T, t)
                s = self.generate_s_trajectory(w_t, t)
                y_temp.append(payoff.payoff_function(s, self.K, self.T, self.r, call))
            var_y_i.append(np.var(y_temp))
            y_i.append(np.mean(y_temp))
        var_ss = (1/self.k) * (1/self.n) * sum(var_y_i)
        res = Result(self.n, self.k, self.M, np.mean(y_i), var_ss, np.sqrt(var_ss)/np.sqrt(self.n))
        return res

    def generate_time(self, equal: bool):
        t = []
        if equal:
            for i in range(self.M + 1):
                t.append(i * self.T / self.M)
        return t

    def generate_brownian_bridge(self, w_T, t):
        W = [0]
        for n in range(1, self.M):
            if n == 1:
                W.append((t[n] - t[n-1])*w_T/(self.T - t[n-1]) + np.sqrt((self.T - t[n])*(t[n] - t[n-1])/(self.T - t[n-1]))*np.random.normal(0, 1, 1))
            else:
                W.append((self.T - t[n])*W[n-1]/(self.T - t[n-1]) + (t[n] - t[n-1])*w_T/(self.T - t[n-1]) + np.sqrt((self.T - t[n])*(t[n] - t[n-1])/(self.T - t[n-1]))*np.random.normal(0, 1, 1))

        return W

    def generate_s_trajectory(self, w, t):
        s = [self.s_0]
        for k in range(1, self.M):
            x1 = np.exp((self.r - 0.5*self.sigma**2)*(t[k] - t[k-1]) + self.sigma*(w[k] - w[k-1]))
            if k == 1:
                s.append(self.s_0*x1)
            else:
                s.append(s[k-1]*x1)
        return s

    def generate_payoff(self, payoff: OptionPricing.Payoff):
        pass


class Result:
    def __init__(self, n, k, M, price, variance, rmse):
        self.n = n
        self.k = k
        self.M = M
        self.price = price
        self.variance = variance
        self.rmse = rmse

    def print_result(self):
        print(f'Option result: (n, k, M) -> ({self.n}, {self.k}, {self.M}) Price -> {self.price}, Variance -> {self.variance}, RMSE -> {self.rmse}')

