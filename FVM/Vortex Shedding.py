import sys

import matplotlib.pyplot as plt
import numpy as np

from Factory import Model_Geometry as mg

domain = mg.ModelManager()
domain.add_rectangle(length=10, width=5)
domain.add_circle(radius=1, x=-2, y=0)
domain.difference(idx_1=0, idx_2=1)
domain.list_all_geometry()
boundary_shape = domain.getBounds()
# domain.show()
print(domain.get_geometry(index=0))
