import matplotlib.pyplot as plt
import numpy as np

import Expansion_Wave as Ew
import Oblique_Shock as Os


def AOA_Plate(alpha):
    theta = np.radians(alpha)
    M_1 = 3
    P_1 = 1
    T_1 = 270
    gamma = 1.4

    # Expansion Wave - Top
    expansion_top = Ew.ExpansionWave(Ma=M_1, theta=theta, gamma=gamma)
    nu_2 = theta + expansion_top.prandtl_meyer(M_1)
    M_2_ex = expansion_top.inverse_prandtl_meyer(nu_2)

    pressure_ratio_ex = expansion_top.pressure_ratio(M_2_ex)
    temp_ratio_ex = expansion_top.temp_ratio(M_2_ex)
    P_2_ex = P_1 * pressure_ratio_ex
    T_2_ex = T_1 * temp_ratio_ex

    # Oblique Shock - Bot
    oblique_bot = Os.ObliqueShock(Ma=M_1, theta=theta, gamma=gamma)
    beta = oblique_bot.inverse_theta_beta_Ma(theta)
    Mn1 = oblique_bot.tangential_Ma_1(beta)
    Mn2 = oblique_bot.tangential_Ma_2_Ma_1(beta)
    M2 = oblique_bot.M2(Mn2, beta, theta)

    rho_ratio_ob = oblique_bot.rho_ratio(Mn1)
    pressure_ratio_ob = oblique_bot.pressure_ratio(Mn1)
    temp_ratio_ob = oblique_bot.temp_ratio(Mn1)
    P_2_ob = P_1 * pressure_ratio_ob
    T_2_ob = T_1 * temp_ratio_ob

    arr = [np.rad2deg(theta), M_2_ex, P_2_ex, T_2_ex, M2, P_2_ob, T_2_ob]
    result_arr = np.array([item if np.isscalar(item) else item[0] for item in arr])
    return result_arr


if __name__ == '__main__':
    theta_arr = [i for i in range(0, 35, 5)]
    result_arr = np.array([])
    for theta in theta_arr:
        if result_arr.size == 0:
            result_arr = AOA_Plate(theta)
        else:
            result_arr = np.vstack([result_arr, AOA_Plate(theta)])

    pressure_diff = result_arr[:, 5] - result_arr[:, 2]

    # Reshape the new columns to be 2D arrays with one column
    cos_component = (pressure_diff * np.cos(np.radians(result_arr[:, 0]))).reshape(-1, 1)
    sin_component = (pressure_diff * np.sin(np.radians(result_arr[:, 0]))).reshape(-1, 1)
    lift_drag_ratio = (cos_component / sin_component).reshape(-1, 1)

    # Concatenate the new columns as 2D arrays
    result_arr = np.concatenate([result_arr, cos_component], axis=1)
    result_arr = np.concatenate([result_arr, sin_component], axis=1)
    result_arr = np.concatenate([result_arr, lift_drag_ratio], axis=1)

    fig, axs = plt.subplots(3, 3, figsize=(12, 10))  # 3 rows, 3 columns of plots

    x = result_arr[:, 0]
    name = ["Expansion Mach", "Expansion Pressure [atm]", "Expansion Temperature [K]",
            "Oblique Mach", "Oblique Pressure [atm]", "Oblique [K]",
            "Lift/L", "Drag/L", "Lift/Drag"]

    # Loop to create 9 plots
    for i in range(9):
        row, col = divmod(i, 3)  # Changed to divmod(i, 3) for 3x3 grid
        axs[row, col].plot(x, result_arr[:, i + 1])
        axs[row, col].set_xlabel('Angle of Attack (Degree)')
        axs[row, col].set_ylabel(name[i])

    plt.tight_layout()  # Adjust layout so plots don't overlap
    plt.show()
