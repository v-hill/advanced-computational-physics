"""
This scripts contains functions for creating the inital positions and 
velocities of the boids.
"""

# ---------------------------------- Imports ----------------------------------

# Standard library imports
import numpy as np
from numpy.random import default_rng
from math import pi, sqrt, ceil

# ----------------------------- Points generators -----------------------------

"""
The following functions are used to generate the inital values for the 
position of each point.
"""

def random(num_points, span):
    """
    This function generates a set of random x and y coordinates using the 
    numpy uniform random number generator 'numpy.random.default_rng().uniform'.

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
    x_vals = default_rng().uniform(span.x_min, span.x_max, num_points)
    y_vals = default_rng().uniform(span.y_min, span.y_max, num_points)
    pts = [list(i) for i in zip(x_vals.tolist(), y_vals.tolist())]
    
    # Alternative version to return numpy array
    # pts = np.concatenate((x_vals, y_vals)).reshape(-1, 2)
    return pts

def lattice(num_points, span):
    """
    This function generates a set of points which are set on a grid. The points
    are spaced equally in x and y using the numpy.linspace function. To have
    a point at every place on the grid requires that the number of points is a
    square number. If the number of points is not a square number, points are
    removed randomly until there are 'num_points' many points returned.

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
    num_sqrt = ceil(sqrt(num_points))
    x_vals = np.linspace(span.x_min, span.x_max, num_sqrt)
    y_vals = np.linspace(span.y_min, span.y_max, num_sqrt)
    _X, _Y = np.meshgrid(x_vals, y_vals)
    pts = [list(i) for i in zip(_X.ravel().tolist(), _Y.ravel().tolist())]
    
    # If the number of points is not square, remove excess points randomly
    if not sqrt(num_points).is_integer():
        current_num = len(pts)
        to_remove = current_num - num_points
        indices = np.random.choice(current_num, to_remove, replace=False)
        pts = [i for j, i in enumerate(pts) if j not in indices]
    return pts

def noisy_lattice(num_points, span, noise_level=5):
    pts = np.asarray(lattice(num_points, span))
    x_noise = np.random.normal(0, noise_level, num_points)
    y_noise = np.random.normal(0, noise_level, num_points)
    
    pts[:, 0] += x_noise
    pts[:, 1] += y_noise

    return pts.tolist()

# ------------------------- Coordinate transformations ------------------------

def polar_to_cart(radius, angle):
    """
    Converts 2D polar coordinates to cartestian. 

    Parameters
    ----------
    radius : list
        list of radii
    angle : list
        list of angles

    Returns
    -------
    vels : lists of lists
        [ [x1, y1], [x2, y2], ... [xn, yn] ]
    """
    x_vals = radius * np.cos(angle)
    y_vals = radius * np.sin(angle)
    vels = [list(i) for i in zip(x_vals.tolist(), y_vals.tolist())]
    return vels

# --------------------------- Velocities generators ---------------------------

def random_velocities(num_vals, max_speed):
    """
    Returns an list of random velocities for 'num_vals' many particles.
    Firstly a distribution of scalar speeds is generated, along with an
    equal number of random angles. The x-y velocity compoents are then 
    calculated from a polar-to-cartesian coordiante transformation.

    Parameters
    ----------
    num_vals : int
        The number of particles to generate velocities for.
    max_speed : int, float
        The maximum scalar speed allowed.
        
    Returns
    -------
    velocities : lists of lists
        [ [x1, y1], [x2, y2], ... [xn, yn] ]
    """
    speeds = default_rng().uniform(-max_speed, max_speed, num_vals)
    angles = default_rng().uniform(0, 2*pi, num_vals)
    velocities = polar_to_cart(speeds, angles)
    return velocities

def test_uni(points):
    for i, row in enumerate(points):
        for j, test in enumerate(points):
            if row[0]==test[0] and row[1]==test[1] and i!=j:
                print(row, test)
