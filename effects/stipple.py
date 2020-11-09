# Import the dependencies
import random
from PIL import Image,ImageColor
import math
from tqdm import tqdm

def stippler(img,imgNew,width,height):
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
                imgNew.putpixel((x,y), (0, 255))
    return imgNew

def stipple_effect(user_file):
    img = Image.open(user_file)
    # Convert the image into Greyscale('L') with alpha transparency('A') to determine how a pixel is rendered when blended with another.
    img = img.convert('LA')

    width, height = img.size
    # here we are converting the image to the greyscale form('L') with an alpha ('A') transparency
    imgNew = Image.new('LA', (width, height))

    imgFinal = stippler(img,imgNew,width,height)

    return imgFinal
