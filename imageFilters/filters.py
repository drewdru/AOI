"""
    @package linearFilters
    Linear filters for images
"""

import threading
import multiprocessing
import math
import numpy
from PIL import Image
from PyQt5.QtCore import QCoreApplication

from . import apertureService

def meanFilter(colorModelTag, currentImageChannelIndex, pixels, imgSize, filterSize):
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

        oldColors = pixels[aperture[aperturePosX][aperturePosY]]
        if currentImageChannelIndex == 0:
            pixels[aperture[aperturePosX][aperturePosY]] = (int(rSum), int(gSum), int(bSum))
        if currentImageChannelIndex == 1:
            pixels[aperture[aperturePosX][aperturePosY]] = (int(rSum), oldColors[1], oldColors[2])
        if currentImageChannelIndex == 2:
            pixels[aperture[aperturePosX][aperturePosY]] = (oldColors[0], int(gSum), oldColors[2])
        if currentImageChannelIndex == 3:
            pixels[aperture[aperturePosX][aperturePosY]] = (oldColors[0], oldColors[1], int(bSum))

def medianFilter(colorModelTag, currentImageChannelIndex, pixels, imgSize, filterSize):
    apertures = apertureService.getApertureMatrixGenerator(imgSize, filterSize)
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

        oldColors = pixels[aperture[aperturePosX][aperturePosY]]
        if currentImageChannelIndex == 0:
            pixels[aperture[aperturePosX][aperturePosY]] = (int(rValue), int(gValue), int(bValue))
        if currentImageChannelIndex == 1:
            pixels[aperture[aperturePosX][aperturePosY]] = (int(rValue), oldColors[1], oldColors[2])
        if currentImageChannelIndex == 2:
            pixels[aperture[aperturePosX][aperturePosY]] = (oldColors[0], int(gValue), oldColors[2])
        if currentImageChannelIndex == 3:
            pixels[aperture[aperturePosX][aperturePosY]] = (oldColors[0], oldColors[1], int(bValue))

def gaussian(x, sigma):
    return (1.0 / (2 * math.pi * (sigma ** 2))) \
        * math.exp(- (x ** 2) / (2 * sigma ** 2))

def gaussianBlur(colorModelTag, currentImageChannelIndex, pixels, imgSize, filterSize):#, r):
    """ Gaussian blur"""
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
        if len(aperture) != 0 and len(aperture[aperturePosX])/2 != 0:
            aperturePosY = int(len(aperture[aperturePosX])/2)
            oldColors = pixels[aperture[aperturePosX][aperturePosY]]
            if currentImageChannelIndex == 0:
                pixels[aperture[aperturePosX][aperturePosY]] = (int(rSum), int(gSum), int(bSum))
            if currentImageChannelIndex == 1:
                pixels[aperture[aperturePosX][aperturePosY]] = (int(rSum), oldColors[1], oldColors[2])
            if currentImageChannelIndex == 2:
                pixels[aperture[aperturePosX][aperturePosY]] = (oldColors[0], int(gSum), oldColors[2])
            if currentImageChannelIndex == 3:
                pixels[aperture[aperturePosX][aperturePosY]] = (oldColors[0], oldColors[1], int(bSum))

def distance(x, y, i, j):
    return math.sqrt((x-i)**2 + (y-j)**2)

def bilateralFilter(colorModelTag, currentImageChannelIndex, pixels, imgSize, filterSize, sigma_i, sigma_s):
    """ Bilateral filter """
    apertures = apertureService.getApertureMatrixGenerator(imgSize, filterSize)
    # sigma_i = 12.5
    # sigma_s = 16.5
    for x, y, aperture in apertures:
        QCoreApplication.processEvents()
        filteredRed = WpRed = filteredGreen = WpGreen = filteredBlue = WpBlue = 0
        for i, apertureLine in enumerate(aperture):
            for apertureCoordinate in apertureLine:
                pixelPosX, pixelPosY = apertureCoordinate
                red, green, blue = pixels[pixelPosX, pixelPosY]
                xyRed, xyGreen, xyBlue = pixels[x, y]

                giRed = gaussian(red - xyRed, sigma_i)
                gsRed = gaussian(distance(pixelPosX, pixelPosY, x, y), sigma_s)
                wRed = giRed * gsRed
                filteredRed += red * wRed
                WpRed += wRed

                giGreen = gaussian(green - xyGreen, sigma_i)
                gsGreen = gaussian(distance(pixelPosX, pixelPosY, x, y), sigma_s)
                wGreen = giGreen * gsGreen
                filteredGreen += green * wGreen
                WpGreen += wGreen

                giBlue = gaussian(blue - xyBlue, sigma_i)
                gsBlue = gaussian(distance(x, y, pixelPosX, pixelPosY), sigma_s)
                wBlue = giBlue * gsBlue
                filteredBlue += blue * wBlue
                WpBlue += wBlue
        filteredRed = int(round(filteredRed / WpRed))
        filteredGreen = int(round(filteredGreen / WpGreen))
        filteredBlue = int(round(filteredBlue / WpBlue))

        aperturePosX = int(len(aperture)/2)
        aperturePosY = int(len(aperture[aperturePosX])/2)
        if len(aperture) != 0 and aperturePosY != 0:
            oldColors = pixels[aperture[aperturePosX][aperturePosY]]
            if currentImageChannelIndex == 0:
                pixels[aperture[aperturePosX][aperturePosY]] = (filteredRed, filteredGreen, filteredBlue)
            if currentImageChannelIndex == 1:
                pixels[aperture[aperturePosX][aperturePosY]] = (filteredRed, oldColors[1], oldColors[2])
            if currentImageChannelIndex == 2:
                pixels[aperture[aperturePosX][aperturePosY]] = (oldColors[0], filteredGreen, oldColors[2])
            if currentImageChannelIndex == 3:
                pixels[aperture[aperturePosX][aperturePosY]] = (oldColors[0], oldColors[1], filteredBlue)

