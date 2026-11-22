"""Deterministic checks for the explanatory models in chapter 14."""
import math
import unittest


class Chapter14MathTests(unittest.TestCase):
    def test_ch14_ar1_yule_walker(self):
        a, s2 = 0.7, 1.0
        R = lambda k: s2*a**abs(k)/(1-a*a)
        self.assertAlmostEqual(R(0), a*R(1)+s2, places=12)
        for k in range(1, 6):
            self.assertAlmostEqual(R(k), a*R(k-1), places=12)

    def test_ch14_ar1_psd_integrates_to_power(self):
        a, s2, N = 0.7, 1.0, 20000
        dw = 2*math.pi/N
        total = 0.0
        for i in range(N):
            w = -math.pi + (i+0.5)*dw
            total += s2/(1-2*a*math.cos(w)+a*a)*dw
        R0 = s2/(1-a*a)
        self.assertAlmostEqual(total/(2*math.pi), R0, places=6)

    def test_ch14_discrete_white_noise_power_finite(self):
        s2 = 3.0
        power = (1/(2*math.pi))*s2*(2*math.pi)   # integrate over [-pi, pi]
        self.assertAlmostEqual(power, s2, places=12)

    def test_ch14_ma_q_autocorrelation_cutoff(self):
        # MA(2): X[n]=eps[n]+0.5 eps[n-1]-0.3 eps[n-2]; R[m]=0 for |m|>2.
        b = [1.0, 0.5, -0.3]
        def r(m):
            return sum(b[j]*b[j+m] for j in range(len(b)-m)) if 0 <= m < len(b) else 0.0
        self.assertNotEqual(r(2), 0.0)
        self.assertEqual(r(3), 0.0)
        self.assertEqual(r(4), 0.0)

    def test_ch14_ar1_stability_bound(self):
        # |a| < 1 keeps the pole outside the unit circle: z = 1/a.
        for a in (0.5, -0.9):
            self.assertGreater(abs(1/a), 1.0)


if __name__ == "__main__":
    unittest.main()
