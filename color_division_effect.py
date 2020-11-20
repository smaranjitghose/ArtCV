# import the necessary packages
from sklearn.cluster import MiniBatchKMeans #for Kmeans algorithm
from tqdm import tqdm #for displaying progress bar
import numpy as np #for matrix manipulation
import argparse # for i/o functions
import cv2 # computer vision library 
from time import sleep # to observe progress on bar.

def color_divisionK3(image):
    sleep(0.1)
    with tqdm(total=100,desc="Progress 1/2: ") as pbar:
        (h, w) = image.shape[:2]
        # convert the image from the RGB color space to the L*a*b*
        # color space -- since we will be clustering using k-means
        # which is based on the euclidean distance, we'll use the
        # L*a*b* color space where the euclidean distance implies
        # perceptual meaning
        image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        sleep(0.1)
        pbar.update(10)
        # reshape the image into a feature vector so that k-means
        # can be applied
        image = image.reshape((image.shape[0] * image.shape[1], 3))
        # apply k-means using the specified number of clusters and
        # then create the quantized image based on the predictions
        clt = MiniBatchKMeans(n_clusters = 3)
        sleep(0.1)
        pbar.update(30)
        labels = clt.fit_predict(image)
        quant = clt.cluster_centers_.astype("uint8")[labels]
        sleep(0.1)
        pbar.update(30)
        # reshape the feature vectors to images
        quant = quant.reshape((h, w, 3))
        image = image.reshape((h, w, 3))
        # convert from L*a*b* to RGB
        res = cv2.cvtColor(quant, cv2.COLOR_LAB2BGR)
        image = cv2.cvtColor(image, cv2.COLOR_LAB2BGR)
        sleep(0.1)
        pbar.update(30)
    return res

def color_divisionK6(image):
    sleep(0.1)
    with tqdm(total=100,desc="Progress 2/2: ") as pbar:
        (h, w) = image.shape[:2]
        image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        sleep(0.1)
        pbar.update(10)
        image = image.reshape((image.shape[0] * image.shape[1], 3))
        clt = MiniBatchKMeans(n_clusters = 6)
        sleep(0.1)
        pbar.update(30)
        labels = clt.fit_predict(image)
        sleep(0.1)
        pbar.update(20)
        res = clt.cluster_centers_.astype("uint8")[labels]
        sleep(0.1)
        pbar.update(10)
        res = res.reshape((h, w, 3))
        image = image.reshape((h, w, 3))
        res = cv2.cvtColor(res, cv2.COLOR_LAB2BGR)
        image = cv2.cvtColor(image, cv2.COLOR_LAB2BGR)
        sleep(0.1)
        pbar.update(30)
    return res

# load the image and grab its width and height
# #construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
args = vars(ap.parse_args())
# reading the image
img = cv2.imread((args["image"]))

# display the images and wait for a keypress
result1=color_divisionK3(image)
result2=color_divisionK6(image)
cv2.imwrite("assets/colorDivisionK3.jpg",result1)
cv2.imwrite("assets/colorDivisionK6.jpg",result2)
print("Your results are ready! ")