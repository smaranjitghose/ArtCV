# Import the dependencies
import argparse
import cv2 #image processing lib
import numpy as np #matrix manipulation
from time import sleep #for slowing down the process to make progress visible

#construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
args = vars(ap.parse_args())

# reading the image
img = cv2.imread((args["image"]))
negative = 255 - img

cv2.imwrite("assets/negative.jpg", negative)
print("Your results are ready!")

#create Window to display images
cv2.imshow('Negative Image', negative)
k = cv2.waitKey(0)