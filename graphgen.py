from tracknode import tracknode as Node
class graphgen:
    def __init__(self):
        self.list_of_nodes = []
        self.origin = (0, 0)
        self.max_distance = 350
        self.bound_function = lambda p: ((p[0] ** 2 + p[1] ** 2) ** 0.5) <= self.max_distance
        self.visited = []
        self.delta = 5

    # check if a location has already been generated for a location
    def checkLocation(self, point):
        return point in self.visited

    # directional node generation methods 
    def createNorthNode(self, previous_location):
        return Node((previous_location[0], previous_location[1] - self.delta))

    def createEastNode(self, previous_location):
        return Node((previous_location[0] + self.delta, previous_location[1]))

    def createSouthNode(self, previous_location):
        return Node((previous_location[0], previous_location[1] + self.delta))

    def createWestNode(self, previous_location):
        return Node((previous_location[0] - self.delta, previous_location[1]))

    # generate locaiton nodes using search method
    def addLocations(self):
        self.searchArea(Node(self.origin))

    # search available space as defined by bounding function on position
    def searchArea(self, curr_node):
        
        self.list_of_nodes.append(curr_node)
        self.visited.append(curr_node.position)

        p_north_node = self.createNorthNode(curr_node.position)
        if self.bound_function(p_north_node.position) and not self.checkLocation(p_north_node.position):
            curr_node.north = p_north_node
            self.searchArea(p_north_node)

        p_east_node = self.createEastNode(curr_node.position)
        if self.bound_function(p_east_node.position) and not self.checkLocation(p_east_node.position):
            curr_node.east = p_east_node
            self.searchArea(p_east_node)

        p_south_node = self.createSouthNode(curr_node.position)
        if self.bound_function(p_south_node.position) and not self.checkLocation(p_south_node.position):
            curr_node.south = p_south_node
            self.searchArea(p_south_node)

        p_west_node = self.createWestNode(curr_node.position)
        if self.bound_function(p_west_node.position) and not self.checkLocation(p_west_node.position):
            curr_node.west = p_west_node
            self.searchArea(p_west_node)

    # return location nodes
    def getLocations(self):
        return self.list_of_nodes





