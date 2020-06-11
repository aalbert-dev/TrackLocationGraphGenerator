from PIL import Image, ImageDraw
from graphgen import graphgen as GraphGenerator
from searchgraph import searcher as Search
import sys

# track constraints in meters & radians
long_straightaway_length = 1006
long_straightaway_width = 15
short_straightaway_length = 201
short_straightaway_width = 15
turn_length = 402
turn_width = 18
turn_banking = 0.1606

# display constraints in pixels
origin = (500, 500)
grid_size = (1000, 1000)
max_point_distance = 350
bg_color = (0, 0, 0)

# car constraints in meters 
length = 5.12318
width = 1.9431
vector = (-1, 0)

# vehicle model constraints
racing_line_distance_weight = 40
vehicle_distance_weight = 10
car_vector_weight = 2000
occupancy_factors = 3
dispersion_rate = 1

# check if a point is within car bounding box
def pointInCarBox(point):
    return point[0] < length / 2 and point[0] > - length / 2 and point[1] < width / 2 and point[1] > - width / 2

# draw pixels
def fillPixels(img, locations):
    for point in locations:
        coordinate = addTuples(origin, point.position)
        if pointInCarBox(point.position): 
            point.occupancy = 1
        else:
            point.occupancy = max(min(getPointTotalOccupancy(coordinate) / occupancy_factors * dispersion_rate, 1), 0)
        drawPoint(img, coordinate, getColorFromOccupancy(point.occupancy))

# scale occupancy input factor between 0 - 1
def scaleFactor(minv, maxv, value):
    return (maxv - value) / maxv

# get distance from a point to the racing line
def getPointTotalOccupancy(point):
    line_distance_factor = scaleFactor(0, max_point_distance / 2, abs(point[1] - origin[1]))
    car_distance_factor = scaleFactor(0, max_point_distance * 2, distance(point, origin) * 2) 
    car_vector_factor = 1 - scaleFactor(0, max_point_distance * 2, origin[0] - point[0]) 
    return line_distance_factor + car_distance_factor + car_vector_factor

# calculate distance between points
def distance(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

# add 2-tuples
def addTuples(t1, t2):
    return (t1[0] + t2[0], t1[1] + t2[1])

# draw line
def drawLine(img, xy1, xy2, color):
    drawing = ImageDraw.Draw(img)
    drawing.line([xy1, xy2], fill=color, width=1)

# draw pixel on image
def drawPoint(img, xy, color):
    drawing = ImageDraw.Draw(img)
    drawing.point(xy, fill=color)

# convert occupancy to color, 1 = red (occupied), 0 = white (unoccupied)
def getColorFromOccupancy(occupancy):
    value = int(255 - (255 * occupancy))
    return (255, value, value)

# draw racing line as vector extending from car
def drawRacingLine(img):
    drawLine(img, (origin[0] - length / 2 - 10, origin[1]), (origin[0] - length / 2 + 10, origin[1]), (0, 255, 0))

# draw vehicle bounding box
def drawVehicle(img):
    drawLine(img, (origin[0] - length / 2, origin[1] - width / 2), (origin[0] + length / 2, origin[1] - width / 2), (0, 0, 235))
    drawLine(img, (origin[0] + length / 2, origin[1] - width / 2), (origin[0] + length / 2, origin[1] + width / 2), (0, 0, 235))
    drawLine(img, (origin[0] + length / 2, origin[1] + width / 2), (origin[0] - length / 2, origin[1] + width / 2), (0, 0, 235))
    drawLine(img, (origin[0] - length / 2, origin[1] + width / 2), (origin[0] - length / 2, origin[1] - width / 2), (0, 0, 235))
    drawRacingLine(img)

# draw vehicles path
def drawPath(img, locations):
    pather = Search(locations)
    tracePath(pather.path(), img)

# trace the minimum cost path
def tracePath(node, img):
    length = 0
    while node.prevNode:
        length += node.nodeDistance + 1.375 * node.prevNode.nodeDistance * (node.prevNode.occupancy + node.occupancy)
        drawLine(img, addTuples(node.position, origin), addTuples(node.prevNode.position, origin), (255, 255, 255))
        node = node.prevNode
    print("Total path length: " + str(length))

# change system default stack frame limit
sys.setrecursionlimit(10**6)
if sys.platform != "win32":
    import resource
    resource.setrlimit(resource.RLIMIT_STACK, (2**29,-1))

# create blank image
image = Image.new('RGB', grid_size, bg_color)

# create graph generator and generate nodes to represent locations
gg = GraphGenerator()

gg.addLocations()

# fill in pixels for each location in graph
fillPixels(image, gg.getLocations())

# draw vehicle bounding box
drawVehicle(image)

# draw example plan
drawPath(image, gg.getLocations())

# show image
image.show()