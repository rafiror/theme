from __future__ import with_statement
from pulp import *
import sys
import logging
import gurobipy

CAPACITY = 100

def cal(n_resource, n_node, capacity, resource_traffic):

    prob = LpProblem('ResourceAllocation', LpMinimize)
    node = [[LpVariable('node%d-%d' % (i, x), cat = LpBinary) for x in range(n_node)] for i in range(n_resource)]
    load = [LpVariable('load%d' % x) for x in range(n_node)]
    node_traffic = [0] * n_node
    sum_load = 0

    for x in range(n_node):
        sum_load += load[x]

    #Objective
    prob += sum_load

    for i in range(n_resource):
        node_const = 0
        for x in range(n_node):
            node_const += node[i][x]
        prob += node_const == 1

    for x in range(n_node):
        for i in range(n_resource):
            node_traffic[x] += resource_traffic[i] * node[i][x]
        prob += node_traffic[x] <= capacity[x]
        prob += (3.0 / 2) * (node_traffic[x] * 1.0 / capacity[x]) <= load[x]
        prob += 3 * (node_traffic[x] * 1.0 / capacity[x]) - 1.0 / 2 <= load[x]
        prob += 6 * (node_traffic[x] * 1.0 / capacity[x]) - 2 <= load[x]
        prob += 15 * (node_traffic[x] * 1.0 / capacity[x]) - 8 <= load[x]
        prob += 50 * (node_traffic[x] * 1.0 / capacity[x]) - 36 <= load[x]

    status = GUROBI().solve(prob)
    loads = [value(load[x]) for x in range(n_node)]
    avg_load = sum(loads) * 1.0 / n_node
    print LpStatus[status], loads
    print avg_load
    logging.info('status %s avg_load %f' % (LpStatus[status], avg_load))
    logging.info('nodes load %s' % str(loads))
    for i in range(n_resource):
        for x in range(n_node):
            logging.info('node[%d][%d] = %d' % (i, x, value(node[i][x])))


if __name__ == "__main__":
    argvs = sys.argv
    argc = len(argvs)
    if argc != 4:
        print 'Usage: # python %s resource_traffic n_node log_file' % argvs[0]
        sys.exit()

    with open(argvs[1]) as resource_traffic_file:
        for line in resource_traffic_file:
            resource_traffic = map(float,line.strip().split(', '))
    n_resource = len(resource_traffic)
    n_node = int(argvs[2])
    capacity = [CAPACITY] * n_node
    logging.basicConfig(filename=argvs[3],level=logging.INFO)
    logging.info('resources traffic %s' % str(resource_traffic))

    cal(n_resource, n_node, capacity, resource_traffic)
