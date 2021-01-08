# Import the dependencies
import cv2
import argparse
import sys
from tqdm import tqdm as tqdm
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
args = vars(ap.parse_args())

# reading the image
img = cv2.imread((args["image"]))

# Make sure img is not empty
if img is None:
    print("Can't read the image file."+
    "\nPlease make sure you are passing a valid path and it points to an image.")
    sys.exit()
for j in tqdm(range(1,10),desc = 'Generating'):
    oil_painting_img = cv2.xphoto.oilPainting(img,7,1)

#create Window to display images
    cv2.imshow('Oil Painting', oil_painting_img)

# Input keypress
k = cv2.waitKey(0)
# If Esc key is pressed
if k == 27 or k == ord('q'):
    # Save the image in the desired path
    cv2.imwrite('assets/oil_painting.jpg',oil_painting_img)
    #close all the opened windows
    cv2.destroyAllWindows()

