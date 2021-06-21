# advanced-computational-physics

## Description
This repository contains my code for the Advanced Computational Physics PHYSM0032 course in parallel programming.
In this project I have implemented the [Boids](https://en.wikipedia.org/wiki/Boids) flocking behaviour simulation. Using the Python programming language, I explore techniques to speed up the run-time of this simulation. I investigate both shared and distributed memory parallel processing architectures using the MPI and OpenMP frameworks. I make use of the BlueCrystal3 high performance computing system available at Bristol to run code on up to 16 cores. I explore the effects of different data structures on code performance, and employ Cython to generate precompiled C modules. Finally, I use a divide and conquer triangulation algorithm to reduce the computational complexity of the boids programme. 

![Alt Text](https://github.com/V-Hill/advanced-computational-physics/blob/main/src/boids_core/tests/100_boid_simulation.gif)

## Overview of repository

The first main challenge of the Boids simulation is determining which boids should be considered neighbours of a given boid.
In the first of the three main source (/src) directories I have written code which implements a [linear search](https://en.wikipedia.org/wiki/Nearest_neighbor_search#Linear_search) method for the nearest neighbour search problem. 

* In *'run_linear_search_comparison.py'* I compare different distance metrics to speed up the linear search. 
* In *'run_cython_linear_search.py'* I use the [Cython](https://en.wikipedia.org/wiki/Cython) programming language to speed up the linear search.
* In *'run_omp_linear_search.py'* I use [OpenMP](https://en.wikipedia.org/wiki/OpenMP) via the 'cython.parallel' module to implement shared-memory multiprocessing to the linear search.
* In *'run_mpi_linear_search.py'* I use the Message Passing Interface ([MPI](https://en.wikipedia.org/wiki/Message_Passing_Interface)) standard via the 'mpi4py' Python library to parallelise the linear search algorithm for distributed-memory parallel computing.

In the second directory in /src called 'delauney_triangulation' stores for my [Delauney triangulation](https://en.wikipedia.org/wiki/Delaunay_triangulation) code. This contains the following run scripts:

* *'run_triangulation_cli.py'* command line interface for the python Delauney triangulation module.
* *'run_triangulation_mpi_cli.py'* command line interface for the python Delauney triangulation module using MPI parallelism.
* *'run_triangulation_test.py'* test script for the python Delauney triangulation module.
* *'run_triangulation_test_mpi.py'* test script for the python Delauney triangulation module using MPI parallelism.

In the third directory in /src called 'boids_core' my implementation of the [Boids](https://en.wikipedia.org/wiki/Boids) flocking simulation is found.  This contains the following run scripts:

* *'run_boids.py'* command line interface for the full Boids animation code.
* *'run_boids__mpi_cli.py'* command line interface for the full Boids animation code parallelised using MPI.
* *'test_boids_linear_search_animation.py'* Simple test of the Boids animation using linear search neighbour finding.
* *'test_boids_linear_search_image.py'* Simple test to plot a single frame using linear search neighbour finding.
* *'test_boids_triangulation_animation.py'* Simple test of the Boids animation using Delauney triangulation neighbour finding.
* *'test_boids_triangulation_image.py'*  Simple test to plot a single frame using Delauney triangulation neighbour finding.

## Project structure

Files starting with 'run_' or 'test_' denote scripts which can be run (labeled ** below).

All other '.py' files are modules containing Python definitions and statements.

The suffix '_cli' specifies command line interface scripts. Run these with the '-h' argument initially for available options. 

This repository is currently structured as follows:

    ├── src                   
        ├── boids_core
        │   ├── tests
        │   │   ├── test_boids_linear_search_animation.py**
        │   │   ├── test_boids_linear_search_image.py**
        │   │   ├── test_boids_triangulation_animation.py**
        │   │   └── test_boids_triangulation_image.py**
        │   ├── boids.py
        │   ├── generate_values.py
        │   ├── plotting.py
        │   └── settings.py
        ├── delauney_triangulation
        │   ├── results
        │   │   └── ...
        │   ├── triangulation_core
        │   │   ├── points_tools
        │   │   │   ├── generate_values.py
        │   │   │   └── split_list.py
        │   │   ├── edge_topology.py
        │   │   ├── linear_algebra.py
        │   │   ├── triangulation.py
        │   │   └── triangulation_primitives.py
        │   ├── utilities
        │   │   ├── plotting.py
        │   │   ├── settings.py
        │   │   └── utilities.py
        │   ├── run_triangulation_cli.py**
        │   ├── run_triangulation_mpi_cli.py**
        │   ├── run_triangulation_test.py**
        │   └── run_triangulation_test_mpi.py**
        ├── linear_search
        │       ├── cython_linear_search
        │       │   ├── cython_linear_search.pyx
        │       │   ├── generate_values.py
        │       │   ├── run_cython_linear_search.py**
        │       │   └── setup.py
        │       ├── linear_search
        │       │   ├── boids.py
        │       │   ├── generate_values.py
        │       │   └── utilities.py
        │       ├── omp_linear_search
        │       │   ├── boids.py
        │       │   ├── omp_linear_search.pyx
        │       │   ├── run_omp_linear_search.py**
        │       │   └── setup.py
        │       ├── results
        │       │   └── ...
        │       ├── run_linear_search_comparison.py**
        │       └── run_mpi_linear_search.py**
        │   run_boids_cli.py**
        └── run_boids__mpi_cli.py**
        
## Example simulation setup

The gif Boid simulation was produced with the following setup:

Simulation options:
- number_of_boids: 100
- still_image: False
- boid_distribution: lattice
    
Boid world options:
- world_width:            500 pixels
- world_height:           500 pixels
    
Output plot options:
- triangle_width:         8 pixels
- triangle_height:        12 pixels
- direction_line_len:     50 pixels
- num_colours:            4
- plot_boid_colours:      True
- plot_border:           True
- border_size:            50
- background_colour:      black
- save_output:            False
    
Boid options:
- max_speed:              2
- field_of_view:          4.147 rad
- vision_distance:        200
- safety_zone:            20
- alignment_perception:   0.08
- cohesion_perception:    0.008
- seperation_perception:  0.25
