# Import the dependencies
import cv2
import argparse
import numpy as np

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
args = vars(ap.parse_args())

# reading the image
img = cv2.imread((args["image"]))

rows, cols = img.shape[:2]

# Create a Gaussian filter
kernel_x = cv2.getGaussianKernel(cols,200)
kernel_y = cv2.getGaussianKernel(rows,200)
kernel = kernel_y * kernel_x.T
filter = 255 * kernel / np.linalg.norm(kernel)
vintage_im = np.copy(img)

# for each channel in the input image, we will apply the above filter
for i in range(3):
    vintage_im[:,:,i] = vintage_im[:,:,i] * filter
cv2.imshow("Vintage",vintage_im)
cv2.imshow("image",img)
cv2.waitKey(0)
cv2.destroyAllWindows()
