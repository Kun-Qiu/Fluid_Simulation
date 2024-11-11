import numpy as np

from shape import Shape


class Triangle(Shape):
    def __init__(self, vertices):
        """
        Initialize a Triangle with given vertices.

        Parameters:
        vertices (list of list): A list of three vertices, where each vertex is a list [x, y].
        """

        if len(vertices) != 3:
            raise ValueError("A triangle must have exactly three vertices.")
        super().__init__(vertices)
        self.centroid = self.calcCellCentroid()
        self.edges = self.calculate_edges()

    def calcCellCentroid(self):
        """Calculate the centroid of the triangle."""
        return np.mean(self.VERTICES, axis=0)

    def calcEdges(self):
        """Calculate the edges of the triangle."""
        edges = []
        for i in range(3):
            edge = self.vertices[(i + 1) % 3] - self.vertices[i]
            edges.append(edge)
        return edges

    def defConnectivity(self):
        """Define the connectivity of the triangle's vertices."""
        # In this simple case, each triangle's connectivity is just the list of its vertices
        return [0, 1, 2]

    def calVolume(self):
        """Calculate the area of the triangle using the cross product method."""
        # Using vertices A, B, and C
        surface_vector = 0.5 * np.cross((self.VERTICES[1] - self.VERTICES[0]),
                                        (self.VERTICES[2] - self.VERTICES[0]))

        self.VOLUME = np.linalg.norm(surface_vector)

        return 0.5 * abs((B[0] - A[0]) * (C[1] - A[1]) - (C[0] - A[0]) * (B[1] - A[1]))

    def perimeter(self):
        """Calculate the perimeter of the triangle."""
        return sum(np.linalg.norm(edge) for edge in self.edges)
