"""Deterministic checks for the explanatory models in chapter 20 (estimation theory)."""
import math
import random
import unittest


class Chapter20MathTests(unittest.TestCase):
    def test_ch20_lmmse_gain_and_orthogonality(self):
        random.seed(20)
        rho, N = 0.6, 200000
        s_ty = s_yy = s_orth = 0.0
        for _ in range(N):
            z1, z2 = random.gauss(0, 1), random.gauss(0, 1)
            th = z1
            y = rho * z1 + math.sqrt(1 - rho * rho) * z2
            s_ty += th * y
            s_yy += y * y
            s_orth += (th - rho * y) * y
        self.assertAlmostEqual(s_ty / s_yy, rho, delta=0.01)
        self.assertLess(abs(s_orth / N), 0.01)

    def test_ch20_unbiased_sample_variance(self):
        random.seed(21)
        trials, n = 20000, 5
        acc = 0.0
        for _ in range(trials):
            v = [random.gauss(0, 1) for _ in range(n)]
            xb = sum(v) / n
            acc += sum((x - xb) ** 2 for x in v) / (n - 1)
        self.assertAlmostEqual(acc / trials, 1.0, delta=0.02)

    def test_ch20_crlb_gaussian_mean(self):
        sigma2, n = 4.0, 25
        fisher = n / sigma2
        self.assertAlmostEqual(1 / fisher, sigma2 / n, places=12)
        self.assertAlmostEqual(1 / fisher, 0.16, places=12)

    def test_ch20_biased_can_beat_unbiased(self):
        # MSE = bias^2 + variance; a small-bias, low-variance estimator can win.
        bias, var = 0.3, 0.5
        biased_mse = bias ** 2 + var
        unbiased_mse = 0.8
        self.assertAlmostEqual(biased_mse, 0.59, places=12)
        self.assertLess(biased_mse, unbiased_mse)


if __name__ == "__main__":
    unittest.main()
