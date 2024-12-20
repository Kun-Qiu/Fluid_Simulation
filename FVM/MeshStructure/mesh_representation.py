import numpy as np
from scipy.sparse import csr_matrix

class VertexBasedMesh:
    def __init__(self):
        self.vertices   = {}        # Vertex data
        self.edges      = {}        # Edge data
        self.cells      = {}        # Cell data
        self.neighbors  = {}        # Neighbor relationships

    # Add a vertex
    def add_vertex(self, v_id, coords):
        self.vertices[v_id] = {
            "coords": np.array(coords),
            "edges": set(),
            "cells": set()
        }

    # Add an edge
    def add_edge(self, e_id, v1, v2):
        self.edges[e_id] = {
            "vertices": (v1, v2),
            "cells": set()
        }
        # Update vertex connectivity
        self.vertices[v1]["edges"].add(e_id)
        self.vertices[v2]["edges"].add(e_id)

    # Add a cell
    def add_cell(self, c_id, vertex_ids, edge_ids):
        # Calculate centroid and volume
        coords = np.array([self.vertices[v_id]["coords"] for v_id in vertex_ids])
        centroid = coords.mean(axis=0)
        volume = 0.5 * abs(np.cross(coords[1] - coords[0], coords[2] - coords[0]))  # For 2D triangle
        
        self.cells[c_id] = {
            "vertices": vertex_ids,
            "edges": edge_ids,
            "centroid": centroid,
            "volume": volume
        }
        # Update vertex and edge connectivity
        for v_id in vertex_ids:
            self.vertices[v_id]["cells"].add(c_id)
        for e_id in edge_ids:
            self.edges[e_id]["cells"].add(c_id)
        self.neighbors[c_id] = set()  # Initialize neighbor list

    # Set neighbors for a cell
    def add_neighbors(self, c_id, neighbor_ids):
        self.neighbors[c_id].update(neighbor_ids)

    # Access cell neighbors
    def get_neighbors(self, c_id):
        return self.neighbors.get(c_id, set())

    # Access boundary edges
    def get_boundary_edges(self):
        return [e_id for e_id, edge_data in self.edges.items() if len(edge_data["cells"]) == 1]

    # Visualize the mesh
    def visualize(self):
        import matplotlib.pyplot as plt

        plt.figure(figsize=(8, 6))
        for e_id, edge_data in self.edges.items():
            v1, v2 = edge_data["vertices"]
            coords = np.array([self.vertices[v1]["coords"], self.vertices[v2]["coords"]])
            plt.plot(coords[:, 0], coords[:, 1], 'k-', linewidth=0.5)
        
        for v_id, vertex_data in self.vertices.items():
            x, y = vertex_data["coords"]
            plt.plot(x, y, 'ro', markersize=3)
            plt.text(x, y, str(v_id), color="blue", fontsize=8)

        plt.xlabel("X")
        plt.ylabel("Y")
        plt.title("Mesh Visualization")
        plt.axis("equal")
        plt.show()

    # Get sparse adjacency matrix for vertices
    def get_vertex_adjacency_matrix(self):
        num_vertices = len(self.vertices)
        adjacency = csr_matrix((num_vertices, num_vertices), dtype=int)
        for e_id, edge_data in self.edges.items():
            v1, v2 = edge_data["vertices"]
            adjacency[v1, v2] = 1
            adjacency[v2, v1] = 1
        return adjacency

    # Flux computation skeleton
    def compute_fluxes(self):
        # Example placeholder for flux calculations
        fluxes = {}
        for c_id, cell_data in self.cells.items():
            centroid = cell_data["centroid"]
            for neighbor_id in self.neighbors[c_id]:
                neighbor_centroid = self.cells[neighbor_id]["centroid"]
                # Flux computation logic here
                fluxes[(c_id, neighbor_id)] = np.linalg.norm(neighbor_centroid - centroid)
        return fluxes
