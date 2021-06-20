import numpy as np

for i in np.arange(0, 100, 0.00001):
    addvalue = i
    currentvalue = i
    list_of_values = [i]
    for a in range(2,15):
        currentvalue *= 0.5
        addvalue += currentvalue
        list_of_values.append(currentvalue)
        if addvalue > 100:
            break
        if addvalue == 100 and a == 14:
            print(i)
            print(list_of_values)
            break