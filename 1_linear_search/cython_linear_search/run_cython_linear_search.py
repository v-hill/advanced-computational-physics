# Python libraries
import time

# Code from local files
import cython_linear_search
import generate_values

num_points = 1000
max_neighbour_dist = 100
world_size = [0, 1000, 0, 1000]
positions = generate_values.random(num_points, world_size)

boids = cython_linear_search.setup(num_points, max_neighbour_dist, positions)

START = time.time()

cython_linear_search.main(boids)

elapsed = time.time() - START
print(f'\t {elapsed*1000:0.1f} ms')
