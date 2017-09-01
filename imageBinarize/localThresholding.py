"""Local thresholding binarize"""
import math
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

from imageFilters import apertureService
from PyQt5.QtCore import QCoreApplication

# Bersen's method
def bernsen(pixels, imgSize, filterSize):
    apertures = apertureService.getApertureMatrixGenerator(imgSize, filterSize)
    for x, y, aperture in apertures:
        QCoreApplication.processEvents()
        minValue = 255
        maxValue = 0

        for apertureLine in aperture:
            for apertureCoordinate in apertureLine:
                pixelPosX, pixelPosY = apertureCoordinate
                if pixels[pixelPosX, pixelPosY] > maxValue:
                    maxValue = pixels[pixelPosX, pixelPosY]
                if pixels[pixelPosX, pixelPosY] < minValue:
                    minValue = pixels[pixelPosX, pixelPosY]
        avg = (minValue + maxValue) / 2

        for apertureLine in aperture:
            for apertureCoordinate in apertureLine:
                pixelPosX, pixelPosY = apertureCoordinate
                if pixels[pixelPosX,pixelPosY] < avg:
                    pixels[pixelPosX,pixelPosY] = 0
                else:
                    pixels[pixelPosX,pixelPosY] = 255

# Niblack's method
def niblack(pixels, imgSize, filterSize, k=0.2):
    apertures = apertureService.getApertureMatrixGenerator(imgSize, filterSize)
    for x, y, aperture in apertures:
        QCoreApplication.processEvents()
        minValue = 255
        maxValue = 0

        for apertureLine in aperture:
            for apertureCoordinate in apertureLine:
                pixelPosX, pixelPosY = apertureCoordinate
                if pixels[pixelPosX, pixelPosY] > maxValue:
                    maxValue = pixels[pixelPosX, pixelPosY]
                if pixels[pixelPosX, pixelPosY] < minValue:
                    minValue = pixels[pixelPosX, pixelPosY]
        avg = (minValue + maxValue) / 2
        RMS = 0
        differenceSum = 0
        for apertureLine in aperture:
            for apertureCoordinate in apertureLine:
                pixelPosX, pixelPosY = apertureCoordinate
                differenceSum = (pixels[pixelPosX, pixelPosY] - avg) ** 2
        RMS += math.sqrt(differenceSum/(filterSize[0]*filterSize[1]))
        value = int(avg + k*RMS)
        for apertureLine in aperture:
            for apertureCoordinate in apertureLine:
                pixelPosX, pixelPosY = apertureCoordinate
                if pixels[pixelPosX, pixelPosY] < value:
                    pixels[pixelPosX, pixelPosY] = 0
                else:
                    pixels[pixelPosX, pixelPosY] = 255

# # Niblack`s method
# def niblack(img, imgSize, filterSize):
#     k = 0.2
#     pixels = img.load()
#     for x in range(imgSize[0]):
#         for y in range(imgSize[1]):
#             minValue = 255
#             maxValue = 0
#             for i in range(filterSize):
#                 for j in range(filterSize):
#                     pixelPosX, pixelPosY = getAperturePosition(x, y, imgSize, i, j, filterSize)
#                     if pixelPosX == -1 or pixelPosY == -1:
#                         continue                  
#                     if pixels[pixelPosX,pixelPosY] > maxValue:
#                         maxValue = pixels[pixelPosX,pixelPosY]
#                     if pixels[pixelPosX,pixelPosY] < minValue:
#                         minValue = pixels[pixelPosX,pixelPosY]
#             avg = (minValue + maxValue) / 2
#             RMS = 0
#             differenceSum = 0
#             for i in range(filterSize):
#                 for j in range(filterSize):
#                     pixelPosX, pixelPosY = getAperturePosition(x, y, imgSize, i, j, filterSize)
#                     if pixelPosX == -1 or pixelPosY == -1:
#                         continue
#                     differenceSum = (pixels[pixelPosX,pixelPosY] - avg) ** 2                    
#             RMS += math.sqrt(differenceSum/filterSize)
#             # value = int(avg + k*RMS)
#             # for i in range(filterSize):
#             #     for j in range(filterSize):
#             #         pixelPosX, pixelPosY = getAperturePosition(x, y, imgSize, i, j, filterSize)
#             #         if pixelPosX == -1 or pixelPosY == -1:
#             #             continue
#             #         pixels[pixelPosX,pixelPosY] = value
#             value = int(avg + k*RMS)
#             for i in range(filterSize):
#                 for j in range(filterSize):
#                     pixelPosX, pixelPosY = getAperturePosition(x, y, imgSize, i, j, filterSize)
#                     if pixelPosX == -1 or pixelPosY == -1:
#                         continue
#                     if pixels[pixelPosX,pixelPosY] < value:
#                         pixels[pixelPosX,pixelPosY] = 0
#                     else:
#                         pixels[pixelPosX,pixelPosY] = 255
#     img.show()

# # Bersen's method
# def bernsen(img, imgSize, filterSize):
#     pixels = img.load()
#     for x in range(imgSize[0]):
#         for y in range(imgSize[1]):
#             minValue = 255
#             maxValue = 0
#             for i in range(filterSize):
#                 for j in range(filterSize):
#                     pixelPosX, pixelPosY = getAperturePosition(x, y, imgSize, i, j, filterSize) 
#                     if pixelPosX == -1 or pixelPosY == -1:
#                         continue                  
#                     if pixels[pixelPosX,pixelPosY] > maxValue:
#                         maxValue = pixels[pixelPosX,pixelPosY]
#                     if pixels[pixelPosX,pixelPosY] < minValue:
#                         minValue = pixels[pixelPosX,pixelPosY]
#             avg = (minValue + maxValue) / 2
#             for i in range(filterSize):
#                 for j in range(filterSize):
#                     pixelPosX, pixelPosY = getAperturePosition(x, y, imgSize, i, j, filterSize)
#                     if pixelPosX == -1 or pixelPosY == -1:
#                         continue
#                     if pixels[pixelPosX,pixelPosY] < avg:
#                         pixels[pixelPosX,pixelPosY] = 0
#                     else:
#                         pixels[pixelPosX,pixelPosY] = 255
#     img.show()
