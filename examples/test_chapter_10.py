"""Deterministic checks for the explanatory models in chapter 10."""
import math
import unittest


class Chapter10MathTests(unittest.TestCase):
    def test_ch10_nyquist_thermal_noise_density(self):
        kB, T, R = 1.380649e-23, 290.0, 1000.0
        density = 4*kB*T*R
        # 4 kT R at room temperature and 1 kOhm is ~1.6e-17 V^2/Hz.
        self.assertAlmostEqual(density/1.6e-17, 1.0, places=1)
        volt = math.sqrt(density)
        self.assertAlmostEqual(volt/4e-9, 1.0, places=1)  # ~4 nV/sqrt(Hz)

    def test_ch10_two_sided_and_one_sided_agree(self):
        N0, B = 2.0, 50.0
        band_power = (1/(2*math.pi))*(N0/2)*(2*(2*math.pi*B))
        self.assertAlmostEqual(band_power, N0*B, places=12)

    def test_ch10_bandlimited_white_noise_power(self):
        N0, B = 0.5, 200.0
        self.assertAlmostEqual(N0*B, 100.0, places=12)

    def test_ch10_discrete_variance_scales_with_sample_rate(self):
        N0, fs = 2.0, 8000.0
        var1 = N0*fs/2
        self.assertAlmostEqual(N0*(2*fs)/2, 2*var1, places=9)

    def test_ch10_ideal_white_noise_power_diverges(self):
        # A constant PSD integrated over a growing band grows without bound.
        N0 = 1.0
        power = lambda W: (1/(2*math.pi))*(N0/2)*(2*W)
        self.assertLess(power(10.0), power(1000.0))
        self.assertLess(power(1000.0), power(1.0e6))
        self.assertGreater(power(1.0e6), 1.0e5)


if __name__ == "__main__":
    unittest.main()
