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
    for x, y, aperture in apertures:
        QCoreApplication.processEvents()
        rSum = gSum = bSum = kSum = 0
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

        aperturePosX = int(len(aperture)/2)
        aperturePosY = int(len(aperture[aperturePosX])/2)
        pixels[aperture[aperturePosX][aperturePosY]] = (int(rSum), int(gSum), int(bSum))

def medianFilter(pixels, imgSize, filterSize):
    apertures = apertureService.getApertureMatrixGenerator(imgSize, filterSize)
    # flagX = 0
    # flagY = 0
    for x, y, aperture in apertures:
        QCoreApplication.processEvents()
        redList = []
        greenList = []
        blueList = []
        for apertureLine in aperture:
            for apertureCoordinate in apertureLine:
                pixelPosX, pixelPosY = apertureCoordinate
                red, green, blue = pixels[pixelPosX, pixelPosY]

                redList.append(red)
                greenList.append(green)
                blueList.append(blue)

        redList.sort()
        greenList.sort()
        blueList.sort()

        apertureCenter = int(len(redList)/2)
        rValue = redList[apertureCenter]
        gValue = greenList[apertureCenter]
        bValue = blueList[apertureCenter]

        aperturePosX = int(len(aperture)/2)
        aperturePosY = int(len(aperture[aperturePosX])/2)
        pixels[aperture[aperturePosX][aperturePosY]] = (int(rValue), int(gValue), int(bValue))

def gaussian(x, sigma):
    return (1.0 / (2 * math.pi * (sigma ** 2))) * math.exp(- (x ** 2) / (2 * sigma ** 2))

def gaussianBlur(pixels, imgSize, filterSize):#, r):
    """ mean filter || homogeneous smoothing || box filter"""
    apertures = apertureService.getApertureMatrixGenerator(imgSize, filterSize)
    sigma = 0.5
    for x, y, aperture in apertures:
        QCoreApplication.processEvents()
        rSum = gSum = bSum = kSum = 0
        for i, apertureLine in enumerate(aperture):
            for apertureCoordinate in apertureLine:
                pixelPosX, pixelPosY = apertureCoordinate
                red, green, blue = pixels[pixelPosX, pixelPosY]

                # double kernelVal = blurArray[i][j];
                kernelVal = gaussian(i, sigma)

                rSum += red * kernelVal
                gSum += green * kernelVal
                bSum += blue * kernelVal

                kSum += kernelVal

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

        aperturePosX = int(len(aperture)/2)
        if (len(aperture) != 0 and len(aperture[aperturePosX])/2 != 0):
            aperturePosY = int(len(aperture[aperturePosX])/2)
            pixels[aperture[aperturePosX][aperturePosY]] = (int(rSum), int(gSum), int(bSum))






# def apply_bilateral_filter(source, filtered_image, x, y, diameter, sigma_i, sigma_s):
#     hl = diameter/2
#     i_filtered = 0
#     Wp = 0
#     i = 0
#     while i < diameter:
#         j = 0
#         while j < diameter:
#             neighbour_x = x - (hl - i)
#             neighbour_y = y - (hl - j)
#             if neighbour_x >= len(source):
#                 neighbour_x -= len(source)
#             if neighbour_y >= len(source[0]):
#                 neighbour_y -= len(source[0])
#             gi = gaussian(source[neighbour_x][neighbour_y] - source[x][y], sigma_i)
#             gs = gaussian(distance(neighbour_x, neighbour_y, x, y), sigma_s)
#             w = gi * gs
#             i_filtered += source[neighbour_x][neighbour_y] * w
#             Wp += w
#             j += 1
#         i += 1
#     i_filtered = i_filtered / Wp
#     filtered_image[x][y] = int(round(i_filtered))


# def bilateral_filter_own(source, filter_diameter, sigma_i, sigma_s):
#     filtered_image = np.zeros(source.shape)

#     i = 0
#     while i < len(source):
#         j = 0
#         while j < len(source[0]):
#             apply_bilateral_filter(source, filtered_image, i, j, filter_diameter, sigma_i, sigma_s)
#             j += 1
#         i += 1
# return filtered_image