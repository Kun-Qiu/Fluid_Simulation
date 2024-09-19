import numpy as np
import sympy as sp

"""
Normal Shock
"""


def mach_downstream(mach_1=None, mach_2=None, upsilon=None):
    M1, M2, gamma = sp.symbols('M1 M2 gamma')

    num = 1 + ((gamma - 1) / 2) * M1 ** 2
    den = gamma * M1 ** 2 - (gamma - 1) / 2

    mach_2_expr = sp.sqrt(num / den)
    equation = sp.Eq(M2, mach_2_expr)

    # Substitute the known values into the equation
    subs_dict = {}
    if mach_1 is not None:
        subs_dict[M1] = mach_1
    if mach_2 is not None:
        subs_dict[M2] = mach_2
    if upsilon is not None:
        subs_dict[gamma] = upsilon

    # Determine which variable is unknown
    unknown = None
    if mach_1 is None:
        unknown = M1
    elif mach_2 is None:
        unknown = M2
    elif upsilon is None:
        unknown = gamma

    # Solve the equation for the unknown variable
    if unknown is not None:
        solution = sp.solve(equation.subs(subs_dict), unknown)
        print(f"{unknown}: {solution[0]}")
        return solution[0]
    else:
        # If all variables are provided, just return the simplified equation
        return equation.subs(subs_dict).simplify()


def density_ratio(rho_ratio=None, mach=None, upsilon=None, rho_1=None, rho_2=None):
    M, gamma = sp.symbols('M gamma')
    rho_ratio_sym = sp.symbols('rho_ratio')

    # Define the equation for the density ratio
    num = (gamma + 1) * M ** 2
    den = 2 + (gamma - 1) * M ** 2
    ratio_expr = num / den
    equation = sp.Eq(rho_ratio_sym, ratio_expr)

    # Substitute the known values into the equation
    subs_dict = {}
    if mach is not None:
        subs_dict[M] = mach
    if rho_ratio is not None:
        subs_dict[rho_ratio_sym] = rho_ratio
    if upsilon is not None:
        subs_dict[gamma] = upsilon

    # Determine which variable is unknown
    unknown = None
    if mach is None:
        unknown = M
    elif rho_ratio is None:
        unknown = rho_ratio_sym
    elif upsilon is None:
        unknown = gamma

    # Solve the equation for the unknown variable
    if unknown is not None:
        solution = sp.solve(equation.subs(subs_dict), unknown)
        solution_value = solution[0]

        if rho_1 is not None:
            rho_2 = rho_1 * solution_value
            print(f"rho_2: {rho_2}")
            return rho_2
        elif rho_2 is not None:
            rho_1 = rho_2 / solution_value
            print(f"rho_1: {rho_1}")
            return rho_1
        else:
            print(f"{unknown}: {solution_value}")
            return solution_value
    else:
        # If all variables are provided, just return the simplified ratio
        return ratio_expr.subs(subs_dict).simplify()


def velocity_ratio(vel_ratio=None, mach=None, upsilon=None, vel_1=None, vel_2=None):
    M, gamma = sp.symbols('M gamma')
    vel_ratio_sym = sp.symbols('vel_ratio')

    # Define the equation for the velocity ratio
    vel_up_stream = (gamma + 1) * M ** 2
    vel_down_stream = 2 + (gamma - 1) * M ** 2
    ratio_expr = vel_down_stream / vel_up_stream
    equation = sp.Eq(vel_ratio_sym, ratio_expr)

    # Substitute the known values into the equation
    subs_dict = {}
    if mach is not None:
        subs_dict[M] = mach
    if vel_ratio is not None:
        subs_dict[vel_ratio_sym] = vel_ratio
    if upsilon is not None:
        subs_dict[gamma] = upsilon

    # Determine which variable is unknown
    unknown = None
    if mach is None:
        unknown = M
    elif vel_ratio is None:
        unknown = vel_ratio_sym
    elif upsilon is None:
        unknown = gamma

    # Solve the equation for the unknown variable
    if unknown is not None:
        solution = sp.solve(equation.subs(subs_dict), unknown)
        solution_value = solution[0]

        if vel_1 is not None:
            vel_2 = vel_1 * solution_value
            print(f"vel_2: {vel_2}")
            return vel_2
        elif vel_2 is not None:
            vel_1 = vel_2 / solution_value
            print(f"vel_1: {vel_1}")
            return vel_1
        else:
            print(f"{unknown}: {solution_value}")
            return solution_value
    else:
        # If all variables are provided, just return the simplified ratio
        return ratio_expr.subs(subs_dict).simplify()


