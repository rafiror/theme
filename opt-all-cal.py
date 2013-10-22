from __future__ import with_statement
from copy import deepcopy
import sys
import logging


MAX = 99999999999999

CONDITIONAL_A = 1.0 / 3
CONDITIONAL_B = 2.0 / 3
CONDITIONAL_C = 9.0 / 10
CONDITIONAL_D = 1
CONDITIONAL_E = 11 / 10
CONDITIONAL_F = MAX

def cal(resource_node, n_node, capacity, resource_traffic):
    n_resource = len(resource_node)
    node_load = [0 for v in range(n_node)]
    link_traffic = [[0 for y in range(n_node)] for x in range(n_node)]
    node_resource_traffic = [[[[0 for y in range(n_node)] for x in range(n_node)] for j in range(n_resource)] for i in range(n_resource)]
    sum_load = 0
    node_traffic = [0] * n_node

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

min_load = MAX
opt_resource_node = []

def resource_node_mapping_cal(n_resource, n_node, n_vm_only_bare, n_vm, resource_node, capacity, resource_traffic):
    global min_load
    global opt_resource_node
    if n_resource == n_vm:
        logging.debug('--------------------------------')
        logging.debug('resource_node %s' % resource_node)
        load = cal(resource_node, n_node, capacity, resource_traffic)
        logging.debug('load %d' % load)
        if load < min_load:
            min_load = load
            opt_resource_node = deepcopy(resource_node)
        #exit()
    else:
        for v in range(n_node):
            if v < n_vm_only_bare:
                continue
            resource_node_add = deepcopy(resource_node)
            resource_node_add[n_resource-1][v] = 1
            resource_node_mapping_cal(n_resource-1, n_node, n_vm_only_bare, n_vm, resource_node_add, capacity, resource_traffic)

if __name__ == "__main__":
    argvs = sys.argv
    argc = len(argvs)
    if argc != 6:
        print 'Usage: # python %s resource_traffic resource_node (int)n_vm_only_bare (int)n_vm log_file' % argvs[0]
        sys.exit()

    with open(argvs[1]) as resource_traffic_file:
        resource_traffic = [map(int,line.strip().split(', ')) for line in resource_traffic_file]
    with open(argvs[2]) as resource_node_file:
        resource_node = [map(int,line.strip().split(', ')) for line in resource_node_file]
    n_resource = len(resource_traffic)
    n_node = len(resource_node[0])
    n_vm_only_bare = int(argvs[3])
    n_vm = int(argvs[4])
    capacity = [20] * n_node
    logging.basicConfig(filename=argvs[5],level=logging.DEBUG)
    logging.debug(resource_traffic)
    logging.debug(resource_node)

    resource_node_mapping_cal(n_resource, n_node, n_vm_only_bare, n_vm, resource_node, capacity, resource_traffic)
    print 'min_load',min_load
    print 'opt_resource_node',opt_resource_node


