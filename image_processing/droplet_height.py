import sys
import numpy as np
import imageio
from PIL import Image

# Init input parameters
img = sys.argv[1] # Image to be proccessed
output_value = sys.argv[2] 
output_image = sys.argv[3] 

image = imageio.v2.imread(img)
(w, h, c) = image.shape
border_color = [0, 255, 247]
h_max = 0
h_min = 10000
for i in range(w):
    for j in range(h):
        if image[i, j, 0] != 0:
            if i > h_max:
                h_max = i
            if i < h_min:
                h_min = i
for j in range(h):
    if (h_min != 10000 and h_max != 0):
        image[h_max, j] = border_color
        image[h_min, j] = border_color

height = h_max - h_min
im = Image.fromarray(image.astype(np.uint8))

# Saving result to the output file
imageio.v2.imwrite(output_image, im, "jpg")

output_value_file = open(output_value, "w")
output_value_file.write(str(height))
output_value_file.close()


