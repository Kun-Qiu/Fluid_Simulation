from FVM.Factory import Model_Geometry as mg
import numpy as np

domain = mg.ModelManager()
domain.add_rectangle(length=20, height=7)
domain.add_circle(radius=1, x=-7.5, y=0) 
domain.difference(idx_1=0, idx_2=1)
domain.generateMesh()
# domain.refineMesh(iter=1)
domain.showMesh()

# Pt Tag    flattened (x1,y1,z1, x2,y2,z2 ...)
# node_tags, node_coords, _ = domain.getNodes()
# nodes = node_coords.reshape(-1, 3)[:, :2]

# # Shape Type    Id for shape   Node tag belong
# # 2 = Tri                       to each shape
# # 3 = Quadril
# elem_types, elem_tags, elem_node_tags = domain.getElements()
# for elem_type, elem_node_tag in zip(elem_types, elem_node_tags):
#     if elem_type == 2:  # 3-node triangles
#         num_nodes_per_elem = 3
#     elif elem_type == 3:  # 4-node quadrilaterals
#         num_nodes_per_elem = 4
#     else:
#         continue  # Skip unsupported element types
    
#     print(len(elem_node_tag))
#     elements = np.array(elem_node_tag).reshape(-1, num_nodes_per_elem) - 1
#     # print(elements)
