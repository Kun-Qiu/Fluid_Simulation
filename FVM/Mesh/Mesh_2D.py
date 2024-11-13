import gmsh
import matplotlib.pyplot as plt
import numpy as np
from FVM.Mesh import Mesh_Base


class Mesh2D(Mesh_Base.MeshModel):
    _instance = None

    def __new__(cls, *args, **kwargs):
        """Ensure only one instance of the class is created."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, granularity=1e-2):
        """Initialize the Mesh2D instance."""
        if not hasattr(self, "_initialized"):
            self.GRANULARITY = granularity

            gmsh.initialize()
            gmsh.model.add("Mesh_2D")
            self._entities = []
            self._size = 0
            self._initialized = True


    def __del__(self):
        """
        Finalize Gmsh upon object deletion
        """

        gmsh.finalize()


    def delete(self, idx_arr):
        """
        Remove entities from the mesh and the Gmsh model.

        :param idx_arr: List of indices of shapes to be removed.
        :return: The removed shapes.
        """
        idx_arr = np.unique(idx_arr)[::-1]  # Sort indices in reverse order
        removed_entities = []
        for idx in idx_arr:
            if 0 <= idx < self._size:
                entity = self._entities.pop(idx)
                gmsh.model.occ.remove([entity[:2]])
                removed_entities.append(entity)
            else:
                raise IndexError(f"Invalid index {idx} for deletion.")

        self._size -= len(removed_entities)
        gmsh.model.occ.synchronize()
        return removed_entities

    def show(self):
        """
        Display the generated mesh using Matplotlib.
        """
        gmsh.model.occ.synchronize()
        gmsh.model.mesh.generate(2)

        # Extract node data
        node_tags, node_coords, _ = gmsh.model.mesh.getNodes()
        nodes = node_coords.reshape(-1, 3)[:, :2]  # Extract x and y coordinates

        # Extract element data
        elem_types, elem_tags, elem_node_tags = gmsh.model.mesh.getElements()

        plt.figure(figsize=(8, 4))

        for elem_type, elem_node_tag in zip(elem_types, elem_node_tags):
            if elem_type == 2:  # 3-node triangles
                num_nodes_per_elem = 3
            elif elem_type == 3:  # 4-node quadrilaterals
                num_nodes_per_elem = 4
            else:
                continue  # Skip unsupported element types

            elements = np.array(elem_node_tag).reshape(-1, num_nodes_per_elem) - 1  # Zero-based indexing

            for elem in elements:
                polygon = nodes[elem]
                polygon = np.vstack([polygon, polygon[0]])  # Close the loop
                plt.plot(polygon[:, 0], polygon[:, 1], 'k-', linewidth=0.5)

        plt.gca().set_aspect('equal')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Mesh Visualization')
        plt.grid(True)
        plt.show()

    # ----------------------------- Geometry Methods -------------------------------------------------

    def addPolygon(self, ptsList):
        """
        Add a polygon to the mesh.

        :param ptsList: List of vertex points defining the polygon.
        :return: Index of the meshed polygon.
        """
        point_tags = [gmsh.model.occ.addPoint(x, y, 0) for x, y in ptsList]

        line_tags = []
        for i in range(len(point_tags)):
            start = point_tags[i]
            end = point_tags[(i + 1) % len(point_tags)]
            line_tags.append(gmsh.model.occ.addLine(start, end))

        curve_loop = gmsh.model.occ.addCurveLoop(line_tags)
        surface = gmsh.model.occ.addPlaneSurface([curve_loop])
        self._entities.append((2, surface, "Polygon"))
        self._size += 1

        gmsh.model.occ.synchronize()
        return self._size - 1

    def addRectangle(self, pt, l, h):
        """
        Add a rectangle to the mesh.

        :param pt: Bottom-left corner point (x, y, z).
        :param l: Length of the rectangle.
        :param h: Height of the rectangle.
        :return: Index of the meshed rectangle.
        """
        x, y, z = pt
        rect = gmsh.model.occ.addRectangle(x, y, z, l, h)
        self._entities.append((2, rect, "Rectangle"))
        self._size += 1

        gmsh.model.occ.synchronize()
        return self._size - 1

    def addCircle(self, pt, r):
        """
        Add a circle to the mesh.

        :param pt: Center point (x, y, z).
        :param r: Radius of the circle.
        :return: Index of the meshed circle.
        """
        x, y, z = pt
        circle = gmsh.model.occ.addDisk(x, y, z, r, r)
        self._entities.append((2, circle, "Circle"))
        self._size += 1

        gmsh.model.occ.synchronize()
        return self._size - 1

    def union(self, idx_arr):
        """
        Perform a union operation on multiple shapes.

        :param idx_arr: List of indices of shapes to union.
        :return: Index of the resulting shape.
        """
        if not all(0 <= idx < self._size for idx in idx_arr):
            raise IndexError("Invalid shape index for union operation.")

        entities = [self._entities[idx][:2] for idx in idx_arr]
        union_result = gmsh.model.occ.union(entities)
        gmsh.model.occ.synchronize()

        self.delete(idx_arr)

        new_entity = union_result[0][0]
        self._entities.append((*new_entity, f"Union {self._size}"))
        self._size += 1

        return self._size - 1

    def intersection(self, idx_arr):
        """
        Perform an intersection operation on multiple shapes.

        :param idx_arr: List of indices of shapes to intersect.
        :return: Index of the resulting shape.
        """
        if not all(0 <= idx < self._size for idx in idx_arr):
            raise IndexError("Invalid shape index for intersection operation.")

        entities = [self._entities[idx][:2] for idx in idx_arr]
        inter_result = gmsh.model.occ.intersect(entities)
        gmsh.model.occ.synchronize()

        self.delete(idx_arr)

        new_entity = inter_result[0][0]
        self._entities.append((*new_entity, f"Intersection {self._size}"))
        self._size += 1

        return self._size - 1

    def difference(self, idx_1, idx_2):
        """
        Perform a boolean difference operation between two shapes.

        :param idx_1: Index of the target shape.
        :param idx_2: Index of the tool shape (to subtract).
        :return: Index of the resulting shape.
        """
        if not (0 <= idx_1 < self._size and 0 <= idx_2 < self._size):
            raise IndexError("Invalid shape index for difference operation.")

        target_entity = self._entities[idx_1][:2]
        tool_entity = self._entities[idx_2][:2]
        diff_result = gmsh.model.occ.cut([target_entity], [tool_entity])
        gmsh.model.occ.synchronize()

        if not diff_result[0]:
            raise ValueError("Difference operation resulted in an empty shape.")

        self.delete([idx_1, idx_2])

        new_entity = diff_result[0][0]
        self._entities.append((*new_entity, f"Difference {self._size}"))
        self._size += 1

        return self._size - 1
    

    def plotUsingGmsh(self):
        """
        Plot the mesh using Gmsh's built-in GUI.
        """
        try:
            gmsh.model.occ.synchronize()  # Ensure the model is up-to-date
            # gmsh.model.mesh.generate(2)   # Generate the 2D mesh
            gmsh.fltk.run()               # Open the Gmsh graphical interface
        except Exception as e:
            print(f"Error while plotting with Gmsh: {e}")
        finally:
            gmsh.finalize()  # Finalize Gmsh after plotting