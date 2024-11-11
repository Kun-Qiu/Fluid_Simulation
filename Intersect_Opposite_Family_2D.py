import matplotlib.pyplot as plt
import numpy as np
import Oblique_Shock as os


def theta_beta_Ma_curve(Ma, gamma=1.4):
    beta_range = np.arange(np.arcsin(1 / Ma), np.radians(90), np.radians(0.5))

    def theta_beta_Ma(beta):
        coeff = 2 / np.tan(beta)
        top = np.square(Ma) * np.square(np.sin(beta)) - 1
        bot = np.square(Ma) * (gamma + np.cos(2 * beta)) + 2
        return np.arctan(coeff * top / bot)

    theta_range = theta_beta_Ma(beta_range)
    return theta_range, beta_range, max(theta_range)


theta_2, beta_2, max_2 = theta_beta_Ma_curve(2)
theta_3, beta_3, max_3 = theta_beta_Ma_curve(3)
theta_5, beta_5, max_5 = theta_beta_Ma_curve(5)

pres_ratio = []
for theta, beta in zip(theta_2, beta_2):
    shock = os.ObliqueShock(3, theta)
    Mn1 = shock.tangential_Ma_1(beta)
    pres_ratio.append(shock.pressure_ratio(Mn1))


plt.figure(figsize=(10, 6))
plt.plot(np.degrees(theta_2), pres_ratio, label=f'Ma = {2}', color='m')
# plt.plot(np.degrees(theta_3), np.degrees(beta_3), label=f'Ma = {3}', color='b')
# plt.plot(np.degrees(theta_5), np.degrees(beta_5), label=f'Ma = {5}', color='r')
plt.xlabel('Theta (Degree)')
plt.ylabel('Pressure Ratio')
plt.legend()
plt.show()

# # Define the system of nonlinear equations
# M2, M3 = 1.993, 2.253
# P2, P3 = 3.77, 2.82
# th_2, th_3 = np.radians(20), np.radians(-15)
#
#
# def theta_beta_M(M, beta):
#     num = 2 * (np.square(M) * np.square(np.sin(beta)) - 1)
#     den = np.tan(beta) * (2 + np.square(M) * (1.4 + np.cos(2 * beta)))
#     return num / den
#
#
# def equations(var):
#     th4_p, b4_p, th4, b4, p4_p, p4, phi = var
#
#     eq1 = np.tan(th4_p) - theta_beta_M(M2, b4_p)
#     eq2 = np.tan(th4) - theta_beta_M(M3, b4)
#     eq3 = p4_p - P2 * (1 + ((2.8 / 2.4) * ((M2 * np.sin(b4_p)) ** 2 - 1)))
#     eq4 = p4 - P3 * (1 + ((2.8 / 2.4) * ((M3 * np.sin(b4)) ** 2 - 1)))
#     eq5 = th4 - phi + th_3
#     eq6 = th4_p + phi - th_2
#     eq7 = p4_p - p4
#
#     return [eq1, eq2, eq3, eq4, eq5, eq6, eq7]
#
#
# initial_guess = np.array([np.radians(15), np.radians(15), np.radians(15), np.radians(15),
#                           1, 1, np.radians(5)])
# solution = fsolve(equations, initial_guess)
# print("Solution:", solution)
# residual = equations(solution)
# print("Residuals:", residual)
