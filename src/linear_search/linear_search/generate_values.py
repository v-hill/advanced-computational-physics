# Python libraries
import numpy as np

def random(num_points, span):
    """
    This function generates a set of random x and y coordinates using the 
    numpy uniform random number generator 'numpy.random.uniform()'.

    Parameters
    ----------
    num_points : int
        The number of points to generate
    span : World class
        The world defines the range of values the coordinates can have

    Returns
    -------
    pts : list
        A list of length num_points, where each element is a point
        e.g. [ [x1, y1], [x2, y2], ... [xn, yn] ]
    """
    x_vals = np.random.uniform(span.x_min, span.x_max, num_points)
    y_vals = np.random.uniform(span.y_min, span.y_max, num_points)
    pts = [list(i) for i in zip(x_vals.tolist(), y_vals.tolist())]
    
    # Alternative version to return numpy array
    # pts = np.concatenate((x_vals, y_vals)).reshape(-1, 2)
    return pts
