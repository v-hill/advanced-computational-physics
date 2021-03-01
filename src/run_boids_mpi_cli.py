"""
This script contains a command line interface for running the full boids 
animation using MPI parallelism. 

Example run command for a 100 boid imulation:
    mpiexec -np 4 python .\run_boids_mpi_cli.py 100
    
Hit 'esc' key to exit at anytime.
"""

# ---------------------------------- Imports ----------------------------------

# Standard library imports
import argparse
from math import pi
from mpi4py import MPI
import time
import cv2 

# Repo module imports
from boids_core.settings import world_options, plotting_options, boids_options
from boids_core.boids import World, Boids
from boids_core import plotting 
import delauney_triangulation.triangulation_core.points_tools.split_list as split_list
from delauney_triangulation.triangulation_core.triangulation import make_primitives
from delauney_triangulation.triangulation_core.triangulation import recursive_group_merge

# --------------------------------- Func defs ---------------------------------

def float_with_range(x):
    try:
        x = float(x)
    except:
        raise argparse.ArgumentTypeError("invalid float value")
    if not 0 < x <= 1:
        raise argparse.ArgumentTypeError("Not in range 0 to 1")
    return x

# ----------------------------- Parse user options ----------------------------

simulation_options = {}
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                 description='Boids run program')

# Simulation options
simulation = parser.add_argument_group('Simulation options')
simulation.add_argument("number_of_boids", 
                        type=int,
                        help=("Number of boids in the simulation \n"
                              "(type: %(type)s)"))

simulation.add_argument("--boid_distribution",
                        default='lattice', const='lattice', nargs="?",
                        choices=['random', 'lattice', 'lattice_with_noise'],
                        help=("Define how the boids are initally arranged "
                              "within the world \n"
                              "(choices: %(choices)s) (default: %(default)s)"))

# Edit world options
world = parser.add_argument_group('Boid world options')
world.add_argument("-ww", "--world_width", 
                    type=int, metavar='',
                    help=("Width of the boids plot in pixels \n"
                          f"(default: {world_options['world_width']}) "
                          "(type: %(type)s)"))
world.add_argument("-wh", "--world_height", 
                    type=int, metavar='',
                    help=("Height of the boids plot in pixels \n"
                          f"(default: {world_options['world_height']}) "
                          "(type: %(type)s)"))

# Edit plotting options
plot_args = parser.add_argument_group('Output plot options')
plot_args.add_argument("-tw", "--triangle_width", 
                    type=int, metavar='',
                    help=("Width of the boid triangles in pixels \n"
                          f"(default: {plotting_options['triangle_width']}) "
                          "(type: %(type)s)"))
plot_args.add_argument("-th", "--triangle_height", 
                    type=int, metavar='',
                    help=("Height of the boid triangles in pixels \n"
                          f"(default: {plotting_options['triangle_height']}) "
                          "(type: %(type)s)"))
plot_args.add_argument("-dpl", "--direction_line_len", 
                    type=int, metavar='',
                    help=("Length of the boid direction arrow pointers "
                          "in pixels \n"
                          f"(default: {plotting_options['direction_line_len']}) "
                          "(type: %(type)s)"))
plot_args.add_argument("-nc", "--num_colours", 
                    type=int, metavar='',
                    help=("Number of possible colours a boid can be \n"
                          f"(default: {plotting_options['num_colours']}) "
                          "(type: %(type)s)"))
plot_args.add_argument("--no_boid_colours", 
                    action="store_true", default=False,
                    help=("Do not plot boids with different colour values \n"
                          "(default: False)"))
plot_args.add_argument("--no_border", 
                    action="store_true", default=False,
                    help=("Do not plot a border around the boid world \n"
                          "(default: False)"))
plot_args.add_argument("-bs", "--border_size", 
                    type=int, metavar='',
                    help=("Size of border around boids world in pixels \n"
                          f"(default: {plotting_options['border_size']}) "
                          "(type: %(type)s)"))
