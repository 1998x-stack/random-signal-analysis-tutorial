"""Deterministic checks for the explanatory models in chapter 17 (narrowband Gaussian)."""
import math
import random
import unittest


class Chapter17MathTests(unittest.TestCase):
    def setUp(self):
        random.seed(17)
        self.N = 200000
        self.Rs, self.phis = [], []
        for _ in range(self.N):
            i, q = random.gauss(0, 1), random.gauss(0, 1)
            self.Rs.append(math.hypot(i, q))
            self.phis.append(math.atan2(q, i))

    def test_ch17_rayleigh_mean_and_variance(self):
        m = sum(self.Rs) / self.N
        v = sum((r - m) ** 2 for r in self.Rs) / self.N
        self.assertAlmostEqual(m, math.sqrt(math.pi / 2), delta=0.01)
        self.assertAlmostEqual(v, 2 - math.pi / 2, delta=0.01)

    def test_ch17_phase_is_uniform(self):
        quad = [0, 0, 0, 0]
        for p in self.phis:
            quad[int((p + math.pi) / (math.pi / 2))] += 1
        self.assertGreater(min(quad) / self.N, 0.24)
        self.assertLess(max(quad) / self.N, 0.26)

    def test_ch17_envelope_and_phase_uncorrelated(self):
        mR = sum(self.Rs) / self.N
        mP = sum(self.phis) / self.N
        cov = sum((self.Rs[i] - mR) * (self.phis[i] - mP) for i in range(self.N)) / self.N
        self.assertLess(abs(cov), 0.01)

    def test_ch17_rayleigh_cdf_deep_fade(self):
        # F_R(r) = 1 - exp(-r^2/(2 sigma^2)), r = 0.1 * E[R] with sigma = 1.
        r = 0.1 * math.sqrt(math.pi / 2)
        p = 1 - math.exp(-r * r / 2)
        self.assertAlmostEqual(p, 0.0078, delta=5e-4)

    def test_ch17_rice_factor_limit(self):
        for sigma in (0.5, 1.0, 2.0):
            self.assertEqual(0.0 ** 2 / (2 * sigma ** 2), 0.0)   # A=0 -> K=0 -> Rayleigh
            self.assertAlmostEqual((3 * sigma) ** 2 / (2 * sigma ** 2), 4.5, places=12)


if __name__ == "__main__":
    unittest.main()
