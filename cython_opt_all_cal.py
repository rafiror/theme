from __future__ import with_statement
import sys
import logging
import map_cal

MAX = 99999999

if __name__ == "__main__":
    argvs = sys.argv
    argc = len(argvs)
    if argc != 6:
        print 'Usage: # python %s resource_traffic resource_node (int)n_vm_only_bare (int)n_vm log_file' % argvs[0]
        sys.exit()

    with open(argvs[1]) as resource_traffic_file:
        resource_traffic = [map(float,line.strip().split(', ')) for line in resource_traffic_file]
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
    min_load = MAX
    opt_resource_node = []
    result = map_cal.mapping_cal(n_resource, n_node, n_vm_only_bare, n_vm, resource_node, capacity, resource_traffic, min_load, opt_resource_node)
    print 'min_load',result[0]#min_load
    print 'opt_resource_node',result[1]#opt_resource_node
