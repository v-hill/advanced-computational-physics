"""
This script tests the boids code with the following details:
    
1) The neighbours of each boid are found using the basic linear search 
    algorithm using the Euclidean distance metric.
    
2) Only a single frame, the first iteration of the boids, is displayed.
    
This script is just to test that all the code is working and as such there is 
no command line interface.
"""

# ---------------------------------- Imports ----------------------------------

# Allow imports from parent folder
import sys, os
sys.path.insert(0, os.path.abspath('..'))

# Repo module imports
import plotting
from settings import options
from boids import World, Boids

# -----------------------------------------------------------------------------  

# Setup world
num_boids = 64
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

def basic():
    boids.get_pos_vel()
    boids.make_neighbourhoods_basic()

# ----------------------------------- Main ------------------------------------

for i in range(num_boids):
    a = boids.members[i]
    a.update_boid(boids.positions, boids.velocities, world)

plot.plot_boids(boids, cmap)
plot.display()
# plot.save(filename)