plot_args.add_argument("--background_colour", 
                    default="black", const="black", nargs="?", 
                    choices=["black", "white"],
                    help=("Set the background colour of the output plot \n"
                          "(choices: %(choices)s)"))
plot_args.add_argument("--save", 
                    type=str,
                    help=("Save the output, given a filename \n"
                          "(type: %(type)s)"))

# Edit boid options
boid = parser.add_argument_group('Boid options')
boid.add_argument("-vmax", "--max_speed",
                  type=int, metavar='',
                  help=("Boid max speed in pixels per timestep \n"
                        f"(default: {boids_options['max_speed']}) "
                        "(type: %(type)s)"))
boid.add_argument("-fov", "--field_of_view", 
                  type=float_with_range, metavar='',
                  help=("Boid field of view, as a fraction of a full "
                        "circle. \ne.g. 0.5 gives \u03C0 radians fov \n"
                        "(default: 0.66) (type: %(type)s)"))
boid.add_argument("-vd", "--vision_distance", 
                  type=int, metavar='',
                  help=("Limit how far away a neighbouring boid can be in"
                        " order to stil be considered a neighbour \n"
                        f"(default: {boids_options['vision_distance']}) "
                        "(type: %(type)s)"))
boid.add_argument("-sz", "--safety_zone", 
                  type=int, metavar='',
                  help=("Set how close another boid can be before "
                        "avoidance behaviour occurs \n"
                        f"(default: {boids_options['safety_zone']}) "
                        "(type: %(type)s)"))
boid.add_argument("-ali", "--alignment_perception", 
                  type=float, metavar='',
                  help=("Strength of boid alignment to neighbours travel "
                        "directions \n"
                        f"(default: {boids_options['alignment_perception']}) "
                        "(type: %(type)s)"))
boid.add_argument("-coh", "--cohesion_perception", 
                  type=float, metavar='',
                  help=("Strength of boid cohesion to neighbours \n"
                        f"(default: {boids_options['cohesion_perception']}) "
                        "(type: %(type)s)"))
boid.add_argument("-sep", "--seperation_perception", 
                  type=float, metavar='',
                  help=("Strength of boid seperation from neighbours \n"
                        f"(default: {boids_options['seperation_perception']}) "
                        "(type: %(type)s)"))

args = parser.parse_args()

# Simulation options
simulation_options['number_of_boids'] = args.number_of_boids
simulation_options['boid_distribution'] = args.boid_distribution

# Edit world options
if args.world_width: 
    world_options['world_width'] = args.world_width
if args.world_height: 
    world_options['world_height'] = args.world_height

# Edit plotting options
if args.triangle_width: 
    plotting_options['triangle_width'] = args.triangle_width
if args.triangle_height: 
    plotting_options['triangle_height'] = args.triangle_height
if args.direction_line_len: 
    plotting_options['direction_line_len'] = args.direction_line_len
if args.num_colours: 
    plotting_options['num_colours'] = args.num_colours
if args.no_boid_colours:
    plotting_options['plot_boid_colours'] = False
if args.no_border:
    plotting_options['plot_border'] = False
if args.border_size: 
    plotting_options['border_size'] = args.border_size
if args.background_colour: 
    plotting_options['background_colour'] = args.background_colour
if args.save:
    plotting_options['save_output'] = True
    plotting_options['save_filename'] = args.save
else:
    del plotting_options['save_filename']
    
# Edit boid options
if args.max_speed:
    boids_options['max_speed'] = args.max_speed
if args.field_of_view:
    boids_options['field_of_view'] = round(args.field_of_view*(2*pi), 3)
if args.vision_distance:
    boids_options['vision_distance'] = args.vision_distance
if args.safety_zone:
    boids_options['safety_zone'] = args.safety_zone
if args.alignment_perception:
    boids_options['alignment_perception'] = args.alignment_perception
if args.cohesion_perception:
    boids_options['cohesion_perception'] = args.cohesion_perception
