"""Deterministic checks for the explanatory models in chapter 08."""
import math
import unittest


class Chapter08MathTests(unittest.TestCase):
    POINTS = [(1, 1), (1, -1), (-1, 1), (-1, -1)]  # (A, B), each prob 1/4
    TH = math.pi/3

    def x(self, n, a, b):
        return a*math.cos(n*self.TH) + b*math.sin(n*self.TH)

    def r(self, n, m):
        return sum(self.x(n, a, b)*self.x(m, a, b) for a, b in self.POINTS)/4

    def test_ch08_wss_counterexample_autocorrelation(self):
        # R depends only on the lag, so the process is wide-sense stationary.
        for n in range(-3, 4):
            for m in range(-3, 4):
                self.assertAlmostEqual(self.r(n, m), math.cos((n-m)*self.TH), places=12)

    def test_ch08_wss_constant_mean_and_variance(self):
        for n in range(-3, 4):
            vals = [self.x(n, a, b) for a, b in self.POINTS]
            self.assertAlmostEqual(sum(vals)/4, 0, places=12)
            self.assertAlmostEqual(sum(v*v for v in vals)/4, 1, places=12)

    def test_ch08_not_sss_marginals_differ(self):
        atoms0 = {round(self.x(0, a, b), 6) for a, b in self.POINTS}
        atoms1 = {round(self.x(1, a, b), 6) for a, b in self.POINTS}
        self.assertEqual(len(atoms0), 2)   # X_0 = A in {-1, +1}
        self.assertEqual(len(atoms1), 4)   # X_1 has four distinct values
        self.assertNotEqual(atoms0, atoms1)

    def test_ch08_gaussian_variant_is_shift_invariant(self):
        # With iid standard Gaussian (A,B) the process is Gaussian, so WSS
        # lifts to SSS: every finite-dimensional covariance is shift invariant.
        def cov(n, m):
            return math.cos((n-m)*self.TH)  # E[A^2]=E[B^2]=1, E[AB]=0
        for n in range(-4, 5):
            for m in range(-4, 5):
                self.assertAlmostEqual(cov(n, m), cov(n+3, m+3), places=12)


if __name__ == "__main__":
    unittest.main()
