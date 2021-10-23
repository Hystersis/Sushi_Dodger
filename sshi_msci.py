# miscellaneous functions for sshi_core/graphics

# Path finding (line drawing edited) based off https://stackoverflow.com/questions/50387606/python-draw-line-between-two-coordinates-in-a-matrix
# Line drawing for coordinates for sshi_core/sshi_graphics

# Events based off https://www.youtube.com/watch?v=oNalXg67XEE&feature=youtu.be & https://www.reddit.com/r/Python/comments/lngfnw/i_never_knew_events_were_this_powerful_a_python

import os
def Apj(name: str) -> str:
    """Shorthand for withdrawing files from Assets folder

    Parameters
    ----------
    name : str
        The name of the file retrieved wanting to be retrieved from the
        Assets folder

    Returns
    -------
    str
        Returns the output of os.path.join('Assets', name)
    """
    return os.path.join('Assets',name)
