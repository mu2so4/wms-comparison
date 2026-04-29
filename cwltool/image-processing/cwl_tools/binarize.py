import sys
import numpy as np
import imageio
from PIL import Image

# Init input parameters
img = sys.argv[1] # Image to be proccessed
thresh_arg = sys.argv[2] # Thresh parameter
output_file = sys.argv[3] # Output file to be written

# Binarization logic
image = imageio.v2.imread(img)
thresh = int(thresh_arg)
max_val = 255
im_bin = Image.fromarray(((image > thresh) * max_val).astype(np.uint8))

# Saving result to the output file
image_bytes = imageio.v2.imwrite("binarize_" + output_file, im_bin, "jpg")

