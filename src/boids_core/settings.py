"""
Stores default definitions for the Boids programme.
"""

# Standard library imports
from math import pi

# -----------------------------------------------------------------------------  

world_options = {'world_width' : 1000,
                 'world_height' : 1000}

plotting_options = {'triangle_width' : 8,
                    'triangle_height' : 12,
                    'direction_line_len' : 50,
                    'num_colours' : 4,
                    'plot_boid_colours' : True,
                    'plot_border' : True,
                    'border_size' : 50,
                    'background_colour' : 'black',
                    'save_output' : False,
                    'save_filename' : 'boids.png'}

boids_options = {'max_speed' : 2,
                 'field_of_view' : round((2*pi)*0.66, 3),
                 'vision_distance' : 200,
                 'safety_zone' : 20,
                 'alignment_perception' : 0.08,
                 'cohesion_perception' : 0.008,
                 'seperation_perception' : 0.25}

options = {**world_options, **plotting_options, **boids_options}