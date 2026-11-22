"""Deterministic numerical assertions underlying chapters 01–03."""
import math
import unittest


class IntroMathTests(unittest.TestCase):
    def test_bayes_radar(self):
        prior, sensitivity, false_alarm = 0.01, 0.90, 0.05
        posterior = sensitivity * prior / (
            sensitivity * prior + false_alarm * (1 - prior)
        )
        self.assertAlmostEqual(posterior, 90 / (90 + 495), places=12)

    def test_zero_covariance_not_independence(self):
        xs = [-1, 0, 1]
        ys = [x * x for x in xs]
        ex, ey = sum(xs) / 3, sum(ys) / 3
        cov = sum((x - ex) * (y - ey) for x, y in zip(xs, ys)) / 3
        self.assertAlmostEqual(cov, 0.0)
        self.assertAlmostEqual(
            sum(x == 0 and y == 0 for x, y in zip(xs, ys)) / 3, 1 / 3
        )
        self.assertNotAlmostEqual(1 / 3, (1 / 3) * (1 / 3))

    def test_discrete_cdf_right_continuity(self):
        pmf = {0: .25, 1: .50, 2: .25}
        cdf = lambda x: sum(p for k, p in pmf.items() if k <= x)
        self.assertAlmostEqual(sum(pmf.values()), 1)
        self.assertAlmostEqual(cdf(0), .25)
        self.assertAlmostEqual(cdf(.999), .25)
        self.assertAlmostEqual(cdf(1), .75)

    def test_uniform_pdf_area_and_mixed_atom(self):
        self.assertAlmostEqual((1.5 - .5) * .5, .5)
        mixed = lambda x: 0 if x < 0 else .2 + .8 * (1-math.exp(-x))
        self.assertEqual(mixed(-.00001), 0)
        self.assertEqual(mixed(0), .2)
        self.assertAlmostEqual(mixed(100), 1, places=12)

    def test_gaussian_one_sigma_probability(self):
        self.assertAlmostEqual(math.erf(1/math.sqrt(2)), .682689492137,
                               places=11)

    def test_covariance_and_conditional_gaussian(self):
        var_x, var_y, cov = 4, 1, 1.5
        self.assertEqual(var_x * var_y - cov*cov, 1.75)
        rho = .6
        self.assertAlmostEqual(rho * 1.0, .6)
        self.assertAlmostEqual(1-rho**2, .64)


if __name__ == "__main__":
    unittest.main()
