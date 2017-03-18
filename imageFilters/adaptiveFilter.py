
import sys
import os
import numpy
from PIL import Image
from PyQt5.QtCore import QCoreApplication
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

def adpmedf(image, size, window, threshold=0):
    ## set filter window and image dimensions
    W = 2*window + 1
    xlength, ylength = size
    vlength = W*W

    ## create 2-D image array and initialize window
    imageArray = numpy.reshape(numpy.array(image, dtype=numpy.uint8), (ylength, xlength))
    filterWindow = numpy.array(numpy.zeros((W, W)))
    targetVector = numpy.array(numpy.zeros(vlength))
    pixelCount = 0

    ## loop over image with specified window W
    for y in range(window, ylength-(window+1)):
        QCoreApplication.processEvents()
        for x in range(window, xlength-(window+1)):
        ## populate window, sort, find median
            filterWindow = imageArray[y-window:y+window+1, x-window:x+window+1]
            targetVector = numpy.reshape(filterWindow, ((vlength),))
            ## internal sort
            median = getMedian(targetVector, vlength)
        ## check for threshold
            if not threshold > 0:
                imageArray[y, x] = median
                pixelCount += 1
            else:
                scale = numpy.zeros(vlength)
                for n in range(vlength):
                    scale[n] = abs(int(targetVector[n]) - int(median))
                scale = numpy.sort(scale)
                Sk = 1.4826 * (scale[int(vlength/2)])
                if abs(int(imageArray[y, x]) - int(median)) > (threshold * Sk):
                    imageArray[y, x] = median
                    pixelCount += 1
    return Image.fromarray(imageArray)

def getMedian(targetArray, arrayLength):
    sorted_array = numpy.sort(targetArray)
    median = sorted_array[int(arrayLength/2)]
    return median

def adaptiveMedianFilter(colorModelTag, currentImageChannelIndex, img, filterSize,
        isBinarization=False, threshold=0):
    if isBinarization:
        img = img.convert(mode='L')
        img = adpmedf(img, img.size, filterSize, threshold)
    else:
        r, g, b = img.split()
        r = adpmedf(r, img.size, filterSize, threshold)
        g = adpmedf(g, img.size, filterSize, threshold)
        b = adpmedf(b, img.size, filterSize, threshold)
        img = Image.merge("RGB", (r, g, b))
    return img
