from copy import deepcopy

cdef double simple_add2(list b):
    cdef int i
    cdef double a = 0
    for i in b:
        a += i
    return a

def simple_add(b):
    return simple_add2(b)
