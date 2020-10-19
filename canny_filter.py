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
upper_threshold = 0.8
lower_threshold = 0.2

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

#On convolution, the size of the image reduces, hence to prevent changing the size of the image sentinel values are added along the edges
def change_dimensions(convoluted_X, convoluted_Y, sobel):
  height_con = convoluted_X.shape[0]
  width_con = convoluted_X.shape[1]
  convoluted_X = np.insert(convoluted_X , [0,height_con-1] , np.zeros(len(convoluted_X[0])) , axis = 0)
  convoluted_X = np.insert(convoluted_X , [0, width_con-1] , np.zeros((len(convoluted_X[:, 0]) ,1)) , axis = 1)    
  convoluted_Y = np.insert(convoluted_Y , [0,height_con-1] , np.zeros(len(convoluted_Y[0])) , axis = 0)
  convoluted_Y = np.insert(convoluted_Y , [0, width_con-1] , np.zeros((len(convoluted_Y[:, 0]) ,1)) , axis = 1)
  sobel = np.insert(sobel , [0,sobel.shape[0]-1] , np.zeros(len(sobel[0])) , axis = 0)
  sobel = np.insert(sobel , [0, sobel.shape[1]-1] , np.zeros((len(sobel[:, 0]) ,1)) , axis = 1)
  return(convoluted_X , convoluted_Y, sobel)

#Non-linear suppression is implemented here, in order to sharpen the edges obtained
def non_linear_suppression(convoluted_X, convoluted_Y, sobel):
  value = 0
  non_linear = []
  height_con = convoluted_X.shape[0] - 1
  width_con = convoluted_X.shape[1] - 1
  for i in range(1, height_con - 1):
    for j in range(1, width_con - 1):
      gradient_x = convoluted_X[i, j]
      gradient_y = convoluted_Y[i, j]
      pixel = sobel[i, j]
      if gradient_y == 0:
        if pixel >= sobel[i, j+1] and pixel >= sobel[i, j-1]:
          value = pixel
        else:
          value = 0
      elif gradient_x == 0:
        if pixel >= sobel[i+1, j] and pixel >= sobel[i-1, j]:
          value = pixel
        else:
          value = 0
      else:
        angle = degrees(atan(gradient_y/gradient_x))
        if gradient_x > 0 and gradient_y > 0:
          gr = angle
        elif gradient_x < 0 and gradient_y < 0:
          gr = 180 + angle
        elif gradient_x > 0 and gradient_y < 0:
          gr = 360 + angle
        else:
          gr = 180 + angle
        p1 = [*range(0,22)]
        p2 = [*range(22,67)]
        p3 = [*range(67,112)]
        p4 = [*range(112,157)]
        p5 = [*range(157,202)]
        p6 = [*range(202,247)] 
        p7 = [*range(247,290)]
        p8 = [*range(290,337)]          
        p9 = [*range(337,360)]
        gr = int(gr)
        if gr in p1 or gr in p5 or gr in p9:
          if pixel >= sobel[i, j+1] and pixel >= sobel[i, j-1]:
            value = pixel
          else:
              value = 0
        elif gr in p2 or gr in p6:
          if pixel >= sobel[i-1, j+1] and pixel >= sobel[i+1, j-1]:
            value = pixel
          else:
              value = 0
        elif gr in p3 or gr in p7:
          if pixel >= sobel[i-1, j] and pixel >= sobel[i+1, j]:
            value = pixel
          else:
              value = 0
        elif gr in p4 or gr in p8:
          if pixel >= sobel[i-1, j-1] and pixel >= sobel[i+1, j + 1]:
            value = pixel
          else:
              value = 0
      non_linear.append(value)

  non_linear = np.array(non_linear).reshape(height_con-2, width_con-2)
  return(non_linear)
    

def double_threshold(non_li):
  height, width = non_li.shape
  high = np.amax(non_li) * upper_threshold
  low = np.amax(non_li) * lower_threshold
  final = []
  for i in range(height):
    for j in range(width):
      if non_li[i,j] > high:
        final.append(255)
      elif low <= non_li[i,j] <= high:
        final.append(non_li[i,j])
      else:
        final.append(0)
  final = np.array(final).reshape(height, width)
  return(final)

if __name__ == "__main__":
    # construct the argument parse and parse the arguments
    for i in range(1):
        ap = argparse.ArgumentParser()
        ap.add_argument("-i", "--image", required=True, help="path to input image")
        args = vars(ap.parse_args())

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
        pbar.update(15)
        
        convoluted_X = apply_convolution(blurred_img, kernel_conv_X, height, width )
        pbar.update(15)

        #The sobel effect is applied
        sobel = sobel_filter(convoluted_X, convoluted_Y)
        pbar.update(15)

        convoluted_X, convoluted_Y, sobel = change_dimensions(convoluted_X, convoluted_Y, sobel)

        #Non-maximal suppression is carried out here
        non_linear_filter = non_linear_suppression(convoluted_X, convoluted_Y, sobel)
        pbar.update(15)

        #Thresholding is applied to retain only certain lines
        canny_filtered_image = double_threshold(non_linear_filter)
        pbar.update(30)

        cv2.imwrite('Canny_filtered_image.JPG', canny_filtered_image)
        cv2.imshow("Canny filter", canny_filtered_image)
        cv2.waitKey(0)
    pbar.close()
