from .import node

class NodeCollection:
    def __init__(self):
        self.nodes = []
        self.count = 0

    def add(self, node):
        """
        Adds a node to the nodes list, will increment number of nodes
        """
        self.nodes.append(node)
        self.count += 1

    def find_node(self, node):
        """
        Accepts a node object as its parameter
        Returns index of node in NodeCollection object
        """
        for i in range(self.count):
            if node.name == self.nodes[i].name:
                return i

        return -1


    def __str__(self):
        """
        Override the string function to return all nodes in the collection
        """
        nodes = ""
        if self.count > 0:
            for n in self.nodes:
                nodes += str(n) + " "
            return nodes
        else:
            return "No Nodes."