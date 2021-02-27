# advanced-computational-physics

## Description
This repository contains my code for the Advanced Computational Physics PHYSM0032 course in parallel programming.
In this project I have implemented the [Boids](https://en.wikipedia.org/wiki/Boids) artificial life program, developed by Craig Reynolds.

The first main challenge of the Boids simulation is determining which boids should be considered neighbours of a given boid.
In the first of the three main source (src) directories I have written code which implements a [linear search](https://en.wikipedia.org/wiki/Nearest_neighbor_search#Linear_search) method for the nearest neighbour search problem. 

* In *'run_linear_search_comparison.py'* I compare different distance metrics to speed up the linear search. 
* In *'run_cython_linear_search.py'* I use the [Cython](https://en.wikipedia.org/wiki/Cython) programming language to speed up the linear search.
* In *'run_omp_linear_search.py'* I use [OpenMP](https://en.wikipedia.org/wiki/OpenMP) via the 'cython.parallel' module to implement shared-memory multiprocessing to the linear search.
* In *'run_mpi_linear_search.py'* I use the Message Passing Interface ([MPI](https://en.wikipedia.org/wiki/Message_Passing_Interface)) standard via the 'mpi4py' Python library to parallelise the linear search algorithm for distributed-memory parallel computing.



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
        │       ├── omp_linear_search
        │       │   ├── boids.py
        │       │   ├── omp_linear_search.pyx
        │       │   └── setup.py
        │       ├── results
        │       │   └── ...
        │       ├── run_linear_search_comparison.py**
        │       └── run_mpi_linear_search.py**
        └── run_boids.py**
