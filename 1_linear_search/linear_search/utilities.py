"""
This script contains basic utility functions.
"""

def base_round(x, base):
    """
    This function takes in a value 'x' and rounds it to the nearest multiple
    of the value 'base'. 

    Parameters
    ----------
    x : int
        Value to be rounded
    base : int
        Tase for x to be rounded to

    Returns
    -------
    int
        The rounded value
    """
    return base*round(x/base)
        
def make_num_pts_list(steps, base=10, repeats=1):
    """
    This function produces a list of 'num_points' values used to test 
    algorithms with.

    Parameters
    ----------
    steps : list/numpy.ndarray
        List of powers.
    base : int, optional
        Round num_points values to nearest multiple of this 'base' value. 
        The default is 10.
    repeats : int, optional
        Number of repeats of each 'num_points' value. The default is 1.

    Returns
    -------
    num_pts_list : list
        List of 'num_points' values to test.
    """
    num_pts_list = []
    
    for step in steps:
        for i in range(repeats):
            num_points = int(10**step)
            num_pts_list.append(base_round(num_points, base))
    return num_pts_list
