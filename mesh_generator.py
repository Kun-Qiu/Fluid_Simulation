import gmsh
import math

# Initialize gmsh
gmsh.initialize()
gmsh.model.add("2D_ConvergingDivergingTube")

# Define geometry parameters for the 2D tube profile
length_converging = 5
length_throat = 2
length_diverging = 5
radius_inlet = 2
radius_throat = 1
radius_outlet = 1.5

# Set a smaller characteristic length for finer mesh
fine_mesh_size = 0.5  # Smaller value increases mesh density

# Define points for the 2D tube profile with fine mesh size
inlet_top = gmsh.model.geo.addPoint(0, radius_inlet, 0, fine_mesh_size)
inlet_bottom = gmsh.model.geo.addPoint(0, -radius_inlet, 0, fine_mesh_size)
converging_end_top = gmsh.model.geo.addPoint(length_converging, radius_throat, 0, fine_mesh_size)
converging_end_bottom = gmsh.model.geo.addPoint(length_converging, -radius_throat, 0, fine_mesh_size)
throat_end_top = gmsh.model.geo.addPoint(length_converging + length_throat, radius_throat, 0, fine_mesh_size)
throat_end_bottom = gmsh.model.geo.addPoint(length_converging + length_throat, -radius_throat, 0, fine_mesh_size)
diverging_end_top = gmsh.model.geo.addPoint(length_converging + length_throat + length_diverging, radius_outlet, 0, fine_mesh_size)
diverging_end_bottom = gmsh.model.geo.addPoint(length_converging + length_throat + length_diverging, -radius_outlet, 0, fine_mesh_size)

# Create lines for the tube shape, ensuring order forms a closed loop
top_inlet_to_converging = gmsh.model.geo.addLine(inlet_top, converging_end_top)
top_converging_to_throat = gmsh.model.geo.addLine(converging_end_top, throat_end_top)
top_throat_to_diverging = gmsh.model.geo.addLine(throat_end_top, diverging_end_top)
right_end = gmsh.model.geo.addLine(diverging_end_top, diverging_end_bottom)
bottom_throat_to_diverging = gmsh.model.geo.addLine(diverging_end_bottom, throat_end_bottom)
bottom_converging_to_throat = gmsh.model.geo.addLine(throat_end_bottom, converging_end_bottom)
bottom_inlet_to_converging = gmsh.model.geo.addLine(converging_end_bottom, inlet_bottom)
left_end = gmsh.model.geo.addLine(inlet_bottom, inlet_top)

# Create a line loop and surface for the tube cross-section
line_loop = gmsh.model.geo.addCurveLoop([
    top_inlet_to_converging,
    top_converging_to_throat,
    top_throat_to_diverging,
    right_end,
    bottom_throat_to_diverging,
    bottom_converging_to_throat,
    bottom_inlet_to_converging,
    left_end
])
surface = gmsh.model.geo.addPlaneSurface([line_loop])

# Synchronize the model to process the geometry
gmsh.model.geo.synchronize()

# Generate the 2D mesh
gmsh.model.mesh.generate(2)

# Display the mesh in the Gmsh GUI
gmsh.fltk.run()

# Finalize gmsh
gmsh.finalize()
