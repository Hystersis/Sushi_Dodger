# miscellaneous functions for sshi_core/graphics

# Path finding (line drawing edited) based off https://stackoverflow.com/questions/50387606/python-draw-line-between-two-coordinates-in-a-matrix
# Line drawing for coordinates for sshi_core/sshi_graphics


import os

def pthfnd(mat, x0, y0, x1, y1, inplace=False):
    crd = []
    crd.append([x0,y0]) # Add the starting coordinate
    if not (0 <= x0 < mat.shape[0] and 0 <= x1 < mat.shape[0] and
            0 <= y0 < mat.shape[1] and 0 <= y1 < mat.shape[1]):
        raise ValueError('Invalid coordinates.')
    if not inplace:
        mat = mat.copy()
    if (x0, y0) == (x1, y1):
        return crd if not inplace else None
    # Swap axes if Y slope is smaller than X slope
    transpose = abs(x1 - x0) < abs(y1 - y0)
    if transpose:
        mat = mat.T
        x0, y0, x1, y1 = y0, x0, y1, x1
    # Swap line direction to go left-to-right if necessary
    if x0 > x1:
        x0, y0, x1, y1 = x1, y1, x0, y0
    # Compute intermediate coordinates using line equation
    x = np.arange(x0 + 1, x1)
    y = np.round(((y1 - y0) / (x1 - x0)) * (x - x0) + y0).astype(x.dtype)
    # Returns the coordinates in order
    for a,b in zip(x,y):
        crd.append([a,b])
    if not inplace:
        crd.append([x1,y1])
        return crd if not transpose else mat.T

# Events based off https://www.youtube.com/watch?v=oNalXg67XEE&feature=youtu.be & https://www.reddit.com/r/Python/comments/lngfnw/i_never_knew_events_were_this_powerful_a_python

from collections import defaultdict

subscribers = defaultdict(list)

def subscribe(event_type: str, fn):
    subscribers[event_type].append(fn)

def post_event(event_type: str, data):
    for fn in subscribers[event_type]:
        fn(data)


def Apj(name: str) -> str:
    '''This is basically os.path.join put
    just does it for the Assets folder'''
    return os.path.join('Assets',name)
