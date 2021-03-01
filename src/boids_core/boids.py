"""
This script contains the code implementing my version of the Boids artificial 
life programme.
"""
# ---------------------------------- Imports ----------------------------------

# Allow imports from parent folder
import sys, os
sys.path.insert(0, os.path.abspath('..'))

# Standard library imports
import timeit
import time
import numpy as np
from math import atan2, sqrt

# Repo module imports
import boids_core.generate_values as generate_values

# Code from delauney triangulation module
from delauney_triangulation.triangulation_core.triangulation import triangulate
from delauney_triangulation.triangulation_core.linear_algebra import (vector_add, 
                                                                      vector_sub, 
                                                                      list_divide, 
                                                                      perpendicular, 
                                                                      normalise)

# ----------------------------- Class definitions -----------------------------

class World():
    """
    A 2D world for the Boids to live in.
    """
    def __init__(self, world_size):
        self.x_min = world_size[0]
        self.x_max = world_size[1]
        self.y_min = world_size[2]
        self.y_max = world_size[3]

class Object():
    def __init__(self, idx, position, stationary=False):
        self.index = idx
        self.stationary = stationary
        self.pos = position
           
class Obstacle(Object):
    def __init__(self, idx, position):
        super().__init__(idx, position, stationary=True)

class Boid(Object):
    """
    Class to represent a single Boid.
    """
    def __init__(self, idx, position, velocity, options):
        super().__init__(idx, position)
        self.vel = velocity
        self.neighbours = []
        self.max_speed = options['max_speed']
        self.field_of_view = options['field_of_view']
        self.vision_distance = options['vision_distance']
        self.safety_zone = options['safety_zone']
        self.alignment_perception = options['alignment_perception']
        self.cohesion_perception = options['cohesion_perception']
        self.separation_perception = options['seperation_perception']
        
    def __repr__(self):
        return f"{self.index}, {self.pos}, {self.vel}"

    def magnitude(self):
        return sqrt(self.vel[0]**2 + self.vel[1]**2)
    
    def direction(self):
        return atan2(self.vel[1], self.vel[0])
        
    def make_tri(self, height, width):
        """
        Generate the co-ordinates of the three points of a triangle used to 
        plot the boid.

        Parameters
        ----------
        height : int
            The height of the boid in pixels.
        width : int
            The width of the boid in pixels.

        Returns
        -------
        numpy.array
            Numpy array with the triangle coordiantes.
        """
        offset_h = list_divide(self.vel, self.magnitude()/height)
        offset_w = list_divide(self.vel, self.magnitude()/width)
        offset_w = perpendicular(offset_w)
        
        p1 = vector_add(self.pos, list_divide(offset_h, 2))
        p2 = p3 = vector_sub(self.pos, list_divide(offset_h, 2))
        p2 = vector_add(p2, list_divide(offset_w, 2))
        p3 = vector_sub(p3, list_divide(offset_w, 2))
        
        return (np.asarray([p1, p2, p3]).astype(int))
    
    def restrict_fov(self, positions):
        """
        Function to limit the field of view of the boid. Neighbours beyond the
        self.field_of_view/2 angle are removed from the set of neighbours. 

        Parameters
        ----------
        positions : list
            List of all coordinates of the boids.
        """
        new_neighbours = []
        boid_dir = atan2(self.vel[0], self.vel[1])
        for neighbour in self.neighbours:
            n_pos = positions[neighbour[1]]
            # Find the angle between boid direction and neighbour
            angle = atan2(n_pos[0]-self.pos[0], n_pos[1]-self.pos[1])
            # print(f"{boid_dir},{boid_dir - self.field_of_view/2},{angle},{boid_dir + self.field_of_view/2}")
            if ((boid_dir - self.field_of_view/2) < angle and
                 angle < (boid_dir + self.field_of_view/2)):
                diff_x = n_pos[0] - self.pos[0]
                diff_y = n_pos[1] - self.pos[1]
                distance = sqrt(diff_x**2 + diff_y**2)
                if distance < self.vision_distance:   
                    new_neighbours.append(neighbour) 
        self.neighbours = new_neighbours
        
    def separation(self, positions):
        """
        Function to implemen the boids seperation rule.
        """
        resultant_x = 0
        resultant_y = 0
        counter = 0
        for neighbour in self.neighbours:
            n_pos = positions[neighbour[1]]
            diff_x = n_pos[0] - self.pos[0]
            diff_y = n_pos[1] - self.pos[1]
            distance = sqrt(diff_x**2 + diff_y**2)
            if distance < self.safety_zone:
                counter += 1
                resultant_x -= diff_x / distance   
                resultant_y -= diff_y / distance

        if counter != 0:
            resultant_x /= counter
            resultant_y /= counter

        vs_x = self.separation_perception * resultant_x   
        vs_y = self.separation_perception * resultant_y
        # print(f"separation,{vs_x:0.4f},{vs_y:0.4f}")
        return [vs_x, vs_y]
        
    def cohesion(self, positions):
        """
        Function to implemen the boids cohesion rule.
        """
        num_neighbours = len(self.neighbours)
        resultant_x = 0
        resultant_y = 0
        
        for neighbour in self.neighbours:
            n_pos = positions[neighbour[1]]
            resultant_x += n_pos[0]   
            resultant_y += n_pos[1]
            
        resultant_x /= num_neighbours
        resultant_y /= num_neighbours

        vc_x = self.cohesion_perception * (resultant_x - self.pos[0])
        vc_y = self.cohesion_perception * (resultant_y - self.pos[1])
        # print(f"cohesion,{vc_x:0.4f},{vc_y:0.4f}")
        return [vc_x, vc_y]

    def alignment(self, velocities):
        """
        Function to implemen the boids alignment rule.
        """
        num_neighbours = len(self.neighbours)
        resultant_vx = 0
        resultant_vy = 0

        for neighbour in self.neighbours:
            n_velo = velocities[neighbour[1]]
            resultant_vx += n_velo[0]   
            resultant_vy += n_velo[1]

        resultant_vx /= num_neighbours   
        resultant_vy /= num_neighbours
        
        va_x = self.alignment_perception * resultant_vx
        va_y = self.alignment_perception * resultant_vy
        # print(f"alignment,{va_x:0.4f},{va_y:0.4f}")
        return [va_x, va_y]

    def wrap_world(self, world):
        """
        Apply period boundary conditions, so if the boid goes off the edge
        of the world it reappears on the opposite edge. 
        """
        if self.pos[0] < 0:                       
            self.pos[0] = world.x_max + self.pos[0]
        if self.pos[0] > world.x_max:
            self.pos[0] = self.pos[0] - world.x_max
        if self.pos[1] < 0:
            self.pos[1] = world.y_max + self.pos[1]
        if self.pos[1] > world.y_max:
            self.pos[1] = self.pos[1] - world.y_max

    def update_boid(self, positions, velocities, world):
        """
        Function to apply all the boid rules to update the position and 
        velocity of a boid for a single time-step.
        """
        self.restrict_fov(positions)
        # print(f"current pos:  {self.pos[0]:0.4f}, {self.pos[1]:0.4f}")
        # print(f"current vel:  {self.vel[0]:0.4f}, {self.vel[1]:0.4f}")
        if len(self.neighbours) >= 1:
            ali = self.alignment(velocities)
            coh = self.cohesion(positions)
            sep = self.separation(positions)
            
            self.vel[0] += (coh[0] + ali[0] + sep[0]) 
            self.vel[1] += (coh[1] + ali[1] + sep[1])
            # curl = perpendicular(self.vel)
            # self.vel = vector_add(self.vel, list_divide(curl, 20))
            
            if sqrt(self.vel[0]**2 + self.vel[1]**2) > self.max_speed:
                new_v = normalise(self.vel, self.max_speed)
                self.vel = new_v

        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.wrap_world(world)
        # print(f"new pos:      {self.pos[0]:0.4f}, {self.pos[1]:0.4f}")
        # print(f"new vel:      {self.vel[0]:0.4f}, {self.vel[1]:0.4f}")
        # print("-"*32)

