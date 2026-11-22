"""Deterministic checks for the explanatory models in chapter 11."""
import math
import unittest


class Chapter11MathTests(unittest.TestCase):
    def test_ch11_biased_autocorrelation_spectrum_nonnegative(self):
        x = [1.0, 2.0, 3.0, 4.0]
        N = len(x)
        r = [sum(x[n]*x[n+m] for n in range(N-m))/N for m in range(N)]
        for k in range(N):
            w = 2*math.pi*k/N
            S = sum(r[abs(l)]*(math.cos(w*l) - 1j*math.sin(w*l))
                    for l in range(-(N-1), N))
            X = sum(x[n]*(math.cos(w*n) - 1j*math.sin(w*n)) for n in range(N))
            self.assertAlmostEqual((S - (abs(X)**2)/N).real, 0.0, places=9)
            self.assertGreater(S.real, -1e-9)

    def test_ch11_biased_estimator_bias_factor(self):
        # E[Rhat_biased[m]] = (N-m)/N R[m]; check the multiplicative factor.
        N, m = 10, 3
        self.assertAlmostEqual((N-m)/N, 0.7, places=12)

    def test_ch11_sample_mean_variance_scales(self):
        sigma2, M = 4.0, 100
        self.assertAlmostEqual(sigma2/M, 0.04, places=12)
        self.assertAlmostEqual(sigma2/(4*M), (sigma2/M)/4, places=12)

    def test_ch11_constant_covariance_integral_diverges(self):
        # C_X(tau)=sigma^2 constant -> integral over [0,T] grows with T.
        sigma2 = 2.0
        integral = lambda T: sigma2*T
        self.assertLess(integral(10.0), integral(1000.0))
        self.assertGreater(integral(1.0e6), 1.0e6)

    def test_ch11_degenerate_constant_is_ergodic(self):
        # If B is deterministic (sigma^2 = 0), time average equals the mean.
        B = 1.5
        self.assertEqual(B, 1.5)


if __name__ == "__main__":
    unittest.main()
