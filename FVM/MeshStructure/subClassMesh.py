import numpy as np

class Vertex:
    def __init__(self, xyz):
        self.x = xyz[0]
        self.y = xyz[1]
        if len(xyz) == 3:
            self.z = xyz[2]
    

class Edge:
    """
    Clockwise traversal of points to ensure correct orientation
    of orthonormal vector
    """
    def __init__(self, xyz1, xyz2):
        """
        Rotational Matrix
        """
        self.R = np.array((0, -1), (1, 0))
        
        self.xyz1 = np.array(xyz1)
        self.xyz2 = np.array(xyz2)
        self.edge = self.xyz1 - self.xyz2
        self.edge_norm = np.linalg.norm(self.edge)
        
        """
        Outward edge normal
        """
        self.normal = -np.matmul(self.R, self.edge) / self.edge_norm


class Cell:
    def __init__(self, UID, ):
        self.UID = UID
        
         