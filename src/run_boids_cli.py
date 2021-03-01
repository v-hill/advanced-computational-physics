"""
This script contains a command line interface for running the full boids 
animation. This full list of possible user arguments is detailed below.

optional arguments:
  -h, --help            show this help message and exit

Simulation options:
  number_of_boids       Number of boids in the simulation
                        (type: int)
  --still_image         Instead of an animation, show a single still frame
                        (default: False)
  --boid_distribution [{random,lattice,lattice_with_noise}]
                        Define how the boids are initally arranged within the world
                        (choices: random, lattice, lattice_with_noise) 
                        (default: lattice)

Boid world options:
  -ww , --world_width   Width of the boids plot in pixels
                        (default: 1000) (type: int)
  -wh , --world_height
                        Height of the boids plot in pixels
                        (default: 1000) (type: int)

Output plot options:
  -tw , --triangle_width
                        Width of the boid triangles in pixels
                        (default: 8) (type: int)
  -th , --triangle_height
                        Height of the boid triangles in pixels
                        (default: 12) (type: int)
  -dpl , --direction_line_len
                        Length of the boid direction arrow pointers in pixels
                        (default: 50) (type: int)
  -nc , --num_colours   Number of possible colours a boid can be
                        (default: 4) (type: int)
  --no_boid_colours     Do not plot boids with different colour values
                        (default: False)
  --no_border           Do not plot a border around the boid world
                        (default: False)
  -bs , --border_size   Size of border around boids world in pixels
                        (default: 50) (type: int)
  --background_colour [{black,white}]
                        Set the background colour of the output plot
                        (choices: black, white)
  --save SAVE           Save the output, given a filename
                        (type: str)

Boid options:
  -vmax , --max_speed   Boid max speed in pixels per timestep
                        (default: 2) (type: int)
  -fov , --field_of_view
                        Boid field of view, as a fraction of a full circle.
                        e.g. 0.5 gives π radians fov
                        (default: 0.66) (type: float_with_range)
  -vd , --vision_distance
                        Limit how far away a neighbouring boid can be in order 
                        to stil be considered a neighbour
                        (default: 200) (type: int)
  -sz , --safety_zone   Set how close another boid can be before avoidance 
                        behaviour occurs
                        (default: 20) (type: int)
  -ali , --alignment_perception
                        Strength of boid alignment to neighbours travel directions
                        (default: 0.08) (type: float)
  -coh , --cohesion_perception
                        Strength of boid cohesion to neighbours
                        (default: 0.008) (type: float)
  -sep , --seperation_perception
                        Strength of boid seperation from neighbours
                        (default: 0.25) (type: float)
"""

# ---------------------------------- Imports ----------------------------------

# Standard library imports
import argparse
from math import pi

# Repo module imports
from boids_core.settings import world_options, plotting_options, boids_options
from boids_core.boids import World, Boids
from boids_core import plotting 

# -----------------------------------------------------------------------------  

def float_with_range(x):
    try:
        x = float(x)
    except:
        raise argparse.ArgumentTypeError("invalid float value")
    if not 0 < x <= 1:
        raise argparse.ArgumentTypeError("Not in range 0 to 1")
    return x

def set_options(world_options, plotting_options, boids_options):
    """
    Function using argparse to parse all user parameters.

    Parameters
    ----------
    world_options : dict
        default options dictionary
    plotting_options : dict
        default options dictionary
    boids_options : dict
        default options dictionary

    Returns
    -------
    options : dict
        All simulation options

    """
    simulation_options = {}
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                     description='Boids run program')
    
    # Simulation options
    simulation = parser.add_argument_group('Simulation options')
    simulation.add_argument("number_of_boids", 
                            type=int,
                            help=("Number of boids in the simulation \n"
                                  "(type: %(type)s)"))
    simulation.add_argument("--still_image", 
                            action="store_true", default=False,
                            help=("Instead of an animation, show a single "
                                  "still frame \n"
                                  "(default: False)"))
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
    simulation_options['still_image'] = args.still_image
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
    return options

# -----------------------------------------------------------------------------  

def main(options):
    # Setup world
    WORLD_SIZE = [0, options['world_width'], 
                  0, options['world_height']]
    world = World(WORLD_SIZE)
    cmap = plotting.ColourMap(options)
    plot = plotting.Plotter(options, world)
    num_boids = options['number_of_boids']
    print_fps_to_console = True
    boids = Boids(num_boids, world, options)
    boids.generate_boids(options, distribution=options['boid_distribution'])
    
    if options['still_image']:
        print("\nPlotting single still image...")
        
        boids.triangulate_boids()
        boids.make_neighbourhoods()
        for i in range(num_boids):
            a = boids.members[i]
            # a.update_boid(boids.positions, boids.velocities, world)
            if a.index%32==0:
                plot.plot_neighbours(a, boids.positions)
        plot.plot_boids(boids, cmap)
        plot.display()
        if plotting_options['save_output']:
            plot.save(plotting_options['save_filename'])
    
    else:
        def plot_func(boids):
            boids.triangulate_boids()
            boids.make_neighbourhoods()
            for i in range(num_boids):
                a = boids.members[i]
                a.update_boid(boids.positions, boids.velocities, world)
                if a.index%int(num_boids/3)==0:
                    plot.plot_neighbours(a, boids.positions)
            return boids
        
        print("\nPlotting animation...")
        print("    Hit 'esc' key to exit at anytime")
        plot = plotting.Plotter(options, world)
        plot.animation(boids, plot_func, cmap, 
                       verbose=print_fps_to_console, print_fps=48)

# ----------------------------------- Main ------------------------------------

if __name__ == '__main__':
    options = set_options(world_options, plotting_options, boids_options)
    main(options)
