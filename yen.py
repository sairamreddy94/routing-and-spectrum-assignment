from dijkstra import DijkstraAlgorithm
import tools

def restoreArc(v, path, graph, temp):
    v_s  = path[path.index(v) + 1]
    temp[v][v_s] = graph[v][v_s]
    return graph[v][v_s], v_s

def insert(X, p):
    length = len(X)
    if not X:
        X.append(p)
    elif X == 1:
        if p['cost'] <= X[0]['cost']:
            X.insert(0, p)
        else:
            X.append(p)
    else:
        s = length//2
        if p['cost'] == X[s]['cost']:
            X.insert(s, p)
        elif p['cost'] > X[s]['cost']:
            r = insert(X[s+1:], p)
            X = X[:s+1] + r
        else:
            r = insert(X[:s], p)
            X = r + X[s:]
    return X

def correctLabelsOf(v, pi, pred, graph, pk, num_nodes, complete_path):
    q = [v]
    index = complete_path.index(v)
    while q:
        i = q.pop(0)
        for j in range(num_nodes):
            if not j in complete_path[:index]:
                if graph[j][i] != float('inf'):
                    if pi[j] > pi[i] + graph[j][i]:
                        pi[j] = pi[i] + graph[j][i]
                        pred[j] = i
                        #if not j in q:
                        q.append(j)

def getCost(complete_path, v, graph, pc):
    pk_cost = 0
    while complete_path[0] != v:
        head = complete_path.pop(0)
        tail = complete_path[0]
        pk_cost += graph[head][tail]

    return pk_cost + pc

def getPath(v, pred, t):
    path = [v]
    while pred[v] != t:
        path.append(pred[v])
        v = pred[v]
    path.append(t)
    return tuple(path)

def calculateForwardStarForm(v, graph, pi, pred, num_nodes):
    for j in range(num_nodes):
        if graph[v][j] != float('inf'):
            if pi[v] > pi[j] + graph[v][j]:
                pi[v] = pi[j] + graph[v][j]
                pred[v] = j 

def restoreNode(v, temp, graph, paths, t, num_nodes, complete_path):
    pk = paths[-1]
    dev_node = pk['dev_node']
    i = complete_path.index(v)
    for j in range(num_nodes):
        if not j in complete_path[:i]:
            temp[v][j] = graph[v][j]
            temp[j][v] = graph[j][v]
    if v == dev_node:
        removeArcsOfPk(temp, paths, t)
    temp[v][complete_path[i+1]] = float('inf')

def transpose(matrix, num_nodes):
    tm = []
    for i in range(num_nodes):
        row = []
        for j in range(num_nodes):
            row.append(matrix[j][i])
        tm.append(row)

    return tm

def removeArcsOfPk(graph, shortestLooplessPaths, t):
    pk = shortestLooplessPaths[-1]
    pk_path = tools.getCompletePath(pk)
    dev_node = pk['dev_node']
    dev_node_index = pk_path.index(dev_node)
    for p in shortestLooplessPaths[:-1]:
        try:
            complete_path = tools.getCompletePath(p)
            i = complete_path.index(dev_node)
            if pk_path[:dev_node_index] == complete_path[:i]:
                j = complete_path[i+1]
                graph[dev_node][j] = float('inf')
        except ValueError as ex:
            pass

def removeLooplessPath(graph, complete_path, num_nodes):
    for node in complete_path[:-1]:
        for j in range(num_nodes):
            graph[node][j] = float('inf')
            graph[j][node] = float('inf')

def getAuxGraph(graph):
    return [list(row) for row in graph]

def YenAlgorithm(graph, s, t, K):
    """The Yen algorithm is an algorithm designed for oriented, heavy and graphs
    without negative cost cycles to determine the minimum K paths between a node
    source s and a destination node t"""

    num_nodes = len(graph)
    shortestLooplessPaths = []

    path, cost = DijkstraAlgorithm(graph, s, t)
    if path != None:
        X = [{'dev_node': s, 'path': path, 'parent': None, 'cost': cost}]
        k = 0

        log = open('log.txt', 'wt')

        while X and k<K-1:
            k = k + 1
            pk = X.pop(0)
            shortestLooplessPaths.append(pk)
            pk_complete_path = tools.getCompletePath(pk)
            aux_graph = getAuxGraph(graph)
            removeLooplessPath(aux_graph, pk_complete_path, num_nodes)
            #removeArcsOfPk(aux_graph, shortestLooplessPaths, t)

            aux_graph, pi, pred = DijkstraAlgorithm(transpose(aux_graph, num_nodes), t) # Pi is the vector of the costs of the tree of the minimum paths with root in t
            aux_graph = transpose(aux_graph, num_nodes)        

            for v in reversed(pk['path'][:-1]):
                restoreNode(v, aux_graph, graph, shortestLooplessPaths, t, num_nodes, pk_complete_path)
                calculateForwardStarForm(v, aux_graph, pi, pred, num_nodes)
                if pi[v] != float('inf'):
                    correctLabelsOf(v, pi, pred, graph, pk, num_nodes, pk_complete_path)
                    p = {'dev_node': v, 'path': getPath(v, pred, t), 'parent': pk, 'cost': getCost(pk_complete_path[:], v, graph, pi[v])}
                    X = insert(X, p)
                
                cost, v_s = restoreArc(v, pk['path'], graph, aux_graph)
                if pi[v] > pi[v_s] + cost:
                    pi[v] = pi[v_s] + cost
                    pred[v] = v_s
                    correctLabelsOf(v, pi, pred, graph, pk, num_nodes, pk_complete_path)

        if X:
            pk = X.pop(0)
            shortestLooplessPaths.append(pk)

        log.close()

    return shortestLooplessPaths
