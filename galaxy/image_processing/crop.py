import sys
import numpy as np
import imageio
from PIL import Image

# Init input parameters
img = sys.argv[1] # Image to be proccessed
start_x = int(sys.argv[2])
start_y = int(sys.argv[3])
crop_x = int(sys.argv[4]) 
crop_y = int(sys.argv[5]) 
output_file = sys.argv[6] # Output file to be written

image = imageio.v2.imread(img)
im = Image.fromarray((image[start_y:start_y + crop_y, start_x:start_x + crop_x, :]).astype(np.uint8))

# Saving result to the output file
image_bytes = imageio.v2.imwrite(output_file, im, "jpg")


