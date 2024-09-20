import numpy as np
from scipy.optimize import fsolve


class ExpansionWave:
    def __init__(self, Ma=1, theta=1, gamma=1.4):
        self.Ma_1 = Ma
        self.theta = theta
        self.gamma = gamma

    def prandtl_meyer(self, Ma=None):
        gamma_coeff = (self.gamma + 1) / (self.gamma - 1)
        if Ma is None:
            term_1 = np.sqrt(gamma_coeff) * np.arctan(np.sqrt((np.square(self.Ma_1) - 1) / gamma_coeff))
            term_2 = np.arctan(np.sqrt(np.square(self.Ma_1) - 1))
        else:
            term_1 = np.sqrt(gamma_coeff) * np.arctan(np.sqrt((np.square(Ma) - 1) / gamma_coeff))
            term_2 = np.arctan(np.sqrt(np.square(Ma) - 1))

        return term_1 - term_2

    def inverse_prandtl_meyer(self, nu):
        def objective(Ma):
            return self.prandtl_meyer(Ma) - nu

        initial_guess = np.array(2.0)
        Ma_solution = fsolve(objective, initial_guess)

        return Ma_solution

    def __temp(self, Ma):
        return 1 + (self.gamma - 1) * np.square(Ma) / 2

    def pressure_ratio(self, Ma_2):
        p_ratio = (self.__temp(self.Ma_1) / self.__temp(Ma_2)) ** (self.gamma / (self.gamma - 1))
        return p_ratio

    def temp_ratio(self, Ma_2):
        return self.__temp(self.Ma_1) / self.__temp(Ma_2)




# # Example usage:
# wave = ExpansionWave(gamma=1.4)
# print(wave.prandtl_meyer(2.0))
# print(wave.inverse_prandtl_meyer(0.5))
