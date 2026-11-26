"""Deterministic checks for the explanatory models in chapter 24 (modern PSD estimation)."""
import math
import random
import unittest
import cmath


def autocorr(x, p):
    N = len(x)
    return [sum(x[n] * x[n + k] for n in range(N - k)) / N for k in range(p + 1)]


def levinson(R, p):
    a = [0.0] * (p + 1)
    a[0] = 1.0
    K = []
    e = R[0]
    for m in range(1, p + 1):
        acc = sum(a[i] * R[m - i] for i in range(1, m))
        km = -(R[m] + acc) / e
        K.append(km)
        anew = a[:]
        for i in range(1, m):
            anew[i] = a[i] + km * a[m - i]
        anew[m] = km
        a = anew
        e = e * (1 - km * km)
    return a, K, e


def ar_psd(a, e, f):
    z = cmath.exp(-2j * math.pi * f)
    val = 1.0 + sum(a[k] * z ** k for k in range(1, len(a)))
    return e / abs(val) ** 2


def periodogram(x):
    N = len(x)
    P = []
    for k in range(N // 2 + 1):
        re = im = 0.0
        for n, v in enumerate(x):
            ang = -2 * math.pi * k * n / N
            re += v * math.cos(ang)
            im += v * math.sin(ang)
        p = (re * re + im * im) / N
        if k != 0 and k != N // 2:
            p *= 2
        P.append(p)
    return P


class Chapter24MathTests(unittest.TestCase):
    def test_ch24_ar2_peak_location_and_height(self):
        f0, r, sig2 = 0.10, 0.95, 1.0
        a = [1.0, -2 * r * math.cos(2 * math.pi * f0), r * r]
        fr = [i / 4000 for i in range(1001)]
        vals = [ar_psd(a, sig2, f) for f in fr]
        peak = fr[vals.index(max(vals))]
        self.assertAlmostEqual(peak, f0, delta=0.005)
        self.assertAlmostEqual(10 * math.log10(max(vals)), 24.8, delta=1.0)

    def test_ch24_levinson_stable_and_solves_yule_walker(self):
        rnd = random.Random(24)
        x = [math.cos(2 * math.pi * 0.10 * n) + 0.5 * math.cos(2 * math.pi * 0.25 * n)
             + 0.6 * rnd.gauss(0, 1) for n in range(128)]
        p = 8
        R = autocorr(x, p)
        a, K, e = levinson(R, p)
        self.assertTrue(all(abs(k) < 1.0 for k in K))       # stability: |K_m| < 1
        self.assertLess(e, R[0])                             # prediction error shrinks
        for m in range(1, p + 1):
            resid = R[m] + sum(a[k] * R[abs(m - k)] for k in range(1, p + 1))
            self.assertAlmostEqual(resid, 0.0, delta=1e-9)   # Yule-Walker residual

    def test_ch24_music_resolves_closer_than_rayleigh(self):
        M = 12
        fsig = [0.100, 0.112]  # separation 0.012 < 1/N = 0.015625
        A = [[cmath.exp(2j * math.pi * f * m) for m in range(M)] for f in fsig]
        G = [[sum(A[i][m].conjugate() * A[j][m] for m in range(M)) for j in range(2)] for i in range(2)]
        det = G[0][0] * G[1][1] - G[0][1] * G[1][0]
        Gi = [[G[1][1] / det, -G[0][1] / det], [-G[1][0] / det, G[0][0] / det]]
        fr = [i / 4000 for i in range(1001)]
        v = []
        for f in fr:
            e = [cmath.exp(2j * math.pi * f * m) for m in range(M)]
            proj = sum((sum(e[m].conjugate() * A[i][m] for m in range(M))) * Gi[i][j]
                       * (sum(A[j][m].conjugate() * e[m] for m in range(M)))
                       for i in range(2) for j in range(2)).real
            v.append(1.0 / (M - proj + 1e-4))
        peaks = [round(fr[i], 4) for i in range(1, len(v) - 1)
                 if 0.06 < fr[i] < 0.17 and v[i] >= v[i - 1] and v[i] >= v[i + 1]
                 and v[i] > 0.2 * max(v)]
        self.assertEqual(len(peaks), 2)
        self.assertAlmostEqual(peaks[0], 0.100, delta=0.004)
        self.assertAlmostEqual(peaks[1], 0.112, delta=0.004)

    def test_ch24_periodogram_merges_the_pair(self):
        rnd = random.Random(7)
        N = 64
        x = [math.cos(2 * math.pi * 0.100 * n) + math.cos(2 * math.pi * 0.112 * n)
             + 0.25 * rnd.gauss(0, 1) for n in range(N)]
        P = periodogram(x)
        fr = [k / N for k in range(len(P))]
        peaks = [fr[i] for i in range(1, len(P) - 1)
                 if 0.06 < fr[i] < 0.17 and P[i] >= P[i - 1] and P[i] >= P[i + 1]
                 and P[i] > 0.3 * max(P)]
        self.assertEqual(len(peaks), 1)  # below Rayleigh limit -> single merged bump
