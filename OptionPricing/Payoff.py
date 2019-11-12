import numpy as np


class Payoff:
    def __init__(self):
        pass

    def payoff_function(self, s, K, r, T, call):
        pass


class ClassicPayoff(Payoff):
    def __init__(self):
        super().__init__()


class TrajectoryPayoff(Payoff):
    def __init__(self):
        super().__init__()

    def payoff_function(self, s, K, T, r, call):
        pass


class BarrierOut(TrajectoryPayoff):
    def __init__(self, A, B):
        super().__init__()
        self.A = A
        self.B = B

    def payoff_function(self, s, K, T, r, call: bool):
        for i in range(len(s)):
            if (s[i] <= self.A) | (s[i] >= self.B):
                return 0
        if call:
            return max(s[len(s) - 1] - K, 0) * np.exp(-r * T)
        else:
            return max(K - s[len(s) - 1], 0) * np.exp(-r * T)
