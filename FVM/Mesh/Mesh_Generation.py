import gmsh
import matplotlib.pyplot as plt
import numpy as np


def create_mesh_and_plot():
    # Initialize gmsh
    gmsh.initialize()
    gmsh.model.add("rectangle_with_circle")

    # Parameters
    rect_width = 10
    rect_height = 5
    circle_radius = 1.5
    circle_center = (rect_width / 2, rect_height / 2)

    # Create the rectangle
    rect = gmsh.model.occ.addRectangle(0, 0, 0, rect_width, rect_height)

    # Create the circle
    circle = gmsh.model.occ.addDisk(circle_center[0], circle_center[1], 0, circle_radius)

    # Cut the circle out of the rectangle
    domain = gmsh.model.occ.cut([(2, rect)], [(2, circle)])
    gmsh.model.occ.synchronize()

    # Add a physical group for the domain
    gmsh.model.addPhysicalGroup(2, [d[1] for d in domain[0]], 1)

    # Generate the mesh
    gmsh.model.mesh.generate(2)

    # Extract mesh data
    node_tags, node_coords, _ = gmsh.model.mesh.getNodes()
    element_types, _, element_node_tags = gmsh.model.mesh.getElements()

    # Filter triangular elements
    triangles = []
    for elem_type, elem_nodes in zip(element_types, element_node_tags):
        if gmsh.model.mesh.getElementProperties(elem_type)[0] == "Triangle":
            triangles = np.array(elem_nodes).reshape(-1, 3) - 1  # Convert to 0-based indexing
            break

    # Extract coordinates for plotting
    node_coords = node_coords.reshape(-1, 3)[:, :2]
    x, y = node_coords[:, 0], node_coords[:, 1]

    # Plot the triangular mesh
    plt.figure(figsize=(10, 5))
    for tri in triangles:
        plt.fill(x[tri], y[tri], edgecolor='black', fill=False, linewidth=0.5)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.title("Triangular Mesh of Rectangular Domain with Circular Hole")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()

    # Finalize
