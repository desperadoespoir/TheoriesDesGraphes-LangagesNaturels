######################################################################
# Auteur : Obossou Ema-Wo, Billy Bouchard, Gnaga Dogbeda Georges
# Matricule: 1780896, 1850477, 1870143
# Version Python: 3.6
######################################################################


class Node:
    def __init__(self, id, hasStation):
        self.station = hasStation
        self.arcs = []
        self.id = id

    def __lshift__(self, arc):
        ######################################################################
        # Operator << overloading to add item to the graph
        # return self is for cascade
        ######################################################################
        self.arcs.append(arc)
        return self

    def __str__(self):
        ######################################################################
        # Overload the str() function for printing
        ######################################################################
        return str(self.id) + ". " + str(self.station) + ": " + reduce(lambda x, y: x + ", " + y, map(lambda x: str(x), self.arcs))

    def __hash__(self):
        ######################################################################
        # Hash the id because its unique so that a node can be a dictionnary
        # key
        ######################################################################
        return hash(self.id)

    def link(self):
        ######################################################################
        # Return all the other Node connected to this node and the time
        # to get there
        ######################################################################
        nodeTime = {}
        for arc in self.arcs:
            nodeTime[arc[self]] = arc.time
        return nodeTime

    def __eq__(self, other):
        ######################################################################
        # With the same Id it's the same node since ids are unique
        ######################################################################
        return self.id == other.id


class Arc:
    def __init__(self, time, node1, node2):
        self.time, self.node1, self.node2 = time, node1, node2
        node1 << self
        node2 << self

    def __str__(self):
        ######################################################################
        # Overload the str() function for printing
        ######################################################################
        return "(" + str(self.node1.id) + "--" + str(self.node2.id) + " :" + str(self.time) + ")"

    def __getitem__(self, node):
        ######################################################################
        # Return the other node than the one given with [] operator
        # else return None
        ######################################################################
        if node != self.node1 and node != self.node2:
            return None
        return self.node2 if self.node1 == node else self.node1


class Graph:
    def __init__(self):
        self.arcs = []
        self.nodes = {}
        self.current_node = 0

    def __lshift__(self, elem):
        ######################################################################
        # Add << operator to add arc or node to their respective array
        # self return is for cascade
        ######################################################################
        if isinstance(elem, Node):
            self.nodes[elem.id] = elem
        elif isinstance(elem, Arc):
            self.arcs.append(elem)
        return self

    def __getitem__(self, nodeId):
        ######################################################################
        # return a node from a node id with [] operator
        ######################################################################
        return self.nodes[nodeId]

    def __iter__(self):
        ######################################################################
        # let us iterate trough nodes with 'for in' opertator
        ######################################################################
        for nodeId in self.nodes:
            yield self.nodes[nodeId]

    def findArcTime(self, node1, node2):
        ######################################################################
        # Return the time to get from node1 to node2 if both are connected
        ######################################################################
        for arc in self.arcs:
            if (arc.node1 == node1 or arc.node2 == node1) and (arc.node1 == node2 or arc.node2 == node2):
                return arc.time
        return None
