# Python libraries
import numpy as np
import timeit

# Code from local files
import omp_linear_search

# -----------------------------------------------------------------------------  

class Boids():
    def __init__(self, number, world, max_dist):
        self.num = number
        self.world = world
        self.members = []
        self.positions = []
        self.max_dist = max_dist
        
    def generate_members(self):
        """
        This function generates a set of random x and y coordinates using the 
        numpy uniform random number generator 'numpy.random.uniform()'. These
        are used as the starting coordinates of the boids.
        """
        zeros = np.zeros((self.num*(self.num), 2))
        x_vals = np.random.uniform(self.world[0], self.world[1], self.num)
        y_vals = np.random.uniform(self.world[2], self.world[3], self.num)
        
        pts = np.concatenate((x_vals, y_vals)).reshape(-1, 2)
        members = np.concatenate((pts, zeros)).reshape(-1, 2)
        members = np.reshape(members, (-1, self.num+1, 2), order='F')

        self.members = members
        self.positions = pts

    def make_neighbourhoods(self):
        """
        Neighbourhood making algorithm which uses the Manhattan distance 
        metric. Neighbours are found within a square box centred on the test 
        boid.
        """
        max_dist_half = self.max_dist/2
        
        for i in range(self.num):
            for j in range(self.num):
                diff_x = self.members[i,0,0] - self.positions[j,0]
                diff_y = self.members[i,0,1] - self.positions[j,1]
                if -max_dist_half < diff_x < max_dist_half and \
                    -max_dist_half < diff_y < max_dist_half:
                    self.members[i,j,:] = self.positions[j,:]

    def make_neighbourhoods2(self):
        """
        This is the same as the above make_neighbourhoods() function, but the
        algorithm here has been modified for execution without the global 
        interpreter lock.
        """
        max_dist_half = self.max_dist/2
        
        for i in range(self.num):
            prime = np.zeros(self.num, dtype=int)
            for j in range(self.num):
                diff_x = self.members[i,0,0] - self.positions[j,0]
                diff_y = self.members[i,0,1] - self.positions[j,1]
                if -max_dist_half < diff_x < max_dist_half and -max_dist_half < diff_y < max_dist_half:
                    prime[j] = 1
            prime = np.vstack((prime, prime)).T
            non_zero = self.positions * prime
            self.members[i, 1:] = non_zero

    def make_neighbourhoods_cython(self):
        """
        Cythonised version of make_neighbourhoods() function.
        Linear seach nearest neighbour algorithm using cython.
        """
        self.members = omp_linear_search.main_non(self.num, self.max_dist, 
                                              self.members, self.positions)
    def make_neighbourhoods_cython2(self, threads):
        """
        Cythonised version of make_neighbourhoods2() function.
        Linear seach nearest neighbour algorithm using cython and prange 
        openmp parallelism.
        """
        self.members = omp_linear_search.main2(threads, self.num, self.max_dist, 
                                              self.members, self.positions)
        