class Instrument:
    def __init__(self,  T, r, mu, sigma, s_0, K):
        self.s_0 = s_0
        self.K = K
        self.T = T
        self.r = r
        self.mu = mu
        self.sigma = sigma