def temperature_ratio(temp_ratio=None, mach=None, upsilon=None, temp_1=None, temp_2=None):
    M, gamma = sp.symbols('M gamma')
    temp_ratio_sym = sp.symbols('temp_ratio')

    # Define the equation for the temperature ratio
    a = gamma + 1
    b = gamma - 1

    ratio_1 = 1 + (2 * gamma * (M ** 2 - 1)) / a
    ratio_2 = (2 + b * M ** 2) / (a * M ** 2)
    temp_ratio_expr = ratio_1 * ratio_2
    equation = sp.Eq(temp_ratio_sym, temp_ratio_expr)

    # Substitute the known values into the equation
    subs_dict = {}
    if mach is not None:
        subs_dict[M] = mach
    if temp_ratio is not None:
        subs_dict[temp_ratio_sym] = temp_ratio
    if upsilon is not None:
        subs_dict[gamma] = upsilon

    # Determine which variable is unknown
    unknown = None
    if mach is None:
        unknown = M
    elif temp_ratio is None:
        unknown = temp_ratio_sym
    elif upsilon is None:
        unknown = gamma

    # Solve the equation for the unknown variable
    if unknown is not None:
        solution = sp.solve(equation.subs(subs_dict), unknown)
        solution_value = solution[0]

        if temp_1 is not None:
            temp_2 = temp_1 * solution_value
            print(f"temp_2: {temp_2} K")
            return temp_2
        elif temp_2 is not None:
            temp_1 = temp_2 / solution_value
            print(f"temp_1: {temp_1} K")
            return temp_1
        else:
            print(f"{unknown}: {solution_value}")
            return solution_value
    else:
        # If all variables are provided, just return the simplified temperature ratio
        return temp_ratio_expr.subs(subs_dict).simplify()


def pressure_ratio(mach, pres_i=None, upsilon=1.4):
    a = upsilon + 1
    b = pow(mach, 2) - 1

    pres_ratio = 1 + (2 * upsilon) * b / a

    if pres_i is not None:
        pres_2 = pres_i * pres_ratio
        print(f"Pressure (P2/P1) ratio: {pres_ratio}\tDownstream pressure: {pres_2} Pa.")
        return pres_i * pres_ratio

    return pres_ratio


def stag_pressure_ratio(mach=None, pres_1=None, pres_2=None, upsilon=1.4):
    # Define symbols
    M, P1, P2, gamma = sp.symbols('M P1 P2 gamma')

    # Define the equation for stagnation pressure ratio
    a = gamma - 1
    power = gamma / a
    pres_ratio_expr = (1 + a * M ** 2 / 2) ** power
    equation = sp.Eq(P2, P1 * pres_ratio_expr)

    # Substitute the known values into the equation
    subs_dict = {gamma: upsilon}
    if mach is not None:
        subs_dict[M] = mach
    if pres_1 is not None:
        subs_dict[P1] = pres_1
    if pres_2 is not None:
        subs_dict[P2] = pres_2

    # Find the unknown variable by excluding known ones
    unknown = None
    if mach is None:
        unknown = M
    elif pres_1 is None:
        unknown = P1
    elif pres_2 is None:
        unknown = P2

    # Solve the equation for the unknown variable
    if unknown is not None:
        solution = sp.solve(equation.subs(subs_dict), unknown)
        print(solution)
        return solution[0]  # Return the first solution
    else:
        # If all variables are provided, just return the equation as solved
        return equation.subs(subs_dict).simplify()


mach_downstream(mach_1=3, mach_2=None, upsilon=1.4)
density_ratio(rho_ratio=None, mach=3, upsilon=1.4, rho_1=1.23, rho_2=None)
velocity_ratio(vel_ratio=None, mach=3, upsilon=1.4, vel_1=3 * 339.6, vel_2=None)
temperature_ratio(temp_ratio=None, mach=3, upsilon=1.4, temp_1=287, temp_2=None)
# pressure_ratio(mach=3, pres_i=1)
# stag_pressure_ratio(mach=0.475, pres_2=12.05)
