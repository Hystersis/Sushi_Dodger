import numpy as np
import matplotlib.pyplot as plt

grid = np.zeros((255,255), dtype=np.bool)
square_length = 0.5
circles = {'c1':[[100,100],8.5]}

# Generate arrays of indices/coordiates so we can do the
# calculations the Numpy way, without resorting to loops
# I always get the index order wrong so double check...
xx = np.arange(grid.shape[0])
yy = np.arange(grid.shape[1])


for val in circles.values():
    radius = val[1]
    # same index caveat here
    # Calling Mr Pythagoras: Find the pixels that lie inside this circle
    inside = (xx[:,None] - val[0][0]) ** 2 + (yy[None, :] - val[0][1])  ** 2 <= (radius ** 2)
    # do grid & inside and initialize grid with ones for intersection instead of union
    print(inside)
    grid = grid | inside

plt.imshow(grid)
plt.show()
