from cython.parallel import prange
cimport cython
import numpy as np
cimport numpy as np

cdef char check(double max_dist_half, double diff) nogil:
	if -max_dist_half < diff < max_dist_half:
		return 'p'
	return 'f'

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef np.ndarray main(int num, double max_dist, np.ndarray mem, np.ndarray pos):
	cdef double max_dist_half = max_dist/2
	cdef double diff_x, diff_y
	cdef np.ndarray[np.float64_t,ndim=3]members = mem
	cdef np.ndarray[np.float64_t,ndim=2]positions = pos
    
	cdef int i, j
	for i in range(num):
		for j in range(num):
			diff_x = members[i,0,0] - positions[j,0]
			diff_y = members[i,0,1] - positions[j,1]
			if check(max_dist_half, diff_x)=='p' and check(max_dist_half, diff_y)=='p':
				members[i][j] = positions[j]
                
	return members

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef np.ndarray main2(int threads, int num, double max_dist, np.ndarray mem, np.ndarray pos):
	cdef double max_dist_half = max_dist/2
	cdef double diff_x, diff_y
	cdef np.ndarray[np.float64_t,ndim=3]members = mem
	cdef np.ndarray[np.float64_t,ndim=2]positions = pos
	cdef np.ndarray[np.int_t,ndim=1]prime
    
	cdef int i, j
	for i in range(num):
		prime = np.zeros(num, dtype = int)
		for j in prange(num, nogil=True, num_threads=threads):
			diff_x = members[i,0,0] - positions[j,0]
			diff_y = members[i,0,1] - positions[j,1]
            
			if check(max_dist_half, diff_x)=='p' and check(max_dist_half, diff_y)=='p':
				prime[j] = 1
                
		non_zero = positions * np.vstack((prime, prime)).T
		members[i, 1:] = non_zero
	return members

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef np.ndarray main3(int num, double max_dist, np.ndarray mem, np.ndarray pos):
	cdef double max_dist_half = max_dist/2
	cdef double diff_x, diff_y
	cdef np.ndarray[np.float64_t,ndim=3]members = mem
	cdef np.ndarray[np.float64_t,ndim=2]positions = pos
	cdef np.ndarray[np.int_t,ndim=1]prime
    
	cdef int i, j
	for i in range(num):
		prime = np.zeros(num, dtype = int)
		for j in range(num):
			diff_x = members[i,0,0] - positions[j,0]
			diff_y = members[i,0,1] - positions[j,1]
            
			if check(max_dist_half, diff_x)=='p' and check(max_dist_half, diff_y)=='p':
				prime[j] = 1
                
		non_zero = positions * np.vstack((prime, prime)).T
		members[i, 1:] = non_zero
	return members