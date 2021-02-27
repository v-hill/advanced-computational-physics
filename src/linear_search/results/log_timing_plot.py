# Python libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

""" Timings plot """

df = pd.read_csv("mpi_timing_data_2021_02_27__18_53.csv")

fig = plt.figure(figsize=(4, 4), dpi=300)
ax = fig.add_subplot(111)
ax.set_yscale('log')
ax.set_xscale('log')
plt.xlim(50, 25000)
plt.ylim(1, 250000)

plt.title("NNS linear search algorithm parallel MPI comparison", fontsize=11)
plt.xlabel("Number of points", fontsize=11)
plt.ylabel("Time in ms", fontsize=11)

plt.plot(df['Number of points'], df['1 Core non-MPI'], 'o--', linewidth=0.5, markersize=4, label="1 Core non-MPI")
plt.plot(df['Number of points'], df['1 Core'], 's--', linewidth=0.5, markersize=4, label="1 Core")
plt.plot(df['Number of points'], df['4 Core'], 'v--', linewidth=0.5, markersize=4, label="4 Core")
plt.plot(df['Number of points'], df['8 Core'], 'D--', linewidth=0.5, markersize=4, label="8 Core")
plt.plot(df['Number of points'], df['16 Core'], '^--', linewidth=0.5, markersize=4, label="16 Core")

# plt.scatter(results_1[:,0], results_1[:,1], marker='x', label="numpy")
# plt.scatter(results_4[:,0], results_4[:,1], marker='x', label="classes")
# plt.scatter(results_2[:,0], results_2[:,1], marker='x', label="lists & cython")
plt.grid(b=True, which='major', color=(0.5, 0.5, 0.5), linestyle='--', linewidth=0.3)

ax.legend()
plt.show()
