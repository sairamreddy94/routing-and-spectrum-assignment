import sys


def getCompletePath(p):
    complete_path = list(p['path'])
    if p['parent'] != None:
        dev_node = p['dev_node']
        while p['parent'] != None:
            parent = p['parent']
            stop_index = parent['path'].index(dev_node)
            parent_path = list(parent['path'][:stop_index])
            complete_path = parent_path + complete_path
            dev_node = parent['dev_node']
            p = parent
        stop_index = p['path'].index(dev_node)
        final_path = list(p['path'][:stop_index])
        complete_path = final_path + complete_path
    return complete_path


def printDistictPaths(paths):
    dist_paths= list()
    edges_used = set()
    k = 0
    for p in paths:
        distict_path = list()
        k += 1
        cost = p['cost']
        complete_path = getCompletePath(p)
        temp_edges = []
        for i in range(len(complete_path) - 1):
            v1, v2 = complete_path[i], complete_path[i + 1]
            if (v1, v2) not in edges_used:  # i.e if edge is not used
                distict_path.append((int(v1) + 1, int(v2) + 1))
                temp_edges.append((v1, v2))
                temp_edges.append((v2, v1))
            else:
                distict_path.clear()
                break  # edges are already path of some previously used path

        if len(distict_path) > 0:
            edges_used.update(temp_edges)
            path_list = []
            dist_paths.append({"path": distict_path, 'cost': cost, 'hops': str(len(distict_path))})
            del (distict_path)
            del (temp_edges)
        else:
            del (distict_path)
            del (temp_edges)
    return dist_paths

def printPaths(paths):
    # node_used = [[False] * num_nodes for i in range(num_nodes)]
    k = 0
    kpaths=[]
    for p in paths:
        k += 1
        cost = p['cost']
        complete_path = getCompletePath(p)
        complete_path = [el+1 for el in complete_path]
        list = [(complete_path[i], complete_path[i + 1]) for i in range(len(complete_path)-1)]
        # line = 'path: {}'  'Cost:' {}  'hops:{}'.format(str(list), str(cost),str(len(complete_path)-1))
        kpaths.append({"path": list, 'cost': cost, 'hops': str(len(list))})
    return kpaths

def getGraphStructure(file_name):
    if file_name.find('/') == -1:  # I go to look for the file in the test folder, so if the folder is not shown
        directory = 'test/'  # I add it to him
        file_name = directory + file_name
    try:
        graph_file = open(file_name, 'rt')
    except Exception as ex:
        sys.exit(ex)
    num_nodes = int(graph_file.readline())  # The first line of each file contains the number of nodes in the graph
    num_arcs = 0
    graph_matrix = [[float('inf')] * num_nodes for i in range(num_nodes)]
    id = [['-'] * (num_nodes+1) for i in range(num_nodes+1)]
    graph_file.readline()  # The second line of the file must be empty

    for line in graph_file:
        num_arcs += 1
        head, tail, cost = line.split(' ')

        head = int(head)  # Decrease because in the data structure the nodes start at 0
        tail = int(tail)

        #Assign id to each edges
        id[head][tail] = str((head, tail))
        id[tail][head] = str((head, tail))


        head = head - 1  # Decrease because in the data structure the nodes start at 0
        tail = tail - 1


        cost = float(cost)

        graph_matrix[head][tail] = cost
        graph_matrix[tail][head] = cost
    graph_file.close()

    for n in range(num_nodes):
        graph_matrix[n] = tuple(graph_matrix[n])  # I create tuples so I can be sure I do not change the data structure
    return graph_matrix, num_nodes, num_arcs, id
