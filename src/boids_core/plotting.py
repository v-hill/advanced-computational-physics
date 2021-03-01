"""
This script contains code for producing the boids animations using the cv2 
library
"""

# ---------------------------------- Imports ----------------------------------

# Allow imports from parent folder
import sys, os
sys.path.insert(0, os.path.abspath('..'))

# Standard library imports
import time
from copy import deepcopy
from math import pi
import numpy as np
from matplotlib import cm
import cv2 

# Repo module imports
try:
    from delauney_triangulation.triangulation_core.linear_algebra import normalise
except:
    from triangulation_core.linear_algebra import normalise
from boids_core.settings import options

# ----------------------------- Class definitions -----------------------------

"""
With the test setup of 1000 boids and a 1000x1000 pixel image.
52.56ms per frame original
15.64ms per frame with imporvements

From 19.0FPS to 63.9FPS
"""

class ColourMap():
    def __init__(self, options, matplot_cmap=cm.gist_rainbow):
        self.num_colours = options['num_colours']
        self.base_cmap = matplot_cmap
        self.bins = np.linspace(-pi, pi, self.num_colours+1)[1:].tolist()
        self.make_cmap()

    def make_cmap(self):
        indices = np.linspace(0, 255, self.num_colours).astype(int)
        cmap_lite = []
        for idx in indices:
            colour = (self.base_cmap(idx, bytes=True)[:3])
            colour = (int(colour[2]), int(colour[1]), int(colour[0]))
            cmap_lite.append(colour)
        self.cmap = cmap_lite
        
    def get_colour_basic(self, direction):
        idx = (direction+pi)*(255/(2*pi))
        colour = (self.base_cmap(int(idx), bytes=True)[:3])
        colour = (int(colour[2]), int(colour[1]), int(colour[0]))
        return colour
        
    def get_colour_np(self, direction):
        """
        Improvements
        ------------
        By making a custom colour map the time taken to plot an all the boids
        is reduced by 27.48ms/frame.
        """
        idx = np.digitize(direction, self.bins)
        return self.cmap[idx] 

    def get_colour_fast(self, direction):
        """
        This function returns an RGB colour based on the direction that the
        boid is facing in radians.
        
        Improvements
        ------------
        6.79ms/frame improvement using get_colour_fast instead of using the
        np.digitize function in get_colour_np.

        Parameters
        ----------
        direction : float
            The direction that the boid is facing in radians

        Returns
        -------
        out : numpy.ndarray
            RGB colour to use when plotting the boid
        """
        if direction <= self.bins[0]:
            return self.cmap[0]
        for i, bin_val in enumerate(self.bins[:-1]):
            if bin_val < direction <= self.bins[i+1]:
                return self.cmap[i+1]

class Plotter():
    def __init__(self, options, world):
        # Plot size options
        if options['plot_border']:
            self.shift = options['border_size']
        else:
            self.shift = 0
        self.width = world.x_max + self.shift*2
        self.height = world.y_max + self.shift*2
        
        # Background colour options
        self.background = options['background_colour']
        self.blank_black = np.zeros((self.height, self.width, 3), np.uint8)
        self.blank_white = deepcopy(self.blank_black) + 255
        
        # Boid triangle plotting
        self.dir_len = options['direction_line_len']
        self.triangle_height = options['triangle_height']
        self.triangle_width = options['triangle_width']
        self.plot_cmap = options['plot_boid_colours']
        
        self.img = self.tabula_rasa()   # Set plot to blank
        
    def tabula_rasa(self):
        """
        2.65ms/frame improvement using deepcopy instead of calling np.zeros
        """
        if self.background == 'white':
            return deepcopy(self.blank_white)
        elif self.background == 'black':
            return deepcopy(self.blank_black)
        else:
            raise ValueError("Invlaid background colour")
    
    def plot_neighbours(self, boid, positions):
        boid_pos = (int(boid.pos[0]+self.shift), int(boid.pos[1]+self.shift))
        boid_direction = normalise(boid.vel)
        dir_x = boid_direction[0]*self.dir_len
        dir_y = boid_direction[1]*self.dir_len
        boid_vel = (int(dir_x+boid_pos[0]), int(dir_y+boid_pos[1]))
        self.img = cv2.line(self.img, boid_pos, boid_vel, (255, 255, 255), 2)
        for neighbour in boid.neighbours:
            n_pos = positions[neighbour[1]]
            n_pos = (int(n_pos[0]+self.shift), int(n_pos[1]+self.shift))
            self.img = cv2.line(self.img, boid_pos, n_pos, (255, 255, 255), 1)
    
    def plot_boids(self, boids, colour_map):
        for i in range(boids.num):
            test_boid = boids.members[i]
            triangle = test_boid.make_tri(self.triangle_height, self.triangle_width)
            direction = test_boid.direction()
            if self.plot_cmap:
                col = colour_map.get_colour_fast(direction)
            elif self.background=='black':
                col = (0, 0, 0)
            elif self.background=='white':
                col = (255, 255, 255)
            
            if self.shift != 0:
                triangle += self.shift    # Shift the triangles to create border
            self.img = cv2.drawContours(self.img, [triangle], 0, col, -1)
            
    def display(self):
        cv2.imshow("image", self.img) 
        cv2.waitKey(0)
        cv2.destroyWindow("image")

    def save(self, filename=options['save_filename']):
        if "." not in filename:
            raise Exception("Must include file extension with filename")
        cv2.imwrite(filename, self.img) 
    
    def animation(self, boids, plot_func, cmap, verbose=False, print_fps=24):
        start = time.time()
        iterations = 0
        cv2.imshow("image", self.img)
        if verbose: print("frame number, frames per second")
        while True:
            self.img = self.tabula_rasa()
            boids = plot_func(boids)
            self.plot_boids(boids, cmap)
            cv2.imshow("image", self.img)
            k = cv2.waitKey(1)
            if k == 27:
                break
            if verbose and iterations%print_fps==0:
                print(f"{iterations},{iterations/(time.time()-start):0.3f}")
            iterations += 1
        cv2.destroyWindow("image")
