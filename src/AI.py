"""Neural network code."""

class Node(object):
    def __init__(self):
        self.input = 0

class Neural(object):
    def __init__(self, sizesornodes):
        self.net(sizesornodes)

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
                node.weights = [1 for i in range(sizes[layerIndex + 1])]
                # node.weights = [sizes[layerIndex + 1]]
        return node



    def each_node(self, visitoutput, callback, *args):
        num = 0 if visitoutput else 1
        lastlayer = len(self.nodes) - num
        for i in range(lastlayer):
            print('-------------------------------')
            print('now in layer', i)
            for j in range(len(self.nodes[i])):
                callback(self.nodes[i][j], i, j, self.nodes, *args)


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

    def _get_weights(self):
        to_return = []
        for i in range(len(self.nodes)):
            to_return.append([])
            for j in range(len(self.nodes[i])):
                try:
                    to_return[i].append(self.nodes[i][j].weights)
                except:
                    to_return[i].append([])
        return to_return

    def _get_thresholds(self):
        to_return = []
        for i in range(len(self.nodes)):
            to_return.append([])
            for j in range(len(self.nodes[i])):
                try:
                    to_return[i].append(self.nodes[i][j].threshold)
                except:
                    to_return[i].append(0)
        return to_return

    def _set_thresholds(self, thresholds):
        self.each_node(False, self._set_thresholds_callback, thresholds)

    def _set_thresholds_callback(self, node, layerIndex, index, nodes, thresholds):
            node.threshold = thresholds[layerIndex][index]

    def _set_weights(self, weights):
        self.each_node(False, self._set_weights_callback, weights)

    def _set_weights_callback(self, node, layerIndex, index, nodes, weights):
            node.weights = weights[layerIndex][index]
            print(weights[layerIndex][index])

    def reset(self):
        self.each_node(True, self._reset_callback)

    def _reset_callback(self, node, layerIndex, index, nodes):
        node.input = 0

    def set_inputs(self, inputs):
        for i in range(len(self.nodes[0])):
            self.nodes[0][i].input = inputs[i]

    def run(self, inputs):
        if inputs:
            self.set_inputs(inputs)
        self.each_node(False, self._run_callback)
        return self.get_outputs()

    def _run_callback(self, node, layerIndex, index, nodes):
        print('+++++++++++++++')
        print('node threshold', node.threshold)
        print('node input', node.input)
        print(layerIndex, index)
        # print('node weights', node.weights)
        if node.input >= node.threshold:
            for i in range(len(node.weights)):
                print('------')
                nodes[layerIndex + 1][i].input += node.weights[i] * node.input
                print('node', i, 'at layer', layerIndex + 1, 'now has input of', nodes[layerIndex + 1][i].input)

    def get_outputs(self):
        to_return = []
        for i in self.nodes[len(self.nodes) - 1]:
            to_return.append(i.input)
        return to_return

    def clone(self):
        return Neural(self.nodes)

    def export(self):
        return {
            'thresholds': self._get_thresholds(),
            'weights': self._get_weights()
        }

    def _import(self, data):
        net = Neural(self.get_sizes(data.thresholds))
        net._set_thresholds(data.thresholds)
        net._set_weights(data.weights)
        return net


if __name__ == '__main__':
    test = Neural([2,4,2])
    print(test._set_weights([[[1, 1, .5, 1], [0, 0, 0, 0]], [[1, 1], [1, 1], [1, 1], [4, 1]], [[], []]]
))
    print(test.run([1,1]))
