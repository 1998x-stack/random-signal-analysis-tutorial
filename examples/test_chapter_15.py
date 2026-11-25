"""Deterministic checks for the explanatory models in chapter 15 (Gaussian processes)."""
import itertools
import math
import unittest


def sym2_eigs(a, b, d):
    """Eigenvalues of the symmetric 2x2 matrix [[a, b], [b, d]]."""
    mid = (a + d) / 2
    rad = math.sqrt(((a - d) / 2) ** 2 + b * b)
    return mid - rad, mid + rad


class Chapter15MathTests(unittest.TestCase):
    def test_ch15_conditional_mean_and_variance(self):
        rho, x2 = 0.6, 0.8
        # Sigma = [[1, rho], [rho, 1]]
        mean_cond = rho / 1.0 * x2
        var_cond = 1.0 - rho * rho
        self.assertAlmostEqual(mean_cond, 0.48, places=12)
        self.assertAlmostEqual(var_cond, 0.64, places=12)

    def test_ch15_non_psd_covariance_has_negative_eigenvalue(self):
        lo, hi = sym2_eigs(1.0, 2.0, 1.0)          # [[1, 2], [2, 1]]
        self.assertAlmostEqual(lo, -1.0, places=12)
        self.assertAlmostEqual(hi, 3.0, places=12)
        self.assertLess(lo, 0.0)

    def test_ch15_psd_covariance_positive_eigenvalues(self):
        lo, hi = sym2_eigs(4.0, 1.0, 2.0)          # [[4, 1], [1, 2]]
        self.assertGreater(lo, 0.0)
        self.assertAlmostEqual(lo, 1.5858, places=3)
        self.assertAlmostEqual(hi, 4.4142, places=3)

    def test_ch15_rbf_covariance_is_positive_semidefinite(self):
        t = [0.0, 0.8, 1.6, 2.4, 3.2]
        K = [[math.exp(-((ti - tj) ** 2) / 2) for tj in t] for ti in t]
        grid = [-2.0, -1.0, -0.3, 0.0, 0.4, 1.0, 2.0]
        worst = min(
            sum(a[i] * a[j] * K[i][j] for i in range(5) for j in range(5))
            for a in itertools.product(grid, repeat=5)
        )
        self.assertGreaterEqual(worst, -1e-9)

    def test_ch15_covariance_is_symmetric(self):
        for ti, tj in itertools.product([0.0, 0.5, 1.5], repeat=2):
            self.assertAlmostEqual(
                math.exp(-((ti - tj) ** 2) / 2), math.exp(-((tj - ti) ** 2) / 2), places=15
            )

    def test_ch15_uncorrelated_not_independent(self):
        # Y = S X with S in {-1, +1} independent of X, E[S] = 0.
        ES, EX2 = 0.0, 1.0
        cov_XY = ES * EX2            # E[S] E[X^2] = 0
        var_Y = EX2                  # S^2 = 1
        self.assertEqual(cov_XY, 0.0)
        self.assertAlmostEqual(var_Y, 1.0, places=12)


if __name__ == "__main__":
    unittest.main()
