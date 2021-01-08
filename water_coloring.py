# Import the dependencies
import cv2
import argparse
from tqdm import tqdm as tqdm
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
args = vars(ap.parse_args())

# reading the image
img = cv2.imread((args["image"]))
for j in tqdm(range(1,10),desc = 'Generating'):
    water_color_img  = cv2.stylization(img, sigma_s = 60,sigma_r = 0.6)
# The smoothing filter replaces the value of a pixel by the weighted sum of its neighbors
# The bigger the neighbourhood, the smoother the image becomes
# The parameter signma_s(Sigma_Spatial) is used for controlling the size of the neighbourhood.
# It's value are from 1-200

# At times it is not possible to replace the color of a pixel by the weighted sum of its neighbors.
# Rather color value at a pixel is repaced by the average of pixels in the neighborhood which also have color similar to the pixel.
# The parameter sigma_r(Sigma_Range) is used for controlling the averaging of dissimilar colors within the neighbourhood.
# It's value range from 0 to 1
# A larger value of sigma_r results in large regions of constant color.

#create Window to display images
    cv2.imshow('Water Coloring', water_color_img)

# Input keypress
k = cv2.waitKey(0)
# If Esc key is pressed
if k == 27 or k == ord('q'):
    # Save the image in the desired path
    cv2.imwrite('assets/water_coloring.jpg', water_color_img)
    #close all the opened windows
    cv2.destroyAllWindows()
