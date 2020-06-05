from PIL import Image, ImageDraw
import tracksim
from graphgen import graphgen as GraphGenerator
import resource, sys

# constraints in meters & radians
long_straightaway_length = 1006
long_straightaway_width = 15
short_straightaway_length = 201
short_straightaway_width = 15
turn_length = 402
turn_width = 18
turn_banking = 0.1606
origin = (500, 500)

# draw pixels
def fillPixels(img, locations):
    for point in locations:
        coordinate = addTuples(origin, point.position)
        drawPoint(img, coordinate, (255, 255, 255))

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

# change default stack limit
sys.setrecursionlimit(10**6)
resource.setrlimit(resource.RLIMIT_STACK, (2**29,-1))

# create blank image
image = Image.new('RGB', (1000, 1000))

# create graph generator and generate nodes to represent locations
gg = GraphGenerator()

gg.addLocations()

# fill in pixels for each location in graph
fillPixels(image, gg.getLocations())

# show image
image.show()