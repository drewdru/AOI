"""
    @package imageMorphology
    Morphology image processing
"""
import math
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

from imageFilters import apertureService
from PyQt5.QtCore import QCoreApplication

def dilation(colorModelTag, currentImageChannelIndex, pixels, imgSize, mask, maskSize, tempPixels):
    apertures = apertureService.getApertureMatrixGenerator(imgSize, maskSize)
    for x, y, aperture in apertures:
        QCoreApplication.processEvents()
        rMax = gMax = bMax = 0
        for i, apertureLine in enumerate(aperture):
            for j, apertureCoordinate in enumerate(apertureLine):
                pixelPosX, pixelPosY = apertureCoordinate
                red, green, blue = pixels[pixelPosX, pixelPosY]
                if mask[i][j]:
                    if red > rMax: rMax = red
                    if green > gMax: gMax = green
                    if blue > bMax: bMax = blue
        aperturePosX = int(len(aperture)/2)
        aperturePosY = int(len(aperture[aperturePosX])/2)
        oldColors = pixels[aperture[aperturePosX][aperturePosY]]
        if currentImageChannelIndex == 0:
            tempPixels[aperture[aperturePosX][aperturePosY]] = (
                rMax, gMax, bMax)
        if currentImageChannelIndex == 1:
            tempPixels[aperture[aperturePosX][aperturePosY]] = (
                rMax, oldColors[1], oldColors[2])
        if currentImageChannelIndex == 2:
            tempPixels[aperture[aperturePosX][aperturePosY]] = (
                oldColors[0], gMax, oldColors[2])
        if currentImageChannelIndex == 3:
            tempPixels[aperture[aperturePosX][aperturePosY]] = (
                oldColors[0], oldColors[1], bMax)


def erosion(colorModelTag, currentImageChannelIndex, pixels, imgSize, mask, maskSize, tempPixels):
    apertures = apertureService.getApertureMatrixGenerator(imgSize, maskSize)
    for x, y, aperture in apertures:
        QCoreApplication.processEvents()
        rMax = gMax = bMax = 255
        for i, apertureLine in enumerate(aperture):
            for j, apertureCoordinate in enumerate(apertureLine):
                pixelPosX, pixelPosY = apertureCoordinate
                red, green, blue = pixels[pixelPosX, pixelPosY]
                if mask[i][j]:
                    if red < rMax: rMax = red
                    if green < gMax: gMax = green
                    if blue < bMax: bMax = blue
        aperturePosX = int(len(aperture)/2)
        aperturePosY = int(len(aperture[aperturePosX])/2)
        oldColors = pixels[aperture[aperturePosX][aperturePosY]]
        if currentImageChannelIndex == 0:
            tempPixels[aperture[aperturePosX][aperturePosY]] = (
                rMax, gMax, bMax)
        if currentImageChannelIndex == 1:
            tempPixels[aperture[aperturePosX][aperturePosY]] = (
                rMax, oldColors[1], oldColors[2])
        if currentImageChannelIndex == 2:
            tempPixels[aperture[aperturePosX][aperturePosY]] = (
                oldColors[0], gMax, oldColors[2])
        if currentImageChannelIndex == 3:
            tempPixels[aperture[aperturePosX][aperturePosY]] = (
                oldColors[0], oldColors[1], bMax)
