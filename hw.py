import matplotlib.pyplot as plt
import numpy as np

L_driver = 3  # m
L_driven = 9  # m

x_right = np.linspace(0, L_driven, 1000)
# Given parameters
gamma = 1.4
R = 287  # J/(kg·K)
T1 = 300  # K
a1 = np.sqrt(gamma * R * T1)  # Speed of sound in region 1
p2p1 = 2.13

# Calculate Ms, Ds, up
Ms = np.sqrt(((gamma + 1) / (2 * gamma)) * (p2p1 - 1) + 1)
W = Ms * a1
up = (a1 / gamma) * (p2p1 - 1) * np.sqrt((2 * gamma / (gamma + 1)) / (p2p1 + (gamma - 1) / (gamma + 1)))
y_incident = 1 / W * x_right

# Parameters for reflected wave
Mr = 1.354
T5 = 442.15
a5 = np.sqrt(gamma * R * T5)
Wr = Mr * a5

x_reflected = np.linspace(2, L_driven, 1000)
c = y_incident[-1] + 1 / Wr * x_right[-1]
y_reflected = - 1 / Wr * x_reflected + c

intersect = c / (1 / Wr + 1 / up)
x_contact = np.linspace(0, intersect, 1000)
y_contact = 1 / up * x_contact

x_region5 = np.ones_like(x_contact) * intersect
y_region5 = np.zeros_like(x_region5)
y_region5[0] = - 1 / Wr * intersect + c
for i in range(1, len(y_region5)):
    val = y_region5[i - 1] + 0.0005
    if val <= 0.025:
        y_region5[i] = val
    else:
        y_region5[i] = 0.03

# Expansion Wave
T2 = 377.1
T4 = 300
T3 = 235.09
a3 = np.sqrt(gamma * R * T3)
a4 = np.sqrt(gamma * R * T4)

x_head = np.linspace(-L_driver, 0, 1000)
y_head = - 1 / a4 * x_head

# Plotting
plt.figure(figsize=(10, 6))

# Incident shock wave: plot with a slope of 1 second per W meters in x, vertical line after intersection
plt.plot(x_right, y_incident, 'r', label='Incident Shock')
plt.plot(x_reflected, y_reflected, 'y', label='Reflected Shock')
plt.plot(x_contact, y_contact, 'g', label='Contact Surface')
plt.plot(x_region5, y_region5, linestyle='--', color='g', label='Region 5')

plt.plot(x_head, y_head, linestyle='--', color='b', label='Expansion')


def slope(dv1, dv2):
    rhs = np.arctan(1 / dv1) + np.arctan(1 / dv2)
    return np.tan(0.5 * rhs)


"""--------------------------Portion 1-2-------------------------------------"""
slope_1_2 = slope(347.2 + 0, 333.9 + 66.576)
c_1_2 = y_head[0] - slope_1_2 * x_head[0]
u2 = 66.576
a2 = 333.9
intersect_1_2 = c_1_2 / ((1 / (u2 - a2)) - slope_1_2)
x_1_2 = np.linspace(-L_driver, intersect_1_2, 1000)
y_1_2 = slope_1_2 * x_1_2 + c_1_2
plt.plot(x_1_2, y_1_2, linestyle='--', color='b')

# Line 2
x_2 = np.linspace(intersect_1_2, 0, 1000)
y_2 = (1 / (u2 - a2)) * x_2
plt.plot(x_2, y_2, linestyle='--', color='b')

"----------------------------Portion 2-3---------------------------------------------"
slope_2_3 = slope(333.9 + 66.576, 320.6 + 133.152)
c_2_3 = y_2[0] - slope_2_3 * x_2[0]

u3 = 133.152
a3 = 320.6
intersect_2_3 = c_2_3 / ((1 / (u3 - a3)) - slope_2_3)
x_2_3 = np.linspace(x_2[0], intersect_2_3, 1000)
y_2_3 = slope_2_3 * x_2_3 + c_2_3
plt.plot(x_2_3, y_2_3, linestyle='--', color='b')
# Line 3
x_3 = np.linspace(intersect_2_3, 0, 1000)
y_3 = (1 / (u3 - a3)) * x_3
plt.plot(x_3, y_3, linestyle='--', color='b')

"----------------------------Portion 2-5---------------------------------------------"
slope_2_5 = slope(66.576 - 333.9, 320.6 + 0)
c_2_5 = y_2[0] - slope_2_5 * x_2[0]
x_2_5 = np.linspace(-L_driver, x_2[0], 1000)
y_2_5 = slope_2_5 * x_2_5 + c_2_5
plt.plot(x_2_5, y_2_5, linestyle='--', color='b')

"----------------------------Portion 5-6, 3-6---------------------------------------------"
slope_5_6 = slope(66.7 + 307.3, 320.6 + 0)
c_5_6 = y_2_5[0] - slope_5_6 * x_2_5[0]

slope_3_6 = slope(133.152 - 320.6, 66.7 - 307.3)
c_3_6 = y_3[0] - slope_3_6 * x_3[0]
intersect_6 = (c_3_6 - c_5_6) / (slope_5_6 - slope_3_6)

x_5_6 = np.linspace(-L_driver, intersect_6, 1000)
y_5_6 = slope_5_6 * x_5_6 + c_5_6
plt.plot(x_5_6, y_5_6, linestyle='--', color='b')

