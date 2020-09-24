# kindly note the code takes considerable amount of time to run depending upon the "size" parameter.
import os  
import cv2  
from PIL import Image  
import cv2
from scipy.spatial.distance import pdist, squareform  
from tsp_solver.greedy_numpy import solve_tsp
import random, argparse
import numpy as np  
import matplotlib.pyplot as plt  

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
args = vars(ap.parse_args())

image_path = args['image'] 
img=cv2.imread(image_path)
img=cv2.resize(img, (580, 740),interpolation = cv2.INTER_AREA) 
grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
(thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 100, 255, cv2.THRESH_BINARY)  
  
bw_image_array = np.array(blackAndWhiteImage, dtype=np.int)  
black_indices = np.argwhere(bw_image_array == 0)  
# Changing "size" to a larger value makes this algorithm take longer,  
# but provides more granularity to the portrait  
chosen_black_indices = black_indices[np.random.choice(black_indices.shape[0],size=8000)]  

#  Now we have to solve the TSP, so we first have to define the distance between every pixel.
#  In this case, we’re going to define distance between two pixels as the Euclidean distance between their x,y coordinates in the image.
#  With that definition in mind, we can calculate the distances between all size(8000) pixels:
#  The result is a giant 8,000 x 8,000 matrix with the Euclidean distances between every pixel.
distances = pdist(chosen_black_indices)  
distance_matrix = squareform(distances)

# Now we provide the Matrix to a TSP sover package which returns the optimized path matrix.
# The library implements a simple "greedy" algorithm:
# Initially, each vertex belongs to its own path fragment. Each path fragment has length 1.
# Find 2 nearest disconnected path fragments and connect them.
# Repeat, until there are at least 2 path fragments.
# This algorightm has polynomial complexity.

optimized_path = solve_tsp(distance_matrix)    
optimized_path_points = [chosen_black_indices[x] for x in optimized_path]    

plt.figure(figsize=(8, 10), dpi=100)  
plt.plot([x[1] for x in optimized_path_points],[x[0] for x in optimized_path_points],color='black', lw=1)  
plt.xlim(0, 600)  
plt.ylim(0, 800)
plt.gca().invert_yaxis() 
plt.xticks([])  
plt.yticks([]) 
plt.savefig('assets/tsp_art.jpg')