from copy import deepcopy
import sys
import logging


cdef int MAX = 99999999

cdef float CONDITIONAL_A = 1.0 / 3
cdef float CONDITIONAL_B = 2.0 / 3
cdef float CONDITIONAL_C = 9.0 / 10
cdef float CONDITIONAL_D = 1.0
cdef float CONDITIONAL_E = 11 / 10
cdef int CONDITIONAL_F = MAX

cdef int cal(list resource_node, int n_node, list capacity, list resource_traffic):
    cdef int n_resource, sum_load
    cdef list node_load, link_traffic, node_resource_traffic, node_traffic
    cdef int x, y, i, j, v
    n_resource = len(resource_node)
    node_load = [0 for v in range(n_node)]
    link_traffic = [[0 for y in range(n_node)] for x in range(n_node)]
    node_resource_traffic = [[[[0 for y in range(n_node)] for x in range(n_node)] for j in range(n_resource)] for i in range(n_resource)]
    sum_load = 0
    node_traffic = [0] * n_node
    cdef float load
    for x in range(n_node):
        for y in range(n_node):
            for i in range(n_resource):
                for j in range(n_resource):
                    if x != y:
                        node_resource_traffic[i][j][x][y] += resource_traffic[i][j] * resource_node[i][x] * resource_node[j][y]
                    link_traffic[x][y] += node_resource_traffic[i][j][x][y]
            node_traffic[x] += link_traffic[x][y]
        #Add IF(node_traffic[x] > capacity[x]) to reduce computation time
        logging.debug('node_traffic[%d] = %d' % (x,node_traffic[x]))
        if node_traffic[x] > capacity[x]:
            return MAX
        else:
            load = (node_traffic[x] * 1.0 / capacity[x])
            if load < CONDITIONAL_A:
                node_load[x] += 1
            elif load < CONDITIONAL_B:
                node_load[x] += 3
            elif load < CONDITIONAL_C:
                node_load[x] += 10
            elif load < CONDITIONAL_D:
                node_load[x] += 70
            elif load < CONDITIONAL_E:
                node_load[x] += 500
            elif load < CONDITIONAL_F:
                node_load[x] += 5000
            sum_load += node_load[x]
    
    return sum_load

cdef list resource_node_mapping_cal(int n_resource, int n_node, int n_vm_only_bare, int n_vm, list resource_node, list capacity, list resource_traffic, int min_load, list opt_resource_node):
    cdef int load, v
    cdef list resource_node_add, result
    if n_resource == n_vm:
        logging.debug('--------------------------------')
        logging.debug('resource_node %s' % resource_node)
        load = cal(resource_node, n_node, capacity, resource_traffic)
        logging.debug('load %d' % load)
        if load < min_load:
            min_load = load
            opt_resource_node = deepcopy(resource_node)
        return [min_load, opt_resource_node]
    else:
        v = 0
        while v < n_node:
            if v < n_vm_only_bare:
                v += 1
                continue
            resource_node_add = deepcopy(resource_node)
            resource_node_add[n_resource-1][v] = 1
            result = resource_node_mapping_cal(n_resource-1, n_node, n_vm_only_bare, n_vm, resource_node_add, capacity, resource_traffic, min_load, opt_resource_node)
            min_load = result[0]
            opt_resource_node = result[1]
            v += 1
        return [min_load, opt_resource_node]

def mapping_cal(n_resource, n_node, n_vm_only_bare, n_vm, resource_node, capacity, resource_traffic, min_load, opt_resource_node):
    return resource_node_mapping_cal(n_resource, n_node, n_vm_only_bare, n_vm, resource_node, capacity, resource_traffic, min_load, opt_resource_node)
