# Import the dependencies
import cv2 #image processing lib
import numpy as np #matrix manipulation
from PIL import Image
from time import sleep #for slowing down the process to make progress visible
from tqdm import tqdm as tqdm # for progess bar

def motionBlur(img):
    # default kernel size.
    size = 70
    # Size of kernel is directly proportional to effect of blur
    # Create the Horizontal and Vertical kernel.
    Hkernel = np.zeros((size, size))
    Vkernel = np.copy(Hkernel)

    # Fill the middle row with ones.
    Hkernel[int((size - 1)/2), :] = np.ones(size)
    Vkernel[:, int((size - 1)/2)] = np.ones(size)

    # Normalize the value under range of 0-1
    Hkernel /= size
    Vkernel /= size
    # Apply the vertical kernel.
    v = cv2.filter2D(img, -1, Vkernel)

    # Apply the horizontal kernel.
    h = cv2.filter2D(img, -1, Hkernel)
    # Create Diagonal filter kernel
    Dkernel = np.copy(Hkernel)
    i=0 #initialize index matching var.
    for x in tqdm(Dkernel):
        for j in range(0,size):
            if(j==i):
                x[i]=1
        i+=1
        sleep(0.01) # to make the progress visible
    # Normalize.
    Dkernel /= size

    # Apply the Diagonal kernel.
    d = cv2.filter2D(img, -1, Dkernel)

    return v,h,d

def blur(user_file, choice):
    img = Image.open(user_file)
    img = np.array(img)

    # Save the outputs.
    v,h,d = motionBlur(img)

    if choice == 1:
        return v
    elif choice == 2:
        return h
    else:
        return d
