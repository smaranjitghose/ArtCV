import cv2 #image processing lib
import numpy as np #matrix manipulation
from time import sleep #for slowing down the process to make progress visible 
from tqdm import tqdm as tqdm # for progess bar 

def cartoonize(img):
    sleep(0.1)
    with tqdm(total=100,desc="Progress") as pbar1:
        # 1) Edges -> xonvert the image to gray scale and blur it using a medianBlur (blurring method).
        # Now apply the adaptiveThresholding to pull out highlighted object boundaries.
        grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        grayImg = cv2.medianBlur(grayImg, 5)
        # Image Blur using Median Blur of filter size 5
        sleep(0.2)# added sleep function inorder to make the progress visisble on the bar as without it processing might be
        # fast and will give 100% progess as soon as we put the filter/function in effect.
        pbar1.update(25)
        edgesOnly = cv2.adaptiveThreshold(grayImg, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 19, 6)
        sleep(0.2)
        pbar1.update(30)
        # 2) Color output using bilateralFilter
        color = cv2.bilateralFilter(img, 9, 30, 30)
        color1 = cv2.medianBlur(color,25)
        #Again blur the image with filter size of 25
        sleep(0.2)
        pbar1.update(25)

        # 3) Cartoon (perform bitwise operation with edge mask)
        cartoon = cv2.bitwise_and(color1, color1, mask=edgesOnly)
        sleep(0.2)
        pbar1.update(20)
        return cv2.medianBlur(cartoon,3),edgesOnly

#construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
args = vars(ap.parse_args())
# reading the image
img = cv2.imread((args["image"]))


print("Wait, Work is in Progess.")

res_img1,res_img2 = cartoonize(img)

cv2.imwrite("assets/cartoon1.jpg", res_img1)
cv2.imwrite("assets/black_and_wihte_cartoon.jpg", res_img2)


print("Your results are ready!")
