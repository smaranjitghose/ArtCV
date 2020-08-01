
# Import the dependencies
import argparse
from PIL import Image, ImageDraw


def get_pixel(image, i, j):
    width, height = image.size
    if i > width or j > height:  # If dimensions are in bounds
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


def color_average(image, i0, j0, i1, j1):
    # Colors
    red, green, blue, alpha = 0, 0, 0, 255
    # Get size
    width, height = image.size
    # Check size restrictions for width
    i_start, i_end = i0, i1
    if i0 < 0:
        i_start = 0
    if i1 > width:
        i_end = width
    # Check size restrictions for height
    j_start, j_end = j0, j1
    if j0 < 0:
        j_start = 0
    if j1 > height:
        j_end = height
    # Discard half the pixels we are comparing to increase speed
    count = 0
    for i in range(i_start, i_end - 2, 2):
        for j in range(j_start, j_end - 2, 2):
            count += 1
            p = get_pixel(image, i, j)
            red, green, blue = p[0] + red, p[1] + green, p[2] + blue

    # Set color average
    red /= count
    green /= count
    blue /= count
    # Return color average
    return int(red), int(green), int(blue), alpha


def convert_pointilize(image):
    # Get size
    width, height = image.size
    # Radius
    radius = 6
    # Intentional error on the positionning of dots to create a wave-like effect
    count = 0
    errors = [1, 0, 1, 1, 2, 3, 3, 1, 2, 1]
    # Create new Image
    new = create_image(width, height)
    # The ImageDraw module provide simple 2D graphics for Image objects
    draw = ImageDraw.Draw(new)
    # Draw circles
    for i in range(0, width, radius+3):
        for j in range(0, height, radius+3):
            # Get the color average
            color = color_average(image, i-radius, j -
                                  radius, i+radius, j+radius)

            # Set error in positions for I and J
            eI = errors[count % len(errors)]
            count += 1
            eJ = errors[count % len(errors)]
            # Create circle
            draw.ellipse((i-radius+eI, j-radius+eJ, i +
                          radius+eI, j+radius+eJ), fill=(color))

    # Return new image
    return new

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
args = vars(ap.parse_args())

# reading the image
img = Image.open((args["image"]))
# Apply Pointilism
sepia_img = convert_pointilize(img)
# Save the  image
sepia_img.save('assets/pointilism.jpg', 'JPEG')
