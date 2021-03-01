"""
This script tests the boids code with the following details:
    
1) The neighbours of each boid are found using delauney triangulation code.
    
2) Only a single frame, the first iteration of the boids, is displayed.
    
This script tests that the boids code, delauney triangulation and plotting 
modules are all working properly.
"""

# ---------------------------------- Imports ----------------------------------

# Allow imports from parent folder
import sys, os
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('../..'))

# Repo module imports
import plotting
from settings import options
from boids import World, Boids

# -----------------------------------------------------------------------------  

# Setup world
num_boids = 1000
WORLD_SIZE = [0, options['world_width'], 0, options['world_height']]
world = World(WORLD_SIZE)
filename = f"{num_boids}_plot.png"

# Setup plot
NUM_COLOURS = options['num_colours']
cmap = plotting.ColourMap(options)
plot = plotting.Plotter(options, world)

# Setup Boids
boids = Boids(num_boids, world, options)
boids.generate_boids(options, distribution='random')

# -----------------------------------------------------------------------------  

def triang_ver():
    boids.triangulate_boids()
    boids.make_neighbourhoods()

# ----------------------------------- Main ------------------------------------

triang_ver()

for i in range(num_boids):
    a = boids.members[i]
    a.update_boid(boids.positions, boids.velocities, world)

plot.plot_boids(boids, cmap)
plot.display()
# plot.save(filename)
