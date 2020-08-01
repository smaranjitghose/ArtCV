# Import the dependencies
import cv2
import argparse

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
args = vars(ap.parse_args())

# reading the image
img = cv2.imread((args["image"]))

water_color_img  = cv2.stylization(img, sigma_s = 60,sigma_r = 0.6)
# Where signma_s is used for controlling the size of the neighbourhood. It's value are from 1-200
# signma_r is used to control how the dissimilar colors within the neighbourhood will be averaged. It's value range from 0 to 1
# A larger value of sigma_r can lead to to large regions of constant color

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
