"""
Command line interface for Delaunay triangulation program.
"""

# ---------------------------------- Imports ----------------------------------

# Standard library imports
import argparse
import time
import numpy as np

# Repo module imports
from triangulation_core.linear_algebra import lexigraphic_sort
import triangulation_core.points_tools.generate_values as generate_values
from triangulation_core.triangulation import triangulate
from utilities.settings import World
from utilities.settings import world_options
import utilities.utilities as utilities
from utilities import plotting

# ---------------------------- Function definitions ---------------------------

def set_options(world_options):
    """
    This function utilises the argparse library to setup all the options of
    the run script.

    Parameters
    ----------
    world_options : dict
        Intial options as defined in 'world_options' file from settings

    Returns
    -------
    options : dict
        Run script options dictionary to be fed into main()
    """
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
    
    return options

def setup_points(options, world):
    num_points = options['num_points']
    if options['points_distribution']=='random':
        positions = generate_values.random(num_points, world)
    elif options['points_distribution']=='lattice':
        positions = generate_values.lattice(num_points, world)
    positions = lexigraphic_sort(positions)
    return positions


def main(options):
    """
    The main attraction.

    Parameters
    ----------
    options : dict
        Dictionary of run options
    """
    # Setup world
    WORLD_SIZE = [0, options['max_x_val'], 
                  0, options['max_y_val']]
    world = World(WORLD_SIZE)

    if options['num_points_scan']:
        steps = np.arange(2, 4.1, 1/3)
        num_pts_list = utilities.make_num_pts_list(steps, base=10, 
                                                   repeats=options['repeats'])
        print('Number of points, time (in ms)')
        for num_pts in num_pts_list:
            options['num_points'] = num_pts
            positions = setup_points(options, world)
            start = time.time()
            triangulation = triangulate(positions)
            elapsed = time.time() - start
            
            # print as comma seperated values for easy cut and paste
            print(f'{num_pts},{elapsed*1000:0.2f}')
            
    else:
        positions = setup_points(options, world)
        start = time.time()
        triangulation = triangulate(positions)
        elapsed = time.time() - start
        print(f'Triangulation completed:\n    Triangulated {options["num_points"]} '
              f'points in {elapsed*1000:0.2f} ms')
        
        if options['plot']:
            print("making plot")
            plt = plotting.basic_plot(WORLD_SIZE, triangulation, positions)
            plt.show()
        
    return triangulation

# ------------------------------------ Main -----------------------------------

if __name__ == '__main__':
    options = set_options(world_options)
    main(options)