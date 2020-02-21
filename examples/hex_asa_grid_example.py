from hcipy import *
import matplotlib.pyplot as plt
import numpy as np

grid = make_hexagonal_asa_grid([100,100],1.0,center=0,center_array=0)

print(np.shape(grid))