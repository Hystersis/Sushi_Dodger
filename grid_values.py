grid_values = {}
def get_grid_values():
    for x in range(256):
        for y in range(256):
            grid_values[(x,y)] = 0
    return grid_values
