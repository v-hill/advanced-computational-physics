# Python libraries
from __future__ import print_function
import numpy as np
cimport numpy as np

cdef class Boid:
    """
    A Boid object is defined by an index, a position
    The Boid has the additional attribute of having neighbours.
    A Boids neighbours are a list of other Boid objects within close proximity.
    """
    cdef int index
    cdef list pos
    cdef list neighbours
    
    def __init__(self, idx, position):
        self.index = idx
        self.pos = position
        self.neighbours = []
        
    def get_pos(self):
        return self.pos
    
    def get_index(self):
        return self.index
    
    def add_neighbour(self, val):
        self.neighbours.append(val)

cdef class Boids:
    cdef int num
    cdef list members, positions
    cdef double max_dist, max_dist_half
    
    def __init__(self, number, max_dist):
        self.num = number
        self.members = []
        self.positions = []
        self.max_dist = max_dist
        self.max_dist_half = self.max_dist/2
        
    def add_boid(self, new_boid):
        self.members.append(new_boid)
        
    def generate_boids(self, list positions):
        """
        This function populates the self.members attribute by generating a 
        number of boids with random positions.
        """
        self.positions = positions
        for i in range(self.num):
            new_boid = Boid(i, positions[i])
            self.add_boid(new_boid)
    
    cdef int check_val(self, list val, list pos):
        diff_x = pos[0] - val[0]
        diff_y = pos[1] - val[1]
        if (-self.max_dist_half < diff_x < self.max_dist_half and 
            -self.max_dist_half < diff_y < self.max_dist_half):
            return 1
        return 0

    cpdef void make_neighbourhoods(self):
        """
        Neighbourhood making algorithm which uses the Manhattan distance 
        metric. Neighbours are found within a square box centred on the test 
        boid.
        """
        cdef int i
        for i in range(self.num):
            for j in range(self.num):
                if self.check_val(self.members[i].get_pos(), self.positions[j]):
                    self.members[i].add_neighbour([self.members[i].get_index(), i])

cpdef setup(int num_points, int max_dist, list positions):
    boids = Boids(num_points, max_dist)
    boids.generate_boids(positions)
    return boids
    
cpdef void main(boids):
    boids.make_neighbourhoods()
    
