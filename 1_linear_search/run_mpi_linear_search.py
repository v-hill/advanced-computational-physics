"""
This scripts implements the nearest neighbour linear search algorithm in 
parallel using MPI.

Example run command, using default 1000 generated points:
        mpiexec -n 4 python .\run_mpi_linear_search.py
        
Example run command to scan through 100 to 10,000 points repeating each 
execution 2 times:
        mpiexec -n 2 python .\run_mpi_linear_search.py --num_points_scan -r 2
"""

# Python libraries
from mpi4py import MPI
import argparse
import numpy as np
import pandas as pd

# Code from local files
from linear_search.boids import World, Boids
import linear_search.utilities as utilities

# --------------------------------- func defs ---------------------------------

def mpi_setup():
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()
    return {'comm':comm, 'size':size, 'rank':rank}

def main(mpi, num_points, max_neighbour_dist, scan):
    # Setup
    world_size = [0, 1000, 0, 1000]
    world = World(world_size)
    boids = Boids(num_points, world, max_neighbour_dist)
    boids.generate_boids()
    
    
    if mpi['rank'] == 0 and not scan:
        print(f'Running on {mpi["size"]} cores...')
        print('Manhattan distance with MPI:')
        
    if mpi['rank'] == 0:
        wt_start = MPI.Wtime()
        pts_per_core = int(len(boids.members)/mpi['size'])+1
        data = [boids.members[i:i + pts_per_core] for i in range(0, len(boids.members), pts_per_core)]
    else:
        data = None
    
    # Start timer
    wt_start = MPI.Wtime()
    
    # Scatter data to seperate cores
    data = mpi['comm'].scatter(data, root=0)
    max_dist_half = boids.max_dist/2
    for member in data:
        for i, pos in enumerate(boids.positions):
            diff_x = pos[0] - member.pos[0]
            diff_y = pos[1] - member.pos[1]
            if -max_dist_half < diff_x < max_dist_half and \
                -max_dist_half < diff_y < max_dist_half:
                member.neighbours.append([member.index, i])
                
    # Gather data
    data_gathered = mpi['comm'].gather(data,root=0)
    
    if mpi['rank'] == 0:
        new_members = []
        for data in data_gathered:
            new_members += data
        
        boids.members = new_members
        
        # End timer and print elasped time
        wt_end = MPI.Wtime()
        elapsed = wt_end - wt_start
        if scan:
            return [num_points, elapsed*1000]
        else:
            return f'\t {elapsed*1000:0.1f} ms'

# ------------------------------------ main -----------------------------------

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Nearest neighbour '
                                     'search algorithm with MPI')
    parser.add_argument('-n', '--num_points', 
                        help='The number of points', 
                        type=int,
                        default = 1000)
    
    parser.add_argument('-mnd', '--max_neighbour_dist', 
                        help='The maximum neighbour distance', 
                        type=int,
                        default = 100)
    
    parser.add_argument('--num_points_scan', 
                        default=False, action='store_true',
                        help=('Run the script multiple times using a range '
                              'of values for the number of points. Values '
                              'range from 100 to 10000 with a logarithmic '
                              'distribution'))
    
    parser.add_argument('-r', '--repeats', 
                        help='The number of times to repeat each num_points '
                        'value', 
                        type=int,
                        default = 1)
    args = parser.parse_args()
    
    mpi = mpi_setup()
    
    # Execute for a single value of num_points
    if not args.num_points_scan:
        res = main(mpi, 
                   args.num_points, 
                   args.max_neighbour_dist, 
                   args.num_points_scan)
        if mpi['rank'] == 0:
            print(res)
    
    # Execute multiple times for a range of num_points values
    else:
        results = []
        steps = np.arange(2, 4.1, 1/3)
        num_pts_list = utilities.make_num_pts_list(steps, base=10, 
                                                   repeats=args.repeats)
        for num_pts in num_pts_list:
            res = main(mpi, 
                       num_pts, 
                       args.max_neighbour_dist, 
                       args.num_points_scan)
            results.append(res)
        
        if mpi['rank'] == 0:
            if args.repeats==0:
                columns = ['Number of points', 
                           ('Execution time for Manhattan distance using '
                           f'MPI on {mpi["size"]} cores (in ms)')]
            else:
                columns = ['Number of points', 
                           ('Execution time using '
                           f'MPI on {mpi["size"]} cores, average of '
                           f'{args.repeats} repeats (in ms)')]   
            
            df = pd.DataFrame(results, columns=columns)
            df = df.groupby('Number of points').mean().reset_index()
            print(df)
            
