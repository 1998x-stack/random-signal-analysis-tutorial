"""Deterministic checks for the explanatory models in chapter 19 (Poisson/shot noise)."""
import math
import random
import unittest


def arrivals(lam, horizon, seed=19):
    random.seed(seed)
    t, ts = 0.0, []
    while True:
        t += random.expovariate(lam)
        if t > horizon:
            break
        ts.append(t)
    return ts


class Chapter19MathTests(unittest.TestCase):
    def setUp(self):
        self.lam, self.T = 4.0, 10000
        self.ts = arrivals(self.lam, self.T)

    def test_ch19_interarrival_mean(self):
        gaps = [self.ts[0]] + [self.ts[i] - self.ts[i - 1] for i in range(1, len(self.ts))]
        self.assertAlmostEqual(sum(gaps) / len(gaps), 1 / self.lam, delta=0.01)

    def test_ch19_window_mean_equals_variance(self):
        counts = [0] * self.T
        for t in self.ts:
            counts[int(t)] += 1
        mean = sum(counts) / self.T
        var = sum((c - mean) ** 2 for c in counts) / self.T
        self.assertAlmostEqual(mean, self.lam, delta=0.15)
        self.assertAlmostEqual(var, self.lam, delta=0.5)
        self.assertLess(abs(mean - var), 0.6)

    def test_ch19_poisson_pmf_sums_to_one(self):
        lamt = 4.0
        total = sum(math.exp(-lamt) * lamt ** k / math.factorial(k) for k in range(40))
        self.assertAlmostEqual(total, 1.0, places=12)

    def test_ch19_exponential_memoryless(self):
        lam = 0.7
        for s, t in [(1.0, 0.5), (2.0, 3.0)]:
            surv = lambda x: math.exp(-lam * x)
            self.assertAlmostEqual(surv(s + t) / surv(s), surv(t), places=12)

    def test_ch19_campbell_delta_pulse(self):
        # h(t)=delta(t): integral=1, |H|=1, so S_II = lam * E[A^2].
        lam, EA2 = 5.0, 4.0
        self.assertAlmostEqual(lam * EA2, 20.0, places=12)


if __name__ == "__main__":
    unittest.main()
