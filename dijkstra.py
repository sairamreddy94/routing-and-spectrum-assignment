def getPath(pred, n, s):
    path = None
    if pred[n] != None:
        path = [n]
        while pred[n] != s:
            path.insert(0, pred[n])
            n = pred[n]
        path.insert(0, s)
    return path

def search(Q, n):
    for d, j in Q:
        if n == j:
            return True
    return False

def insert(Q, n):
    length = len(Q)
    if not Q:
        Q.append(n)
    elif Q == 1:
        if n[0] <= Q[0][0]:
            Q.insert(0, n)
        else:
            Q.append(n)
    else:
        s = length//2
        if n[0] == Q[s][0]:
            Q.insert(s, n)
        elif n[0] > Q[s][0]:
            r = insert(Q[s+1:], n)
            Q = Q[:s+1] + r
        else:
            r = insert(Q[:s], n)
            Q = r + Q[s:]
    return Q

def DijkstraAlgorithm(graph, s, t=-1):
    """Dijkstra's algorithm allows you to calculate what it is
        the TREE of the minimum paths from a node s, called the root node"""

    num_nodes = len(graph)
    queue = [(0, s)]
    d = [float('inf')]*num_nodes
    pred = [None]*num_nodes
    d[s] = 0
    pred[s] = s

    while queue:
        n = queue.pop(0)
        i = n[1]
        for j in range(num_nodes):
            if graph[i][j] != float('inf'):
                if d[i] + graph[i][j] < d[j]:
                    pred[j] = i
                    d[j] = d[i] + graph[i][j]
                    if not search(queue, j):
                        queue = insert(queue, (d[j], j))

    #At the end I will have found the vector pred and d (of the #durations)
    if t != -1:
        path = getPath(pred, t, s)
        if path != None:
            path = tuple(path)
        return path, d[t]
    else:
        paths = []
        for n in range(num_nodes):
            if pred[n] == None:
                path = None
            else:
                path = getPath(pred, n, s)
            paths.append(path)

        graph_matrix = [[float('inf')]*num_nodes for i in range(num_nodes)]
        for path in paths:
            if path != None:
                while len(path) > 1:
                    head = path.pop(0)
                    tail = path[0]
                    graph_matrix[head][tail] = graph[head][tail]

        return graph_matrix, d, pred