"""
    @package meanFilter
    Add mean filter to image
"""

import threading
import multiprocessing
import math
import numpy
from PIL import Image
from PyQt5.QtCore import QCoreApplication

import apertureService

def meanFilter(pixels, imgSize, filterSize):
    apertures = apertureService.getApertureMatrixGenerator(imgSize, filterSize)
    # for index, aperture in enumerate(apertures):
    for x, y, aperture in apertures:
        rSum = gSum = bSum = kSum = 0
        # print(x, y)
        print(aperture)
        for apertureLine in aperture:
            for apertureCoordinate in apertureLine:
                pixelPosX, pixelPosY = apertureCoordinate
                red, green, blue = pixels[pixelPosX, pixelPosY]

                rSum += red
                gSum += green
                bSum += blue

                kSum += 1

        if kSum <= 0: kSum = 1

        rSum /= kSum
        if rSum < 0: rSum = 0
        if rSum > 255: rSum = 255

        gSum /= kSum
        if gSum < 0: gSum = 0
        if gSum > 255: gSum = 255

        bSum /= kSum
        if bSum < 0: bSum = 0
        if bSum > 255: bSum = 255

        for apertureLine in aperture:
            for apertureCoordinate in apertureLine:
                pixelPosX, pixelPosY = apertureCoordinate
                pixels[pixelPosX, pixelPosY] = (int(rSum), int(gSum), int(bSum))

img = Image.open('test.png')
img = img.convert(mode='RGB')
img.show()
meanFilter(img.load(), img.size, (3, 3))
img.show()
