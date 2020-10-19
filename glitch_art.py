import os
import argparse
from PIL import Image
import numpy as np 
import math
from tqdm import tqdm

# generating a random number for dividing the image's height
def gen_divisors(n):
  for i in range(2, math.floor(math.sqrt(n))):
    if n % i == 0:
      yield i

# generating the extedned padded image
def pad_to_square(imgobj):    
      """Pad to the nearest 100th"""
      square = Image.new('RGB', ((imgobj.width // 100 + 1) * 100,(imgobj.height // 100 + 1) * 100), (0, 0, 0))
      # pasting the original image object over the extended black padded background and returning it
      square.paste(imgobj, imgobj.getbbox())
      return square

# the function returns the glitched image with given step size
def pixel_sort(imgobj, step_size=8):
      # padding the image to transform into square
      padded = pad_to_square(imgobj)
      # image to array
      data = np.array(padded)
      # dividing the image into stripes
      stripes = np.split(data, data.shape[0] // step_size, axis=0)
      sorted_data = []
      # sort by rows
      for stripe in tqdm(stripes):
        sorted_data.append(np.sort(stripe, axis=0))
      sorted_arr = np.array(sorted_data)
      # shaping the sorted array into the padded image shape
      sorted_arr = sorted_arr.reshape(padded.height, padded.width, 3)
      # remove padding
      sorted_arr = sorted_arr[:imgobj.height, :imgobj.width, :]  
      # generating image from array
      return Image.fromarray(sorted_arr)

def glitch_image(fname):
      """
      Return a glitched image object
      """
      orginal, step_size = None, None
      original = Image.open(fname)
      # randomly generate a step size that divides the image's height
      divisors = list(gen_divisors(original.height))
      # randomly choosing the index for divisors
      idx = np.random.choice(len(divisors))
      step_size = divisors[idx]
      try:
        return pixel_sort(original, step_size=step_size)      
      except:
        print('Dimension errors processing ' + fname + ' Please try again.')
        return None

def main():
      parser = argparse.ArgumentParser()
      parser.add_argument('-f', '--file', type=str)
      args = parser.parse_args()
      glitched = glitch_image(args.file)
      if glitched is not None:
        glitched.show()
        dirname, fname = os.path.split(args.file)
        glitched.save(dirname + '/glitched_' + fname)
          
if __name__ == '__main__':
  main()
