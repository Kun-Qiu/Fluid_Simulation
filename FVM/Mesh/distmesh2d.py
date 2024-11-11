import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import Delaunay


class MeshGenerator:
    def __init__(self, x_min, x_max, y_min, y_max, resolution):
        """
        Initializes the mesh generator with the domain boundaries and resolution.

        Parameters:
        - x_min, x_max: float, domain boundaries in the x-direction
        - y_min, y_max: float, domain boundaries in the y-direction
        - resolution: float, spacing between points in the grid
        """
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.resolution = resolution
        self.points = None
        self.tri = None

    def generate_meshgrid(self):
        """
        Generates a mesh grid of points within the specified domain.
        """
        x = np.arange(self.x_min, self.x_max + self.resolution, self.resolution)
        y = np.arange(self.y_min, self.y_max + self.resolution, self.resolution)
        xx, yy = np.meshgrid(x, y)
        self.points = np.vstack((xx.ravel(), yy.ravel())).T

    def remove_outside_points(self, condition_func):
        """
        Removes points that do not satisfy a given condition.

        Parameters:
        - condition_func: function, returns True for points to keep
        """
        mask = condition_func(self.points)
        self.points = self.points[mask]

    def triangulate(self):
        """
        Generates a triangulation of the current set of points.
        """
        if self.points is not None:
            self.tri = Delaunay(self.points)
        else:
            raise ValueError("Points have not been generated.")

    def plot_wireframe(self):
        """
        Plots the wireframe mesh of the triangulated points.
        """
        if self.tri is not None:
            plt.triplot(self.points[:, 0], self.points[:, 1], self.tri.simplices)
            plt.plot(self.points[:, 0], self.points[:, 1], 'o')
            plt.show()
        else:
            raise ValueError("Triangulation has not been performed.")

    def smooth_mesh(self, iterations=1):
        """
        Smooths the mesh using Laplacian smoothing.

        Parameters:
        - iterations: int, number of smoothing iterations
        """
        if self.tri is None:
            raise ValueError("Triangulation has not been performed.")

        for _ in range(iterations):
            new_points = self.points.copy()
            for idx in range(len(self.points)):
                neighbors = self.get_vertex_neighbors(idx)
                if neighbors.size > 0:
                    new_points[idx] = np.mean(self.points[neighbors], axis=0)
            self.points = new_points
            self.tri = Delaunay(self.points)

    def get_vertex_neighbors(self, idx):
        """
        Retrieves the indices of neighboring vertices for a given vertex.

        Parameters:
        - idx: int, index of the vertex

        Returns:
        - neighbors: ndarray, indices of neighboring vertices
        """
        neighbors = set()
        indices, indptr = self.tri.vertex_neighbor_vertices
        start, end = indices[idx], indices[idx + 1]
        neighbors.update(indptr[start:end])
        neighbors.discard(idx)
        return np.array(list(neighbors))


# Define a condition function to keep points inside a circle
def inside_circle(points, center=(0, 0), radius=1):
    return np.sum((points - center) ** 2, axis=1) <= radius ** 2


# Initialize the mesh generator
mesh_gen = MeshGenerator(x_min=-2, x_max=2, y_min=-2, y_max=2, resolution=0.1)

# Generate the mesh grid
mesh_gen.generate_meshgrid()

# Remove points outside the circle
mesh_gen.remove_outside_points(lambda pts: inside_circle(pts, radius=2))

# Perform triangulation
mesh_gen.triangulate()

# Plot the initial wireframe mesh
mesh_gen.plot_wireframe()

# Smooth the mesh
mesh_gen.smooth_mesh(iterations=10)

# Plot the smoothed wireframe mesh
mesh_gen.plot_wireframe()
