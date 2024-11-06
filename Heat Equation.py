import matplotlib.pyplot as plt
import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve

"""
Heat equation subjected to the following

If using the explicit method check stability condition for explicit method 
(Courant–Friedrichs–Lewy condition)

The Crank Nicolson approximate solutions can still contain spurious oscillations 
if the ratio of (time step Δt * thermal diffusivity) over the square of space step 
Δx^2 is larger than 1/2

Dirichlet Boundary Conditions:
u[t, 0] = 0 = u[t, length]

Neumann Boundary Conditons:
dT/dt[t, 0] = 0 = dT/dt[t, length]
"""


class HeatEqnBase:
    def __init__(self, k, rho, c_p, N, dt, t, length, T_i):
        if isinstance(length, (float, int)):
            self.DIM = 1
            self.LENGTH = [length]
        elif hasattr(length, "__iter__"):
            self.DIM = len(length)
            self.LENGTH = length

        self.NUM_PT = N
        self.TIME_STEP = dt
        self.TIME = t
        self.ALPHA = k / (rho * c_p)
        self.b = T_i
        self.A = None
        self.Ac = None
        self.LIMIT_Y = np.max(T_i)
        self.GRID = None
        self.time = 0
        self.fig, self.ax = plt.subplots()

    def construct_grid(self):
        raise NotImplementedError("This method should be implemented in child classes.")

    def build_matrix(self):
        raise NotImplementedError("This method should be implemented in child classes.")

    def solve(self):
        raise NotImplementedError("This method should be implemented in child classes.")

    def update_plot(self, time):
        raise NotImplementedError("This method should be implemented in child classes.")


class HeatEqn1D(HeatEqnBase):
    def __init__(self, k, rho, c_p, N, dt, t, length, T_i):
        super().__init__(k, rho, c_p, N, dt, t, length, T_i)
        self.SPACE_STEP_X_1 = self.LENGTH[0] / (self.NUM_PT - 1)

    def construct_grid(self):
        grid_range = np.linspace(0, self.LENGTH[0], self.NUM_PT)
        self.GRID = grid_range

        return grid_range

    def build_matrix(self):
        coeffs = (self.ALPHA * self.TIME_STEP) / np.square(self.SPACE_STEP_X_1)
        grid_size = np.power(self.NUM_PT, self.DIM)
        offsets = [0, -1, 1]

        def general_matrix(main_diagonal, off_diagonal):
            # Initialize main diagonal and set values based on main_diagonal parameter
            diag = np.ones(grid_size)
            diag[1:self.NUM_PT - 1] *= main_diagonal

            # Initialize off-diagonal values
            off_diag = np.ones(grid_size - 2) * off_diagonal

            return [diag, np.append(off_diag, 0), np.append(0, off_diag)]

        self.A = diags(general_matrix((1 + coeffs), (-coeffs / 2)), offsets=offsets, format='csc')
        self.Ac = diags(general_matrix((1 - coeffs), (coeffs / 2)), offsets=offsets, format='csc')

    def solve(self):
        plt.ion()
        self.construct_grid()  # Ensure grid is initialized
        self.build_matrix()

        while self.time < self.TIME:
            rhs = self.Ac.dot(self.b)
            T_new = spsolve(self.A, rhs)
            self.b = T_new

            self.update_plot(self.time)
            plt.pause(0.1)

            self.time += self.TIME_STEP

    def update_plot(self, time):
        """Updates the plot with the current temperature profile and time."""
        self.ax.clear()
        self.ax.plot(self.GRID, self.b, label=f"t={time:.2f}")
        self.ax.set_xlabel("Position")
        self.ax.set_ylabel("Temperature")
        self.ax.set_ylim(0, self.LIMIT_Y)  # Set y-axis limits
        self.ax.legend()
        plt.draw()


