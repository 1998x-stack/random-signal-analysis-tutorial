"""Deterministic checks for the explanatory models in chapter 16 (narrowband signals)."""
import math
import unittest
from cmath import exp, pi

N = 64


def dft(x, inv=False):
    s = 1 if inv else -1
    return [sum(x[n] * exp(s * 2j * pi * k * n / N) for n in range(N)) for k in range(N)]


def hilbert(x):
    X = dft(x)
    Y = []
    for k in range(N):
        f = k if k < N // 2 else k - N          # signed frequency index
        Y.append(X[k] * (-1j if f > 0 else (1j if f < 0 else 0)))
    return [v / N for v in dft(Y, inv=True)]


class Chapter16MathTests(unittest.TestCase):
    def test_ch16_hilbert_of_cosine_is_sine(self):
        x = [math.cos(2 * pi * 3 * n / N) for n in range(N)]
        xh = hilbert(x)
        err = max(abs(xh[n] - math.sin(2 * pi * 3 * n / N)) for n in range(N))
        self.assertLess(err, 1e-6)

    def test_ch16_double_transform_negates(self):
        x = [math.cos(2 * pi * 3 * n / N) for n in range(N)]
        xx = hilbert(hilbert(x))
        err = max(abs(xx[n] + x[n]) for n in range(N))
        self.assertLess(err, 1e-6)

    def test_ch16_orthogonality_and_energy(self):
        x = [math.cos(2 * pi * 3 * n / N) for n in range(N)]
        xh = hilbert(x)
        self.assertLess(abs(sum(x[n] * xh[n] for n in range(N))), 1e-6)
        e0 = sum(abs(v) ** 2 for v in x)
        e1 = sum(abs(v) ** 2 for v in xh)
        self.assertLess(abs(e0 - e1) / e0, 1e-6)

    def test_ch16_dc_maps_to_zero(self):
        x = [1.0] * N
        xh = hilbert(x)
        self.assertLess(max(abs(v) for v in xh), 1e-9)

    def test_ch16_iq_reconstruction(self):
        # x(t)=I cos - Q sin with I=a cos phi, Q=a sin phi  =>  a^2=I^2+Q^2
        for a, phi in [(2.0, 0.3), (1.5, -1.1)]:
            I = a * math.cos(phi)
            Q = a * math.sin(phi)
            self.assertAlmostEqual(I * I + Q * Q, a * a, places=12)
            self.assertAlmostEqual(math.atan2(Q, I), phi, places=12)


if __name__ == "__main__":
    unittest.main()
