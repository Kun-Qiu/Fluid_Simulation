import numpy as np

class MeshRep:
    def __init__(self, vertices, edges, faces, cells):
        """
        Initialize the mesh representation.
        
        Args:
            vertices (ndarray): Array of vertex coordinates, shape (n_vertices, 3).
            edges (ndarray): Array of edges, each row [v1, v2] (indices of vertices).
            faces (ndarray): List of arrays, each array contains vertex indices forming a face.
            cells (ndarray): List of arrays, each array contains face indices forming a cell.
        """
        self.vertices = np.array(vertices)  # Vertex coordinates
        self.edges = np.array(edges)  # Edges (pairs of vertex indices)
        self.faces = [np.array(face) for face in faces]  # Faces (arrays of vertex indices)
        self.cells = [np.array(cell) for cell in cells]  # Cells (arrays of face indices)
    
    def compute_face_normals(self):
        """
        Compute normals for all faces.
        
        Returns:
            ndarray: Array of face normals, shape (n_faces, 3).
        """
        normals = []
        for face in self.faces:
            # Use the first three vertices of the face to compute the normal
            v0, v1, v2 = self.vertices[face[:3]]
            normal = np.cross(v1 - v0, v2 - v0)
            normals.append(normal / np.linalg.norm(normal))
        return np.array(normals)
    
    def compute_cell_volumes(self):
        """
        Compute volumes for all cells (assuming convex polyhedra).
        
        Returns:
            ndarray: Array of cell volumes, shape (n_cells,).
        """
        volumes = []
        for cell in self.cells:
            cell_volume = 0.0
            for face_idx in cell:
                face = self.faces[face_idx]
                centroid = np.mean(self.vertices[face], axis=0)
                normal = np.mean(self.compute_face_normals()[face_idx])
                # Compute the volume contribution by this face
                tetra_volume = np.dot(centroid, normal)
                cell_volume += abs(tetra_volume)
            volumes.append(cell_volume / 3.0)
        return np.array(volumes)
    
    def boundary_faces(self):
        """
        Identify boundary faces (faces belonging to only one cell).
        
        Returns:
            list: List of boundary face indices.
        """
        face_count = {}
        for cell in self.cells:
            for face_idx in cell:
                face_count[face_idx] = face_count.get(face_idx, 0) + 1
        return [face for face, count in face_count.items() if count == 1]

    def add_vertex(self, vertex):
        """
        Add a new vertex to the mesh.
        
        Args:
            vertex (list or tuple): Coordinates of the new vertex.
        """
        self.vertices = np.vstack([self.vertices, vertex])
    
    def add_edge(self, edge):
        """
        Add a new edge to the mesh.
        
        Args:
            edge (list or tuple): Indices of the two vertices forming the edge.
        """
        self.edges = np.vstack([self.edges, edge])
    
    def add_face(self, face):
        """
        Add a new face to the mesh.
        
        Args:
            face (list): Vertex indices forming the face.
        """
        self.faces.append(np.array(face))
    
    def add_cell(self, cell):
        """
        Add a new cell to the mesh.
        
        Args:
            cell (list): Face indices forming the cell.
        """
        self.cells.append(np.array(cell))
