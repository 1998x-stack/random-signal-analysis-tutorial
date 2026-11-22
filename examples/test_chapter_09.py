"""Deterministic checks for the explanatory models in chapter 09."""
import math
import unittest


class Chapter09MathTests(unittest.TestCase):
    def test_ch09_lorentzian_spectrum_power(self):
        # R(tau)=sigma^2 exp(-alpha|tau|) <-> S(w)=2 alpha sigma^2/(alpha^2+w^2).
        sigma2, alpha, big = 1.0, 2.0, 1.0e9
        integral = 2*alpha*sigma2/alpha*(math.atan(big/alpha) - math.atan(-big/alpha))
        self.assertAlmostEqual(integral/(2*math.pi), sigma2, places=8)

    def test_ch09_bandlimited_white_noise_power(self):
        # S(w)=N0/2 on |w|<=2 pi B gives total power N0 B.
        N0, B = 0.5, 100.0
        power = (1/(2*math.pi))*(N0/2)*(4*math.pi*B)
        self.assertAlmostEqual(power, N0*B, places=12)

    def test_ch09_random_phase_sine_impulses(self):
        # S(w)=(pi A^2/2)[delta(w-w0)+delta(w+w0)] integrates to A^2/2.
        A = 1.0
        power = (1/(2*math.pi))*((math.pi*A*A/2) + (math.pi*A*A/2))
        self.assertAlmostEqual(power, A*A/2, places=12)
        self.assertAlmostEqual(A*A/2, 0.5, places=12)

    def test_ch09_dc_impulse_area(self):
        # Nonzero mean mu adds 2 pi mu^2 delta(w), contributing mu^2 to power.
        mu = 1.5
        self.assertAlmostEqual((1/(2*math.pi))*(2*math.pi*mu*mu), mu*mu, places=12)

    def test_ch09_lorentzian_is_even_and_nonnegative(self):
        # Real signals give an even, nonnegative PSD.
        sigma2, alpha = 2.0, 3.0
        s = lambda w: 2*alpha*sigma2/(alpha**2 + w**2)
        for w in (0.0, 0.7, 12.3, 250.0):
            self.assertAlmostEqual(s(w), s(-w), places=15)
            self.assertGreater(s(w), 0.0)


if __name__ == "__main__":
    unittest.main()
