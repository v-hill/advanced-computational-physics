# Python libraries
import time

# Code from local files
from boids import Boids

# ----------------------------------- setup -----------------------------------

num_points = 100
max_neighbour_dist = 100
world_size = [0, 1000, 0, 1000]
boids = Boids(num_points, world_size, max_neighbour_dist)
boids.generate_members()

openmp_threads = 1

# ------------------------------------ main -----------------------------------

print('Comparing cython implementations of the linear search nearest '
      'neighbour algorithm')
print(f'Finding the neighbours of {num_points} generated points...')
        
print('Execution time for make_neighbourhoods function, pure python linear '
      'search algorithm:')
START = time.time()
boids.make_neighbourhoods()
elapsed = time.time() - START
print(f'\t {elapsed*1000:0.2f} ms')

print('Execution time for make_neighbourhoods_cython function, cythonised '
      'linear search algorithm:')
START = time.time()
boids.make_neighbourhoods_cython()
elapsed = time.time() - START
print(f'\t {elapsed*1000:0.2f} ms')

print('Execution time for make_neighbourhoods_cython2 function, cythonised '
      f'and openmp linear search algorithm running on {openmp_threads} threads:')
START = time.time()
boids.make_neighbourhoods_cython2(openmp_threads)
elapsed = time.time() - START
print(f'\t {elapsed*1000:0.2f} ms')
