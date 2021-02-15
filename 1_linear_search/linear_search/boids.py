# Python libraries
from math import sqrt

# Code from local files
try:
    from linear_search import generate_values
except:
    import generate_values
# -----------------------------------------------------------------------------  

class World():
    """
    A 2D world for the Boids to live in.
    """
    def __init__(self, world_size):
        self.x_min = world_size[0]
        self.x_max = world_size[1]
        self.y_min = world_size[2]
        self.y_max = world_size[3]

# -----------------------------------------------------------------------------  

class Object():
    """
    Define an general object which exists within the World.
    """
    def __init__(self, idx, position):
        self.index = idx
        self.pos = position

class Boid(Object):
    """
    A Boid is a subclass of the Object() class. 
    The Boid has the additional attribute of having neighbours.
    A Boids neighbours are a list of other Boid objects within close proximity.
    """
    def __init__(self, idx, position):
        super().__init__(idx, position)
        self.neighbours = []

    def __repr__(self):
        return f"{self.index}, {self.pos}"

# -----------------------------------------------------------------------------  

class Boids():
    def __init__(self, number, world, max_dist):
        self.num = number
        self.world = world
        self.members = []
        self.positions = []
        self.max_dist = max_dist
        
    def add_boid(self, new_boid):
        self.members.append(new_boid)
        
    def generate_boids(self):
        """
        This function populates the self.members attribute by generating a 
        number of boids with random positions.
        """
        positions = generate_values.random(self.num, self.world)
        self.positions = positions
        for i in range(self.num):
            new_boid = Boid(i, positions[i])
            self.add_boid(new_boid)
    
    def make_neighbourhoods_1(self):
        """
        This function iterates through all boids and finds the neighbours of
        each boid. The neighbours of a boid are points which are less than the
        'max_dist' away using the following distance metric.
            Distance: sqrt((x1-x2)**2+(y1-y2)**2)
        """
        for member in self.members:
            for i, pos in enumerate(self.positions):
                diff_x = pos[0] - member.pos[0]
                diff_y = pos[1] - member.pos[1]
                distance = sqrt(diff_x**2 + diff_y**2)
                if 0 < distance < self.max_dist:
                    member.neighbours.append([member.index, i])

    def make_neighbourhoods_2(self):
        """
        This is an alternative neighbourhood making algorithm which uses a
        different distance metric, the square of the Euclidean distance. This
        removes the need to perform the square root calculation 
        'num_points'**2 many times.
            Distance: (x1-x2)**2+(y1-y2)**2
        """
        max_dist_sq = self.max_dist**2
        for member in self.members:
            for i, pos in enumerate(self.positions):
                diff_x = pos[0] - member.pos[0]
                diff_y = pos[1] - member.pos[1]
                distance = diff_x**2 + diff_y**2
                if 0 < distance < max_dist_sq:
                    member.neighbours.append([member.index, i])
                    
    def make_neighbourhoods_3(self):
        """
        This is an alternative neighbourhood making algorithm which uses the
        Manhattan distance metric. Neighbours are now found within a square
        box centred on the test boid. This removes the need perform a squaring
        operation 2*'num_points'^2 many times
            X distance: (x1-x2)
            Y distance: (y1-y2)
        """
        max_dist_half = self.max_dist/2
        for member in self.members:
            for i, pos in enumerate(self.positions):
                diff_x = pos[0] - member.pos[0]
                diff_y = pos[1] - member.pos[1]
                if -max_dist_half < diff_x < max_dist_half and \
                    -max_dist_half < diff_y < max_dist_half:
                    member.neighbours.append([member.index, i])
                    
