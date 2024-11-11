import numpy as np
from scipy.optimize import fsolve

# Define the system of nonlinear equations
A_s = 0.25
Po1, P3 = 1, 0.6


def area_mach_ratio(M, gamma=1.4):
    term_1 = 1 / np.square(M)
    term_2 = (2 / (gamma + 1)) * (1 + ((gamma - 1) / 2) * np.square(M))
    return np.sqrt(term_1 * (term_2 ** ((gamma + 1) / (gamma - 1))))


def stag_presure_static_pressure(M, gamma=1.4):
    term_1 = (1 + (gamma - 1) / 2 * np.square(M))
    return term_1 ** (gamma / (gamma - 1))


def P2_P1(M, gamma=1.4):
    term_1 = 1 + (((2 * gamma) / (gamma + 1)) * (np.square(M) - 1))
    return term_1


def M2_M1(M, gamma=1.4):
    term_1 = 1 + ((gamma - 1) / 2) * np.square(M)
    term_2 = gamma * np.square(M) - (gamma - 1) / 2
    return np.sqrt(term_1 / term_2)


solution_prob = np.array([])


def equations(var):
    M_shock = var[0]

    A_shock = area_mach_ratio(M_shock) * A_s
    M2 = M2_M1(M_shock)
    Po2 = Po1 * (1 / stag_presure_static_pressure(M_shock)) * \
          P2_P1(M_shock) * (stag_presure_static_pressure(M2))
    A_s_new = A_shock / area_mach_ratio(M2)
    eq1 = P3 - Po2 / (stag_presure_static_pressure(M2))

    print(A_shock, M2, P2_P1(M_shock), Po2 / (stag_presure_static_pressure(M2)), A_s_new, eq1)
    return eq1


initial_guess = np.array([2])
solution = fsolve(equations, initial_guess)
print("Solution:", solution)
residual = equations(solution)
print("Residuals:", residual)
