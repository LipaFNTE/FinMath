import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from OptionPricing import Payoff

class AmericanOptions(Payoff.TrajectoryPayoff):
    def __init__(self, T, N, M, d, call):
        super().__init__(call)
        self.T = T
        self.N = N
        self.M = M
        self.d = d
        self.delta = self.T/self.M


    def pricingOption(self, r, K, s0, sigma):
        s = self.trajGen(r, s0, sigma)
        v = self.getFinalValue(s[len(s) - 1], K, r)
        opt = {}
        for j in range(self.M, 1, -1):
            data = self.getData(np.exp(-self.delta * j * r)* v,  s[j])
            model = self.getRegression(data[data.y > 0])
            c = self.getApproximation(data, model)
            v = self.getValue(s[j], K, j, r)
            for i in range(len(v)):
                if v > c:
                    opt[i] = v
            if self.checkOptimality(v, c):
                time = j
                return 1/self.N * np.exp(- self.delta*j*r) * sum(v)

    def generate_trajectory(self, r, K, s0, sigma):
        return [self.trajGen(r, s0, sigma) for _ in range(self.N)]

    def getData(self, y, x):
        data = pd.DataFrame({'y': y,
                             'x': x})
        for i in range(2, self.d + 1):
            data[f'x{i}'] = pow(data['x'], i)
        return data

    def getRegression(self, data):
        model: LinearRegression = LinearRegression().fit(data['y'], data.iloc[:, 1:])
        return model

    def getApproximation(self, data, model):
        return model.predict(data.iloc[:, 1:])

    def checkOptimality(self, v, c):
        pass

    def getFinalValue(self, s, k, r):
        if self.call:
            return [np.exp(-self.T*r) * max(s_ - k, 0) for s_ in s]
        else:
            return [self.T * max(k - s_, 0) for s_ in s]

    def getValue(self, s, k, m, r):
        if self.call:
            return [np.exp(-self.delta*m*r) * max(s_ - k, 0) for s_ in s]
        else:
            return [np.exp(-self.delta*m*r) * max(k - s_, 0) for s_ in s]

    def trajGen(self, r, s0, sigma):
        _z = list(np.random.normal(size=self.N))
        _s = [s0 * np.exp((r - 0.5 * sigma ** 2) * self.delta +
                          sigma * np.sqrt(self.delta) * _z[0])]
        for i in range(1, self.M):
            _s.append(_s[i - 1] * np.exp((r - 0.5 * sigma ** 2) * self.delta +
                                         sigma * np.sqrt(self.delta) * _z[0]))
        return _s

