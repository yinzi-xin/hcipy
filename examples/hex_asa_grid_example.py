from hcipy import *
import matplotlib.pyplot as plt
import numpy as np

grid = make_hexagonal_asa_grid([int(100/np.sqrt(3)),100],1.0,center=0,center_array=0)

#to convert to cartesian grid (this is exact, but unstructured)
cart_grid = grid.as_('cartesian')

plt.plot(cart_grid.x, cart_grid.y, '+')
plt.axis('equal')
plt.show()

#make a field, left half is 0, right half is 1
values = np.zeros(np.shape(grid.a))
values[grid.c>0] = 1.0

field = Field(values, grid)

print(np.shape(field.shaped))