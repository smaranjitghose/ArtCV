import time
import cv2
import numpy as np
import os, glob
import shutil
from PIL import Image
from datetime import datetime
import argparse #for implementing command-line interface

parser = argparse.ArgumentParser()
parser.add_argument("--verbose", action="store_true", help="specify --verbose flag in the command to get output with more details")
parser.add_argument("--visibility", action="store_true", help="specify --visibility flag in the command to retain the temporary files and folders created")
parser.add_argument("--res", type=int, help="Photomosaic output resolution (optimal value between 10 and 50) \nHigher value leads to low resolution photomosaic(small file size) and smaller value leads to high resolution photomosaic(large file size)")
parser.add_argument("--tile", type=int, help="resolution(in pixels) of the individual filler images that will used as the mosaic tiles (optimal value is between 50 and 100)")
args = parser.parse_args()

sdelay = 3
mdelay = 6
hdelay = 12
biar = 0    #blocks in a row
biac = 0    #blocks in a column
main_img_block_details = []
filler_img_details = []
matched_images = []

if type(args.res) == int:
    divider = args.res
else: divider = 10
#area assigned to an individual img on main img
#higher value leads to low resolution output
#smaller value leads to high resolution output

if type(args.tile) == int:
    size = args.tile, args.tile
else: size = 75, 75   
#size of an individual square img or block size
#higher value leads to better quality individual imgs
#smaller value leads to low quality individual imgs


def initialise():
    print ("Initialising...")
    try:
        if args.verbose: print ("Deleting previous 'main_image_blocks' folder")
        shutil.rmtree("main_image_blocks")
    except Exception as e:
        if args.verbose: print (e)
    if args.verbose: time.sleep(sdelay)

    try:
        if args.verbose: print ("Deleting previous 'renamed_filler_images' folder")
        shutil.rmtree("renamed_filler_images")
    except Exception as e:
        if args.verbose: print (e)
    if args.verbose: time.sleep(sdelay)

    try:
        if args.verbose: print ("Deleting previous 'cropped_filler_images' folder")
        shutil.rmtree("cropped_filler_images")
    except Exception as e:
        if args.verbose: print (e)
    if args.verbose: time.sleep(sdelay)

    try:
        if args.verbose: print ("Deleting previous 'resized_filler_images' folder")
        shutil.rmtree("resized_filler_images")
    except Exception as e:
        if args.verbose: print (e)
    if args.verbose: time.sleep(sdelay)

    try:
        if args.verbose: print ("Deleting previous 'matched_images' folder")
        shutil.rmtree("matched_images")
    except Exception as e:
        if args.verbose: print (e)
    if args.verbose: time.sleep(sdelay)


def split_main_image():
    print ("\nSTEP 1 -->    Splitting the Main image")
    if args.verbose: time.sleep(sdelay)
    
    os.mkdir("main_image_blocks")   #create a new folder for storing the main image blocks

    img = cv2.imread('./main_image/img.jpg', 1) #load the colour image
    if args.verbose: print ("\nMain image shape")
    if args.verbose: print (" height   : ", img.shape[0])
    if args.verbose: print (" width    : ", img.shape[1])
    if args.verbose: time.sleep(sdelay)

    #after loading the main image, trim the extra rows/columns of main image for proper splitting so that
    #the image can be perfectly divided with the DIVIDER value provided, without getting any partial splits 
    extra_row = img.shape[0] % divider
    extra_column = img.shape[1] % divider

    #trim the image for proper splitting
    img = img[0:img.shape[0]-extra_row, 0:img.shape[1]-extra_column]
    global biar
    global biac
    biar = int(img.shape[1]/divider)     #biar : blocks in a row
    biac = int(img.shape[0]/divider)     #biac : blocks in a column
    if args.verbose: print ("\nWhen the main image is splitted we get")
    if args.verbose: print (" blocks in a row     : ", biar)
    if args.verbose: print (" blocks in a column  : ", biac)
    if args.verbose: print (" total blocks        : ", biar*biac)
    if args.verbose: print (" NOTE : removed {} extra rows and {} extra columns".format(extra_row, extra_column))
    if args.verbose: time.sleep(mdelay)

    #after trimming the image is split into (biar*biac) number of blocks
    count = 0
    xposition = 0
    yposition = 0
    for i in range(0, biar):
        for j in range(0, biac):
            temp_img = img[:][:]
            temp_img = temp_img[yposition:yposition+divider, xposition:xposition+divider]
            count += 1
            if args.verbose: print ("STEP 1 -->    ", count, '/', biar*biac, ' completed')
            cv2.imwrite('./main_image_blocks/{}.jpg'.format(str(j)+'_'+str(i)), temp_img)
            yposition  += divider
        yposition = 0
        xposition += divider
    if args.verbose: time.sleep(sdelay)

