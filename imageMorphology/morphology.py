"""
    @package imageMorphology
    Morphology image processing
"""
import math
import sys
import os
import numpy

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

from imageFilters import apertureService
from imageProcessor import colorModel
from PyQt5.QtCore import QCoreApplication
from PIL import Image, ImageChops

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

def closing(colorModelTag, currentImageChannelIndex, img, mask, maskSize):
    if colorModelTag == 'RGB':
        tempImg = img.copy()
        dilation(colorModelTag, currentImageChannelIndex, img.load(),
            img.size, mask, maskSize, tempImg.load())
        img = tempImg.copy()
        erosion(colorModelTag, currentImageChannelIndex, img.load(),
            img.size, mask, maskSize, tempImg.load())
        img = tempImg.copy()
    if colorModelTag == 'YUV':
        colorModel.rgbToYuv(img.load(), img.size)
        tempImg = img.copy()
        dilation(colorModelTag, currentImageChannelIndex, img.load(),
            img.size, mask, maskSize, tempImg.load())
        img = tempImg.copy()
        erosion(colorModelTag, currentImageChannelIndex, img.load(),
            img.size, mask, maskSize, tempImg.load())
        img = tempImg.copy()
        colorModel.yuvToRgb(img.load(), img.size)
    if colorModelTag == 'HSL':
        data = numpy.asarray(img, dtype="float")
        data = colorModel.rgbToHsl(data)
        dataTemp = numpy.copy(data)
        dilation(colorModelTag, currentImageChannelIndex, data,
            data.shape, mask, maskSize, dataTemp)
        data = dataTemp.copy()
        erosion(colorModelTag, currentImageChannelIndex, data,
            data.shape, mask, maskSize, dataTemp)
        data = colorModel.hslToRgb(dataTemp)
        img = Image.fromarray(numpy.asarray(numpy.clip(data, 0, 255), dtype="uint8"))
    return img

def opening(colorModelTag, currentImageChannelIndex, img, mask, maskSize):
    if colorModelTag == 'RGB':
        tempImg = img.copy()
        erosion(colorModelTag, currentImageChannelIndex, img.load(),
            img.size, mask, maskSize, tempImg.load())
        img = tempImg.copy()
        dilation(colorModelTag, currentImageChannelIndex, img.load(),
            img.size, mask, maskSize, tempImg.load())
        img = tempImg.copy()
    if colorModelTag == 'YUV':
        colorModel.rgbToYuv(img.load(), img.size)
        tempImg = img.copy()
        erosion(colorModelTag, currentImageChannelIndex, img.load(),
            img.size, mask, maskSize, tempImg.load())
        img = tempImg.copy()
        dilation(colorModelTag, currentImageChannelIndex, img.load(),
            img.size, mask, maskSize, tempImg.load())
        img = tempImg.copy()
        colorModel.yuvToRgb(img.load(), img.size)
    if colorModelTag == 'HSL':
        data = numpy.asarray(img, dtype="float")
        data = colorModel.rgbToHsl(data)
        dataTemp = numpy.copy(data)
        erosion(colorModelTag, currentImageChannelIndex, data,
            data.shape, mask, maskSize, dataTemp)
        data = dataTemp.copy()
        dilation(colorModelTag, currentImageChannelIndex, data,
            data.shape, mask, maskSize, dataTemp)
        data = colorModel.hslToRgb(dataTemp)
        img = Image.fromarray(numpy.asarray(numpy.clip(data, 0, 255), dtype="uint8"))
    return img

