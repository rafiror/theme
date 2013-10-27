import random

class traffic_generate:
    
    def __init__(self, n_path, avg_traffic, sigma, traffic_quota, n_bare):
        self.n_path = n_path
        self.avg_traffic = avg_traffic
        self.sigma = sigma
        self.traffic_quota = traffic_quota
        self.n_bare = n_bare
    
    def get_web(self):
        traffic = [random.lognormvariate(self.avg_traffic, self.sigma) for i in range(self.n_path)]
        sum_traffic = sum(traffic)
        traffic_coefficient = self.traffic_quota / sum_traffic
        adjust_traffic = [traffic[i] * traffic_coefficient for i in range(self.n_path)]
        n_resource = 4 * self.n_path
        resource_traffic = [[0 for j in range(n_resource)] for i in range(n_resource)]
        router_start_resource = self.n_path
        lb_start_resource = 2 * self.n_path
        fw_start_resource = 3 * self.n_path
        for i in range(self.n_path):
            #vm traffic output
            resource_traffic[i][router_start_resource + i] = adjust_traffic[i]
            #router traffic input,output
            resource_traffic[router_start_resource + i][i] = adjust_traffic[i]
            resource_traffic[router_start_resource + i][lb_start_resource + i] = adjust_traffic[i]
            #lb traffic input,output
            resource_traffic[lb_start_resource + i][router_start_resource + i] = adjust_traffic[i]
            resource_traffic[lb_start_resource + i][fw_start_resource + i] = adjust_traffic[i]
            #fw traffic input
            resource_traffic[fw_start_resource + i][lb_start_resource + i] = adjust_traffic[i]

        return resource_traffic