class HeatEqn2D(HeatEqnBase):
    def __init__(self, k, rho, c_p, N, dt, t, length, T_i):
        super().__init__(k, rho, c_p, N, dt, t, length, T_i)
        self.SPACE_STEP_X_1 = self.LENGTH[0] / (self.NUM_PT - 1)
        self.SPACE_STEP_X_2 = self.LENGTH[1] / (self.NUM_PT - 1)
        self.colorbar = None

    def construct_grid(self):
        x = np.linspace(0, self.LENGTH[0], self.NUM_PT)
        y = np.linspace(0, self.LENGTH[1], self.NUM_PT)
        self.GRID = np.meshgrid(x, y, indexing='ij')
        return self.GRID

    def build_matrix(self):
        coeffs = (self.ALPHA * self.TIME_STEP) * \
                 np.array([1 / np.square(self.SPACE_STEP_X_1),
                           1 / np.square(self.SPACE_STEP_X_2)])

        grid_size = np.power(self.NUM_PT, self.DIM)
        offsets = [0, -1, 1, -self.NUM_PT, self.NUM_PT]

        def general_matrix(main_diagonal, off_diagonal_x, off_diagonal_y, NUM_PT):
            diag = np.ones(grid_size)
            off_diag_1 = np.zeros(grid_size)
            off_diag_2 = np.zeros(grid_size)

            non_boundary_indices = np.where(
                (np.arange(grid_size) % NUM_PT != 0) &  # Not on left boundary
                ((np.arange(grid_size) + 1) % NUM_PT != 0) &  # Not on right boundary
                (np.arange(grid_size) >= NUM_PT) &  # Not in top boundary row
                (np.arange(grid_size) < grid_size - NUM_PT)  # Not in bottom boundary row
            )

            diag[non_boundary_indices] *= main_diagonal
            off_diag_1[non_boundary_indices] = off_diagonal_x
            off_diag_2[non_boundary_indices] = off_diagonal_y

            return [diag, off_diag_1[1:], off_diag_1[:-1],
                    off_diag_2[self.NUM_PT:], off_diag_2[:(-self.NUM_PT)]]

        self.A = diags(general_matrix((1 + 2 * (coeffs[0] + coeffs[1])),
                                      (-coeffs[0]), -coeffs[1], self.NUM_PT),
                       offsets=offsets, format='csc')
        self.Ac = diags(general_matrix((1 - 2 * (coeffs[0] + coeffs[1])),
                                       (coeffs[0]), coeffs[1], self.NUM_PT),
                        offsets=offsets, format='csc')

    def solve(self):
        plt.ion()
        self.construct_grid()  # Ensure grid is initialized
        self.build_matrix()

        mat_shape = np.shape(self.b)
        while self.time < self.TIME:
            rhs = self.Ac.dot(self.b.flatten())
            T_new = spsolve(self.A, rhs)
            self.b = T_new.reshape(mat_shape)

            self.update_plot(self.time)
            plt.pause(0.1)

            self.time += self.TIME_STEP

    def update_plot(self, time):
        """Updates the plot with the current temperature profile and time."""
        self.ax.clear()
        contour = self.ax.contourf(self.GRID[0], self.GRID[1], self.b, cmap='hot')

        # Remove previous colorbar if it exists
        if self.colorbar is not None:
            self.colorbar.remove()

        # Add new colorbar and store the reference
        self.colorbar = plt.colorbar(contour, ax=self.ax, label="Temperature")

        self.ax.set_title(f"Temperature at t={time:.2f}")
        self.ax.set_xlabel("X Position")
        self.ax.set_ylabel("Y Position")
        plt.draw()


# class HeatEqn3D(HeatEqnBase):
#     def construct_grid(self):
#         self.SPACE_STEP_X_1 = self.LENGTH[0] / (self.NUM_PT - 1)
#         self.SPACE_STEP_X_2 = self.LENGTH[1] / (self.NUM_PT - 1)
#         self.SPACE_STEP_X_3 = self.LENGTH[2] / (self.NUM_PT - 1)
#         x = np.linspace(0, self.LENGTH[0], self.NUM_PT)
#         y = np.linspace(0, self.LENGTH[1], self.NUM_PT)
#         z = np.linspace(0, self.LENGTH[2], self.NUM_PT)
#         self.GRID = np.meshgrid(x, y, z, indexing='ij')
#         return self.GRID
#
#     def update_plot(self, ax, time):
#         ax.clear()
#         x, y, z = self.GRID
#         scatter = ax.scatter(x.flatten(), y.flatten(), z.flatten(), c=self.b.flatten(), cmap='hot')
#         plt.colorbar(scatter, ax=ax)
#         ax.set_xlabel("X Position")
#         ax.set_ylabel("Y Position")
#         ax.set_zlabel("Z Position")


# Example Usage
k = 237
rho = 2710
c_p = 900
N = 100
dt = 0.1
time = 2000
init_temp = 100
length_1d = [1.0]
T_initial_1d = np.zeros(N)
T_initial_1d[0] = T_initial_1d[-1] = init_temp

# heat_eqn_1d = HeatEqn1D(k, rho, c_p, N, dt, time, length_1d, T_initial_1d)
# heat_eqn_1d.solve()

length_2d = [2.0, 1.0]  # Length of the domain
T_initial_2d = np.zeros((N, N))
T_initial_2d[0, :] = T_initial_2d[-1, :] = T_initial_2d[:, 0] = T_initial_2d[:, -1] = init_temp

heat_eqn_2d = HeatEqn2D(k, rho, c_p, N, dt, time, length_2d, T_initial_2d)
heat_eqn_2d.solve()