# def skeleton(colorModelTag, currentImageChannelIndex, img, mask, maskSize):
#     tempImg1 = img.copy()
#     tempImg2 = img.copy()
#     EMsk = []
#     OMsk = []
#     for i in range(3):
#         EMaskRow = []
#         OMaskRow = []
#         for j in range(3):
#             EMaskRow.append(True)
#             OMaskRow.append(True)
#         EMsk.append(EMaskRow)
#         OMsk.append(OMaskRow)
#     OMsk[0][0] = False
#     OMsk[0][2] = False
#     OMsk[2][0] = False
#     OMsk[2][2] = False
#     differencesCount = 0
#     while True:
#         tempImg1 = opening(colorModelTag, currentImageChannelIndex, tempImg1, OMsk, maskSize)
#     #     tempImg1.show()
#     #     # img = ImageChops.difference(img, tempImg1)
#     #     differencesCount = 0
#     #     imgPixels = img.load()
#     #     tempImg1Pixels = tempImg1.load()
#     #     tempImg2Pixels = tempImg2.load()
#     #     for i in range(img.size[0]):
#     #         QCoreApplication.processEvents()
#     #         for j in range(img.size[1]):
#     #             r, g, b = imgPixels[i, j]
#     #             newR, newG, newB = tempImg1Pixels[i, j]
#     #             newR = abs(r - newR)
#     #             newG = abs(g - newG)
#     #             newB = abs(b - newB)
#     #             if newR == 0: differencesCount += 1
#     #             if newG == 0: differencesCount += 1
#     #             if newB == 0: differencesCount += 1
#     #             tempImg2Pixels[i, j] = (newR, newG, newB)
#     # #     apertures = apertureService.getApertureMatrixGenerator(img.size(), maskSize)
#     # #     pixelsImg = img.load()
#     # #     pixelstempImg1 = tempImg1.load()
#     # #     for i, pixels in enumerate(pixelsArray):
#     # #         QCoreApplication.processEvents()
#     # #         for j, pixel in enumerate(pixels):
#     # #                 pixelPosX, pixelPosY = apertureCoordinate
#     # #                 # red, green, blue = pixels[pixelPosX, pixelPosY]
#     # #                 pixel = img[x][y] - tempImg1[x][y]
#     # # #               skel[x][y] = skel[x][y] | pixel;
#     #     # tempImg = img.copy()
#         img = tempImg1.copy()
#         erosion(colorModelTag, currentImageChannelIndex, img.load(),
#             img.size, EMsk, maskSize, tempImg1.load())
#         img = tempImg1.copy()
#         differencesCount += 1
#         if differencesCount < 30:
#             break
#     return img
        
#     # Erosion(img, EMask, eimg)
#     # if colorModelTag == 'RGB':
#     #     tempImg = img.copy()
#     #     erosion(colorModelTag, currentImageChannelIndex, img.load(),
#     #         img.size, mask, maskSize, tempImg.load())
#     #     img = tempImg.copy()
#     #     dilation(colorModelTag, currentImageChannelIndex, img.load(),
#     #         img.size, mask, maskSize, tempImg.load())
#     #     img = tempImg.copy()
#     # if colorModelTag == 'YUV':
#     #     colorModel.rgbToYuv(img.load(), img.size)
#     #     tempImg = img.copy()
#     #     erosion(colorModelTag, currentImageChannelIndex, img.load(),
#     #         img.size, mask, maskSize, tempImg.load())
#     #     img = tempImg.copy()
#     #     dilation(colorModelTag, currentImageChannelIndex, img.load(),
#     #         img.size, mask, maskSize, tempImg.load())
#     #     img = tempImg.copy()
#     #     colorModel.yuvToRgb(img.load(), img.size)
#     # if colorModelTag == 'HSL':
#     #     data = numpy.asarray(img, dtype="float")
#     #     data = colorModel.rgbToHsl(data)
#     #     dataTemp = numpy.copy(data)
#     #     erosion(colorModelTag, currentImageChannelIndex, data,
#     #         data.shape, mask, maskSize, dataTemp)
#     #     data = dataTemp.copy()
#     #     dilation(colorModelTag, currentImageChannelIndex, data,
#     #         data.shape, mask, maskSize, dataTemp)
#     #     data = colorModel.hslToRgb(dataTemp)
#     #     img = Image.fromarray(numpy.asarray(numpy.clip(data, 0, 255), dtype="uint8"))


# # def skeleton(BIT* img[], BIT* skel[])
# # {
# #     BIT eimg[W][H], oimg[W][H]; bool EMsk[3][3], OMsk[3][3];
# #     for(m = 0; m < 3; m++)
# #       for(n = 0; n < 3; n++)
# #           EMask[m][n] = OMask[m][n] = TRUE;
# #     OMsk[0][0] = OMsk[0][2] = OMsk[2][0] = OMsk[2][2] = FALSE;
# #     while( !empty(img) )
# #     {
# #         Open(img, OMsk, oimg);
# #         for(y = 0; y < H; y++)
# #           for(x = 0; x < W; x++)
# #           {
# #               pixel = img[x][y] – oimg[x][y];
# #               skel[x][y] = skel[x][y] | pixel;
# #           }
# #         Erosion(img, EMask, eimg); Copy(img, eimg);
# #     }
# # }