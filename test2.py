import numpy as np

for x in np.arange(0,5,0.00001):
    z = x.copy()
    for y in range(1, 50):
        z *= 2
        if z == 5:
            print(x)
        elif z > 5:
            break