"""
Code for producing plots of triangulation results.
"""

# ---------------------------------- Imports ----------------------------------

# Standard library imports
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------------  

def basic_plot(world_size, triangulation, positions):
    """
    Make a plot using matplotlib of the final triangulation.

    Parameters
    ----------
    world_size : list
        Range of x and y values for the points
    triangulation : edge_topology.TriangulationEdges
        Completed Delaunay triangulation
    positions : TYPE
        DESCRIPTION.

    Returns
    -------
    plt : matplotlib.pyplot.plot
        Plot of triangulation
    """
    fig = plt.figure(figsize=(8, 8), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_aspect('equal', adjustable='box')
    
    plt.xlim(-5+world_size[0], 5+world_size[1])
    plt.ylim(-5+world_size[2], 5+world_size[3])
    
    plt.xlabel("x")
    plt.ylabel("y")
    
    for edge in triangulation.edges:
        if edge.deactivate==0 and edge.index%2==0:
            x_values = []
            y_values = []
            x_values.append(positions[edge.org][0])
            x_values.append(positions[edge.dest][0])
            y_values.append(positions[edge.org][1])
            y_values.append(positions[edge.dest][1])
            
            plt.plot(x_values, y_values, linewidth=1, linestyle="-", c="k")
            
    plt.scatter([item[0] for item in positions], 
                [item[1] for item in positions], color='k', s=20)
    
    print("done plot")
    return plt