x_3_6 = np.linspace(intersect_6, x_3[0], 1000)
y_3_6 = slope_3_6 * x_3_6 + c_3_6
plt.plot(x_3_6, y_3_6, linestyle='--', color='b')

"----------------------------Portion 6-8---------------------------------------------"
slope_6_8 = slope(66.7 - 307.3, 0 - 293.9)
c_6_8 = y_3_6[0] - slope_6_8 * x_3_6[0]

x_6_8 = np.linspace(-L_driver, intersect_6, 1000)
y_6_8 = slope_6_8 * x_6_8 + c_6_8
plt.plot(x_6_8, y_6_8, linestyle='--', color='b')

"----------------------------Portion 3-4---------------------------------------------"
slope_3_4 = slope(320.6 + 133.152, 200 + 307.34)
c_3_4 = y_3[0] - slope_3_4 * x_3[0]
intersect_4 = (c_3_4) / (1/(200 - 307.34) - slope_3_4)

x_3_4 = np.linspace(x_3[0], intersect_4, 1000)
y_3_4 = slope_3_4 * x_3_4 + c_3_4
plt.plot(x_3_4, y_3_4, linestyle='--', color='b')

# Line 4 - Tail
x_tail = np.linspace(intersect_4, 0, 1000)
y_tail = 1 / (up - 307.34) * x_tail
plt.plot(x_tail, y_tail, linestyle='--', color='b')

"----------------------------Portion 6-7, 4-7---------------------------------------------"
slope_6_7 = slope(66.7 + 307.3, 294 + 133)
c_6_7 = y_3_6[0] - slope_6_7 * x_3_6[0]

slope_4_7 = slope(200 - 307.34, 66.7 - 307.3)
c_4_7 = y_tail[0] - slope_4_7 * x_tail[0]
intersect_7 = (c_6_7 - c_4_7) / (slope_4_7 - slope_6_7)

x_6_7 = np.linspace(x_3_6[0], intersect_7, 1000)
y_6_7 = slope_6_7 * x_6_7 + c_6_7
plt.plot(x_6_7, y_6_7, linestyle='--', color='b')

x_4_7 = np.linspace(intersect_7, x_tail[0], 1000)
y_4_7 = slope_4_7 * x_4_7 + c_4_7
plt.plot(x_4_7, y_4_7, linestyle='--', color='b')

"----------------------------Portion 8-9, 7-9---------------------------------------------"
slope_8_9 = slope(66.31 + 280.7, 293.9 + 0)
c_8_9 = y_6_8[0] - slope_8_9 * x_6_8[0]

slope_7_9 = slope(133 - 294, 66.31 - 280.7)
c_7_9 = y_4_7[0] - slope_7_9 * x_4_7[0]
intersect_9 = (c_7_9 - c_8_9) / (slope_8_9 - slope_7_9)

x_8_9 = np.linspace(x_6_8[0], intersect_9, 1000)
y_8_9 = slope_8_9 * x_8_9 + c_8_9
plt.plot(x_8_9, y_8_9, linestyle='--', color='b')

x_7_9 = np.linspace(intersect_9, x_4_7[0], 1000)
y_7_9 = slope_7_9 * x_7_9 + c_7_9
plt.plot(x_7_9, y_7_9, linestyle='--', color='b')

"----------------------------Portion 9-10---------------------------------------------"
slope_9_10 = slope(66.31 - 280.7, 267.4 + 0)
c_9_10 = y_7_9[0] - slope_9_10 * x_7_9[0]
x_9_10 = np.linspace(-L_driver, intersect_9, 1000)
y_9_10 = slope_9_10 * x_9_10 + c_9_10
plt.plot(x_9_10, y_9_10, linestyle='--', color='b')

"----------------------------Reflected---------------------------------------------"
slope_4_inf = 1 / (307.34 + 200)
c_4_inf = y_tail[0] - slope_4_inf * x_tail[0]
x_4_inf = np.linspace(x_tail[0], 0, 1000)
y_4_inf = slope_4_inf * x_4_inf + c_4_inf
plt.plot(x_4_inf, y_4_inf, linestyle='--', color='b')

slope_7_inf = 1 / (294 + 133)
c_7_inf = y_4_7[0] - slope_7_inf * x_4_7[0]
x_7_inf = np.linspace(x_4_7[0], 0, 1000)
y_7_inf = slope_7_inf * x_7_inf + c_7_inf
plt.plot(x_7_inf, y_7_inf, linestyle='--', color='b')

slope_9_inf = 1 / (280.7 + 66.31)
c_9_inf = y_7_9[0] - slope_9_inf * x_7_9[0]
x_9_inf = np.linspace(x_7_9[0], 0, 1000)
y_9_inf = slope_9_inf * x_9_inf + c_9_inf
plt.plot(x_9_inf, y_9_inf, linestyle='--', color='b')

slope_10_inf = 1 / (267.4)
c_10_inf = y_9_10[0] - slope_10_inf * x_9_10[0]
x_10_inf = np.linspace(x_9_10[0], 0, 1000)
y_10_inf = slope_10_inf * x_10_inf + c_10_inf
plt.plot(x_10_inf, y_10_inf, linestyle='--', color='b')

# Labels and legend
plt.title('Wave Diagram (x-t Diagram) of the Shock Tube')
plt.xlabel('Position x (m)')
plt.ylabel('Time t (s)')
plt.legend()
plt.xlim(-L_driver, L_driven)
plt.show()
