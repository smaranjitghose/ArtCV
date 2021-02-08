# Import the dependencies
import argparse
import numpy as np #matrix manipulation
from PIL import Image #image processing lib
from time import sleep #for slowing down the process to make progress visible

#construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
args = vars(ap.parse_args())

# reading the image
img = Image.open((args["image"])).convert("RGB")
width, height = img.size
pixels = img.load()

# Main program starts here
for py in range(height):
    for px in range(width):
        r,g,b = img.getpixel((px,py))
        newr = r
        newg = 0
        newb = b
        pixels[px,py] = (newr,newg,newb)

# Export of the image
img.save("assets/pink.jpg")
print("Your results are ready!")


