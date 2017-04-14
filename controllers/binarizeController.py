"""
    @package binarizeController
    Controller for qml Binarize
"""
import sys
import os
import numpy
import matplotlib.pyplot as plt
import random
import time
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

from imageProcessor import colorModel, histogramService, imageService, imageComparison
from imageBinarize import globalThresholding, localThresholding
from imageMorphology import morphology
from PyQt5.QtCore import QCoreApplication, QDir 
from PyQt5.QtCore import QObject, pyqtSlot, QVariant #, QVariantList
from PyQt5.QtQml import QJSValue
from PIL import Image

class BinarizeController(QObject):
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

    @pyqtSlot(str, int, bool, int)
    def otsuBinarize(self, colorModelTag, currentImageChannelIndex, isOriginalImage,
            otsu_k):
        """
            Otsu Binarize
        """
        img = self.imageService.openImage(isOriginalImage)
        if img is None:
            return
        img = img.convert(mode='L')
        methodTimer = time.time()
        globalThresholding.histogramSegmentation(img.load(), img.size, 'otsu', otsu_k)
        methodTimer = time.time() - methodTimer
        logFile = '{}/temp/log/otsuBinarize.log'.format(self.appDir)
        with open(logFile, "a+") as text_file:
            text_file.write("Timer: {}: {}\n".format(colorModelTag, methodTimer))
        img = img.convert(mode='RGB')
        img.save('{}/temp/processingImage.png'.format(self.appDir))
        imageComparison.calculateImageDifference(colorModelTag, logFile)

    @pyqtSlot(str, int, bool, int)
    def histThresholdBinarize(self, colorModelTag, currentImageChannelIndex, isOriginalImage,
            otsu_k):
        """
            Binarize with histogram threshold
        """
        img = self.imageService.openImage(isOriginalImage)
        if img is None:
            return
        img = img.convert(mode='L')
        methodTimer = time.time()
        globalThresholding.histogramSegmentation(img.load(), img.size, 'histPeakValue', otsu_k)
        methodTimer = time.time() - methodTimer
        logFile = '{}/temp/log/histThresholdBinarize.log'.format(self.appDir)
        with open(logFile, "a+") as text_file:
            text_file.write("Timer: {}: {}\n".format(colorModelTag, methodTimer))
        img = img.convert(mode='RGB')
        img.save('{}/temp/processingImage.png'.format(self.appDir))
        imageComparison.calculateImageDifference(colorModelTag, logFile)

    @pyqtSlot(str, int, bool, int, int)
    def bernsenBinarize(self, colorModelTag, currentImageChannelIndex, isOriginalImage,
            aperture_height, aperture_width):
        """
            Bersen's method
        """
        img = self.imageService.openImage(isOriginalImage)
        if img is None:
            return
        img = img.convert(mode='L')
        methodTimer = time.time()
        localThresholding.bernsen(img.load(), img.size, (aperture_height, aperture_width))
        methodTimer = time.time() - methodTimer
        logFile = '{}/temp/log/bersenBinarize.log'.format(self.appDir)
        with open(logFile, "a+") as text_file:
            text_file.write("Timer: {}: {}\n".format(colorModelTag, methodTimer))
        img = img.convert(mode='RGB')
        img.save('{}/temp/processingImage.png'.format(self.appDir))
        imageComparison.calculateImageDifference(colorModelTag, logFile)

    @pyqtSlot(str, int, bool, int, int)
    def niblackBinarize(self, colorModelTag, currentImageChannelIndex, isOriginalImage,
            aperture_height, aperture_width):
        """
            Niblack's method
        """
        img = self.imageService.openImage(isOriginalImage)
        if img is None:
            return
        img = img.convert(mode='L')
        methodTimer = time.time()
        localThresholding.niblack(img.load(), img.size, (aperture_height, aperture_width))
        methodTimer = time.time() - methodTimer
        logFile = '{}/temp/log/niblackBinarize.log'.format(self.appDir)
        with open(logFile, "a+") as text_file:
            text_file.write("Timer: {}: {}\n".format(colorModelTag, methodTimer))
        img = img.convert(mode='RGB')
        img.save('{}/temp/processingImage.png'.format(self.appDir))
        imageComparison.calculateImageDifference(colorModelTag, logFile)


    @pyqtSlot(str, int, bool, int, int)
    def morphDilation(self, colorModelTag, currentImageChannelIndex, isOriginalImage,
            maskWidth, maskHeight):
        """
            morphDilation
        """
        img = self.imageService.openImage(isOriginalImage)
        if img is None:
            return
        tempImg = img.copy()
        methodTimer = time.time()
        if colorModelTag == 'RGB':
            morphology.dilation(colorModelTag, currentImageChannelIndex, img.load(),
                img.size, self.maskList, (maskWidth, maskHeight), tempImg.load())
            methodTimer = time.time() - methodTimer
            img = tempImg.copy()
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
        if colorModelTag == 'YUV':
            colorModel.rgbToYuv(img.load(), img.size)
            morphology.dilation(colorModelTag, currentImageChannelIndex, img.load(),
                img.size, self.maskList, (maskWidth, maskHeight), tempImg.load())
            colorModel.yuvToRgb(img.load(), img.size)
            methodTimer = time.time() - methodTimer
            img = tempImg.copy()
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
        if colorModelTag == 'HSL':
            data = numpy.asarray(img, dtype="float")
            data = colorModel.rgbToHsl(data)
            dataTemp = numpy.copy(data)
            morphology.dilation(colorModelTag, currentImageChannelIndex, data,
                data.shape, self.maskList, (maskWidth, maskHeight), dataTemp)
            methodTimer = time.time() - methodTimer
            data = numpy.copy(dataTemp)
            self.histogramService.saveHistogram(data=data, model=colorModelTag)
            timerTemp = time.time()
            data = colorModel.hslToRgb(data)
            img = Image.fromarray(numpy.asarray(numpy.clip(data, 0, 255), dtype="uint8"))
            methodTimer = time.time() - timerTemp + methodTimer
        logFile = '{}/temp/log/morphDilation.log'.format(self.appDir)
        with open(logFile, "a+") as text_file:
            text_file.write("Timer: {}: {}\n".format(colorModelTag, methodTimer))
        img.save('{}/temp/processingImage.png'.format(self.appDir))
        imageComparison.calculateImageDifference(colorModelTag, logFile)

    @pyqtSlot(str, int, bool, int, int)
    def morphErosion(self, colorModelTag, currentImageChannelIndex, isOriginalImage,
            maskWidth, maskHeight):
        """
            morphErosion
        """
        img = self.imageService.openImage(isOriginalImage)
        if img is None:
            return
        tempImg = img.copy()
        methodTimer = time.time()
        if colorModelTag == 'RGB':
            morphology.erosion(colorModelTag, currentImageChannelIndex, img.load(),
                img.size, self.maskList, (maskWidth, maskHeight), tempImg.load())
            methodTimer = time.time() - methodTimer
            img = tempImg.copy()
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
        if colorModelTag == 'YUV':
            colorModel.rgbToYuv(img.load(), img.size)
            morphology.erosion(colorModelTag, currentImageChannelIndex, img.load(),
                img.size, self.maskList, (maskWidth, maskHeight), tempImg.load())
            colorModel.yuvToRgb(img.load(), img.size)
            methodTimer = time.time() - methodTimer
            img = tempImg.copy()
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
        if colorModelTag == 'HSL':
            data = numpy.asarray(img, dtype="float")
            data = colorModel.rgbToHsl(data)
            dataTemp = numpy.copy(data)
            morphology.erosion(colorModelTag, currentImageChannelIndex, data,
                data.shape, self.maskList, (maskWidth, maskHeight), dataTemp)
            methodTimer = time.time() - methodTimer
            data = numpy.copy(dataTemp)
            self.histogramService.saveHistogram(data=data, model=colorModelTag)
            timerTemp = time.time()
            data = colorModel.hslToRgb(data)
            img = Image.fromarray(numpy.asarray(numpy.clip(data, 0, 255), dtype="uint8"))
            methodTimer = time.time() - timerTemp + methodTimer
        logFile = '{}/temp/log/morphDilation.log'.format(self.appDir)
        with open(logFile, "a+") as text_file:
            text_file.write("Timer: {}: {}\n".format(colorModelTag, methodTimer))
        img.save('{}/temp/processingImage.png'.format(self.appDir))
        imageComparison.calculateImageDifference(colorModelTag, logFile)

