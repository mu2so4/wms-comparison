import sys
import numpy as np
import imageio
from scipy import ndimage
from PIL import Image

# Init input parameters
img = sys.argv[1] # Image to be proccessed
output_file = sys.argv[2] # Output file to be written

image = imageio.v2.imread(img)

# Saving result to the output file
imageio.v2.imwrite(output_file, image, "jpg")


