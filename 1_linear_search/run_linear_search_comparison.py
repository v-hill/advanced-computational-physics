"""
This script runs a comparison between three different ways of computing 
nearest-neighbours:
    1) Euclidean distance
    2) Euclidean distance squared
    3) Manhattan distance
    
Points are generated in 2D. 
Each program computes the neighbours of every point within a given max 
distance denoted 'max_neighbour_dist'.
By default there are 'num_points' points with coordiantes values inside the
square defined by 'world_size'.
"""

# Python libraries
import argparse
import time
import numpy as np

# Code from local files
from linear_search.boids import World, Boids
import linear_search.utilities as utilities

# --------------------------------- func defs ---------------------------------

def setup_boids(world, num_points, max_dist):
    boids = Boids(num_points, world, max_dist)
    boids.generate_boids()
    return boids

def function_timer(method, num_points, scan=False):
    START = time.time()
    method()
    elapsed = time.time() - START
    if scan:
        print(f'{num_points},{elapsed*1000:0.2f}')
    else:
        print(f'\t {elapsed*1000:0.1f} ms')

# ----------------------------------- setup -----------------------------------

num_points = 1000
max_neighbour_dist = 100
world_size = [0, 1000, 0, 1000]
world = World(world_size)

# --------------------------------- func defs ---------------------------------

def main(world, num_points, max_neighbour_dist):
    """
    This functions runs the linear search nearest neighbour algorithm to the 
    find the neighbours of 'num_points' many generated points. A comparison of
    three different distance metrics for the to compute the distance between
    neighbours is used.

    Parameters
    ----------
    world : linear_search.boids.World
        Defines the range of x and y coordinates the points can take
    num_points : int
        The number of points to generate and find neighbours of
    max_neighbour_dist : int
        The maximum distance a point can be away from a given test poin in
        order to still be considered a neighbour of said test point
    """
    # Find all neighbours using euclidean distance metric
    boids = setup_boids(world, num_points, max_neighbour_dist)
    print('Euclidean distance:')
    function_timer(boids.make_neighbourhoods_1, num_points)
    
    # Find all neighbours using euclidean square distance metric
    boids = setup_boids(world, num_points, max_neighbour_dist)
    print('Euclidean squared:')
    function_timer(boids.make_neighbourhoods_2, num_points)
    
    # Find all neighbours using Manhattan distance metric
    boids = setup_boids(world, num_points, max_neighbour_dist)
    print('Manhattan distance:')
    function_timer(boids.make_neighbourhoods_3, num_points)
    
def main_scan(world, max_neighbour_dist):
    """
    This function performs the same as the above main() function, but for a 
    range of values for 'num_points'. Seven values are used which range
    between 100 and 10000 distrubued logarithmicly.

    Parameters
    ----------
    world : linear_search.boids.World
        Defines the range of x and y coordinates the points can take
    max_neighbour_dist : int
        The maximum distance a point can be away from a given test poin in
        order to still be considered a neighbour of said test point
    """
    
    print('Euclidean distance:')
    for num_pts in num_pts_list:
        boids = setup_boids(world, num_pts, max_neighbour_dist)
        function_timer(boids.make_neighbourhoods_1, num_pts, scan=True)
        
    print('Euclidean squared:')
    for num_pts in num_pts_list:
        boids = setup_boids(world, num_pts, max_neighbour_dist)
        function_timer(boids.make_neighbourhoods_2, num_pts, scan=True)
        
    print('Manhattan distance:')
    for num_pts in num_pts_list:
        boids = setup_boids(world, num_pts, max_neighbour_dist)
        function_timer(boids.make_neighbourhoods_3, num_pts, scan=True)

# ------------------------------------ main -----------------------------------

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Nearest neighbour '
                                     'search algorithm comparison')
    parser.add_argument('-n', '--num_points', 
                        help='The number of points', 
                        type=int,
                        default = num_points)
    
    parser.add_argument('-mnd', '--max_neighbour_dist', 
                        help='The maximum neighbour distance', 
                        type=int,
                        default = max_neighbour_dist)
    
    parser.add_argument('--num_points_scan', 
                        default=False, action='store_true',
                        help=('Run the script multiple times using a range '
                              'of values for the number of points. Values '
                              'range from 100 to 10000 with a logarithmic '
                              'distribution'))
    
    parser.add_argument('-r', '--repeats', 
                        help='The number of times to repeat each num_points '
                        'value', 
                        type=int,
                        default = 1)

    args = parser.parse_args()
    
    # Execute for a single value of num_points
    if not args.num_points_scan:
        print('Comparing optimisations of the linear search nearest '
              'neighbour algorithm')
        print(f'Finding the neighbours of {num_points} generated points...')
        main(world, args.num_points, args.max_neighbour_dist)
        
    # Execute multiple times for a range of num_points values
    else:
        steps = np.arange(2, 4.1, 1/3)
        num_pts_list = utilities.make_num_pts_list(steps, base=10, 
                                                   repeats=args.repeats)
        main_scan(world, args.max_neighbour_dist)
        
