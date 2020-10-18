from scipy import stats # apply statistical knowledge from scitific python lib
import numpy as np # matrix manipulation
import cv2 # image processing lib
import argparse # input and output file.
from time import sleep # time based library
from collections import defaultdict # DS
from tqdm import tqdm as tqdm # for progess bar 

# K-means algorithm to cluster the histogram of image
# Value of K is auto-selected

def animefy(input_image,old=0):
    output = np.array(input_image)
    x, y, channel = output.shape
    # hists = []
    for i in range(channel):
        #apply bilateral filter on image with i skip value
        output[:, :, i] = cv2.bilateralFilter(output[:, :, i], 5, 50, 50)
    edge = cv2.Canny(output, 100, 200)
    #Convert image from one color space to another (RGB to HSV value)
    output = cv2.cvtColor(output, cv2.COLOR_RGB2HSV)
    # Initialize a histogram values for HSV specifically
    hists = []
    #H val histogram
    hist, _ = np.histogram(output[:, :, 0], bins=np.arange(180+1))
    hists.append(hist)
    #S val histogram
    hist, _ = np.histogram(output[:, :, 1], bins=np.arange(256+1))
    hists.append(hist)
    #V val histogram
    hist, _ = np.histogram(output[:, :, 2], bins=np.arange(256+1))
    hists.append(hist)

    Collect = [] 
    #for collecting all H,S,V histograms after apply KHist fuction on all.
    for h in tqdm(hists,desc="Progress 1 of 2"):
        sleep(0.2)
        Collect.append(KHist(h))
    """print("centroids: {0}".format(Collect))"""

    output = output.reshape((-1, channel))
    for i in tqdm(range(channel),desc="Progress 2 of 2"):
        channel1 = output[:, i]
        index = np.argmin(np.abs(channel1[:, np.newaxis] - Collect[i]), axis=1)
        output[:, i] = Collect[i][index]
    output = output.reshape((x, y, channel))
    output = cv2.cvtColor(output, cv2.COLOR_HSV2RGB)
    # contours find and apply on org. image
    contours, _ = cv2.findContours(edge,
                                   cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(output, contours, -1, 0, thickness=1)
    output2=cv2.cvtColor(output, cv2.COLOR_BGR2XYZ)
    output3=cv2.cvtColor(output, cv2.COLOR_BGR2HLS)
    #multip-value return statement needed
    if(old==0):
        return output,output2,output3
    else:
        output1 = output.copy()
        output = np.array(output, dtype=np.float64) # converting to float to prevent loss
        output = cv2.transform(output, np.matrix([[0.272, 0.534, 0.131],
                                    [0.349, 0.686, 0.168],
                                    [0.393, 0.769, 0.189]])) # multipying image with special vintage view matrix
        output[np.where(output > 255)] = 255 # normalizing values greater than 255 to 255
        output = np.array(output, dtype=np.uint8) # converting back to int
        return output1,output2,output3,output


def update_C(C, histogram):
    #update centroids until they don't change

    while (True):
        groups = defaultdict(list)
        # Assign pixel values
        for i in range(len(histogram)):
            if histogram[i] == 0:
                continue
            d = np.abs(C-i)
            index = np.argmin(d)
            groups[index].append(i)

        new_C = np.array(C)
        for i, indice in groups.items():
            if np.sum(histogram[indice]) == 0:
                continue
            new_C[i] = int(np.sum(indice*histogram[indice])/np.sum(histogram[indice]))
        if np.sum(new_C-C) == 0:
            break
        C = new_C
    return C, groups


def KHist(hist):
    #Choose the most appropriate K for k-means and get the centroids accordingly

    alpha = 0.001 # p-value threshold for normaltest
    N = 80  # minimun group size for normaltest
    C = np.array([128])

    while True:
        C, groups = update_C(C, hist)

        #start increase K if possible
        new_C = set()     # use set to avoid same value when seperating centroid
        for i, indice in groups.items():
            #if there are not enough values in the group, do not seperate
            if len(indice) < N:
                new_C.add(C[i])
                continue

            # judge whether we should seperate the centroid by testing if the values of the group is under a normal distribution
            z, pval = stats.normaltest(hist[indice])
            if pval < alpha:
                #not a normal dist, seperate
                left = 0 if i == 0 else C[i-1]
                right = len(hist)-1 if i == len(C)-1 else C[i+1]
                delta = right-left
                if delta >= 3:
                    c1 = (C[i]+left)/2
                    c2 = (C[i]+right)/2
                    new_C.add(c1)
                    new_C.add(c2)
                else:
                    # though it is not a normal dist, we have no extra space to seperate
                    new_C.add(C[i])
            else:
                # normal dist, no need to seperate
                new_C.add(C[i])
        if len(new_C) == len(C):
            break
        else:
            C = np.array(sorted(new_C))
    return C

if __name__ == '__main__':
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="path to input image")
    args = vars(ap.parse_args())

    #reading the image
    image = cv2.imread((args["image"]))

    start_time = time.time()
    print("Wait, Work is in Progess.")
    output,output2,output3,output4 = animefy(image,1)
    end_time = time.time()
    t = end_time-start_time # processing time
    print('time: {0}s'.format(t))
    

    cv2.imwrite("assets/anime_effect.jpg", output) # save the image
    cv2.imwrite("assets/anime_Blue_effect.jpg", output2) 
    cv2.imwrite("assets/anime_PredatorView_effect.jpg", output3) 
    cv2.imwrite("assets/anime_vintage_effect.jpg", output4)
    print("Your results are ready!")