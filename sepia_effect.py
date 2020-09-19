# Import the dependencies
import argparse
from PIL import Image, ImageDraw
from tqdm import tqdm
def get_pixel(image, i, j):
    width, height = image.size
    if i > width or j > height: # If dimensions are in bounds
        return None
    # Get Pixel
    pixel = image.getpixel((i, j))
    return pixel

def get_max(value):
    if value > 255:  # Limit maximum value to 255
        return 255
    return int(value)

def create_image(i, j):
    image = Image.new("RGB", (i, j), "white")
    return image

def get_sepia_pixel(red, green, blue, alpha):
    tRed = get_max((0.759 * red) + (0.398 * green) + (0.194 * blue))
    tGreen = get_max((0.676 * red) + (0.354 * green) + (0.173 * blue))
    tBlue = get_max((0.524 * red) + (0.277 * green) + (0.136 * blue))
    # Return sepia color
    return tRed, tGreen, tBlue, alpha

def convert_sepia(image):
    # Get size
    width, height = image.size
    # Create new Image and a Pixel Map
    new = create_image(width, height)
    pixels = new.load()
    # Convert each pixel to sepia
    for i in tqdm(range(0, width, 1)):
        for j in range(0, height, 1):
            p = get_pixel(image, i, j)
            pixels[i, j] = get_sepia_pixel(p[0], p[1], p[2], 255)
    # Return new image
    return new


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
args = vars(ap.parse_args())

# reading the image
img = Image.open((args["image"]))
# Convert to sepia
sepia_img = convert_sepia(img)
# Save the  image
sepia_img.save('assets/sepia_effect.jpg', 'JPEG')
