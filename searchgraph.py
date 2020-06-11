import heapq
class searcher:
    def __init__(self, node_list):
        self.nodes = node_list
        self.visited = []

    # example method to select nodes to use as start/end points
    def getMaxXnodes(self):
        leftNode = min(self.nodes, key=lambda x: x.position[0])
        rightNode = max(self.nodes, key=lambda x: x.position[0])
        return (leftNode, rightNode)

    # example test path
    def path(self):
        l, r = self.getMaxXnodes()
        return self.minPath(l, r)
    
    # find minimum distance path between two nodes
    def minPath(self, start, end):
        self.dijkstra(start, end)
        return end

    # get the weight of an edge between two nodes by averaging the 
    # oppacities * distance between each node
    def getEdgeWeight(self, node1, node2):
        return node1.nodeDistance + 1 * node2.nodeDistance * (node1.occupancy + node2.occupancy)
 
    # dijkstra style minimum path method
    def dijkstra(self, start, end):

        # set initial distance to each node to be max int
        start.distanceTo = 0
        for node in self.nodes:
            heapq.heappush(self.visited, node)
        
        # relax each edge adjacent to the current node until all nodes have a minimum distance
        while True:
            curr_node = heapq.heappop(self.visited)
            value = curr_node.distanceTo

            if curr_node == end: break

            if curr_node.north:
                north_distance = self.getEdgeWeight(curr_node, curr_node.north)
                new_distance = value + north_distance

                if new_distance < curr_node.north.distanceTo:
                    self.decreaseNodeValue(curr_node.north, new_distance)
                    curr_node.north.prevNode = curr_node

            if curr_node.east:
                east_distance = self.getEdgeWeight(curr_node, curr_node.east)
                new_distance = value + east_distance

                if new_distance < curr_node.east.distanceTo:
                    self.decreaseNodeValue(curr_node.east, new_distance)
                    curr_node.east.prevNode = curr_node

            if curr_node.south:
                south_distance = self.getEdgeWeight(curr_node, curr_node.south)
                new_distance = value + south_distance

                if new_distance < curr_node.south.distanceTo:
                    self.decreaseNodeValue(curr_node.south, new_distance)
                    curr_node.south.prevNode = curr_node

            if curr_node.west:
                west_distance = self.getEdgeWeight(curr_node, curr_node.west)
                new_distance = value + west_distance
                
                if new_distance < curr_node.west.distanceTo:
                    self.decreaseNodeValue(curr_node.west, new_distance)
                    curr_node.west.prevNode = curr_node

    def decreaseNodeValue(self, node, newValue):
        node.distanceTo = newValue
        heapq.heapify(self.visited)