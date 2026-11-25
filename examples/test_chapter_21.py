"""Deterministic checks for the explanatory models in chapter 21 (Wiener filtering)."""
import unittest


def solve(A, b):
    n = len(b)
    M = [A[i][:] + [b[i]] for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda i: abs(M[i][c]))
        M[c], M[p] = M[p], M[c]
        for i in range(n):
            if i != c:
                f = M[i][c] / M[c][c]
                for j in range(c, n + 1):
                    M[i][j] -= f * M[c][j]
    return [M[i][n] / M[i][i] for i in range(n)]


class Chapter21MathTests(unittest.TestCase):
    def setUp(self):
        a = 0.8
        self.Rss = [1 / (1 - a * a) * a ** m for m in range(3)]
        Rxx = [self.Rss[0] + 1] + self.Rss[1:]
        self.R = [[Rxx[abs(i - j)] for j in range(3)] for i in range(3)]

    def test_ch21_normal_equations_orthogonality(self):
        h = solve(self.R, self.Rss)
        res = [self.Rss[i] - sum(self.R[i][j] * h[j] for j in range(3)) for i in range(3)]
        self.assertLess(max(abs(v) for v in res), 1e-9)

    def test_ch21_filter_taps_and_dc_gain(self):
        h = solve(self.R, self.Rss)
        self.assertAlmostEqual(sum(h), 0.86, places=9)
        self.assertAlmostEqual(h[0], 0.58, places=9)
        self.assertAlmostEqual(h[1], 0.20, places=9)

    def test_ch21_frequency_gain_in_unit_interval(self):
        for snr in (0.1, 1.0, 10.0, 100.0):
            H = snr / (snr + 1)
            self.assertGreaterEqual(H, 0.0)
            self.assertLess(H, 1.0)

    def test_ch21_ar1_psd_matches_dc(self):
        # PSD at omega=0 for AR(1) is sigma_w^2 / |1-a|^2 = 1/(0.2)^2 = 25.
        self.assertAlmostEqual(1 / (0.2 ** 2), 25.0, places=9)


if __name__ == "__main__":
    unittest.main()