def laplacian(x, y, sigma):
    return (-1/(math.pi * (sigma**4))) * \
        (1 - (x**2 + y**2)/(2*(sigma**2))) * \
        math.exp(-(x**2)/(2*(sigma**2)))

def laplacianBlur(colorModelTag, currentImageChannelIndex, pixels, imgSize, filterSize, sigma):
    """ Laplacian blur"""
    # sigma = 2.4
    apertures = apertureService.getApertureMatrixGenerator(imgSize, filterSize)
    for x, y, aperture in apertures:
        QCoreApplication.processEvents()
        rSum = gSum = bSum = kSum = 0
        for i, apertureLine in enumerate(aperture):
            for j, apertureCoordinate in enumerate(apertureLine):
                pixelPosX, pixelPosY = apertureCoordinate
                red, green, blue = pixels[pixelPosX, pixelPosY]

                # double kernelVal = blurArray[i][j];
                kernelVal = laplacian(i, j, sigma)
                # print(kernelVal)
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
        if len(aperture) != 0 and len(aperture[aperturePosX])/2 != 0:
            aperturePosY = int(len(aperture[aperturePosX])/2)
            oldColors = pixels[aperture[aperturePosX][aperturePosY]]
            if currentImageChannelIndex == 0:
                pixels[aperture[aperturePosX][aperturePosY]] = (int(rSum), int(gSum), int(bSum))
            if currentImageChannelIndex == 1:
                pixels[aperture[aperturePosX][aperturePosY]] = (int(rSum), oldColors[1], oldColors[2])
            if currentImageChannelIndex == 2:
                pixels[aperture[aperturePosX][aperturePosY]] = (oldColors[0], int(gSum), oldColors[2])
            if currentImageChannelIndex == 3:
                pixels[aperture[aperturePosX][aperturePosY]] = (oldColors[0], oldColors[1], int(bSum))

def clippingColor(value1, value0, threshold):
    if value1 - value0 <= threshold:
        return value1
    return 0

def suitabilityValue(value1, value0, threshold):
    if value1 - value0 <= threshold:
        return 1
    return 0

def cleanerFilterByJimCasaburi(colorModelTag, currentImageChannelIndex, pixels, imgSize, filterSize, threshold):
    """ Laplacian blur"""
    threshold = 50
    apertures = apertureService.getApertureMatrixGenerator(imgSize, filterSize)
    for x, y, aperture in apertures:
        QCoreApplication.processEvents()
        ccRed = svRed = ccGreen = svGreen = ccBlue = svBlue = 0
        centerRed, centerGreen, centerBlue = pixels[x, y]
        for i, apertureLine in enumerate(aperture):
            for j, apertureCoordinate in enumerate(apertureLine):
                pixelPosX, pixelPosY = apertureCoordinate
                red, green, blue = pixels[pixelPosX, pixelPosY]

                ccRed += clippingColor(red, centerRed, threshold)
                svRed += suitabilityValue(red, centerRed, threshold)

                ccGreen += clippingColor(green, centerGreen, threshold)
                svGreen += suitabilityValue(green, centerGreen, threshold)

                ccBlue += clippingColor(blue, centerBlue, threshold)
                svBlue += suitabilityValue(blue, centerBlue, threshold)
        if svRed != 0:
            R = int(ccRed/svRed)
        else:
            R = centerRed
        if svGreen != 0:
            G = int(ccGreen/svGreen)
        else:
            G = centerGreen
        if svBlue != 0:
            B = int(ccBlue/svBlue)
        else:
            B = centerBlue

        aperturePosX = int(len(aperture)/2)
        if len(aperture) != 0 and len(aperture[aperturePosX])/2 != 0:
            aperturePosY = int(len(aperture[aperturePosX])/2)
            oldColors = pixels[aperture[aperturePosX][aperturePosY]]
            if currentImageChannelIndex == 0:
                pixels[aperture[aperturePosX][aperturePosY]] = (R, G, B)
            if currentImageChannelIndex == 1:
                pixels[aperture[aperturePosX][aperturePosY]] = (R, oldColors[1], oldColors[2])
            if currentImageChannelIndex == 2:
                pixels[aperture[aperturePosX][aperturePosY]] = (oldColors[0], G, oldColors[2])
            if currentImageChannelIndex == 3:
                pixels[aperture[aperturePosX][aperturePosY]] = (oldColors[0], oldColors[1], B)
