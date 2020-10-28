# Import the dependencies
import argparse
import cv2 #image processing lib
import numpy as np #matrix manipulation
from time import sleep #for slowing down the process to make progress visible 
from tqdm import tqdm as tqdm # for progess bar 

def emboss_effect(img):
    height, width = img.shape[:2]
    y = np.ones((height, width), np.uint8) * 128
    output = np.zeros((height, width), np.uint8) #creation of output file for grayscale emboss effect
    # generating the kernels
    kernel1 = np.array([[0, -1, -1], # kernel for embossing bottom left side
                        [1, 0, -1],
                        [1, 1, 0]])
    kernel2 = np.array([[-1, -1, 0], # kernel for embossing bottom right side
                        [-1, 0, 1],
                        [0, 1, 1]])
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)# changing the image to grayscale
    output1 = cv2.add(cv2.filter2D(gray, -1, kernel1), y) # emboss on bottom left side
    output2 = cv2.add(cv2.filter2D(gray, -1, kernel2), y) # emboss on bottom right side
    # output image formation
    for i in tqdm(range(height)):
        for j in range(width):
            #accumulating maximum values.
            output[i, j] = max(output1[i, j], output2[i, j])
    #working on colored emboss effect
    kernel = np.array([[0,-1,-1],
                        [1,0,-1],
                        [1,1,0]])
    return cv2.filter2D(img, -1, kernel),output


#construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
args = vars(ap.parse_args())
# reading the image
img = cv2.imread((args["image"]))

# Convert to image with emboss effect
output1,output2 = emboss_effect(img)
# Save the  image
cv2.imwrite('assets/emboss_effect_grayscale.jpg',output2)
cv2.imwrite('assets/emboss_effect_coloured.jpg',output1)
print("Your results are ready!")