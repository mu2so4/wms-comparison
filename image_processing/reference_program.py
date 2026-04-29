from os import walk
import time 
import numpy as np
from PIL import Image    #  pip install Pillow
import imageio
from scipy import ndimage

write_all_files = True

f = []
for (dirpath, dirnames, filenames) in walk("/home/ilya/Projects/WMSs/image_processing_input_data"):
    f.extend(filenames)
    break

start_x = 464
start_y = 193
crop_x = 169
crop_y = 154
thresh = 50

heights = []

start = time.time()
for filename in filenames:
    image = imageio.v2.imread(f'/home/ilya/Projects/WMSs/image_processing_input_data/{filename}')
    im = (image[start_y:start_y + crop_y, start_x:start_x + crop_x, :]).astype('int32')
    if (write_all_files):
        imageio.v2.imwrite("./output/crop_" + filename, im, "jpg")
    #im = im.astype('int32')
    dx = ndimage.sobel(im, 0)  # horizontal derivative
    dy = ndimage.sobel(im, 1)  # vertical derivative
    mag = np.hypot(dx, dy)  # magnitude
    im = mag * 255.0 / np.max(mag)  # normalize (Q&D)
    if (write_all_files):
        imageio.v2.imwrite("./output/sobel_" + filename, im, "jpg")
    max_val = 255
    im_bin = ((im > thresh) * max_val).astype(np.uint8)
    if (write_all_files):
        imageio.v2.imwrite("./output/binarize_" + filename, im_bin, "jpg")
    (w, h, c) = im_bin.shape
    border_color = [0, 255, 247]
    h_max = 0
    h_min = 10000
    for i in range(w):
        for j in range(h):
            if im_bin[i, j, 0] != 0:
                if i > h_max:
                    h_max = i
                if i < h_min:
                    h_min = i
    for j in range(h):
        if (h_min != 10000 and h_max != 0):
            im_bin[h_max, j] = border_color
            im_bin[h_min, j] = border_color
    height = h_max - h_min
    heights.append([filename, height])
    if (write_all_files):
        imageio.v2.imwrite("./output/height_" + filename, im_bin, "jpg")


end = time.time() - start ## собственно время работы программы

print(end) ## вывод времени
print(heights)
