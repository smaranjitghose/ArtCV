from matplotlib import pyplot as plt
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from skimage.color import rgb2lab, lab2rgb, rgb2gray
from keras.models import model_from_json
from skimage.io import imsave
import numpy as np
import tensorflow as tf
import cv2
import os
import argparse
import sys
from tqdm import tqdm as tqdm

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
args = vars(ap.parse_args())

# load json and create model

json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)

# load weights into new model
loaded_model.load_weights("model.h5")

if args["image"] is None:
    print("Can't read the image file." + "\nPlease make sure you are passing a valid path and it points to an image.")
    sys.exit()
for j in tqdm(range(1, 10), desc="Generating"):
    colorize = [img_to_array(load_img(args["image"]))]
    colorize = np.array(colorize, dtype=float)
    colorize = rgb2lab(1.0 / 255 * colorize)[:, :, :, 0]
    colorize = colorize.reshape(colorize.shape + (1,))
    output = loaded_model.predict(colorize)
    output = output * 128
    cur = np.zeros((256, 256, 3))
    cur[:, :, 0] = colorize[0][:, :, 0]
    cur[:, :, 1:] = output[0]
    resImage = lab2rgb(cur)
    newSize = (output.shape[1],output.shape[2])
    resImage = cv2.resize(resImage,newSize, interpolation=cv2.INTER_CUBIC)
    cv2.imshow('Colorized Image', resImage)

# Input keypress
k = cv2.waitKey(0)
# If Esc key is pressed
if k == 27 or k == ord('q'):
    # Save the image in the desired path
    cv2.imwrite('assets/colored_img.jpg', resImage)
    # close all the opened windows
    cv2.destroyAllWindows()
