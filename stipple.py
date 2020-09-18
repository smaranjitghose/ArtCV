# Import the dependencies
import argparse
import PIL
import random
from PIL import Image
from PIL import ImageColor
import math
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
args = vars(ap.parse_args())


img = Image.open(args['image'])
img = img.convert('LA')

width, height = img.size
imgNew = Image.new('LA', (width, height))

print('generating...')
# here performing the operation where we are randomly selecting the pixel and adding the effect.
for x in range(width):
    for y in range(height):
        point = img.getpixel( (x,y) )[0]
        randNum = random.randint(0, 260)
        if randNum >= point:
            imgNew.putpixel( (x,y), (0, 255))
            
            

imgNew.save('assets/Stippled.png')