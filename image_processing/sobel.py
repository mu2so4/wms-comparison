import sys
import numpy as np
import imageio
from scipy import ndimage
from PIL import Image

# Init input parameters
img = sys.argv[1] # Image to be proccessed
output_file = sys.argv[2] # Output file to be written

image = imageio.v2.imread(img)
im = image.astype('int32')
dx = ndimage.sobel(im, 0)  # horizontal derivative
dy = ndimage.sobel(im, 1)  # vertical derivative
mag = np.hypot(dx, dy)  # magnitude
result = mag * 255.0 / np.max(mag)  # normalize (Q&D)
im = Image.fromarray(result.astype(np.uint8))

# Saving result to the output file
image_bytes = imageio.v2.imwrite(output_file, im, "jpg")


