"""Deterministic checks for the explanatory models in chapter 18 (Markov chains)."""
import unittest

P = [[0.2, 0.3, 0.5],
     [0.2, 0.4, 0.4],
     [0.3, 0.2, 0.5]]
P_T = [list(r) for r in zip(*P)]


def mv(A, v):
    return [sum(A[i][j] * v[j] for j in range(len(v))) for i in range(len(A))]


def mul(A, B):
    return [[sum(A[i][t] * B[t][j] for t in range(len(B))) for j in range(len(B[0]))]
            for i in range(len(A))]


def stationary():
    pi = [1 / 3, 1 / 3, 1 / 3]
    for _ in range(1000):
        pi = mv(P_T, pi)
    return pi


class Chapter18MathTests(unittest.TestCase):
    def test_ch18_stochastic_matrix(self):
        for row in P:
            self.assertAlmostEqual(sum(row), 1.0, places=12)
            self.assertTrue(all(x >= 0 for x in row))

    def test_ch18_stationary_distribution(self):
        pi = stationary()
        self.assertAlmostEqual(sum(pi), 1.0, places=9)
        for j in range(3):
            self.assertAlmostEqual(pi[j], sum(pi[i] * P[i][j] for i in range(3)), places=12)
        self.assertAlmostEqual(pi[0], 0.2472, places=3)
        self.assertAlmostEqual(pi[2], 0.4719, places=3)

    def test_ch18_limit_forgets_initial_state(self):
        pi = stationary()
        for start in range(3):
            v = [0.0, 0.0, 0.0]
            v[start] = 1.0
            for _ in range(60):
                v = mv(P_T, v)
            for j in range(3):
                self.assertAlmostEqual(v[j], pi[j], places=9)

    def test_ch18_ck_associativity(self):
        left = mul(mul(P, P), P)
        right = mul(P, mul(P, P))
        for i in range(3):
            for j in range(3):
                self.assertAlmostEqual(left[i][j], right[i][j], places=12)


if __name__ == "__main__":
    unittest.main()
