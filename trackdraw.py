from PIL import Image, ImageDraw
import tracksim
from graphgen import graphgen as GraphGenerator
import resource, sys

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

# car constraints in meters 
length = 5.12318 * 10
width = 1.9431 * 10
vector = (-1, 0)

# vehicle model constraints
racing_line_distance_weight = 5
vehicle_distance_weight = 1
occupancy_over_distance_numerator = 200

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
            point.occupancy = occupancy_over_distance_numerator / distanceToLine(coordinate)
        drawPoint(img, coordinate, getColorFromOccupancy(point.occupancy))

# get distance from a point to the racing line
def distanceToLine(point):
    line_distance =  abs(point[1] - origin[1]) * racing_line_distance_weight
    car_distance = distance(point, origin) * vehicle_distance_weight
    return line_distance + car_distance

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
    drawLine(img, origin, (origin[0]- 200, origin[1]), (0, 0, 235))

# draw vehicle bounding box

# change system default stack frame limit
sys.setrecursionlimit(10**6)
resource.setrlimit(resource.RLIMIT_STACK, (2**29,-1))

# create blank image
image = Image.new('RGB', (1000, 1000))

# create graph generator and generate nodes to represent locations
gg = GraphGenerator()

gg.addLocations()

# fill in pixels for each location in graph
fillPixels(image, gg.getLocations())

# draw line to represent racing line
# drawRacingLine(image)

# draw vehicle bounding box
drawVehicle(image)

# show image
image.show()