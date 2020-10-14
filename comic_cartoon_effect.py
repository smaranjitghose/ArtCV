import cv2 #image processing lib
import numpy as np #matrix manipulation
import time 

def comic(img):
    # do edge detection on a grayscale image
    grayImg = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
    edgesOnly = cv2.blur(grayImg, (3, 3)) # this blur gets rid of some noise
    edgesOnly = cv2.Canny(edgesOnly, 50, 150, apertureSize=3) # this is the edge detection

    # the edges are a bit thin, this blur and threshold make them a bit fatter
    kernel = np.ones((3,3), dtype=np.float) / 12.0
    edgesOnly = cv2.filter2D(edgesOnly, 0, kernel)
    edgesOnly = cv2.threshold(edgesOnly, 50, 255, 0)[1]

    # convert to colour...
    edgesOnly = cv2.cvtColor(edgesOnly, cv2.COLOR_GRAY2BGR)

    # this operation blurs things but keeps track of
    # colour boundaries
    shifted = cv2.pyrMeanShiftFiltering(img, 5, 20)

    # now compose with the edges, the edges are white so take them away
    # to leave black
    return cv2.subtract(shifted, edgesOnly)

# Driver's code 
#img = cv2.imread("assets/kolkata.jpg")

#construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
args = vars(ap.parse_args())
# reading the image
img = cv2.imread((args["image"]))


print("Wait, Work is in Progess.")

res_img3 = comic(img)
cv2.imwrite("assets/comic_cartoon_effect.jpg", res_img3)


print("Your results are ready!")