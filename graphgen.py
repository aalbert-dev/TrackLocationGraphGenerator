from tracknode import tracknode as Node
class graphgen:
    def __init__(self):
        self.list_of_nodes = []
        self.origin = (0, 0)
        self.max_distance = 250
        self.bound_function = lambda p: ((p[0] ** 2 + p[1] ** 2) ** 0.5) <= self.max_distance
        self.visited = []
        self.delta = 5

    # check if a location has already been generated for a location
    def checkLocation(self, point):
        return point in self.visited
    
    # add delta in direction to position tuple
    def northPosition(self, position):
        return (position[0], position[1] - self.delta)

    def eastPosition(self, position):
        return (position[0] + self.delta, position[1])
    
    def southPosition(self, position):
        return (position[0], position[1] + self.delta)

    def westPosition(self, position):
        return (position[0] - self.delta, position[1])

    # directional node generation methods 
    def createNorthNode(self, previous_location):
        return Node(self.northPosition(previous_location), self.delta)

    def createEastNode(self, previous_location):
        return Node(self.eastPosition(previous_location), self.delta)

    def createSouthNode(self, previous_location):
        return Node(self.southPosition(previous_location), self.delta)

    def createWestNode(self, previous_location):
        return Node(self.westPosition(previous_location), self.delta)

    # generate locaiton nodes using search method
    def addLocations(self):
        self.searchArea(Node(self.origin, self.delta))
        self.repairConnections()

    # search available space as defined by bounding function on position
    def searchArea(self, curr_node):
        
        self.list_of_nodes.append(curr_node)
        self.visited.append(curr_node.position)

        p_north_node = self.createNorthNode(curr_node.position)
        if self.bound_function(p_north_node.position) and not self.checkLocation(p_north_node.position):
            curr_node.north = p_north_node
            p_north_node.south = curr_node
            self.searchArea(p_north_node)

        p_east_node = self.createEastNode(curr_node.position)
        if self.bound_function(p_east_node.position) and not self.checkLocation(p_east_node.position):
            curr_node.east = p_east_node
            p_east_node.west = curr_node
            self.searchArea(p_east_node)

        p_south_node = self.createSouthNode(curr_node.position)
        if self.bound_function(p_south_node.position) and not self.checkLocation(p_south_node.position):
            curr_node.south = p_south_node
            p_south_node.north = curr_node
            self.searchArea(p_south_node)

        p_west_node = self.createWestNode(curr_node.position)
        if self.bound_function(p_west_node.position) and not self.checkLocation(p_west_node.position):
            curr_node.west = p_west_node
            p_west_node.east = curr_node
            self.searchArea(p_west_node)

    # repaid connections by looking at current node position and bounding function
    # to add adjacent nodes to direction fields
    def repairConnections(self):
        for node in self.list_of_nodes:
            self.addConnections(node)

    # check/add directional fields to hold edges between nodes
    def addConnections(self, node):

        # for each direction check if bounds allow neighbor and if neighbor exists
        # then add pointer to neighbor if needed
        north_pos = self.northPosition(node.position)
        if not node.north and self.bound_function(north_pos):
            node.north = self.findNode(north_pos)
        
        east_pos = self.eastPosition(node.position)
        if not node.east and self.bound_function(east_pos):
            node.east = self.findNode(east_pos)

        south_pos = self.southPosition(node.position)
        if not node.south and self.bound_function(south_pos):
            node.south = self.findNode(south_pos)

        west_pos = self.westPosition(node.position)
        if not node.west and self.bound_function(west_pos):
            node.west = self.findNode(west_pos)

    # find a node with specified position
    def findNode(self, position):
        for node in self.list_of_nodes:
            if node.position == position:
                return node
        return None

    # return location nodes
    def getLocations(self):
        return self.list_of_nodes