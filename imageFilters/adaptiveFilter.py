
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import random
from PIL import Image
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))
import apertureService


def PIL2array(img):
    return np.array(img.getdata(),
                    np.uint8).reshape(img.size[1], img.size[0], 3)

def array2PIL(arr, size):
    mode = 'RGBA'
    arr = arr.reshape(arr.shape[0]*arr.shape[1], arr.shape[2])
    if len(arr[0]) == 3:
        arr = np.c_[arr, 255*np.ones((len(arr),1), np.uint8)]
    return Image.frombuffer(mode, size, arr.tostring(), 'raw', mode, 0, 1)

def adpmedf(image, size, window, threshold):
    
    ## set filter window and image dimensions
    W = 2*window + 1
    xlength, ylength = size
    vlength = W*W

    print(np.array(image, dtype=np.uint8), (ylength,xlength))
    
    ## create 2-D image array and initialize window
    image_array = np.reshape(np.array(image, dtype=np.uint8), (ylength,xlength))
    filter_window = np.array(np.zeros((W,W)))
    target_vector = np.array(np.zeros(vlength))
    pixel_count = 0
    ## loop over image with specified window W
    for y in range(window, ylength-(window+1)):
        for x in range(window, xlength-(window+1)):
        ## populate window, sort, find median
            filter_window = image_array[y-window:y+window+1,x-window:x+window+1]
            target_vector = np.reshape(filter_window, ((vlength),))
            ## internal sort
            median = demo(target_vector, vlength)
            ##median = medians_1D.quick_select(target_vector, vlength)
        ## check for threshold
            if not threshold > 0:
                image_array[y,x] = median
                pixel_count += 1
            else:
                scale = np.zeros(vlength)
                for n in range(vlength):
                    scale[n] = abs(int(target_vector[n]) - int(median))
                scale = np.sort(scale)
                Sk = 1.4826 * (scale[int(vlength/2)])
                if abs(int(image_array[y,x]) - int(median)) > (threshold * Sk):
                    image_array[y,x] = median
                    pixel_count += 1
    return Image.fromarray(image_array)

def demo(target_array, array_length):
    sorted_array = np.sort(target_array)
    # print(target_array, array_length)
    median = sorted_array[int(array_length/2)]
    return median

img = Image.open('./test3.jpg')
img = img.convert(mode='L')
img.show()

img = adpmedf(img, img.size, 3, 0)

# Convert array to Image
# img = Image.fromarray(arr)
img.show()
