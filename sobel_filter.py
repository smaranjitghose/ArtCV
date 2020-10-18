#Imports and dependencies
import numpy as np
import cv2
from math import sqrt, atan
from math import atan, degrees
import argparse
from tqdm import tqdm
pbar = tqdm(total=100)

#Constants
kernel_blur = np.array([0.11,0.11,0.11,0.11,0.11,0.11,0.11,0.11,0.11]).reshape(3,3)
kernel_conv_Y = np.array([-1,-2,-1,0,0,0,1,2,1]).reshape(3,3)
kernel_conv_X = kernel_conv_Y.transpose()

'''In the implementation of the canny filter, the following steps are implemented:
 - Conversion to grayscale
 - Gaussian filter for blurring and to reduce the sharpness
 - Apply sobel filter in X and Y direction to detect the edges
 - With the gradient obtained previously, non-maximal supression is performed
 - Hystersis and double thresholding to thin the lines
'''

#The concept of convolution is used here, a kernel matrix (here, of size 3X3) convolves over the image
#This is used to blur as well as apply the sobel filter for edge-detection

def apply_convolution(img, kernel, height, weight):
  pixels = []
  #pixels are extracted from the image converted to grayscale
  for i in range(height):
    for j in range(width):
      pixels.append(img[i,j])

  #The pixels array is resized in accordance with the size of the image
  pixels = np.array(pixels).reshape(height,width)

  #To handle the edge cases, sentinel values are used
  #The pixels array is bound by zeros on all edges

            # 00000000
            # 0PIXELS0
            # 00000000
  #This is done to ensure that the kernel is applied to all the pixels
  #Sentinel values to ensure the edges arent missed out

  #Along the rows and columns
  pixels = np.insert(pixels , [0,height] , np.zeros(len(pixels[0])) , axis = 0)
  pixels = np.insert(pixels , [0, width] , np.zeros((len(pixels[:, 0]) ,1)) , axis = 1)

  #Convolution is applied here
  convolute = []
  for i in range(1,height):
    for j in range(1,width):
      temp = pixels[i:i+3 , j:j+3]
      product = np.multiply(temp,kernel)
      convolute.append(sum(sum(product)))

  convolute = np.array(convolute).reshape(height-1,width-1)
  return(convolute)

#In the implementation of the sobel filter, X and Y direction convolutions are obtained separately and the resultant is extracted
def sobel_filter(convoluted_X, convoluted_Y):
  sobel = []
  #arc = []
  #Considering the square of the pixel value in X direction as pixel_X, in Y direction as pixel_Y,
  #The resultant in the Z-direction is the sqrt(pixel_X + pixel_Y)
  for i in range(height-2):
    for j in range(width-2):
      pixel_X = pow(convoluted_X[i,j], 2)
      pixel_Y = pow(convoluted_Y[i,j], 2)
      #pixel_X = convoluted_X[i,j]
      #pixel_Y = convoluted_Y[i,j]
      pixel_Z = sqrt(pixel_X + pixel_Y)
      sobel.append(pixel_Z)
  sobel = np.array(sobel).reshape(height-2, width-2)
  return(sobel)

if __name__ == "__main__":
    # construct the argument parse and parse the arguments
    for i in range(1):
        ap = argparse.ArgumentParser()
        ap.add_argument("-i", "--image", required=True, help="path to input image")
        args = vars(ap.parse_args())
        pbar.update(10)
        
        # reading the image in grayscale
        img = cv2.imread((args["image"]), 0)
        height = img.shape[0]
        width = img.shape[1]
        pbar.update(10) 
    
        #Image is blurred
        blurred_img = apply_convolution(img, kernel_blur, height, width)
        height = height - 1
        width = width - 1

        convoluted_Y = apply_convolution(blurred_img, kernel_conv_Y, height, width)
        pbar.update(20)

        convoluted_X = apply_convolution(blurred_img, kernel_conv_X, height, width )
        pbar.update(20)
        
        #The sobel effect is applied
        sobel_filtered_image = sobel_filter(convoluted_X, convoluted_Y)
        pbar.update(40)

        cv2.imwrite('Sobel_filtered_image.JPG', sobel_filtered_image)
        cv2.imshow("Sobel filter", sobel_filtered_image)
        cv2.waitKey(0)
    pbar.close()

