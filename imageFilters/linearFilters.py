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

from . import apertureService

def meanFilter(pixels, imgSize, filterSize):
    """ mean filter || homogeneous smoothing || box filter"""
    apertures = apertureService.getApertureMatrixGenerator(imgSize, filterSize)
    # print(apertures, imgSize, filterSize)
    # for index, aperture in enumerate(apertures):
    for x, y, aperture in apertures:
        QCoreApplication.processEvents()
        rSum = gSum = bSum = kSum = 0
        # print(x, y)
        # print(aperture)
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

def medianFilter(pixels, imgSize, filterSize):
    apertures = apertureService.getApertureMatrixGenerator(imgSize, filterSize)
    flagX = 0
    flagY = 0
    for x, y, aperture in apertures:
        QCoreApplication.processEvents()
        redList = []
        greenList = []
        blueList = []
        for apertureLine in enumerate(aperture):
            for apertureCoordinate in apertureLine:
                pixelPosX, pixelPosY = apertureCoordinate
                red, green, blue = pixels[pixelPosX, pixelPosY]

                redList.append(red)
                greenList.append(green)
                blueList.append(blue)

        redList.sort()
        greenList.sort()
        blueList.sort()

        rValue = redList[int(len(redList)/2)]
        gValue = greenList[int(len(redList)/2)]
        bValue = blueList[int(len(redList)/2)]

        for apertureLine in aperture:
            for apertureCoordinate in apertureLine:
                pixelPosX, pixelPosY = apertureCoordinate
                pixels[pixelPosX, pixelPosY] = (int(rValue), int(gValue), int(bValue))
