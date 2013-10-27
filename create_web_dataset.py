import sys

from generate_data import traffic_generate

argvs = sys.argv
argc = len(argvs)
if argc != 8:
    print 'Usage: # python %s (int)n_path (float)avg_traffic (float)sigma (float)traffic_quota (int)n_bare resource_traffic_file resource_node_file' % argvs[0]
    sys.exit()

n_path = int(argvs[1])
avg_traffic = float(argvs[2])
sigma = float(argvs[3])
traffic_quota = float(argvs[4])
n_bare = int(argvs[5])
n_resource = 4 * n_path
web_traffic = traffic_generate(n_path, avg_traffic, sigma, traffic_quota, n_bare)
web_traffic_dataset = web_traffic.get_web()
f = lambda j: 1 if (i < n_path) & (j == 0) else 0
web_node_dataset = [[f(j) for j in range(n_bare)] for i in range(n_resource)]

print web_traffic_dataset
print web_node_dataset

resource_traffic_file = open(argvs[6], 'w')
resource_node_file = open(argvs[7], 'w')
for i in range(n_resource):
    for j in range(n_resource):
        resource_traffic_file.write(str(web_traffic_dataset[i][j]))
        if j < n_resource - 1:
            resource_traffic_file.write(', ')
    resource_traffic_file.write('\n')
    
    for j in range(n_bare):
        resource_node_file.write(str(web_node_dataset[i][j]))
        if j < n_bare - 1:
            resource_node_file.write(', ')
    resource_node_file.write('\n')

resource_traffic_file.close()
resource_node_file.close()
