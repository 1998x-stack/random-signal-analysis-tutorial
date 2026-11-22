"""Deterministic checks for the explanatory models in chapter 13."""
import math
import unittest


class Chapter13MathTests(unittest.TestCase):
    def test_ch13_rc_equivalent_noise_bandwidth(self):
        RC, W = 1.0, 1.0e9
        one_sided = (1/RC)*math.atan(W*RC)   # int_0^inf |H|^2 dw = pi/(2 RC)
        self.assertAlmostEqual(one_sided, math.pi/(2*RC), places=6)

    def test_ch13_rc_output_power_frequency_domain(self):
        RC, N0, W = 1.0, 2.0, 1.0e9
        whole = (1/RC)*(math.atan(W*RC) - math.atan(-W*RC))
        self.assertAlmostEqual(whole/(2*math.pi)*(N0/2), N0/(4*RC), places=6)

    def test_ch13_noise_bandwidth_exceeds_3db(self):
        RC = 1.0
        B3 = 1/RC                        # 3 dB corner in rad/s
        Bn = math.pi/(2*RC)              # one-sided equivalent noise bandwidth
        self.assertGreater(Bn, B3)
        self.assertAlmostEqual(Bn/B3, math.pi/2, places=12)

    def test_ch13_ideal_lowpass_white_noise_power(self):
        N0, B = 2.0, 100.0
        power = (N0/2)*(1/(2*math.pi))*(2*(2*math.pi*B))
        self.assertAlmostEqual(power, N0*B, places=12)

    def test_ch13_whitening_makes_unit_spectrum(self):
        # |H_w|^2 * S_X = 1 for H_w magnitude 1/sqrt(S_X).
        for s in (0.25, 1.0, 4.0):
            hw2 = 1.0/s
            self.assertAlmostEqual(hw2*s, 1.0, places=12)


if __name__ == "__main__":
    unittest.main()
