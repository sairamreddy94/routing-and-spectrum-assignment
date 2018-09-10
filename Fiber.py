import numpy as np,sys

#Assumin that the central frequency is at location 284
# so to get the indices around this central frequency use: index= index - central_index
class Fiber():
    def __init__(self, graph,path_list):
        self.graph = graph
        self.path_list = path_list
        self.ids = {}
        self.max_spectrum = 4850
        np.set_printoptions(threshold=np.inf)

    def initiateEdges(self):
        intialfreq = self.generateFreqWav()
        for i in range(len(self.graph)):
            for j in range(i + 1, len(self.graph)):
                if i != j and self.graph[i][j] != float('inf'):
                    self.ids[((i + 1, j + 1))] = {"id": (i + 1, j + 1), "slots_occupied":[],"slots_sum":0,"unused_slots":769,"total_spec":0,"unused_spec":4850,'array':0,'used_spec': [],"spec_occupied":[]}  # assigning ids
                    self.ids[((j + 1, i + 1))] = {"id": (i + 1, j + 1), "slots_occupied":[],"slots_sum":0,"unused_slots":769,"total_spec":0,"unused_spec":4850,'array': 0,'used_spec': [],"spec_occupied":[]}

        return self.ids


    def getId(self, edge):
        return self.ids[(edge[0],edge[1])]['id']

    def getCompleteedgeId(self, path):
        path_id= []
        for edge in path:
            path_id.append(self.getId(edge))
        return path_id

    def updateSpectrum(self,edge,usedSpec):
        self.ids[edge]['used_spec'] += usedSpec             # assigning cost to node 1 and node 2
        self.ids[(edge[1], edge[0])]['used_spec'] += usedSpec

    def updateLink1(self,edge,parameter_list, amount_list):
        for i in range(len(parameter_list)):
            self.ids[edge][parameter_list[i]] += [amount_list[i]]  # assigning cost to node 1 and node 2
            self.ids[(edge[1], edge[0])][parameter_list[i]] += [amount_list[i]]

    def updateLink2(self, edge, parameter_list,amount_list):   # used for assigning things which are summed up
        for i in range(len(parameter_list)):
            self.ids[edge][parameter_list[i]] += amount_list[i]
            self.ids[(edge[1], edge[0])][parameter_list[i]] += amount_list[i]

    def updateLink4(self, edge, parameter_list, amount_list, value):  # used for assigning things which are subtracted
        for i in range(len(parameter_list)):
            self.ids[edge][parameter_list[i]] -= amount_list[i]
            self.ids[(edge[1], edge[0])][parameter_list[i]] -= amount_list[i]

    def updateLink3(self, edge, parameter_list, amount_list):           # used for assigning things which are constant
        for i in range(len(parameter_list)):
            self.ids[edge][parameter_list[i]] = amount_list[i]
            self.ids[(edge[1], edge[0])][parameter_list[i]] = amount_list[i]


    def spectrumLeftOut(self,specoccupied):
        return self.max_spectrum - specoccupied

    def check_availability(self,edge, amount):
        freq= self.ids[(edge)]["array"]


    def generateFreqWav(self):
        base_freq = 191.325e12
        freq = []
        new_freq = base_freq
        while new_freq <= 196.125e12:
            freq.append(np.round((new_freq), 4))
            new_freq += 0.00625e12
        freq = np.round(np.array(freq) / 1e12, 4)
        freq_all = (freq).reshape(1, -1)  # frequency generated from 191.2-196.1
        freq_all = np.vstack((freq_all, np.zeros((1, freq_all.shape[1]), dtype=bool)))
        Lambda = np.round(((2.99792458e8 / freq) / 1e3), 4).reshape(1, -1)
        freq_all = np.vstack((freq_all, Lambda))
        self.freq_array =freq_all
        return freq_all


    def assignPath(self):
        if len(self.path_list) == 0:
            sys.exit("No path available... Visit again !!!!")
        #print(self.path_list)
        for path in self.path_list:
            pass


'''
    def spectrumAvailable(self, link_id):
        pass
        return self.max_spectrum - self.ids[link_id]['used_spec']
'''