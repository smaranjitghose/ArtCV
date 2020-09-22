# pip install tsp_solver
# kindly note the code takes considerable amount of time to run depending upon the "size" parameter.
import os  
import cv2  
from PIL import Image  
import cv2
from scipy.spatial.distance import pdist, squareform  
from tsp_solver.greedy_numpy import solve_tsp
import os, random, argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
args = vars(ap.parse_args())

image_path = args['image'] 
img=cv2.imread(image_path)
img=cv2.resize(img, (580, 740),interpolation = cv2.INTER_AREA) 
grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
(thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 100, 255, cv2.THRESH_BINARY)  

import numpy as np  
import matplotlib.pyplot as plt  
  
bw_image_array = np.array(blackAndWhiteImage, dtype=np.int)  
black_indices = np.argwhere(bw_image_array == 0)  
# Changing "size" to a larger value makes this algorithm take longer,  
# but provides more granularity to the portrait  
chosen_black_indices = black_indices[np.random.choice(black_indices.shape[0],size=8000)]  

distances = pdist(chosen_black_indices)  
distance_matrix = squareform(distances)

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