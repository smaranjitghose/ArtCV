# Import the dependencies
import cv2
import sys
import numpy as np
from PIL import Image

def oil_effect(user_file):
    # Reading the image
    img = Image.open(user_file)
    img = np.array(img)

    # Making sure img is not empty
    if img is None:
        print("Can't read the image file."+
        "\nPlease make sure you are passing a valid path and it points to an image.")
        sys.exit()
    else:
        # Applying the effect
        oil_painting_img = cv2.xphoto.oilPainting(img, 7, 1)

        return oil_painting_img
