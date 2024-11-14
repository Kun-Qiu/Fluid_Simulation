import matplotlib.pyplot as plt
import numpy as np

from FVM.Factory import Model_Geometry as mg

domain = mg.ModelManager()
# domain.add_rectangle(length=20, height=7)
domain.add_rectangle(length=15, height=7)
domain.add_circle(radius=1, x=-7.5, y=0) 
domain.list_all_geometry() 
# domain.difference(idx_1=0, idx_2=1)
# domain.intersection(0, 1)
domain.union(1, 0)
# domain.list_all_geometry() 
domain.generateMesh()
domain.refineMesh(iter=2)
domain.showMesh()
# domain.show()
