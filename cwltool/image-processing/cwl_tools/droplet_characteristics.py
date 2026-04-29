import numpy as np
import imageio
import sys
from PIL import Image
from scipy import ndimage

# Init input parameters
img = sys.argv[1] 
start_x = int(sys.argv[2])
start_y = int(sys.argv[3])
crop_x = int(sys.argv[4]) 
crop_y = int(sys.argv[5]) 
thresh = int(sys.argv[6]) 
output_value = sys.argv[7] 
output_image = sys.argv[8] 

image = imageio.v2.imread(img)
im = (image[start_y:start_y + crop_y, start_x:start_x + crop_x, :]).astype('int32')
dx = ndimage.sobel(im, 0)  # horizontal derivative
dy = ndimage.sobel(im, 1)  # vertical derivative
mag = np.hypot(dx, dy)  # magnitude
result = mag * 255.0 / np.max(mag)  # normalize (Q&D)
im = result.astype(np.uint8)
max_val = 255
im = ((im > thresh) * max_val).astype(np.uint8)
(w, h, c) = im.shape
border_color = [0, 255, 247]
h_max = 0
h_min = 10000
for i in range(w):
    for j in range(h):
        if im[i, j, 0] != 0:
            if i > h_max:
                h_max = i
            if i < h_min:
                h_min = i
for j in range(h):
    if (h_min != 10000 and h_max != 0):
        im[h_max, j] = border_color
        im[h_min, j] = border_color

height = h_max - h_min
im = Image.fromarray(im.astype(np.uint8))

# Saving result to the output file
imageio.v2.imwrite(output_image, im, "jpg")

output_value_file = open(output_value, "w")
output_value_file.write(str(height))
output_value_file.close()