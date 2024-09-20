import numpy as np
from scipy.optimize import fsolve


class ObliqueShock:
    def __init__(self, Ma, theta, gamma=1.4):
        self.Ma_1 = Ma
        self.theta = theta
        self.gamma = gamma

    # Initialization functions for class
    def set_gamma(self, gamma):
        self.gamma = gamma

    def theta_beta_Ma(self, beta):
        coeff = 2 / np.tan(beta)
        top = np.square(self.Ma_1) * np.square(np.sin(beta)) - 1
        bot = np.square(self.Ma_1) * (self.gamma + np.cos(2 * beta)) + 2
        return np.arctan(coeff * top / bot)

    def inverse_theta_beta_Ma(self, theta):

        def objective(beta):
            return theta - self.theta_beta_Ma(beta)

        initial_guess = np.array(np.radians(5.0))
        beta_solution = fsolve(objective, initial_guess)

        return beta_solution

    def tangential_Ma_1(self, beta):
        return self.Ma_1 * np.sin(beta)

    def tangential_Ma_2_Ma_1(self, beta):
        Mn1 = self.tangential_Ma_1(beta)
        coeff = 2 / (self.gamma - 1)
        Ma_2 = np.sqrt((np.square(Mn1) + coeff) / (self.gamma * coeff * np.square(Mn1) - 1))
        return Ma_2

    def M2(self, Mn2, beta, theta):
        return Mn2 / np.sin(beta - theta)

    def pressure_ratio(self, Mn_1):
        p_ratio = 1 + (2 * self.gamma / (self.gamma + 1)) * (np.square(Mn_1) - 1)
        return p_ratio

    def rho_ratio(self, Mn_1):
        rho_ratio = ((self.gamma + 1) * np.square(Mn_1)) / \
                    ((self.gamma - 1) * np.square(Mn_1) + 2)
        return rho_ratio

    def temp_ratio(self, Mn_1):
        return self.pressure_ratio(Mn_1) / self.rho_ratio(Mn_1)

