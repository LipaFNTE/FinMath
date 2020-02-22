import numpy as np
import pandas as pd
import statsmodels.api as sm
from OptionPricing import Payoff

class AmericanOptions(Payoff.TrajectoryPayoff):
    def __init__(self, T, N, M, d, call):
        super().__init__(call)
        self.T = T
        self.N = N
        self.M = M
        self.d = d
        self.delta = self.T/self.M

    def pricingOption(self, r, K, s0, sigma, T, N, M, d, call, itm: bool):
        delta = T/M
        s = self.generate_trajectory(r, s0, sigma, N, M, delta)
        v = self.getFinalValue(s[len(s) - 1], K, r, T, call)
        opt = {}
        for j in range(M, 1, -1):
            data = self.getData([np.exp(-delta * j * r) * _v for _v in v], s[j-1], d)
            if itm:
                model = self.getRegression(data[data.y > 0])
            else:
                model = self.getRegression(data)
            c = self.getApproximation(data, model)
            v = self.getValue(s[j - 1], K, j, r, delta, call)
            for i in range(len(v)):
                if v[i] >= c[i]:
                    opt[i] = v[i]
        return [np.mean(list(opt.values())), np.std(list(opt.values()))/np.sqrt(N)]

    def generate_trajectory(self, r, s0, sigma, N, M, delta):
        s = {0: [s0 for _ in range(N - 1)]}
        for i in range(1, M):
            s[i] = [(_s * np.exp((r - 0.5 * sigma ** 2) * delta +
                                         sigma * np.sqrt(delta) * np.random.normal())) for _s in s[i-1]]
        return s

    def getData(self, y, x, d):
        data = pd.DataFrame({'y': y,
                             'x': x})
        for i in range(2, d + 1):
            data[f'x{i}'] = pow(data['x'], i)
        return data

    def getRegression(self, data):
        model: sm.OLS = sm.OLS(data['y'], data.iloc[:, 1:]).fit()
        return model

    def getApproximation(self, data, model):
        return model.predict(data.iloc[:, 1:])

    def checkOptimality(self, v, c):
        pass

    def getFinalValue(self, s, k, r, T, call):
        if call:
            return [np.exp(-T*r) * max(s_ - k, 0) for s_ in s]
        else:
            return [np.exp(-T*r) * max(k - s_, 0) for s_ in s]

    def getValue(self, s, k, m, r, delta, call):
        if call:
            return [np.exp(-delta*m*r) * max(s_ - k, 0) for s_ in s]
        else:
            return [np.exp(-delta*m*r) * max(k - s_, 0) for s_ in s]

    def trajGen(self, r, s0, sigma, m, N, delta):
        _s = []
        if m == 0:
            _s = [s0 for _ in range(N)]
        else:
            _s = [(s0 * np.exp((r - 0.5 * sigma ** 2) * delta * m +
                                         sigma * np.sqrt(delta) * m * np.random.normal())) for _ in range(N)]
        return _s


if __name__ == '__main__':
    ao = AmericanOptions(1, 1000, 100, 3, False)
    print(ao.pricingOption(0.01, 100, 95, 0.15, 1, 8000, 600, 3, False, True))