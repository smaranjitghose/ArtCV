# Import the dependencies
import argparse
import PIL
import random
from PIL import Image,ImageColor
import math
from tqdm import tqdm

def stippler(imgNew,width,height):
    # here performing the operation where we are randomly selecting the pixel and adding the effect.
    for x in tqdm(range(width)):
        for y in range(height):
            # here we extract the pixel value of the image.
            point = img.getpixel( (x,y) )[0]
            # generating a random value
            randNum = random.randint(0, 260)
            # condition for manipulating the particular pixels value.
            if randNum >= point:
                # changing the value of the pixel.
                imgNew.putpixel( (x,y), (0, 255))
    return imgNew

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
args = vars(ap.parse_args())


img = Image.open(args['image'])
img = img.convert('LA') # Convert the image into Greyscale('L') with alpha transparency('A') to determine how a pixel is rendered when blended with another.

width, height = img.size
# here we are converting the image to the greyscale form('L') with an alpha ('A') transparency
imgNew = Image.new('LA', (width, height))

imgNew=stippler(imgNew,width,height)
            
imgNew.save('assets/Stippled.png')
