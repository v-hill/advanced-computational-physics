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

# Code from local files
from linear_search.boids import World, Boids

# --------------------------------- func defs ---------------------------------

def setup_boids(world, num_points, max_dist):
    boids = Boids(num_points, world, max_dist)
    boids.generate_boids()
    return boids

def function_timer(method, time_format='ms'):
    START = time.time()
    method()
    elapsed = time.time() - START
    if time_format=='ms':
        print(f"\t {elapsed*1000/1.0970:0.1f} ms")
    if time_format=='s':
        print(f"\t {elapsed/1.0970:0.1f} s")

# ----------------------------------- setup -----------------------------------

num_points = 1000
max_neighbour_dist = 100
world_size = [0, 1000, 0, 1000]
world = World(world_size)

# ------------------------------------ main -----------------------------------

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description = 'Nearest neighbour '
                                     'search algorithm comparison')
    parser.add_argument('-n', '--num_points', 
                        help='the number of points', 
                        type=int,
                        default = num_points)
    
    parser.add_argument('-mnd', '--max_neighbour_dist', 
                        help='the maximum neighbour distance', 
                        type=int,
                        default = max_neighbour_dist)
    
    args = parser.parse_args()
    
    print("Comparing optimisations of the linear search nearest neighbour algorithm")
    print(f"Finding the neighbours of {num_points} points...")
    
    # Find all neighbours using euclidean distance metric
    boids = setup_boids(world, args.num_points, max_neighbour_dist)
    print("Euclidean distance:")
    function_timer(boids.make_neighbourhoods_1)
    
    # Find all neighbours using euclidean square distance metric
    boids = setup_boids(world, args.num_points, max_neighbour_dist)
    print("Euclidean squared:")
    function_timer(boids.make_neighbourhoods_2)
    
    # Find all neighbours using Manhattan distance metric
    boids = setup_boids(world, args.num_points, max_neighbour_dist)
    print("Manhattan distance:")
    function_timer(boids.make_neighbourhoods_3)
    
