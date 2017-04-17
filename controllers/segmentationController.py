"""
    @package segmentationController
    Controller for qml Segmentation
"""
import sys
import os
import numpy
import matplotlib.pyplot as plt
import random
import time
import math
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

from imageProcessor import colorModel, histogramService, imageService, imageComparison
from imageSegmentation import segmentation
from imageFilters import filters
from PyQt5.QtCore import QCoreApplication, QDir 
from PyQt5.QtCore import QObject, pyqtSlot, QVariant #, QVariantList
from PyQt5.QtQml import QJSValue
from PIL import Image, ImageChops

class SegmentationController(QObject):
    """ Controller for binarize view """
    def __init__(self):
        QObject.__init__(self)
        self.appDir = QDir.currentPath()
        self.histogramService = histogramService.HistogramService()
        self.imageService = imageService.ImageService()

        self.maskList = []
        self.createMaskList(3, 3)

    @pyqtSlot(int, int)
    def createMaskList(self, apertureWidth, apertureHeight):
        if len(self.maskList) ==  apertureHeight and len(self.maskList) > 0:
            if len(self.maskList[0]) == apertureWidth:
                return
        self.maskList = []
        for height in range(apertureHeight):
            modelRow = []
            for width in range(apertureWidth):
                modelRow.append(False)
            self.maskList.append(modelRow)

    @pyqtSlot(int, int, bool)
    def updateCellMaskList(self, y, x, value):
        self.maskList[x][y] = value

    @pyqtSlot(str, int, bool, float, float)
    def segRoberts(self, colorModelTag, currentImageChannelIndex, isOriginalImage,
            amplifier, threshold):
        """
            Roberts
        """
        img = self.imageService.openImage(isOriginalImage)
        if img is None:
            return
        methodTimer = time.time()
        if colorModelTag == 'RGB':
            tempImg = img.copy()
            segmentation.roberts(colorModelTag, currentImageChannelIndex, img.load(),
                img.size, tempImg.load(), amplifier, threshold)
            methodTimer = time.time() - methodTimer
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
        if colorModelTag == 'YUV':
            colorModel.rgbToYuv(img.load(), img.size)
            tempImg = img.copy()
            segmentation.roberts(colorModelTag, currentImageChannelIndex, img.load(),
                img.size, tempImg.load(), amplifier, threshold)
            methodTimer = time.time() - methodTimer
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
            timerTemp = time.time()
            colorModel.yuvToRgb(img.load(), img.size)
            methodTimer = time.time() - methodTimer
        if colorModelTag == 'HSL':
            data = numpy.asarray(img, dtype="float")
            data = colorModel.rgbToHsl(data)
            dataTemp = numpy.copy(data)
            segmentation.roberts(colorModelTag, currentImageChannelIndex, data,
                data.shape, dataTemp, amplifier, threshold)
            methodTimer = time.time() - methodTimer
            # data = numpy.copy(dataTemp)
            self.histogramService.saveHistogram(data=data, model=colorModelTag)
            timerTemp = time.time()
            data = colorModel.hslToRgb(data)
            img = Image.fromarray(numpy.asarray(numpy.clip(data, 0, 255), dtype="uint8"))
            methodTimer = time.time() - timerTemp + methodTimer
        logFile = '{}/temp/log/segRoberts.log'.format(self.appDir)
        with open(logFile, "a+") as text_file:
            text_file.write("Timer: {}: {}\n".format(colorModelTag, methodTimer))
        img.save('{}/temp/processingImage.png'.format(self.appDir))
        imageComparison.calculateImageDifference(colorModelTag, logFile)

    @pyqtSlot(str, int, bool, float, float)
    def segCanny(self, colorModelTag, currentImageChannelIndex, isOriginalImage,
            amplifier, threshold):
        """
            Canny
        """
        img = self.imageService.openImage(isOriginalImage)
        if img is None:
            return

        methodTimer = time.time()
        if colorModelTag == 'RGB':
            gaussianImg = img.copy()
            gaussianDeviation = 1.0 ##############################################
            gaussianFilterSize = math.floor(gaussianDeviation*3.0)
            filters.gaussianBlur(colorModelTag, currentImageChannelIndex, gaussianImg.load(),
                gaussianImg.size, (gaussianFilterSize, gaussianFilterSize))
            segmentation.canny(colorModelTag, currentImageChannelIndex, img.load(), img.size,
                gaussianImg.load(), amplifier, threshold)
            methodTimer = time.time() - methodTimer
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
        if colorModelTag == 'YUV':
            colorModel.rgbToYuv(img.load(), img.size)
            gaussianImg = img.copy()
            gaussianDeviation = 1.0 ##############################################
            gaussianFilterSize = math.floor(gaussianDeviation*3.0)
            filters.gaussianBlur(colorModelTag, currentImageChannelIndex, gaussianImg.load(),
                gaussianImg.size, (gaussianFilterSize, gaussianFilterSize))
            segmentation.canny(colorModelTag, currentImageChannelIndex, img.load(), img.size,
                gaussianImg.load(), amplifier, threshold)
            methodTimer = time.time() - methodTimer
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
            timerTemp = time.time()
            colorModel.yuvToRgb(img.load(), img.size)
            methodTimer = time.time() - methodTimer
        if colorModelTag == 'HSL':
            data = numpy.asarray(img, dtype="float")
            data = colorModel.rgbToHsl(data)
            gaussianData = numpy.copy(data)
            gaussianDeviation = 1.0 ##############################################
            gaussianFilterSize = math.floor(gaussianDeviation*3.0)
            filters.gaussianBlur(colorModelTag, currentImageChannelIndex, gaussianData,
                gaussianData.shape, (gaussianFilterSize, gaussianFilterSize))
            segmentation.canny(colorModelTag, currentImageChannelIndex, gaussianData,
                gaussianData.shape, gaussianData, amplifier, threshold)
            methodTimer = time.time() - methodTimer
            # data = numpy.copy(dataTemp)
            self.histogramService.saveHistogram(data=data, model=colorModelTag)
            timerTemp = time.time()
            data = colorModel.hslToRgb(data)
            img = Image.fromarray(numpy.asarray(numpy.clip(data, 0, 255), dtype="uint8"))
            methodTimer = time.time() - timerTemp + methodTimer
        logFile = '{}/temp/log/segRoberts.log'.format(self.appDir)
        with open(logFile, "a+") as text_file:
            text_file.write("Timer: {}: {}\n".format(colorModelTag, methodTimer))
        img.save('{}/temp/processingImage.png'.format(self.appDir))
        imageComparison.calculateImageDifference(colorModelTag, logFile)
