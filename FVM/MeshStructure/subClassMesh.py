import numpy as np

class Vertex:
    def __init__(self, x, y, z = 0):
        self.x = x
        self.y = y
        self.z = z
    

class Edge:
    """
    Clockwise traversal of points to ensure correct orientation
    of orthonormal vector
    """
    def __init__(self, vt1, vt2):
        """
        Rotational Matrix
        """
        self.R = np.array((0, -1), (1, 0))
        
        self.vt1 = np.array(vt1)
        self.vt2 = np.array(vt2)
        self.edge = self.vt1 - self.vt2
        self.edge_norm = np.linalg.norm(self.edge)
        
        """
        Outward edge normal
        """
        self.normal = -np.matmul(self.R, self.edge) / self.edge_norm

         