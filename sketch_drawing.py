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
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 125, 255, cv2.THRESH_BINARY)

cv2.imwrite("assets/sketch_drawing.jpg", thresh)
print("Your results are ready!")

#create Window to display images
cv2.imshow('Sketch-drawing', thresh)
k = cv2.waitKey(0)