def rename_filler_images():
    print ("\nSTEP 2 -->    Renaming the filler images")
    if args.verbose: time.sleep(sdelay)
    os.mkdir("renamed_filler_images")   #create a new folder for storing renamed filler images
    
    # load the filler images to be renamed
    total_img_count = 0
    count = 0
    for infile in glob.glob("./filler_images/*.*"):
        total_img_count += 1
    for infile in glob.glob("./filler_images/*.*"):
        im = Image.open(infile)
        count += 1
        im.save("./renamed_filler_images/" + str(count) + ".jpg", "JPEG")
        if args.verbose: print ("STEP 2 -->    ", count, "/", total_img_count, "images renamed")
    if args.verbose: time.sleep(sdelay)


def crop_filler_images():
    print ("\nSTEP 3 -->    Cropping the filler images into square shape")
    if args.verbose: time.sleep(sdelay)
    os.mkdir("cropped_filler_images")   #create a new folder for storing the square filler images

    #loading the renamed filler images to cropped into square shapes
    count = 0
    total_img_count = 0
    for infile in glob.glob("./renamed_filler_images/*.jpg"):
        total_img_count += 1
    for infile in glob.glob("./renamed_filler_images/*.jpg"):
        count += 1
        img = cv2.imread('./renamed_filler_images/' + str(count) + '.jpg', 1)
        if img.shape[0] < img.shape[1]:     #landscape orientation
            remove_value = img.shape[1] - img.shape[0]
            img = img[:, :img.shape[1]-remove_value]
        elif img.shape[0] > img.shape[1]:   #potrait orientation
            remove_value = img.shape[0] - img.shape[1]
            img = img[:img.shape[0]-remove_value, :]
        cv2.imwrite("./cropped_filler_images/" + str(count) + ".jpg", img)
        if args.verbose: print ("STEP 3 -->    ", count, '/', total_img_count, 'images cropped and made into squares')
    if args.verbose: time.sleep(sdelay)


def resize_filler_images():
    print ("\nSTEP 4 -->    Resizing the filler images")
    if args.verbose: time.sleep(sdelay)
    os.mkdir("resized_filler_images")   #create a new folder for storing the resized filler images

    #load cropped filler images to be resized
    total_img_count = 0
    count = 0
    for infile in glob.glob("./cropped_filler_images/*.jpg"):
        total_img_count += 1
    for infile in glob.glob("./cropped_filler_images/*.jpg"):
        file, ext = os.path.splitext(infile)
        im = Image.open(infile)
        im.thumbnail(size)
        im.save("./resized_filler_images/" + str(count) + '.jpg', "JPEG")
        count += 1
        if args.verbose: print ("STEP 4 -->    ", count, '/', total_img_count, 'filler images resized')
    if args.verbose: time.sleep(sdelay)

def avg_rgb_filler_images():
    print ("\nSTEP 5 -->    Finding the average RGB value of each filler image")
    if args.verbose: time.sleep(sdelay)

    total_img_count = 0
    count = 0

    for infile in glob.glob("./resized_filler_images/*.jpg"):
        total_img_count += 1
    for infile in glob.glob("./resized_filler_images/*.jpg"):
        filler_img = cv2.imread("resized_filler_images/" + str(count) + ".jpg", 1)
        sum_red = sum_green = sum_blue = 0
        pixel_count = 0
        for i in range(filler_img.shape[0]):
            for j in range(filler_img.shape[1]):
                temp_red, temp_green, temp_blue = filler_img[i][j][2], filler_img[i][j][1], filler_img[i][j][0] #opencv loads images in BGR by default
                sum_red += temp_red
                sum_green += temp_green
                sum_blue += temp_blue
                pixel_count += 1
        avg_red = sum_red/pixel_count
        avg_green = sum_green/pixel_count
        avg_blue = sum_blue/pixel_count
        filler_img_details.append({
            'file_name': str(count),
            'avg_red': avg_red,
            'avg_green': avg_green,
            'avg_blue': avg_blue
            })
        count += 1
        if args.verbose: print ("STEP 5 -->    ", count, '/', total_img_count, "filler images' average RGB value calculated")
    if args.verbose: time.sleep(sdelay)

