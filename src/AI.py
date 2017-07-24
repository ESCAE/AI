"""Neural network code."""

class Node(object):
    def __init__(self):
        self.input = 0

class Neural(object):
    def __init__(self):
        pass
    def get_sizes(self, nodes):
        """Returns the amount of nodes in each layer."""
        return list(map(lambda x: len(x), nodes))


    def make_node(self, layerIndex, index, sizes, nodes=None):
        node = Node()
        if layerIndex < len(sizes) - 1:
            try:
                node.threshold = nodes[layerIndex][index].threshold
            except:
                node.threshold = 1
        try:
            node.weights = map(lambda x: x, nodes[layerIndex][index].weights)
        except:
            try:
                node.weights = [sizes[layerIndex + 1]]
            except:
                node.weights = 'no node weights'
        return node


    def net(self, sizesornodes):
        sizes = []
        nodes = []
        if type(sizesornodes[0]) == list:
            sizes = self.get_sizes(sizesornodes)
            nodes = sizesornodes
        else:
            sizes = sizesornodes
        self.nodes = []
        for i in range(len(sizes)):
            self.nodes.append([])
            for j in range(sizes[i]):
                self.nodes[i].append(self.make_node(i, j, sizes, nodes))
        return self.nodes
        



if __name__ == '__main__':
    test = Neural()
    thing = test.net([[1,2,3],[1,2,3],[1,2,3],[1,2,3]])
    for i in thing:
        for j in i:
                try:
                    print('--------')
                    print(j.threshold)
                    print(j.weights)
                except:
                    print('--------')
                    print(j.weights)