if args.seperation_perception:
    boids_options['seperation_perception'] = args.seperation_perception
    
print("Simulation options:")
for key, val in simulation_options.items():
    print(f"    {key:22} {val}")

print("Boid world options:")
for key, val in world_options.items():
    print(f"    {key:22} {val}")
    
print("Output plot options:")
for key, val in plotting_options.items():
    print(f"    {key:22} {val}")
    
print("Boid options:")
for key, val in boids_options.items():
    print(f"    {key:22} {val}")

options = {**world_options, 
           **plotting_options, 
           **boids_options, 
           **simulation_options}

# ------------------------------ Setup simulation -----------------------------

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

print(f'Running MPI boids simulaiton of {size} cores...')

WORLD_SIZE = [0, options['world_width'], 
              0, options['world_height']]
world = World(WORLD_SIZE)
cmap = plotting.ColourMap(options)
plot = plotting.Plotter(options, world)

num_boids = options['number_of_boids']
num_boids = num_boids-(num_boids%size)
options['number_of_boids'] = num_boids

print_fps_to_console = True
boids = Boids(num_boids, world, options)
boids.generate_boids(options, distribution=options['boid_distribution'])

# ----------------------------- MPI triangulation -----------------------------

def plot_func(boids):
    """
    This function performs a single iterations of the Boids simulation using
    MPI to compute the boid beighourhoods in parallel.

    Parameters
    ----------
    boids : boids.Boids
        Boids class

    Returns
    -------
    boids : boids.Boids
        Boids class
    """
    boids.setup_triangulate_boids()
    
    if rank == 0:
        positions = boids.positions
        split_pts = split_list.groups_of_3(positions)
        pts_per_core = int(len(split_pts)/size)+1
        data = [split_pts[i:i + pts_per_core] for i in range(0, len(split_pts), pts_per_core)]
    else:
        data = None
    data = comm.scatter(data, root=0)
    
    primitives = make_primitives(data)
    groups = [primitives[i:i+2] for i in range(0, len(primitives), 2)]
    triangulation = recursive_group_merge(groups)
    
    new_groups = comm.gather(triangulation,root=0)
    
    if rank == 0:
        final_groups = []
        # Account for MPI on 1 core
        if size>1:
            for i in range(0, size, 2):
                group = [new_groups[i][0][0], new_groups[i+1][0][0]]
                final_groups.append(group)
        else:
            final_groups = new_groups[0]
        triangulation = recursive_group_merge(final_groups)
        triangulation = triangulation[0][0]

        boids.triangulation = triangulation

        boids.make_neighbourhoods()
        for i in range(num_boids):
            a = boids.members[i]
            a.update_boid(boids.positions, boids.velocities, world)
            if a.index%int(num_boids/3)==0:
                plot.plot_neighbours(a, boids.positions)
                
    return boids

# ------------------------------ Main animation -------------------------------

def animation_mpi(self, rank, boids, plot_func, cmap, verbose=False, print_fps=24):
    """
    Animation function from plotting.Plotter adapted for MPI.
    """
    start = time.time()
    iterations = 0
    if rank == 0: cv2.imshow("image", self.img)
    if verbose: print("frame number, frames per second")
    while True:
        if rank == 0:
            self.img = self.tabula_rasa()
        boids = plot_func(boids)
        if rank == 0:
            self.plot_boids(boids, cmap)
            cv2.imshow("image", self.img)
        k = cv2.waitKey(1)
        if k == 27:
            break
        if verbose and iterations%print_fps==0:
            print(f"{iterations},{iterations/(time.time()-start):0.3f}")
        iterations += 1
    if rank == 0: cv2.destroyWindow("image")
    
plotting.Plotter.animation_mpi = animation_mpi

print("\nPlotting animation...")
print("    Hit 'esc' key to exit at anytime")

plot = plotting.Plotter(options, world)
plot.animation_mpi(rank, boids, plot_func, cmap, 
                verbose=print_fps_to_console, print_fps=48)
