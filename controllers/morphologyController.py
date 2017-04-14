"""
    @package morphologyController
    Controller for qml Morphology
"""
import sys
import os
import numpy
import matplotlib.pyplot as plt
import random
import time
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

from imageProcessor import colorModel, histogramService, imageService, imageComparison
from imageMorphology import morphology
from PyQt5.QtCore import QCoreApplication, QDir 
from PyQt5.QtCore import QObject, pyqtSlot, QVariant #, QVariantList
from PyQt5.QtQml import QJSValue
from PIL import Image, ImageChops

class MorphologyController(QObject):
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
        logFile = '{}/temp/log/morphErosion.log'.format(self.appDir)
        with open(logFile, "a+") as text_file:
            text_file.write("Timer: {}: {}\n".format(colorModelTag, methodTimer))
        img.save('{}/temp/processingImage.png'.format(self.appDir))
        imageComparison.calculateImageDifference(colorModelTag, logFile)

    # http://achawk.narod.ru/Morph.html
    @pyqtSlot(str, int, bool, int, int)
    def morphClosing(self, colorModelTag, currentImageChannelIndex, isOriginalImage,
            maskWidth, maskHeight):
        """
            morphClosing
        """
        self.morphDilation(colorModelTag, currentImageChannelIndex, isOriginalImage,
            maskWidth, maskHeight)
        self.morphErosion(colorModelTag, currentImageChannelIndex, False,
            maskWidth, maskHeight)

    @pyqtSlot(str, int, bool, int, int)
    def morphOpening(self, colorModelTag, currentImageChannelIndex, isOriginalImage,
            maskWidth, maskHeight):
        """
            morphOpening
        """
        self.morphErosion(colorModelTag, currentImageChannelIndex, isOriginalImage,
            maskWidth, maskHeight)
        self.morphDilation(colorModelTag, currentImageChannelIndex, False,
            maskWidth, maskHeight)

    @pyqtSlot(str, int, bool, int, int)
    def morphInnerEdge(self, colorModelTag, currentImageChannelIndex, isOriginalImage,
            maskWidth, maskHeight):
        """
            morphInnerEdge
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
            img = ImageChops.difference(img, tempImg)
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
        if colorModelTag == 'YUV':
            colorModel.rgbToYuv(img.load(), img.size)
            morphology.erosion(colorModelTag, currentImageChannelIndex, img.load(),
                img.size, self.maskList, (maskWidth, maskHeight), tempImg.load())
            colorModel.yuvToRgb(img.load(), img.size)
            methodTimer = time.time() - methodTimer
            img = ImageChops.difference(img, tempImg)
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
        if colorModelTag == 'HSL':
            data = numpy.asarray(img, dtype="float")
            data = colorModel.rgbToHsl(data)
            dataTemp = numpy.copy(data)
            morphology.erosion(colorModelTag, currentImageChannelIndex, data,
                data.shape, self.maskList, (maskWidth, maskHeight), dataTemp)
            methodTimer = time.time() - methodTimer
            # data = numpy.copy(dataTemp)
            data = numpy.absolute(data - dataTemp)
            self.histogramService.saveHistogram(data=data, model=colorModelTag)
            timerTemp = time.time()
            data = colorModel.hslToRgb(data)
            img = Image.fromarray(numpy.asarray(numpy.clip(data, 0, 255), dtype="uint8"))
            methodTimer = time.time() - timerTemp + methodTimer
        logFile = '{}/temp/log/morphInnerEdge.log'.format(self.appDir)
        with open(logFile, "a+") as text_file:
            text_file.write("Timer: {}: {}\n".format(colorModelTag, methodTimer))
        img.save('{}/temp/processingImage.png'.format(self.appDir))
        imageComparison.calculateImageDifference(colorModelTag, logFile)

    @pyqtSlot(str, int, bool, int, int)
    def morphOuterEdge(self, colorModelTag, currentImageChannelIndex, isOriginalImage,
            maskWidth, maskHeight):
        """
            morphOuterEdge
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
            img = ImageChops.difference(tempImg, img)
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
        if colorModelTag == 'YUV':
            colorModel.rgbToYuv(img.load(), img.size)
            morphology.dilation(colorModelTag, currentImageChannelIndex, img.load(),
                img.size, self.maskList, (maskWidth, maskHeight), tempImg.load())
            colorModel.yuvToRgb(img.load(), img.size)
            methodTimer = time.time() - methodTimer
            img = ImageChops.difference(tempImg, img)
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
        if colorModelTag == 'HSL':
            data = numpy.asarray(img, dtype="float")
            data = colorModel.rgbToHsl(data)
            dataTemp = numpy.copy(data)
            morphology.dilation(colorModelTag, currentImageChannelIndex, data,
                data.shape, self.maskList, (maskWidth, maskHeight), dataTemp)
            methodTimer = time.time() - methodTimer
            # data = numpy.copy(dataTemp)
            data = numpy.absolute(dataTemp - data)
            self.histogramService.saveHistogram(data=data, model=colorModelTag)
            timerTemp = time.time()
            data = colorModel.hslToRgb(data)
            img = Image.fromarray(numpy.asarray(numpy.clip(data, 0, 255), dtype="uint8"))
            methodTimer = time.time() - timerTemp + methodTimer
        logFile = '{}/temp/log/morphOuterEdge.log'.format(self.appDir)
        with open(logFile, "a+") as text_file:
            text_file.write("Timer: {}: {}\n".format(colorModelTag, methodTimer))
        img.save('{}/temp/processingImage.png'.format(self.appDir))
        imageComparison.calculateImageDifference(colorModelTag, logFile)

