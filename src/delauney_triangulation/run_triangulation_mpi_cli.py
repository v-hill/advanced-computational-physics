"""
Command line interface for MPI Delaunay triangulation program.

Example run command:
    mpiexec -np 4 python .\run_triangulation_mpi_cli.py
"""

# ---------------------------------- Imports ----------------------------------

# Standard library imports
import argparse
import numpy as np
from mpi4py import MPI
import time

# Repo module imports
import triangulation_core.points_tools.generate_values as generate_values
from triangulation_core.linear_algebra import lexigraphic_sort
from triangulation_core.points_tools.split_list import groups_of_3
from triangulation_core.triangulation import make_primitives
from triangulation_core.triangulation import recursive_group_merge

import utilities.utilities as utilities
from utilities.settings import World
from utilities.settings import world_options
from utilities import plotting

# ---------------------------- Function definitions ---------------------------

def run_mpi(comm, options):
    num_points = options['num_points']
    
    # Setup MPI
    size = comm.Get_size()
    rank = comm.Get_rank()
    wt_start = MPI.Wtime()  # start timer
    
    if rank == 0:
        WORLD_SIZE = [0, options['max_x_val'], 
                      0, options['max_y_val']]
        world = World(WORLD_SIZE)
    
        positions = generate_values.random(num_points, world)
        positions = lexigraphic_sort(positions)
        split_pts = groups_of_3(positions)
        pts_per_core = int(len(split_pts)/size)+1
        data = [split_pts[i:i + pts_per_core] for i in range(0, len(split_pts), pts_per_core)]
    else:
        data = None
    data = comm.scatter(data, root=0)
    
    primitives = make_primitives(data)
    groups = [primitives[i:i+2] for i in range(0, len(primitives), 2)]
    triangulation = recursive_group_merge(groups)
    # print(f"Rank: {rank}, elapsed time: {(MPI.Wtime()-wt_start)*1000:0.3f} ms")
    
    new_groups = comm.gather(triangulation,root=0)
    
    if rank == 0:
        # print(f"After recombination, elapsed time: {(MPI.Wtime()-wt_start)*1000:0.3f} ms")
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
        wt_end = MPI.Wtime()
        elapsed = wt_end - wt_start
        
        if options['num_points_scan']:
            # print as comma seperated values for easy cut and paste
            print(f'{num_pts},{elapsed*1000:0.2f}')
        else:
            print(f'Triangulation completed:\n    '
                  f'Triangulated {options["num_points"]} points in '
                  f'{elapsed*1000:0.2f} ms')
        
    return triangulation

# -------------------------------- Set options --------------------------------

comm = MPI.COMM_WORLD

general_options = {}
points_options = {}
scan_options = {}
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                 description='Triangulation run script')

parser.add_argument('--plot', 
                  default=False, action='store_true',
                  help=('Plot the resulting Delauney triangulation. '
                        'Only available without --num_points_scan option.'))

# Points options
points = parser.add_argument_group('Points options')

points.add_argument('-n', '--num_points', 
                    type=int,
                    default=1000,
                    help=('Number of points to generate \n'
                          '(type: %(type)s)'))
points.add_argument('--points_distribution',
                    default='random', const='random', nargs="?",
                    choices=['random', 'lattice'],
                    help=('Define how the points are initally arranged '
                          'within the world \n'
                          '(choices: %(choices)s) (default: %(default)s)'))

# Edit world options
world = parser.add_argument_group('Points world options')
world.add_argument('-xm', '--max_x_val', 
                    type=float, metavar='',
                    help=('Max x-value of generated points \n'
                          f'(default: {world_options["max_x_val"]}) '
                          '(type: %(type)s)'))
world.add_argument('-ym', '--max_y_val', 
                    type=float, metavar='',
                    help=('Max y-value of generated points \n'
                          f'(default: {world_options["max_y_val"]}) '
                          '(type: %(type)s)'))

# Scan arguments
scan = parser.add_argument_group('Scan number of points options')
scan.add_argument('--num_points_scan', 
                  default=False, action='store_true',
                  help=('Run the script multiple times using a range of '
                        'values for the number of points. Values range '
                        'from 100 to 10000 with a logarithmic '
                        'distribution'))
scan.add_argument('-r', '--repeats', 
                  help='The number of times to repeat each num_points '
                  'value', 
                  type=int,
                  default = 1)

args = parser.parse_args()

# General options
general_options['plot'] = args.plot

# Points options
points_options['num_points'] = args.num_points
points_options['points_distribution'] = args.points_distribution

# Scan options
scan_options['num_points_scan'] = args.num_points_scan
scan_options['repeats'] = args.repeats

# Edit world options
if args.max_x_val: 
    world_options['max_x_val'] = args.max_x_val
if args.max_y_val: 
    world_options['max_y_val'] = args.max_y_val

if comm.Get_rank() == 0:
    print('Points options:')
    for key, val in points_options.items():
        print(f'    {key:22} {val}')
        
    print('Points world options:')
    for key, val in world_options.items():
        print(f'    {key:22} {val}')
        

    print('Scan number of points options:')
    for key, val in scan_options.items():
        print(f'    {key:22} {val}')

options = {**general_options,
           **world_options, 
           **points_options,
           **scan_options}

# ------------------------------------ Main -----------------------------------

# Setup world
WORLD_SIZE = [0, options['max_x_val'], 
              0, options['max_y_val']]

if options['num_points_scan']:
    steps = np.arange(2, 4.1, 1/3)
    num_pts_list = utilities.make_num_pts_list(steps, base=10, 
                                               repeats=options['repeats'])
    if comm.Get_rank() == 0: print('Number of points, time (in ms)')
    for num_pts in num_pts_list:
        options['num_points'] = num_pts
        triangulation = run_mpi(comm, options)
else:
    start = time.time()
    triangulation = run_mpi(comm, options)
    elapsed = time.time() - start
    if comm.Get_rank() == 0:
        positions = triangulation.points
        if options['plot']:
            plt = plotting.basic_plot(WORLD_SIZE, triangulation, positions)
            plt.show()
            