def avg_rgb_main_image_blocks():
    print ("\nSTEP 6 -->    Finding the average RGB value of each main image block")
    if args.verbose: time.sleep(sdelay)
    
    total_img_count = 0
    count = 0
    
    for infile in glob.glob('./main_image_blocks/*.jpg'):
        total_img_count += 1
    for i in range(0, biar):
        for j in range(0, biac):
            main_img_block = cv2.imread('./main_image_blocks/{}.jpg'.format(str(j)+'_'+str(i)), 1)
            sum_red = 0            
            sum_green = 0                      
            sum_blue = 0
            pixel_count = 0
            for p in range(main_img_block.shape[0]):
                for q in range(main_img_block.shape[1]):
                    temp_red, temp_green, temp_blue = main_img_block[p][q][2], main_img_block[p][q][1], main_img_block[p][q][0] #opencv loads images in BGR by default
                    sum_red += temp_red
                    sum_green += temp_green
                    sum_blue += temp_blue
                    pixel_count += 1
            avg_red = sum_red/pixel_count
            avg_green = sum_green/pixel_count
            avg_blue = sum_blue/pixel_count
            main_img_block_details.append({
                'file_name': str(j)+'_'+str(i),
                'avg_red': avg_red,
                'avg_green': avg_green,
                'avg_blue': avg_blue
                })
            count += 1
            if args.verbose: print ("STEP 6 -->    ", count, '/', total_img_count, "main image blocks' average RGB value calculated")
    if args.verbose: time.sleep(sdelay)

def image_match():
    print ('\nSTEP 7 -->    Finding the matching filler images for the main image blocks based on the average RGB values')
    os.mkdir('matched_images')
    if args.verbose: time.sleep(sdelay)

    total_img_count = 0
    count = 0

    for infile in glob.glob('./main_image_blocks/*.jpg'):
        total_img_count += 1
    for i in main_img_block_details:
        count += 1
        distance = 1000
        flag = 0
        for j in filler_img_details:
            distance_candidate = (((i['avg_red']-j['avg_red'])**2)+((i['avg_green']-j['avg_green'])**2)+((i['avg_blue']-j['avg_blue'])**2)) ** 0.5
            if distance_candidate < distance:
                distance = distance_candidate
                if flag == 1:
                    matched_images.pop()
                matched_images.append({
                    'main_img_block_name': i['file_name'],
                    'matched_filler_img_name': j['file_name']
                    })
                flag = 1
        if args.verbose: print ("STEP 7 -->    ", count, '/', total_img_count, "blocks of the main image matched")

    for data in matched_images:
        img = cv2.imread("./resized_filler_images/{}.jpg".format(data['matched_filler_img_name']), 1)
        cv2.imwrite("./matched_images/{}.jpg".format(data['main_img_block_name']), img)
    if args.verbose: time.sleep(sdelay)

def image_stitch():
    print ('\nSTEP 8 -->    Stitching the matched filler images to form the final photomosaic')
    if args.verbose: time.sleep(sdelay)

    row = []
    count = 0
    total_img_count = 0
    temp_img = []
    for i in glob.glob("./matched_images/*.jpg"):
        total_img_count += 1
    for i in range(0, biac):
        for j in range(0, biar):
            img = cv2.imread("./matched_images/{}.jpg".format(str(i)+'_'+str(j)), 1)
            row.append(img)
            count += 1
            if args.verbose: print ("STEP 8 -->    ", count, '/', total_img_count, "images stitched")
        temp_img.append(np.hstack(row))
        row = []
    photomosaic = np.vstack(temp_img)
    cv2.imwrite ("mosaic_{}.jpg".format(datetime.today().strftime("%Y%m%d_%H%M%S")), photomosaic)
    if args.verbose: time.sleep(sdelay)

def remove_temp_files():
    try:
        if args.verbose: print ("Deleting temporary 'main_image_blocks' folder")
        shutil.rmtree("main_image_blocks")
    except Exception as e:
        if args.verbose: print (e)
    if args.verbose: time.sleep(sdelay)

    try:
        if args.verbose: print ("Deleting temporary 'renamed_filler_images' folder")
        shutil.rmtree("renamed_filler_images")
    except Exception as e:
        if args.verbose: print (e)
    if args.verbose: time.sleep(sdelay)

    try:
        if args.verbose: print ("Deleting temporary 'cropped_filler_images' folder")
        shutil.rmtree("cropped_filler_images")
    except Exception as e:
        if args.verbose: print (e)
    if args.verbose: time.sleep(sdelay)

    try:
        if args.verbose: print ("Deleting temporary 'resized_filler_images' folder")
        shutil.rmtree("resized_filler_images")
    except Exception as e:
        if args.verbose: print (e)
    if args.verbose: time.sleep(sdelay)

    try:
        if args.verbose: print ("Deleting temporary 'matched_images' folder")
        shutil.rmtree("matched_images")
    except Exception as e:
        if args.verbose: print (e)
    if args.verbose: time.sleep(sdelay)


initialise()
split_main_image()
rename_filler_images()
crop_filler_images()
resize_filler_images()
avg_rgb_filler_images()
avg_rgb_main_image_blocks()
image_match()
image_stitch()
if args.visibility == False: remove_temp_files()

print ("\nDONE")