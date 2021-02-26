"""
This script tests the boids code with the following details:
    
1) The neighbours of each boid are found using the basic linear search 
    algorithm using the Euclidean distance metric.
    
2) The full animation is shown, with the frames per second being displayed in
    the command line by deafult (using the 'print_fps_to_console' variable).
    
This script tests that the boids code, delauney triangulation and plotting 
modules produce the correct/expected result. This script has also used to tune
the boids parameters and plot settings as found in 'settings.py'.
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
num_boids = 150
WORLD_SIZE = [0, options['world_width'], 0, options['world_height']]
world = World(WORLD_SIZE)

# Other options
filename = f"{num_boids}_plot.png"
print_fps_to_console = True

# Setup plot
NUM_COLOURS = options['num_colours']
cmap = plotting.ColourMap(options)
plot = plotting.Plotter(options, world)

# Setup Boids
boids = Boids(num_boids, world, options)
boids.generate_boids(options, distribution='random')

# -----------------------------------------------------------------------------  

def plot_func(boids):
    boids.triangulate_boids()
    boids.make_neighbourhoods()
    for i in range(num_boids):
        a = boids.members[i]
        a.update_boid(boids.positions, boids.velocities, world)
        if a.index%50==0:
            plot.plot_neighbours(a, boids.positions)
    return boids

# ----------------------------------- Main ------------------------------------

plot.animation(boids, plot_func, cmap, 
               verbose=print_fps_to_console, print_fps=48)
