from functools import total_ordering
@total_ordering
class tracknode:
    def __init__(self, position, distance):

        # occupancy represents probability of vehicle at this node
        self.occupancy = 0

        # directional edges
        self.north = None
        self.north_east = None
        self.east = None
        self.south_east = None
        self.south = None
        self.south_west = None
        self.west = None
        self.north_west = None

        # position relative to track origin
        self.position = position

        # distance between nodes
        self.nodeDistance = distance

        # hold previous node for dijkstra search
        self.prevNode = None

        # distance to this node from origin
        self.distanceTo = 9999999

    # comparison methods
    def __eq__(self, other):
        return self.distanceTo == other.distanceTo

    def __gt__(self, other):
        return self.distanceTo > other.distanceTo