class Boids():
    """
    A Class to store the full set of Boid Class objects, along with associated
    functions on all boids.
    """
    def __init__(self, number, world, options):
        self.num = number
        self.world = world
        self.members = []
        self.positions = []
        self.velocities = []
        self.triangulation = None
        self.max_speed = options['max_speed']
        
    def add_boid(self, new_boid):
        self.members.append(new_boid)
        
    def generate_boids(self, options, distribution='random'):
        """
        Setup the inital positions and velocities of the boids.

        Parameters
        ----------
        options : dict
            Dictionary of setup options.
        distribution : TYPE, optional
            Choose how the boids are initially distributed. 
            The default is 'random'. 'lattice' and 'lattice_with_noise' are 
            alternative options.
        """
        if distribution == 'random':
            positions = generate_values.random(self.num, self.world)
        if distribution == 'lattice':
            positions = generate_values.lattice(self.num, self.world)
        if distribution == 'lattice_with_noise':
            positions = generate_values.noisy_lattice(self.num, self.world)      

        velocities = generate_values.random_velocities(self.num, self.max_speed)

        for i in range(self.num):
            new_boid = Boid(i, positions[i], velocities[i], options)
            self.add_boid(new_boid)
            
    def get_pos_vel(self):
        positions = []
        velocities = []
        for boid in self.members:
            positions.append(boid.pos)
            velocities.append(boid.vel)
            
        self.positions = positions
        self.velocities = velocities
        
    def sort_boids(self):
        """
        Perform a lexicographic sort on the boids by position.
        """
        sorted_b = sorted(self.members, key=lambda b: [b.pos[0], b.pos[1]])
        self.members = sorted_b
        
    def triangulate_boids(self):
        """
        Use the delauney_triangulation module to triangulate the set of boids.
        """
        self.sort_boids()
        self.get_pos_vel()
        self.triangulation = triangulate(self.positions)
        
    def setup_triangulate_boids(self):
        """
        Setup the triangulation with actually performing the Delauney 
        triangulation algorithm. This is used for the MPI implementation 
        (in 'run_boids_mpi_cli.py) where there is a custom MPI triangulate 
         function.
        """
        self.sort_boids()
        self.get_pos_vel()
        
    def make_neighbourhoods(self):
        """
        Make neighbourhoods using the Delanunay triangulation module.
        """
        points_seen = []
        for edge in self.triangulation.edges:
            if edge.org not in points_seen and not edge.deactivate:
                connections = edge.find_connections(self.triangulation.edges)
                self.members[edge.org].neighbours = connections
                
    def make_neighbourhoods_basic(self, max_dist=5):
        """
        Make neighbourhoods using the linear seach algorithm.
        """
        for member in self.members:
            member.neighbours = []
            for i, pos in enumerate(self.positions):
                diff_x = pos[0] - member.pos[0]
                diff_y = pos[1] - member.pos[1]
                distance = sqrt(diff_x**2 + diff_y**2)
                if 0<distance<max_dist:
                    # print(i, member.pos, pos)
                    member.neighbours.append([member.index, i])
