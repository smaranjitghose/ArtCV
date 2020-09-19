# Import the dependencies
from PIL import Image, ImageDraw, ImageFilter
from scipy.spatial import Delaunay
import random
import argparse
from tqdm import tqdm
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
args = vars(ap.parse_args())

# reading the image
img = Image.open((args["image"]))

n = 1000
rows, cols = img.size
cpy = img.copy()
cpy = cpy.convert('L')
cpy = cpy.filter(ImageFilter.FIND_EDGES)
cpy = cpy.convert('1')
pix = cpy.load()
vertices = []
for i in range(rows):
	for j in range(cols):
	    WHITE = 255
	    if pix[i, j] == WHITE:vertices.append((i, j))

random.shuffle(vertices)
vertices = vertices[:n]

vertices.append((0, 0))
vertices.append((0, cols - 1))
vertices.append((rows - 1, 0))
vertices.append((rows - 1, cols - 1))

triangulation = Delaunay(vertices)

draw = ImageDraw.Draw(img)
pix = img.load()

for i, j, k in tqdm(triangulation.simplices):
	a = tuple(vertices[i])
	b = tuple(vertices[j])
	c = tuple(vertices[k])

	i = (a[0] + b[0] + c[0]) // 3
	j = (a[1] + b[1] + c[1]) // 3

	draw.polygon([a, b, c], fill=pix[i, j])

# Save the image
img.save('assets/low_poly.jpg', 'JPEG')

