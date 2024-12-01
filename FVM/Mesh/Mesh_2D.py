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
            self._mesh_initialized = False


    def __del__(self):
        """
        Destrctor of mesh object -> Finalize Gmsh
        """

        gmsh.finalize()


    def _add(self, tag, name, dim=2):
        """

        """
        cur_idx = self._size
        self._entities.append((dim, tag, f"{name} {self._size}"))
        self._size += 1

        return cur_idx


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
                removed_entities.append(entity)
            else:
                raise IndexError(f"Invalid index {idx} for deletion.")

        self._size -= len(removed_entities)
        return removed_entities


    def refine(self, iter=1):
        """
        Refine the mesh

        :return:    None
        """
        if not self._mesh_initialized:
            raise ValueError("Mesh have not been generated yet.")
        
        gmsh.model.mesh.refine()    
        gmsh.model.mesh.optimize("Laplace2D")


    def generate(self):
        """
        Generate the Mesh
        """
        gmsh.model.occ.synchronize()
        gmsh.option.setNumber("Mesh.Algorithm", 5)
        gmsh.model.mesh.generate(2)
        self._mesh_initialized = True


    def getNodes(self):
        return gmsh.model.mesh.getNodes()

    
    def getElements(self):
        return gmsh.model.mesh.getElements()


    def show(self):
        """
        Display the generated mesh using Matplotlib.

        :return     :   None
        """
    
        # Extract node data
        node_tags, node_coords, _ = self.getNodes()
        nodes = node_coords.reshape(-1, 3)[:, :2]  # Extract x and y coordinates

        # Extract element data
        elem_types, elem_tags, elem_node_tags = self.getElements()

        plt.figure(figsize=(8, 4))

        for elem_type, elem_node_tag in zip(elem_types, elem_node_tags):
            if elem_type == 2:  # 3-node triangles
                num_nodes_per_elem = 3
            elif elem_type == 3:  # 4-node quadrilaterals
                num_nodes_per_elem = 4
            else:
                continue  # Skip unsupported element types

            elements = np.array(elem_node_tag).reshape(-1, num_nodes_per_elem) - 1  # Zero-based indexing

            for i, elem in enumerate(elements):
                polygon = nodes[elem]
                polygon = np.vstack([polygon, polygon[0]])  # Close the loop
                plt.plot(polygon[:, 0], polygon[:, 1], 'k-', linewidth=0.5)

                centroid_x = np.mean(polygon[:-1, 0])  # Exclude the repeated last point
                centroid_y = np.mean(polygon[:-1, 1])

                # Label the cell with its unique ID
                cell_id = i  # Retrieve the element ID
                plt.text(centroid_x, centroid_y, str(cell_id), color='red', 
                         fontsize=8, ha='center', va='center')

        plt.gca().set_aspect('equal')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Mesh Visualization')
        plt.grid(False)
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
        polygon_tag = gmsh.model.occ.addPlaneSurface([curve_loop])
        gmsh.model.occ.synchronize()
        
        return self._add(tag=polygon_tag, name="Polygon", dim=2)


    def addRectangle(self, pt, l, h):
        """
        Add a rectangle to the mesh.

        :param pt: Bottom-left corner point (x, y, z).
        :param l: Length of the rectangle.
        :param h: Height of the rectangle.
        :return: Index of the meshed rectangle.
        """
        x, y, z = pt
        rect_tag = gmsh.model.occ.addRectangle(x, y, z, l, h)
        gmsh.model.occ.synchronize()

        return self._add(tag=rect_tag, name="Rectangle", dim=2)


    def addCircle(self, pt, r):
        """
        Add a circle to the mesh.

        :param pt: Center point (x, y, z).
        :param r: Radius of the circle.
        :return: Index of the meshed circle.
        """
        x, y, z = pt
        circle_tag = gmsh.model.occ.addDisk(x, y, z, r, r)
        gmsh.model.occ.synchronize()

        return self._add(tag=circle_tag, name="Circle", dim=2)


    def union(self, idx_1, idx_2):
        """
        Perform a union operation on multiple shapes.

        :param idx_1: Index of the target shape.
        :param idx_2: Index of the tool shape (to intersect).
        :return: Index of the resulting shape.
        """

        if not (0 <= idx_1 < self._size and 0 <= idx_2 < self._size):
            raise IndexError("Invalid shape index for intersection operation.")

        object_tag, tool_tag = self._entities[idx_1][:2], self._entities[idx_2][:2]
        dim, union_tag = gmsh.model.occ.fuse([object_tag], [tool_tag],
                                             removeObject=True, removeTool=True)[0][0]
        gmsh.model.occ.synchronize()
        self.delete([idx_1, idx_2])
        return self._add(tag=union_tag, name="Union", dim=dim)


    def intersection(self, idx_1, idx_2):
        """
        Perform an intersection operation on multiple shapes.

        :param idx_1: Index of the target shape.
        :param idx_2: Index of the tool shape (to intersect).
        :return: Index of the resulting shape.
        """

        if not (0 <= idx_1 < self._size and 0 <= idx_2 < self._size):
            raise IndexError("Invalid shape index for intersection operation.")

        object_tag, tool_tag = self._entities[idx_1][:2], self._entities[idx_2][:2]
        dim, inter_tag = gmsh.model.occ.intersect([object_tag], [(tool_tag)],
                                                  removeObject=True, removeTool=True)[0][0]
        gmsh.model.occ.synchronize()

        self.delete([idx_1, idx_2])
        return self._add(tag=inter_tag, name="Intersect", dim=dim)

        
    def difference(self, idx_1, idx_2):
        """
        Perform a boolean difference operation between two shapes.

        :param idx_1: Index of the target shape.
        :param idx_2: Index of the tool shape (to subtract).
        :return: Index of the resulting shape.
        """

        if not (0 <= idx_1 < self._size and 0 <= idx_2 < self._size):
            raise IndexError("Invalid shape index for difference operation.")

        object_tag, tool_tag = self._entities[idx_1][:2], self._entities[idx_2][:2]
        dim, diff_tag = gmsh.model.occ.cut([object_tag], [tool_tag],
                                           removeObject=True, removeTool=True)[0][0]
        gmsh.model.occ.synchronize()
        
        self.delete([idx_1, idx_2])
        return self._add(tag=diff_tag, name="Difference", dim=dim)