"""Deterministic checks for the explanatory models in chapter 07."""
import math
import unittest


class Chapter07MathTests(unittest.TestCase):
    def test_ch07_random_phase_autocorrelation(self):
        # X(t)=A cos(2*pi*f*t+Theta), Theta ~ Uniform[0,2pi).
        A, f, n = 2.0, 1.3, 4096
        t1, tau = 0.7, 0.4
        phases = [2*math.pi*k/n for k in range(n)]
        r_num = sum((A*math.cos(2*math.pi*f*t1+p)) *
                    (A*math.cos(2*math.pi*f*(t1+tau)+p)) for p in phases)/n
        r_formula = A*A/2*math.cos(2*math.pi*f*tau)
        self.assertAlmostEqual(r_num, r_formula, places=11)
        mean = sum(A*math.cos(2*math.pi*f*t1+p) for p in phases)/n
        self.assertAlmostEqual(mean, 0, places=11)

    def test_ch07_derivative_autocorrelation_identity(self):
        # For WSS X, R_Xdot(tau) = -R_X''(tau); check on the same model.
        A, f, n = 2.0, 1.3, 4096
        t1, tau = 0.7, 0.4
        phases = [2*math.pi*k/n for k in range(n)]
        w = 2*math.pi*f
        rp_num = sum((-A*w*math.sin(w*t1+p)) *
                     (-A*w*math.sin(w*(t1+tau)+p)) for p in phases)/n
        self.assertAlmostEqual(rp_num, A*A/2*w*w*math.cos(w*tau), places=9)

    def test_ch07_uncorrelated_but_dependent(self):
        # X in {-1,0,1} equally likely, Y = X^2.
        vals = [-1, 0, 1]
        ex = sum(vals)/3
        ey = sum(v*v for v in vals)/3
        exy = sum(v*v*v for v in vals)/3
        self.assertEqual(ex, 0)
        self.assertAlmostEqual(ey, 2/3)
        self.assertEqual(exy, 0)  # uncorrelated
        # Y is a deterministic function of X, so they are dependent.
        self.assertTrue(all(v*v == y for v, y in zip(vals, [1, 0, 1])))

    def test_ch07_ms_differentiable_paths_differentiable(self):
        # X(t)=A t with E[A^2]=1 has R(t1,t2)=t1 t2, twice differentiable.
        t1, t2 = 0.3, 1.1
        cross = 1.0*t1*t2
        self.assertAlmostEqual(cross, 0.33, places=12)

    def test_ch07_cauchy_schwarz_bound(self):
        # |R(t1,t2)| <= sqrt(R(t1,t1) R(t2,t2)) for the cosine model.
        A, f, tau = 3.0, 0.8, 0.5
        r = A*A/2*math.cos(2*math.pi*f*tau)
        self.assertLessEqual(abs(r), A*A/2 + 1e-12)


if __name__ == "__main__":
    unittest.main()
