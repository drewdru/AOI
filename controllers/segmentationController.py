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
from imageSegmentation import egbis, gabor, gaborSegment, kMeans, sphc
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

    @pyqtSlot(str, int, bool, float, float, float, float, str, str)
    def EfficientGraphBasedImageSegmentation(self, colorModelTag, currentImageChannelIndex, isOriginalImage,
            sigma, neighborhood, k, min_comp_size, xPix, yPix):
        """
            EfficientGraphBasedImageSegmentation
        """
        if xPix == '' or yPix == '':
            pixMouse=None
        else:
            pixMouse=(int(xPix), int(yPix))
        outImagePath, imgPath = self.imageService.getImagePath(isOriginalImage)
        if imgPath is None:
            return
        img = self.imageService.openImage(isOriginalImage)
        if img is None:
            return
        segmentCount = 0
        methodTimer = time.time()
        if colorModelTag == 'RGB':
            methodTimer = time.time()
            data1, data2, segmentCount, forest = egbis.segmentateRun(sigma, neighborhood, k, min_comp_size,
                img, outImagePath, pixMouse)
            methodTimer = time.time() - methodTimer
            img = self.imageService.openImage(False)
            if img is None:
                return
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
        if colorModelTag == 'YUV':
            colorModel.rgbToYuv(img.load(), img.size)
            methodTimer = time.time()
            data1, data2, segmentCount, forest = egbis.segmentateRun(sigma, neighborhood, k, min_comp_size,
                img, outImagePath, pixMouse)
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
            data1, data2, segmentCount, forest = egbis.segmentateRun(sigma, neighborhood, k, min_comp_size,
                data, outImagePath, pixMouse)
            methodTimer = time.time() - methodTimer
            self.histogramService.saveHistogram(data=data, model=colorModelTag)
            timerTemp = time.time()
            data = colorModel.hslToRgb(data)
            img = Image.fromarray(numpy.asarray(numpy.clip(data, 0, 255), dtype="uint8"))
            methodTimer = time.time() - timerTemp + methodTimer
        logFile = '{}/temp/log/EfficientGraphBasedImageSegmentation.log'.format(self.appDir)
        with open(logFile, "a+") as text_file:
            text_file.write("Timer: {}: {}\n".format(colorModelTag, methodTimer))
        # img.save('{}/temp/processingImage.png'.format(self.appDir))
        imageComparison.calculateSegmentationCriterias(logFile, data1, data2, segmentCount)

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

    @pyqtSlot(str, int, bool, int)
    def KMeans(self, colorModelTag, currentImageChannelIndex, isOriginalImage, countOfClusters):
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
            kMeans.doKMeans(imgPath, outImagePath, countOfClusters)
            methodTimer = time.time() - methodTimer
            img = self.imageService.openImage(False)
            if img is None:
                return
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
        if colorModelTag == 'YUV':
            colorModel.rgbToYuv(img.load(), img.size)
            methodTimer = time.time()
            kMeans.doKMeans(imgPath, outImagePath, countOfClusters)
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
            kMeans.doKMeans(imgPath, outImagePath, countOfClusters)
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

    @pyqtSlot(str, int, bool, int, float, int, float, str, str)
    def segSPHC(self, colorModelTag, currentImageChannelIndex, isOriginalImage,
            numSegments, Sigma, segmentsToMerge, distance_limit, xPix, yPix):
        """
            segSPHC
        """
        if xPix == '' or yPix == '':
            pixMouse=None
        else:
            pixMouse=(int(xPix), int(yPix))
        segmentCount = 0
        outImagePath, imgPath = self.imageService.getImagePath(isOriginalImage)
        if imgPath is None:
            return
        img = self.imageService.openImage(isOriginalImage)
        if img is None:
            return
        methodTimer = time.time()
        if colorModelTag == 'RGB':
            methodTimer = time.time()
            data1, data2, segmentCount, segm_dict = sphc.doSPHC(imgPath, outImagePath, numSegments, Sigma,
                    segmentsToMerge, distance_limit, pixMouse)
            methodTimer = time.time() - methodTimer
            img = self.imageService.openImage(False)
            if img is None:
                return
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
        if colorModelTag == 'YUV':
            colorModel.rgbToYuv(img.load(), img.size)
            methodTimer = time.time()
            data1, data2, segmentCount, segm_dict = sphc.doSPHC(imgPath, outImagePath, numSegments, Sigma,
                    segmentsToMerge, distance_limit, pixMouse)
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
            data1, data2, segmentCount, segm_dict = sphc.doSPHC(imgPath, outImagePath, numSegments, Sigma,
                    segmentsToMerge, distance_limit, pixMouse)
            methodTimer = time.time() - methodTimer
            self.histogramService.saveHistogram(data=data, model=colorModelTag)
            timerTemp = time.time()
            data = colorModel.hslToRgb(data)
            img = Image.fromarray(numpy.asarray(numpy.clip(data, 0, 255), dtype="uint8"))
            methodTimer = time.time() - timerTemp + methodTimer
        logFile = '{}/temp/log/segSPHC.log'.format(self.appDir)
        with open(logFile, "a+") as text_file:
            text_file.write("Timer: {}: {}\n".format(colorModelTag, methodTimer))
        # img.save('{}/temp/processingImage.png'.format(self.appDir))
        imageComparison.calculateSegmentationCriterias(logFile, data1, data2, segmentCount)


    @pyqtSlot(str, int, bool, float, float, float, float, str, str, int, float, int, float, str, str)
    def CompareEGBISandSPHC(self, colorModelTag, currentImageChannelIndex, isOriginalImage,
            sigmaEGBIS, neighborhoodEGBIS, kEGBIS, min_comp_sizeEGBIS, xPixEGBIS, yPixEGBIS,
            numSegmentsSPHC, SigmaSPHC, segmentsToMergeSPHC, distance_limitSPHC, xPixSPHC, yPixSPHC):
        """
            CompareEGBISandSPHC
        """
        pixMouseEGBIS=None
        pixMouseSPHC=None
        # if xPixEGBIS == '' or yPixEGBIS == '':
        #     pixMouseEGBIS=None
        # else:
        #     pixMouseEGBIS=(int(xPixEGBIS), int(yPixEGBIS))
        outImagePath, imgPath = self.imageService.getImagePath(isOriginalImage)
        if imgPath is None:
            return
        img = self.imageService.openImage(isOriginalImage)
        if img is None:
            return
        segmentCountEGBIS = 0
        segmentCountSPHC = 0
        methodTimer = time.time()
        if colorModelTag == 'RGB':
            methodTimer = time.time()
            data1EGBIS, data2EGBIS, segmentCountEGBIS, forest = egbis.segmentateRun(sigmaEGBIS, neighborhoodEGBIS, kEGBIS, min_comp_sizeEGBIS,
                img, outImagePath, pixMouseEGBIS)
            data1SPHC, data2SPHC, segmentCountSPHC, segm_dict = sphc.doSPHC(imgPath, outImagePath, numSegmentsSPHC, SigmaSPHC,
                    segmentsToMergeSPHC, distance_limitSPHC, pixMouseSPHC, isTest=True)
            methodTimer = time.time() - methodTimer
            img = self.imageService.openImage(True)
            if img is None:
                return
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
        if colorModelTag == 'YUV':
            colorModel.rgbToYuv(img.load(), img.size)
            methodTimer = time.time()
            data1EGBIS, data2EGBIS, segmentCountEGBIS, forest = egbis.segmentateRun(sigmaEGBIS, neighborhoodEGBIS, kEGBIS, min_comp_sizeEGBIS,
                img, outImagePath, pixMouseEGBIS)
            data1SPHC, data2SPHC, segmentCountSPHC, segm_dict = sphc.doSPHC(imgPath, outImagePath, numSegmentsSPHC, SigmaSPHC,
                    segmentsToMergeSPHC, distance_limitSPHC, pixMouseSPHC, isTest=True)
            methodTimer = time.time() - methodTimer
            img = self.imageService.openImage(True)
            if img is None:
                return
            # img.show()
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
            # colorModel.yuvToRgb(img.load(), img.size)
        if colorModelTag == 'HSL':
            data = numpy.asarray(img, dtype="float")
            data = colorModel.rgbToHsl(data)
            methodTimer = time.time()
            data1EGBIS, data2EGBIS, segmentCountEGBIS, forest = egbis.segmentateRun(sigmaEGBIS, neighborhoodEGBIS, kEGBIS, min_comp_sizeEGBIS,
                data, outImagePath, pixMouseEGBIS)
            data1SPHC, data2SPHC, segmentCountSPHC, segm_dict = sphc.doSPHC(imgPath, outImagePath, numSegmentsSPHC, SigmaSPHC,
                    segmentsToMergeSPHC, distance_limitSPHC, pixMouseSPHC, isTest=True)
            methodTimer = time.time() - methodTimer
            self.histogramService.saveHistogram(data=data, model=colorModelTag)
            timerTemp = time.time()
            data = colorModel.hslToRgb(data)
            img = Image.fromarray(numpy.asarray(numpy.clip(data, 0, 255), dtype="uint8"))
            methodTimer = time.time() - timerTemp + methodTimer
        logFile = '{}/temp/log/CompareEGBISandSPHC.log'.format(self.appDir)
        with open(logFile, "a+") as text_file:
            text_file.write("Timer: {}: {}\n".format(colorModelTag, methodTimer))
        # img.save('{}/temp/processingImage.png'.format(self.appDir))
        imageComparison.calculateSegmentationDifferences(logFile, data1EGBIS, data2EGBIS, segmentCountEGBIS, forest, data1SPHC, data2SPHC, segmentCountSPHC, segm_dict)


    @pyqtSlot(str, int, bool)
    def detectRoadLane(self, colorModelTag, currentImageChannelIndex, isOriginalImage):
        #detectRoadLane.detectLane()
        pass
