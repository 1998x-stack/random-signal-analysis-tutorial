"""Deterministic checks for the explanatory models in chapter 23 (classical PSD estimation)."""
import math
import random
import unittest


def dft_power(x, k):
    re = im = 0.0
    N = len(x)
    for n, v in enumerate(x):
        a = -2 * math.pi * k * n / N
        re += v * math.cos(a)
        im += v * math.sin(a)
    return re * re + im * im


def periodogram(x):
    N = len(x)
    P = []
    for k in range(N // 2 + 1):
        p = dft_power(x, k) / N
        if k != 0 and k != N // 2:
            p *= 2
        P.append(p)
    return P


def make_signal(N, seed, sigma=0.7, A1=1.0, f1=0.0977, A2=0.6, f2=0.25):
    rnd = random.Random(seed)
    return [A1 * math.cos(2 * math.pi * f1 * n) + A2 * math.cos(2 * math.pi * f2 * n)
            + sigma * rnd.gauss(0, 1) for n in range(N)]


def bartlett(x, K):
    N = len(x)
    M = N // K
    acc = [0.0] * (M // 2 + 1)
    for i in range(K):
        P = periodogram(x[i * M:(i + 1) * M])
        for j, p in enumerate(P):
            acc[j] += p
    return [a / K for a in acc], M


def window_spectrum_db(sig, freqs):
    out = []
    for f in freqs:
        re = im = 0.0
        for n, v in enumerate(sig):
            a = -2 * math.pi * f * n
            re += v * math.cos(a)
            im += v * math.sin(a)
        out.append(10 * math.log10(max(re * re + im * im, 1e-12)))
    return out


def first_sidelobe_db(dbs):
    peak = dbs.index(max(dbs))
    best = -999.0
    for i in range(peak + 2, len(dbs) - 1):
        if dbs[i] >= dbs[i - 1] and dbs[i] >= dbs[i + 1]:
            best = max(best, dbs[i])
    return best


class Chapter23MathTests(unittest.TestCase):
    def test_ch23_periodogram_peaks_at_true_frequencies(self):
        x = make_signal(256, 23)
        P = periodogram(x)
        self.assertEqual(max(range(129), key=lambda k: P[k]), 25)  # f1 = 0.0977 -> k≈25
        self.assertGreater(P[25], P[64])  # stronger tone wins
        # Noiseless tones: one-sided periodogram peak = A^2 * N / 2.
        s1 = [math.cos(2 * math.pi * 0.0977 * n) for n in range(256)]
        s2 = [0.6 * math.cos(2 * math.pi * 0.25 * n) for n in range(256)]
        self.assertAlmostEqual(max(periodogram(s1)), 1.0 ** 2 * 256 / 2, delta=1.0)
        self.assertAlmostEqual(periodogram(s2)[64], 0.6 ** 2 * 256 / 2, delta=0.5)

    def test_ch23_white_noise_expected_value(self):
        acc = [0.0] * 129
        S = 200
        for s in range(S):
            rnd = random.Random(1000 + s)
            xn = [0.7 * rnd.gauss(0, 1) for _ in range(256)]
            Pn = periodogram(xn)
            for k in range(2, 128):
                acc[k] += Pn[k]
        mean_interior = sum(acc[2:128]) / (126 * S)
        self.assertAlmostEqual(mean_interior, 0.98, delta=0.08)  # 2*sigma^2, one-sided

    def test_ch23_periodogram_relative_variance_is_order_one(self):
        x = make_signal(256, 23)
        P = periodogram(x)
        noise = [P[k] for k in range(2, 129) if not (22 <= k <= 29) and not (61 <= k <= 67)]
        m = sum(noise) / len(noise)
        rel = sum((p - m) ** 2 for p in noise) / len(noise) / m ** 2
        self.assertAlmostEqual(rel, 1.21, delta=0.25)  # inconsistent estimator: rel var ~ 1

    def test_ch23_bartlett_reduces_relative_variance(self):
        x = make_signal(256, 23)
        P = periodogram(x)
        B, M = bartlett(x, 8)
        raw = [P[k] for k in range(2, 129) if not (22 <= k <= 29) and not (61 <= k <= 67)]
        mr = sum(raw) / len(raw)
        rvr = sum((p - mr) ** 2 for p in raw) / len(raw) / mr ** 2
        nb = [B[k] for k in range(1, 17) if not (2 <= k <= 4) and not (7 <= k <= 9)]
        mb = sum(nb) / len(nb)
        rvb = sum((p - mb) ** 2 for p in nb) / len(nb) / mb ** 2
        self.assertEqual(M, 32)
        self.assertAlmostEqual(rvb, 0.093, delta=0.05)  # ~ 1/K = 0.125
        self.assertLess(rvb, rvr)

    def test_ch23_window_sidelobe_levels(self):
        M = 128
        f0 = 40.5 / M
        rect = [math.cos(2 * math.pi * f0 * n) for n in range(M)]
        hann = [rect[n] * (0.5 - 0.5 * math.cos(2 * math.pi * n / (M - 1))) for n in range(M)]
        freqs = [j / 1024 for j in range(0, 513)]
        dr = window_spectrum_db(rect, freqs)
        dh = window_spectrum_db(hann, freqs)
        dr = [d - max(dr) for d in dr]
        dh = [d - max(dh) for d in dh]
        self.assertAlmostEqual(first_sidelobe_db(dr), -13.5, delta=1.0)
        self.assertAlmostEqual(first_sidelobe_db(dh), -31.5, delta=1.0)
