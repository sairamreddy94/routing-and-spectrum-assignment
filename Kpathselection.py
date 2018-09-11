from yen import YenAlgorithm
import numpy as np,hashlib,sys,tools

class Kpathselection():


    def __init__(self, s, t):
        self.s = s
        self.t = t

    def YenKpath(self):
        """this computes the k shortest paths and the disjoint paths"""
        kpath_list = []
        file_name = './test/nsfnet.txt'
        self.graph, self.num_nodes, self.num_arcs, id = tools.getGraphStructure(file_name)
        while True:
            K = 5  #int(input('Enter the number of paths to search: '))

            if K == 0:
                sys.exit('No path required ... Goodbye!')

            if self.s == self.t or not 1 <= self.s <= self.num_nodes or not 1 <= self.t <= self.num_nodes or K < 0:
                print('WARNING! Recheck the entered values. We remind you that '
                      'the source node and the well node must be different and K> 0'
                      '(K=0 to exit).')
            else:
                break
        shortest_path_tree = YenAlgorithm(self.graph, self.s - 1, self.t - 1,K)  # Decrease the nodes of one because in the data structure the nodes start at 0

        if shortest_path_tree:
            kpaths = tools.printPaths(shortest_path_tree)
            for k in kpaths:
                kpath_list.append(k)                 # these are the k shortest paths
            for kpaths1 in kpath_list:
                print("this is k shortest paths",kpaths1)
            self.dist_path = tools.printDistictPaths(shortest_path_tree)
            for path in self.dist_path:
                print("disjoint path \t{}\t distance: {}\t hops: {}".format(path['path'], path['cost'], path['hops']))
        else:
            print('No path between the source and the well node!')
        return kpath_list,self.graph
        # return self.dist_path,self.graph


    def getPath(self,path_list):
        for value,path in enumerate(path_list,start=1):
            value =1 #np.random.randint(0, len(path_list))          # selecting a randon path from the k paths
            costOfLink = path_list[value]['cost']
            hops = path_list[value]['hops']
            return path_list[value],value,costOfLink,hops

    def path_id(self,path_get):
        for value in self.dist_path:        #trying to create path ids for the topology
            result = hashlib.md5(str(value['path']).encode()).hexdigest()
            if value["path"] == path_get:
                return result

    def path_class(self):
            self.path_contents = {"route":0,"id":0,"source":0,"destination":0,"weight":0,"cost":0,"hops":0,"number_of_slots":0}
            return self.path_contents


    def updatepath(self,parameter_list, amount_list):           # used for assigning things which are constant
        for i in range(len(parameter_list)):
            self.path_contents[parameter_list[i]] = amount_list[i]


