"""
This script tests the boids code with the following details:
    
1) The neighbours of each boid are found using the basic linear search 
    algorithm using the Euclidean distance metric.
    
2) The full animation is shown, with the frames per second being displayed in
    the command line by deafult (using the 'print_fps_to_console' variable).
    
This script tests the boids code with a simple linear search algorithm to 
determine nearest neighbours.
Below 150 boids this linear search performs better than the triangulation 
neighbour finding approach. However, performance quickly drops below the
triangulation approach for higher numbers of boids.
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
num_boids = 150
max_boid_dist = 100
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
boids.get_pos_vel()

# -----------------------------------------------------------------------------  

def plot_func(boids):
    boids.make_neighbourhoods_basic(max_dist=max_boid_dist)
    for i in range(num_boids):
        a = boids.members[i]
        a.update_boid(boids.positions, boids.velocities, world)
        if a.index%50==0:
            plot.plot_neighbours(a, boids.positions)
    return boids

# ----------------------------------- Main ------------------------------------

plot.animation(boids, plot_func, cmap, 
               verbose=print_fps_to_console, print_fps=48)
