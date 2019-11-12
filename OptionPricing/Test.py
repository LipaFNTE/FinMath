from OptionPricing import StratifiedSampling, Payoff


class Test:
    A = 80
    B = 130
    ss = StratifiedSampling.StratifiedSampling(50000, 100, 1, 0.001, 0, 0.15, 100, 118, 10)
    payoff = Payoff.BarrierOut(A, B)
    result = ss.run(True, payoff, True)
    result.print_result()
