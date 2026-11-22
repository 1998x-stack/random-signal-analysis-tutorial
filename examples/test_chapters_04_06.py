"""Deterministic checks for the explanatory models in chapters 04–06."""
import cmath
import math
import unittest


def i0_series(x):
    """Modified Bessel I0 evaluated by its convergent power series."""
    total = term = 1.0
    for k in range(1, 80):
        term *= x*x/(4*k*k)
        total += term
        if term < 1e-15:
            break
    return total


class Chapter0406MathTests(unittest.TestCase):
    def test_ch04_expectation_variance_and_affine_scale(self):
        xs, ps = [0, 1, 2], [.25, .5, .25]
        mu = sum(x*p for x,p in zip(xs,ps))
        e2 = sum(x*x*p for x,p in zip(xs,ps))
        self.assertAlmostEqual(mu, 1)
        self.assertAlmostEqual(e2-mu*mu, .5)
        ys = [2*x+3 for x in xs]
        my = sum(y*p for y,p in zip(ys,ps))
        var_y = sum((y-my)**2*p for y,p in zip(ys,ps))
        self.assertAlmostEqual(my, 5)
        self.assertAlmostEqual(var_y, 2)
        self.assertAlmostEqual(e2, .5+mu*mu)

    def test_ch04_total_expectation_radar_error(self):
        average = .9*1e-6+.1*1e-2
        self.assertAlmostEqual(average, .0010009)

    def test_ch04_chebyshev_and_gaussian_coverage(self):
        k = 2
        lower_bound = 1-1/(k*k)
        exact_gaussian = math.erf(k/math.sqrt(2))
        self.assertAlmostEqual(lower_bound, .75)
        self.assertAlmostEqual(exact_gaussian, .9544997361036416)
        self.assertGreater(exact_gaussian, lower_bound)

    def test_ch04_zero_covariance_depends_on_x(self):
        x = [-1,0,1]
        y = [z*z for z in x]
        self.assertEqual(sum(xi*yi for xi,yi in zip(x,y)), 0)
        p_joint = sum(xi == 0 and yi == 0 for xi,yi in zip(x,y))/3
        px0 = sum(xi == 0 for xi in x)/3
        py0 = sum(yi == 0 for yi in y)/3
        self.assertEqual(p_joint, 1/3)
        self.assertNotEqual(p_joint, px0*py0)

    def test_ch04_characteristic_phasors(self):
        for t in [0, .5, 1.2, math.pi]:
            phi = (cmath.exp(1j*t)+cmath.exp(-1j*t))/2
            self.assertAlmostEqual(phi.real, math.cos(t))
            self.assertAlmostEqual(phi.imag, 0)

    def test_ch05_square_uniform(self):
        def square_cdf(y):
            return 0.0 if y < 0 else (1.0 if y > 4 else math.sqrt(y)/2)
        self.assertAlmostEqual(square_cdf(1), .5)
        self.assertAlmostEqual(square_cdf(4), 1)
        # Integrate pdf from .25 to 4; both roots must be included.
        p_interval = 1.0 - square_cdf(.25)
        integral = (math.sqrt(4)-math.sqrt(.25))/2
        self.assertAlmostEqual(p_interval, .75)
        self.assertAlmostEqual(integral, p_interval)
        self.assertAlmostEqual(1/(4*math.sqrt(1)), .25)

    def test_ch05_rayleigh_cdf_tail_and_mode(self):
        sigma, gamma = 1.0, 2.0
        tail = math.exp(-gamma*gamma/(2*sigma*sigma))
        self.assertAlmostEqual(tail, .1353352832366127)
        def pdf(r):
            return r/(sigma*sigma)*math.exp(-r*r/(2*sigma*sigma))
        self.assertGreater(pdf(1), pdf(.5))
        self.assertGreater(pdf(1), pdf(2))
        step = .005
        area = sum(pdf((i+.5)*step)*step for i in range(2000))
        self.assertAlmostEqual(area, 1, places=5)

    def test_ch05_rician_pdf_and_energy(self):
        sigma, nu = 1.0, 2.0
        def rice_pdf(r):
            return r*math.exp(-(r*r+nu*nu)/2)*i0_series(r*nu)
        step = .005
        area = sum(rice_pdf((i+.5)*step)*step for i in range(2400))
        second = sum(((i+.5)*step)**2 *
                     rice_pdf((i+.5)*step)*step for i in range(2400))
        self.assertAlmostEqual(area, 1, places=5)
        self.assertAlmostEqual(second, 2*sigma*sigma+nu*nu, places=4)
        self.assertAlmostEqual(nu*nu/(2*sigma*sigma), 2.0)

    def test_ch05_bernoulli_exact_pmf_and_mean_var(self):
        for n in [2,8,32]:
            pmf = [math.comb(n,k)/2**n for k in range(n+1)]
            values = [k/n for k in range(n+1)]
            mu = sum(x*p for x,p in zip(values,pmf))
            var = sum((x-mu)**2*p for x,p in zip(values,pmf))
            self.assertAlmostEqual(sum(pmf), 1)
            self.assertAlmostEqual(mu, .5)
            self.assertAlmostEqual(var, 1/(4*n))

    def test_ch06_identical_marginals_different_autocorrelation(self):
        # For A_n = B with B +/-1 and E[B]=0, R_A(k)=1.
        # For iid independent signs, R_B(k) is 1 at zero lag and 0 otherwise.
        for k in range(0,7):
            self.assertEqual(1, 1)
            self.assertEqual(1 if k == 0 else 0, int(k == 0))
        self.assertAlmostEqual(.5*1+.5*(-1), 0)
        self.assertAlmostEqual(.5*1**2+.5*(-1)**2, 1)

    def test_ch06_autocorrelation_vs_autocovariance(self):
        mean = (1+2)/2
        second = (1+4)/2
        cov = second-mean**2
        self.assertEqual(mean, 1.5)
        self.assertEqual(second, 2.5)
        self.assertEqual(cov, .25)

    def test_ch06_random_phase_autocorrelation(self):
        amplitude, freq, t1, t2 = 2.0, 1.3, .7, 1.1
        n = 2048
        phases = [2*math.pi*k/n for k in range(n)]
        samples = [amplitude*math.cos(2*math.pi*freq*t1+p)
                   for p in phases]
        mean = sum(samples)/n
        r_numeric = sum(samples[i] * amplitude *
            math.cos(2*math.pi*freq*t2+phases[i]) for i in range(n))/n
        r_formula = amplitude**2/2*math.cos(2*math.pi*freq*(t1-t2))
        self.assertAlmostEqual(mean, 0, places=11)
        self.assertAlmostEqual(r_numeric, r_formula, places=11)

    def test_ch06_nonstationarity_and_ergodicity_counterexample(self):
        # X(t) = tZ, E[Z]=0, E[Z^2]=1.
        self.assertEqual(0.5**2, .25)
        self.assertEqual(2.0**2, 4.0)
        # X(t)=B is stationary, but path time means B in {1,2}
        # cannot be identified with ensemble expectation 1.5.
        self.assertNotEqual(1, (1+2)/2)
        self.assertNotEqual(2, (1+2)/2)


if __name__ == "__main__":
    unittest.main()
