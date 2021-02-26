"""
Simple test of triangulation code for debugging purposes.
"""
# ---------------------------------- Imports ----------------------------------

# Standard library imports
import timeit
import time

# Repo module imports
from triangulation_core.linear_algebra import lexigraphic_sort
import triangulation_core.points_tools.generate_values as generate_values
from triangulation_core.triangulation import triangulate
from utilities.settings import World
from utilities import plotting

# ------------------------------------ Main -----------------------------------

start = time.time()
world_size = [0, 1000, 0, 1000]
world = World(world_size)
num_points = 1000

positions = generate_values.random(num_points, world)
positions = lexigraphic_sort(positions)

start = time.time()
triangulation = triangulate(positions)
elapsed = time.time() - start
print(f"{num_points} {elapsed*1000:0.3f} ms")

# # Option to plot results
# plt = plotting.basic_plot(world_size, triangulation, positions)
# plt.show()
