"""Deterministic checks for the explanatory models in chapter 22 (Kalman filter)."""
import random
import unittest


def run_kf(seed=22):
    random.seed(seed)
    dt = 1.0
    xt, xe, P = [0.0, 1.0], [0.0, 1.0], [[5.0, 0.0], [0.0, 5.0]]
    Q00 = Q11 = 0.01
    R = 2.0
    Ks, Ps = [], []
    for _ in range(20):
        xt = [xt[0] + dt * xt[1] + random.gauss(0, 0.1), xt[1] + random.gauss(0, 0.1)]
        z = xt[0] + random.gauss(0, R ** 0.5)
        xp = [xe[0] + dt * xe[1], xe[1]]
        Pp = [[P[0][0] + dt * P[1][0] + dt * (P[0][1] + dt * P[1][1]) + Q00, P[0][1] + dt * P[1][1]],
              [P[1][0] + dt * P[1][1], P[1][1] + Q11]]
        S = Pp[0][0] + R
        K = [Pp[0][0] / S, Pp[1][0] / S]
        innov = z - xp[0]
        xe = [xp[0] + K[0] * innov, xp[1] + K[1] * innov]
        P = [[(1 - K[0]) * Pp[0][0], (1 - K[0]) * Pp[0][1]],
             [Pp[1][0] - K[1] * Pp[0][0], Pp[1][1] - K[1] * Pp[0][1]]]
        Ks.append(K[0])
        Ps.append(P[0][0])
    return Ks, Ps


class Chapter22MathTests(unittest.TestCase):
    def test_ch22_gain_converges(self):
        Ks, _ = run_kf()
        self.assertAlmostEqual(Ks[0], 0.8335, delta=0.005)
        self.assertAlmostEqual(Ks[-1], 0.3188, delta=0.005)

    def test_ch22_covariance_monotone_decreases(self):
        _, Ps = run_kf()
        for i in range(len(Ps) - 1):
            self.assertLessEqual(Ps[i + 1], Ps[i] + 1e-9)
        self.assertAlmostEqual(Ps[-1], 0.638, delta=0.005)

    def test_ch22_scalar_gain_limits(self):
        # K = P/(P+R): large P/R -> K -> 1, small P/R -> K -> 0.
        self.assertGreater(1e6 / (1e6 + 1.0), 0.999)
        self.assertLess(1.0 / (1.0 + 1e6), 1e-3)

    def test_ch22_estimator_uncertainty_shrinks(self):
        # Posterior variance is smaller than prior: P = (1-K) P_prior with 0<=K<1.
        for K in (0.2, 0.32, 0.83):
            self.assertLess((1 - K) * 5.0, 5.0)


if __name__ == "__main__":
    unittest.main()
