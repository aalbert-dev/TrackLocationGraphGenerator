class tracknode:
    def __init__(self, position):

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
