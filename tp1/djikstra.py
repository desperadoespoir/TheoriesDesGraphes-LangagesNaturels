######################################################################
# Auteur : Obossou Ema-Wo, Billy Bouchard, Gnaga Dogbeda Georges
# Matricule: 1780896, 1850477, 1870143
# Version Python: 3.6
######################################################################
MAX = 100000


class DjikstraNode:
    ######################################################################
    # Custom made class to have every properties necessary in order
    # to make djikstra function work easily
    ######################################################################
    def __init__(self, startNode):
        self.weight = MAX if not startNode else 0
        self.fuel = 0 if not startNode else 100
        self.ancientNode = None
        self.ancientNodeIndex = None
        self.visited = False

    def set(self, weight, fuel, ancientNode, ancientNodeIndex):
        self.weight = weight
        self.fuel = fuel
        self.ancientNode = ancientNode
        self.ancientNodeIndex = ancientNodeIndex


class DjikstraNodeSolutionContainer:
    def __init__(self, node, startNode):
        self.node = node
        self.solutions = [DjikstraNode(startNode)]
        self.size = 1

    def __lshift__(self, solution):
        self.solutions.append(solution)
        self.size += 1
        return self

    def __iter__(self):
        for i in range(self.size):
            yield i

    def __getitem__(self, index):
        return self.solutions[index]


def djikstra(graph, startNodeId, endNodeId, fuelConsuption):
    ######################################################################
    # Algorith tht find the smallest path through a graph givn
    # a certain fuel consuption between startNodeId and endNodeId
    ######################################################################
    endNode = graph[endNodeId]
    nodes = {}
    for node in graph:
        nodes[node] = DjikstraNodeSolutionContainer(
            node, node.id == startNodeId)
    currentNode, currentNodeIndex = selectNextNode(nodes)
    while (currentNode != endNode):
        nodes = updateNodes(nodes, currentNode,
                            currentNodeIndex, endNode, fuelConsuption)
        currentNode, currentNodeIndex = selectNextNode(nodes)
        if not(currentNode):
            break
        if currentNode.station:
            nodes[currentNode][currentNodeIndex].fuel = 100
    return getSolution(nodes, currentNode, currentNodeIndex)


def selectNextNode(nodes):
    ######################################################################
    # This function select the next smallest weight node and returns
    # its type
    ######################################################################
    smallest = MAX
    smallestNode = None
    smallestNodeIndex = 0
    for node in nodes:
        for i in nodes[node]:
            if (nodes[node][i].weight < smallest and not(nodes[node][i].visited)):
                smallest = nodes[node][i].weight
                smallestNode = node
                smallestNodeIndex = i
    return smallestNode, smallestNodeIndex


def getSolution(nodes, endNode, endNodeIndex):
    ######################################################################
    # Functions take the nodes dictionnary and retrun the way to get to
    # the end node from the start node in a list
    ######################################################################
    solution = []
    if not(endNode):
        return []
    node = nodes[endNode]
    while True:
        solution.append(node.node)
        if not(node[endNodeIndex].ancientNode):
            break
        tempIndex = endNodeIndex
        endNodeIndex = node[endNodeIndex].ancientNodeIndex
        node = nodes[node[tempIndex].ancientNode]
    solution.reverse()
    return solution


def updateNodes(nodes, currentNode, currentNodeIndex, endNode, fuelConsuption):
    ######################################################################
    # This function update the nodes from the current node
    # it modify the weight of every node connecting to it
    ######################################################################
    nodesTime = currentNode.link()
    for node in nodesTime:
        weight = nodesTime[node] * 60 + \
            nodes[currentNode][currentNodeIndex].weight
        nodeFuel = nodes[currentNode][currentNodeIndex].fuel - \
            nodesTime[node] * fuelConsuption
        if nodeFuel < 0:
            weight = MAX
            nodeFuel = -1
        elif nodeFuel < 12 and (node != endNode) and not (node.station):
            weight = MAX
        if node.station:
            weight += 15
        for i in nodes[node]:
            if nodes[node][i].visited:
                continue
            if (nodes[node][i].weight > weight) and nodes[node][i].fuel <= nodeFuel:
                nodes[node][i].set(weight, nodeFuel,
                                   currentNode, currentNodeIndex)
            elif ((nodes[node][i].weight <= weight) and (nodes[node][i].fuel < nodeFuel)) \
                    or nodes[node][i].weight > weight:
                newSolution = DjikstraNode(False)
                newSolution.set(weight, nodeFuel,
                                currentNode, currentNodeIndex)
                nodes[node] << newSolution
    nodes[currentNode][currentNodeIndex].visited = True
    return nodes
