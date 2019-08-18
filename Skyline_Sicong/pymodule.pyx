from pythonmodule import result
from libc.stdlib cimport malloc
import numpy as np
cimport numpy as np


cdef public np.ndarray getNPArray():
    """ Return array from pythonmodule. """
    return <np.ndarray>result

cdef public int getShape(np.ndarray arr, int shape):
    """ Return Shape of the Array based on shape par value. """
    return <int>arr.shape[1] if shape else <int>arr.shape[0]

cdef public void copyData(float *** dst, np.ndarray src):
    """ Copy data from src numpy array to dst. """
    cdef float **tmp
    cdef int i, j, m = src.shape[0], n=src.shape[1];

    # Allocate initial pointer
    tmp = <float **>malloc(m * sizeof(float *))
    if not tmp:
        raise MemoryError()

    # Allocate rows
    for j in range(m):
        tmp[j] = <float *>malloc(n * sizeof(float))
        if not tmp[j]:
            raise MemoryError()

    # Copy numpy Array
    for i in range(m):
        for j in range(n):
            tmp[i][j] = src[i, j]

    # Assign pointer to dst
    dst[0] = tmp
