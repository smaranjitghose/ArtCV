import os, random, argparse, sys, glob
from PIL import Image, UnidentifiedImageError
import numpy as np
from tqdm import tqdm
import sys


parser = argparse.ArgumentParser(description='Creates a photomosaic from input images')
parser.add_argument('--target', dest='target', required=True, help="Image to create mosaic from")
parser.add_argument('--images', dest='images', required=True, help="Diectory of images")
args = parser.parse_args()

def getImages(images_directory):
    #catching all png, jpeg and jpg files in the directory
    image_list = (glob.glob(images_directory + "/*.png") + 
              glob.glob(images_directory + "/*.jpg") +
              glob.glob(images_directory + "/*.jpeg"))
    
    if not image_list:
        print("There is no valid image file in the directory passed as argument to --images.")
        sys.exit()

    images = []
    for img in image_list:
        try:
            fp = open(img, "rb")
            im = Image.open(fp)
            images.append(im)
            im.load()
            fp.close()
        except ValueError:
            print("Invalid parameters passed to PIL.Image.open() method.")
            sys.exit()
        except UnidentifiedImageError:
            #If cant open the file, ignore it and continue
            print("WARNING: Can not identify and open one file. Ignoring it...")
            continue
        
    return (images)

# computing the average value for the image
def getAverageRGB(image):
    im = np.array(image)
    w, h, d = im.shape
    return (tuple(np.average(im.reshape(w * h, d), axis=0)))

# splitting the image into tiles
def splitImage(image, size):
    W, H = image.size[0], image.size[1]
    m, n = size
    w, h = int(W / n), int(H / m)
    imgs = []
    for j in range(m):
        for i in range(n):
            imgs.append(image.crop((i * w, j * h, (i + 1) * w, (j + 1) * h)))
    return (imgs)
# selecting the best match from the mosaic images based on average values of the original image.
def getBestMatchIndex(input_avg, avgs):
    avg = input_avg
    index = 0
    min_index = 0
    min_dist = float("inf")
    for val in avgs:
        dist = ((val[0] - avg[0]) * (val[0] - avg[0]) +
                (val[1] - avg[1]) * (val[1] - avg[1]) +
                (val[2] - avg[2]) * (val[2] - avg[2]))
        if dist < min_dist:
            min_dist = dist
            min_index = index
        index += 1
    return (min_index)
# creating the image grid for tiles to fit in
def createImageGrid(images, dims):
    m, n = dims
    width = max([img.size[0] for img in images])
    height = max([img.size[1] for img in images])
    grid_img = Image.new('RGB', (n * width, m * height))
    for index in range(len(images)):
        row = int(index / n)
        col = index - n * row
        grid_img.paste(images[index], (col * width, row * height))
    return (grid_img)

# creating the mosaic
def createPhotomosaic(target_image, input_images, grid_size,
                      reuse_images=True):
    target_images = splitImage(target_image, grid_size)

    output_images = []
    count = 0
    batch_size = int(len(target_images) / 10)
    avgs = []
    for img in input_images:
        try:
            avgs.append(getAverageRGB(img))
        except:
            continue

    for img in tqdm(target_images):
        try:
            avg = getAverageRGB(img)
        except:
            continue
        match_index = getBestMatchIndex(avg, avgs)
        output_images.append(input_images[match_index])
        count += 1
        # remove selected image from input if flag set
        if not reuse_images:
            input_images.remove(match_index)

    mosaic_image = createImageGrid(output_images, grid_size)
    return (mosaic_image)

try:
    target_image = Image.open(args.target)
except FileNotFoundError:
    print("Can not find the specified --target file. Please, make sure the passed file exists.")
    sys.exit()
except ValueError:
	print("Invalid parameters passed to PIL.Image.open() method.")
	sys.exit()
except UnidentifiedImageError:
	print("Can not identify and open the image file specified. Please, make sure the file passed is a valid image.")
	sys.exit()
except IsADirectoryError:
    print("The argument passed as --target is a directory without any files. Image file path expected.")
    sys.exit()

# input images
input_images = getImages(args.images)

# shuffle list - to get a more varied output?
random.shuffle(input_images)
# size of grid
grid_size = (200, 200)
# re-use any image in input
reuse_images = True
# resize the input to fit original image size?
resize_input = True

# resizing input
if resize_input:
    # for given grid size, compute max dims w,h of tiles
    dims = (int(target_image.size[0] / grid_size[1]),
            int(target_image.size[1] / grid_size[0]))
    # resize
    for img in input_images:
        img.thumbnail(dims)

# create photomosaic
mosaic_image = createPhotomosaic(target_image, input_images, grid_size, reuse_images)

# write out mosaic
mosaic_image.save('assets/mosaic.jpg', 'JPEG')
