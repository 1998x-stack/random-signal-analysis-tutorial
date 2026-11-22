"""Deterministic checks for the explanatory models in chapter 12."""
import math
import unittest


class Chapter12MathTests(unittest.TestCase):
    RC = 1.0
    N0 = 2.0

    def h(self, t):
        return (1/self.RC)*math.exp(-t/self.RC) if t >= 0 else 0.0

    def psi(self, tau, n=20000, T=40.0):
        dt = T/n
        return sum(self.h((i+0.5)*dt)*self.h((i+0.5)*dt+tau)*dt for i in range(n))

    def test_ch12_effective_system_autocorrelation(self):
        for tau in (0.0, 0.5, 1.5):
            self.assertAlmostEqual(self.psi(tau),
                                   (1/(2*self.RC))*math.exp(-tau/self.RC), places=3)

    def test_ch12_rc_output_power_time_domain(self):
        power = (self.N0/2)*(1/(2*self.RC))
        self.assertAlmostEqual(power, self.N0/(4*self.RC), places=12)

    def test_ch12_rc_output_power_frequency_domain(self):
        W = 1.0e7
        I = (self.N0/2)*(1/self.RC)*(math.atan(W*self.RC) - math.atan(-W*self.RC))
        self.assertAlmostEqual(I/(2*math.pi), self.N0/(4*self.RC), places=6)

    def test_ch12_single_convolution_is_twice_output_power(self):
        # R_XY(0) = (N0/2) h(0) = N0/(2 RC); true R_Y(0) = N0/(4 RC).
        rxy0 = (self.N0/2)*self.h(0.0)
        ry0 = self.N0/(4*self.RC)
        self.assertAlmostEqual(rxy0/ry0, 2.0, places=12)

    def test_ch12_dc_gain_is_unity_for_rc(self):
        # Integral of h over [0, inf) is 1 for this RC low-pass.
        n, T = 200000, 60.0
        dt = T/n
        area = sum(self.h((i+0.5)*dt)*dt for i in range(n))
        self.assertAlmostEqual(area, 1.0, places=4)


if __name__ == "__main__":
    unittest.main()
