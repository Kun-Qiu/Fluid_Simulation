import matplotlib.pyplot as plt
import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve

"""
Heat equation subjected to the following 

Dirichlet Boundary Conditions:
u[t, 0] = 0 = u[t, length]

Neumann Boundary Conditons:
dT/dt[t, 0] = 0 = dT/dt[t, length]
"""


class Heat_Eqn:
    def __init__(self, k, rho, c_p, N, dt, t, length, T_i):

        if isinstance(length, (float, int)):
            self.DIM = 1
            self.LENGTH = [length]
        elif hasattr(length, "__iter__"):
            self.DIM = len(length)
            self.LENGTH = length

        self.NUM_PT = N  # Number of spatial points
        for i in range(self.DIM):
            setattr(self, f'SPACE_STEP_X_{i + 1}', self.LENGTH[i] / (N-1))
        self.TIME_STEP = dt  # Temporal Resolution
        self.TIME = t
        self.ALPHA = k / (rho * c_p)  # Thermal diffusivity
        self.A = self.Ac = self.coeffs = None
        self.b = T_i

        """
        The approximate solutions can still contain (decaying) spurious oscillations 
        if the ratio of time step Δt times the thermal diffusivity over the square of space step, 
        Δx^2 is larger than 1/2
        
        """
        # If using the explicit method
        # Check stability condition for explicit method (Courant–Friedrichs–Lewy condition)
        # if self.dt > self.dx ** 2 / (2 * self.alpha):
        #     raise ValueError("Time step too large for stability; consider reducing dt or increasing dx.")

    def construct_grid(self):
        grid_range = [np.linspace(0, self.LENGTH[i], self.NUM_PT) for i in range(self.DIM)]
        self.GRID = grid_range

        if self.DIM == 1:
            return grid_range[0]
        elif self.DIM == 2:
            x, y = np.meshgrid(grid_range[0], grid_range[1], indexing='ij')
            return x, y
        elif self.DIM == 3:
            x, y, z = np.meshgrid(grid_range[0], grid_range[1], grid_range[2], indexing='ij')
            return x, y, z
        else:
            raise ValueError("Dimension must be 1, 2, or 3.")

    def construct_matrix(self):
        """
        Construct the matrix for solving the heat transfer equation
        Coefficient - alpha * dt / x_i^2
        :return:
        """
        self.coeffs = [
            (self.ALPHA * self.TIME_STEP) / np.square(getattr(self, f"SPACE_STEP_X_{i}"))
            for i in range(1, self.DIM + 1)
        ]
        print(self.coeffs)
        grid_size = np.power(self.NUM_PT, self.DIM)

        if self.DIM == 1:
            diag = np.ones(grid_size) * (1 + sum(val for val in self.coeffs))
            diag2 = np.ones(grid_size) * (1 - sum(val for val in self.coeffs))
            diag[0] = diag[-1] = diag2[0] = diag2[-1] = 1
        elif self.DIM == 2:
            diag = np.ones(grid_size) * (1 + sum((2 * val) for val in self.coeffs))
            diag[0:self.NUM_PT] = diag[-self.NUM_PT:] = 1
            diag[::self.NUM_PT] = diag[self.NUM_PT - 1::self.NUM_PT] = 1

        diagonals = [diag]
        diag2 = [diag2]
        offsets = [0]

        for i, coeff in enumerate(self.coeffs, start=1):
            off_diag = np.ones(grid_size - 2 * i) * (-coeff) / 2
            diagonals.extend([np.append(off_diag.copy(), 0), np.append([0], off_diag.copy())])
            diag2.extend([np.append(-1 * off_diag.copy(), 0), np.append([0], -1 * off_diag.copy())])
            offsets.extend([-i, i])

        self.A = diags(diagonals, offsets=offsets, format='csc')
        self.Ac = diags(diag2, offsets=offsets, format='csc')

    def solve(self):
        time = 0
        plt.ion()
        fig, ax = plt.subplots()
        # Time-stepping loop
        while time + self.TIME_STEP < self.TIME:

            # Update plot based on dimension
            if self.DIM == 1:
                x = self.GRID[0]

                line, = ax.plot(x, self.b, label=f"t={time}")
                plt.xlabel("Position")
                plt.ylabel("Temperature")

                # temp = self.Ac.toarray()
                rhs = self.Ac.dot(self.b)
                T_new = spsolve(self.A, rhs)

                line.set_ydata(T_new)
                ax.legend([f"t={time:.2f}"])

            elif self.DIM == 2:
                x, y = np.meshgrid(self.GRID[0], self.GRID[1], indexing='ij')

                # Initial plot
                contour = ax.contourf(x, y, self.b.copy(), cmap='hot')
                plt.xlabel("X Position")
                plt.ylabel("Y Position")
                colorbar = fig.colorbar(contour, ax=ax, label="Temperature")

                T_flattened = self.b.flatten()
                T_new = spsolve(self.A, T_flattened).reshape(np.shape(self.b))

                # Dirchelet Condition -> Left, Right, Top, Bottom Boundaries are zeros
                T_new[0, :] = T_new[-1, :] = 0  # Bottom boundary
                T_new[:, 0] = T_new[:, -1] = 0

                colorbar.remove()
                contour = ax.contourf(x, y, T_new, cmap='hot')
                colorbar.update_normal(contour)


            elif self.DIM == 3:
                ax = fig.add_subplot(111, projection='3d')
                x, y, z = np.meshgrid(self.GRID[0], self.GRID[1], self.GRID[2], indexing='ij')

                # Initial plot
                scatter = ax.scatter(x.flatten(), y.flatten(), z.flatten(), c=self.b.flatten(), cmap='hot')
                fig.colorbar(scatter, ax=ax, label="Temperature")
                ax.set_xlabel("X Position")
                ax.set_ylabel("Y Position")
                ax.set_zlabel("Z Position")

                ax.clear()
                scatter = ax.scatter(x.flatten(), y.flatten(), z.flatten(), c=T_new.flatten(), cmap='hot')
                fig.colorbar(scatter, ax=ax, label="Temperature")
                ax.set_xlabel("X Position")
                ax.set_ylabel("Y Position")
                ax.set_zlabel("Z Position")

                # Update the temperature array for the next step
            self.b = T_new
            time += self.TIME_STEP

            # Update the plot
            plt.draw()
            plt.pause(0.5)

        plt.ioff()  # Turn off interactive mode
        plt.show()


k = 237  # W/mK
rho = 2710  # kg/m^3
c_p = 900  # Specific heat capacity
N = 100  # Number of spatial points
dt = 10  # Time step size
time = 2000
init_temp = 100

length = [1.0]  # Length of the domain
T_initial = np.zeros(N)
T_initial[0] = T_initial[-1] = init_temp

# length = [2.0, 1.0]  # Length of the domain
# T_initial = np.zeros((N, N))
# T_initial[0, :] = T_initial[-1, :] = T_initial[:, 0] = T_initial[:, -1] = init_temp

# Create an instance of the Heat_Eqn class
heat_eqn = Heat_Eqn(k, rho, c_p, N, dt, time, length, T_initial)
heat_eqn.construct_matrix()
grid_1d = heat_eqn.construct_grid()
heat_eqn.solve()
