import gmsh
import matplotlib.pyplot as plt
import numpy as np
from Mesh import Mesh_Base


class MeshModel(Mesh_Base): 
    _instance = None 

    def __new__(cls, *args, **kwargs):
        # Ensure only one instance is created
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, granularity=1e-2):
        # Initialize only if it's the first instance
        if not hasattr(self, "_initialized"):
            self.GRANULARITY = granularity
            self._initialize_gmsh()  # Encapsulate GMSH initialization
            self.MESH = gmsh.model.add("Mesh_2D")
            self._initialized = True
            self._entities = []


    def addPolygon(self, ptsList):
        """Add a polygon using `gmsh.model.occ`."""
        point_tags = [gmsh.model.occ.addPoint(x, y, 0) for x, y in ptsList]
        
        # Create lines between consecutive points
        line_tags = []
        for i in range(len(point_tags)):
            start = point_tags[i]
            end = point_tags[(i + 1) % len(point_tags)]
            line_tags.append(gmsh.model.occ.addLine(start, end))
        
        # Create a wire (closed loop) and a surface
        wire = gmsh.model.occ.addWire(line_tags)
        surface = gmsh.model.occ.addPlaneSurface([wire])
        self._entities.append((2, surface, "Polygon"))


    def addRectangle(self, pt, l, h):
        """Add a rectangle using `gmsh.model.occ`."""
        x, y, z = pt
        rect = gmsh.model.occ.addRectangle(x, y, z, l, h)
        self._entities.append((2, rect, "Rectangle"))


    def addCircle(self, pt, r):
        """Add a circle using `gmsh.model.occ`."""
        x, y, z = pt
        circle = gmsh.model.occ.addDisk(x, y, z, r)
        self._entities.append((2, circle, "Circle"))


    def union(self, shape1, shape2):
        """
        Union operation of two shapes
        """
        

    def discretize_rectangle_with_global_mesh_size():
        try:
            gmsh.initialize()
            gmsh.model.add("rectangle_global")

            # Parameters for the rectangle
            rect_width = 10
            rect_height = 5
            mesh_size = 0.25  # Global mesh size

            # Create four corner points with the global mesh size
            p1 = gmsh.model.occ.addPoint(0, 0, 0, mesh_size)
            p2 = gmsh.model.occ.addPoint(rect_width, 0, 0, mesh_size)
            p3 = gmsh.model.occ.addPoint(rect_width, rect_height, 0, mesh_size)
            p4 = gmsh.model.occ.addPoint(0, rect_height, 0, mesh_size)

            # Create lines between the points
            l1 = gmsh.model.occ.addLine(p1, p2)
            l2 = gmsh.model.occ.addLine(p2, p3)
            l3 = gmsh.model.occ.addLine(p3, p4)
            l4 = gmsh.model.occ.addLine(p4, p1)

            # Create a curve loop and plane surface
            loop = gmsh.model.occ.addCurveLoop([l1, l2, l3, l4])
            surface = gmsh.model.occ.addPlaneSurface([loop])

            gmsh.model.occ.synchronize()

            # Add a physical group for the surface
            gmsh.model.addPhysicalGroup(2, [surface], 1)

            # Generate the mesh
            gmsh.model.mesh.generate(2)

            # Extract and plot the mesh as before
            plot_mesh()

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            gmsh.finalize()

    def plot_mesh():
        # Extract node data
        node_tags, node_coords, _ = gmsh.model.mesh.getNodes()
        nodes = node_coords.reshape(-1, 3)[:, :2]  # Extract x and y coordinates

        # Extract element data
        elem_types, elem_tags, elem_node_tags = gmsh.model.mesh.getElements(2, 1)  # Surface physical group id =1

        # Determine element type
        if elem_types[0] == 2:  # 3-node triangles
            num_nodes_per_elem = 3
        elif elem_types[0] == 3:  # 4-node quadrilaterals
            num_nodes_per_elem = 4
        else:
            raise ValueError(f"Unsupported element type: {elem_types[0]}")

        elements = np.array(elem_node_tags[0]).reshape(-1, num_nodes_per_elem) - 1  # zero-based indexing

        # Plotting the mesh
        plt.figure(figsize=(8, 4))
        for elem in elements:
            polygon = nodes[elem]
            polygon = np.vstack([polygon, polygon[0]])  # Close the loop
            plt.plot(polygon[:, 0], polygon[:, 1], 'k-', linewidth=0.5)

        plt.gca().set_aspect('equal')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Mesh with Global Mesh Size')
        plt.grid(True)
        plt.show()

discretize_rectangle_with_global_mesh_size()
