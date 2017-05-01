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
from imageSegmentation import egbis, gabor, gaborSegment, kMeans
#from roadLaneDetection import detectRoadLane
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

    @pyqtSlot(str, int, bool, float, float, float, float)
    def EfficientGraphBasedImageSegmentation(self, colorModelTag, currentImageChannelIndex, isOriginalImage,
            sigma, neighborhood, k, min_comp_size):
        """
            morphDilation
        """
        outImagePath, imgPath = self.imageService.getImagePath(isOriginalImage)
        if imgPath is None:
            return
        img = self.imageService.openImage(isOriginalImage)
        if img is None:
            return
        methodTimer = time.time()
        if colorModelTag == 'RGB':
            methodTimer = time.time()
            egbis.segmentateRun(sigma, neighborhood, k, min_comp_size,
                img, outImagePath)
            methodTimer = time.time() - methodTimer
            img = self.imageService.openImage(False)
            if img is None:
                return
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
        if colorModelTag == 'YUV':
            colorModel.rgbToYuv(img.load(), img.size)
            methodTimer = time.time()
            egbis.segmentateRun(sigma, neighborhood, k, min_comp_size,
                img, outImagePath)
            methodTimer = time.time() - methodTimer
            img = self.imageService.openImage(False)
            if img is None:
                return
            # img.show()
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
            # colorModel.yuvToRgb(img.load(), img.size)
        if colorModelTag == 'HSL':
            data = numpy.asarray(img, dtype="float")
            data = colorModel.rgbToHsl(data)
            methodTimer = time.time()
            egbis.segmentateRun(sigma, neighborhood, k, min_comp_size,
                data, outImagePath)
            methodTimer = time.time() - methodTimer
            self.histogramService.saveHistogram(data=data, model=colorModelTag)
            timerTemp = time.time()
            data = colorModel.hslToRgb(data)
            img = Image.fromarray(numpy.asarray(numpy.clip(data, 0, 255), dtype="uint8"))
            methodTimer = time.time() - timerTemp + methodTimer
        logFile = '{}/temp/log/morphDilation.log'.format(self.appDir)
        with open(logFile, "a+") as text_file:
            text_file.write("Timer: {}: {}\n".format(colorModelTag, methodTimer))
        # img.save('{}/temp/processingImage.png'.format(self.appDir))
        imageComparison.calculateImageDifference(colorModelTag, logFile)

    @pyqtSlot(str, int, bool)
    def GaborEdge(self, colorModelTag, currentImageChannelIndex, isOriginalImage):
        """
            GaborEdge
        """
        outImagePath, imgPath = self.imageService.getImagePath(isOriginalImage)
        if imgPath is None:
            return
        img = self.imageService.openImage(isOriginalImage)
        if img is None:
            return
        methodTimer = time.time()
        if colorModelTag == 'RGB':
            methodTimer = time.time()
            gabor.doGabor(imgPath, outImagePath)
            methodTimer = time.time() - methodTimer
            img = self.imageService.openImage(False)
            if img is None:
                return
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
        if colorModelTag == 'YUV':
            colorModel.rgbToYuv(img.load(), img.size)
            methodTimer = time.time()
            gabor.doGabor(imgPath, outImagePath)
            methodTimer = time.time() - methodTimer
            img = self.imageService.openImage(False)
            if img is None:
                return
            # img.show()
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
            # colorModel.yuvToRgb(img.load(), img.size)
        if colorModelTag == 'HSL':
            data = numpy.asarray(img, dtype="float")
            data = colorModel.rgbToHsl(data)
            methodTimer = time.time()
            gabor.doGabor(imgPath, outImagePath)
            methodTimer = time.time() - methodTimer
            self.histogramService.saveHistogram(data=data, model=colorModelTag)
            timerTemp = time.time()
            data = colorModel.hslToRgb(data)
            img = Image.fromarray(numpy.asarray(numpy.clip(data, 0, 255), dtype="uint8"))
            methodTimer = time.time() - timerTemp + methodTimer
        logFile = '{}/temp/log/morphDilation.log'.format(self.appDir)
        with open(logFile, "a+") as text_file:
            text_file.write("Timer: {}: {}\n".format(colorModelTag, methodTimer))
        # img.save('{}/temp/processingImage.png'.format(self.appDir))
        imageComparison.calculateImageDifference(colorModelTag, logFile)

    @pyqtSlot(str, int, bool)
    def GaborSegmentation(self, colorModelTag, currentImageChannelIndex, isOriginalImage):
        """
            GaborSegmentation
        """
        outImagePath, imgPath = self.imageService.getImagePath(isOriginalImage)
        if imgPath is None:
            return
        img = self.imageService.openImage(isOriginalImage)
        if img is None:
            return
        methodTimer = time.time()
        if colorModelTag == 'RGB':
            methodTimer = time.time()
            gaborSegment.doSegment(imgPath, outImagePath)
            methodTimer = time.time() - methodTimer
            img = self.imageService.openImage(False)
            if img is None:
                return
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
        if colorModelTag == 'YUV':
            colorModel.rgbToYuv(img.load(), img.size)
            methodTimer = time.time()
            gaborSegment.doSegment(imgPath, outImagePath)
            methodTimer = time.time() - methodTimer
            img = self.imageService.openImage(False)
            if img is None:
                return
            # img.show()
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
            # colorModel.yuvToRgb(img.load(), img.size)
        if colorModelTag == 'HSL':
            data = numpy.asarray(img, dtype="float")
            data = colorModel.rgbToHsl(data)
            methodTimer = time.time()
            gaborSegment.doSegment(imgPath, outImagePath)
            methodTimer = time.time() - methodTimer
            self.histogramService.saveHistogram(data=data, model=colorModelTag)
            timerTemp = time.time()
            data = colorModel.hslToRgb(data)
            img = Image.fromarray(numpy.asarray(numpy.clip(data, 0, 255), dtype="uint8"))
            methodTimer = time.time() - timerTemp + methodTimer
        logFile = '{}/temp/log/morphDilation.log'.format(self.appDir)
        with open(logFile, "a+") as text_file:
            text_file.write("Timer: {}: {}\n".format(colorModelTag, methodTimer))
        # img.save('{}/temp/processingImage.png'.format(self.appDir))
        imageComparison.calculateImageDifference(colorModelTag, logFile)

    @pyqtSlot(str, int, bool)
    def KMeans(self, colorModelTag, currentImageChannelIndex, isOriginalImage):
        """
            GaborSegmentation
        """
        outImagePath, imgPath = self.imageService.getImagePath(isOriginalImage)
        if imgPath is None:
            return
        img = self.imageService.openImage(isOriginalImage)
        if img is None:
            return
        methodTimer = time.time()
        if colorModelTag == 'RGB':
            methodTimer = time.time()
            kMeans.doKMeans(imgPath, outImagePath)
            methodTimer = time.time() - methodTimer
            img = self.imageService.openImage(False)
            if img is None:
                return
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
        if colorModelTag == 'YUV':
            colorModel.rgbToYuv(img.load(), img.size)
            methodTimer = time.time()
            kMeans.doKMeans(imgPath, outImagePath)
            methodTimer = time.time() - methodTimer
            img = self.imageService.openImage(False)
            if img is None:
                return
            # img.show()
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
            # colorModel.yuvToRgb(img.load(), img.size)
        if colorModelTag == 'HSL':
            data = numpy.asarray(img, dtype="float")
            data = colorModel.rgbToHsl(data)
            methodTimer = time.time()
            kMeans.doKMeans(imgPath, outImagePath)
            methodTimer = time.time() - methodTimer
            self.histogramService.saveHistogram(data=data, model=colorModelTag)
            timerTemp = time.time()
            data = colorModel.hslToRgb(data)
            img = Image.fromarray(numpy.asarray(numpy.clip(data, 0, 255), dtype="uint8"))
            methodTimer = time.time() - timerTemp + methodTimer
        logFile = '{}/temp/log/morphDilation.log'.format(self.appDir)
        with open(logFile, "a+") as text_file:
            text_file.write("Timer: {}: {}\n".format(colorModelTag, methodTimer))
        # img.save('{}/temp/processingImage.png'.format(self.appDir))
        imageComparison.calculateImageDifference(colorModelTag, logFile)

    @pyqtSlot(str, int, bool)
    def detectRoadLane(self, colorModelTag, currentImageChannelIndex, isOriginalImage):
        #detectRoadLane.detectLane()
        pass
