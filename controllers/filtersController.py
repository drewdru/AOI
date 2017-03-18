"""
    @package colorCorrectorController
    Controller for qml colorCorrector
"""
import sys
import os
import numpy
import matplotlib.pyplot as plt
import random
import time
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

from imageFilters import filters, adaptiveFilter
from imageProcessor import colorModel, histogramService, imageService, imageComparison
from PyQt5.QtCore import QCoreApplication, QDir 
from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtQml import QJSValue
from PIL import Image

class FiltersController(QObject):
    """ Controller for color corrector view """
    def __init__(self):
        QObject.__init__(self)
        self.appDir = QDir.currentPath()
        self.histogramService = histogramService.HistogramService()
        self.imageService = imageService.ImageService()

    @pyqtSlot(str, int, bool, int, int)
    def meanFilter(self, colorModelTag, currentImageChannelIndex, isOriginalImage,
            filterWidth, filterHeight):
        """
            Mean filter
        """
        img = self.imageService.openImage(isOriginalImage)
        if img is None:
            return
        methodTimer = time.time()
        if colorModelTag == 'RGB':
            filters.meanFilter(colorModelTag, currentImageChannelIndex, img.load(),
                img.size, (filterWidth, filterHeight))
            methodTimer = time.time() - methodTimer
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
        if colorModelTag == 'YUV':
            colorModel.rgbToYuv(img.load(), img.size)
            filters.meanFilter(colorModelTag, currentImageChannelIndex, img.load(),
                img.size, (filterWidth, filterHeight))
            colorModel.yuvToRgb(img.load(), img.size)
            methodTimer = time.time() - methodTimer
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
        if colorModelTag == 'HSL':
            data = numpy.asarray(img, dtype="float")
            data = colorModel.rgbToHsl(data)
            filters.meanFilter(colorModelTag, currentImageChannelIndex, data,
                data.shape, (filterWidth, filterHeight))
            methodTimer = time.time() - methodTimer
            self.histogramService.saveHistogram(data=data, model=colorModelTag)
            timerTemp = time.time()
            data = colorModel.hslToRgb(data)
            img = Image.fromarray(numpy.asarray(numpy.clip(data, 0, 255), dtype="uint8"))
            methodTimer = time.time() - timerTemp + methodTimer
        with open('{}/temp/log/meanFilter.log'.format(self.appDir), "a+") as text_file:
            text_file.write("{}: {}\n".format(colorModelTag, methodTimer))
        img.save('{}/temp/processingImage.png'.format(self.appDir))
        imageComparison.calculateImageDifference()

    @pyqtSlot(str, int, bool, int, int)
    def medianFilter(self, colorModelTag, currentImageChannelIndex, isOriginalImage,
            filterWidth, filterHeight):
        """
            Mean filter
        """
        img = self.imageService.openImage(isOriginalImage)
        if img is None:
            return
        methodTimer = time.time()
        if colorModelTag == 'RGB':
            filters.medianFilter(colorModelTag, currentImageChannelIndex, img.load(),
                img.size, (filterWidth, filterHeight))
            methodTimer = time.time() - methodTimer
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
        if colorModelTag == 'YUV':
            colorModel.rgbToYuv(img.load(), img.size)
            filters.medianFilter(colorModelTag, currentImageChannelIndex, img.load(),
                img.size, (filterWidth, filterHeight))
            colorModel.yuvToRgb(img.load(), img.size)
            methodTimer = time.time() - methodTimer
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
        if colorModelTag == 'HSL':
            data = numpy.asarray(img, dtype="float")
            data = colorModel.rgbToHsl(data)
            filters.medianFilter(colorModelTag, currentImageChannelIndex, data,
                data.shape, (filterWidth, filterHeight))
            methodTimer = time.time() - methodTimer
            self.histogramService.saveHistogram(data=data, model=colorModelTag)
            timerTemp = time.time()
            data = colorModel.hslToRgb(data)
            img = Image.fromarray(numpy.asarray(numpy.clip(data, 0, 255), dtype="uint8"))
            methodTimer = time.time() - timerTemp + methodTimer
        with open('{}/temp/log/medianFilter.log'.format(self.appDir), "a+") as text_file:
            text_file.write("{}: {}\n".format(colorModelTag, methodTimer))
        img.save('{}/temp/processingImage.png'.format(self.appDir))

    @pyqtSlot(str, int, bool, int, int)
    def gaussianBlur(self, colorModelTag, currentImageChannelIndex, isOriginalImage,
            filterWidth, filterHeight):
        """
            Mean filter
        """
        img = self.imageService.openImage(isOriginalImage)
        if img is None:
            return
        methodTimer = time.time()
        if colorModelTag == 'RGB':
            filters.gaussianBlur(colorModelTag, currentImageChannelIndex, img.load(),
                img.size, (filterWidth, filterHeight))
            methodTimer = time.time() - methodTimer
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
        if colorModelTag == 'YUV':
            colorModel.rgbToYuv(img.load(), img.size)
            filters.gaussianBlur(colorModelTag, currentImageChannelIndex, img.load(),
                img.size, (filterWidth, filterHeight))
            colorModel.yuvToRgb(img.load(), img.size)
            methodTimer = time.time() - methodTimer
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
        if colorModelTag == 'HSL':
            data = numpy.asarray(img, dtype="float")
            data = colorModel.rgbToHsl(data)
            filters.gaussianBlur(colorModelTag, currentImageChannelIndex, data,
                data.shape, (filterWidth, filterHeight))
            methodTimer = time.time() - methodTimer
            self.histogramService.saveHistogram(data=data, model=colorModelTag)
            timerTemp = time.time()
            data = colorModel.hslToRgb(data)
            img = Image.fromarray(numpy.asarray(numpy.clip(data, 0, 255), dtype="uint8"))
            methodTimer = time.time() - timerTemp + methodTimer
        with open('{}/temp/log/gaussianBlur.log'.format(self.appDir), "a+") as text_file:
            text_file.write("{}: {}\n".format(colorModelTag, methodTimer))
        img.save('{}/temp/processingImage.png'.format(self.appDir))

    @pyqtSlot(str, int, bool, int, int, int, int)
    def bilateralFilter(self, colorModelTag, currentImageChannelIndex, isOriginalImage,
            filterWidth, filterHeight, sigma_i, sigma_s):
        """
            Mean filter
        """
        img = self.imageService.openImage(isOriginalImage)
        if img is None:
            return
        methodTimer = time.time()
        if colorModelTag == 'RGB':
            filters.bilateralFilter(colorModelTag, currentImageChannelIndex, img.load(),
                img.size, (filterWidth, filterHeight), sigma_i, sigma_s)
            methodTimer = time.time() - methodTimer
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
        if colorModelTag == 'YUV':
            colorModel.rgbToYuv(img.load(), img.size)
            filters.bilateralFilter(colorModelTag, currentImageChannelIndex, img.load(),
                img.size, (filterWidth, filterHeight), sigma_i, sigma_s)
            colorModel.yuvToRgb(img.load(), img.size)
            methodTimer = time.time() - methodTimer
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
        if colorModelTag == 'HSL':
            data = numpy.asarray(img, dtype="float")
            data = colorModel.rgbToHsl(data)
            filters.bilateralFilter(colorModelTag, currentImageChannelIndex, data,
                data.shape, (filterWidth, filterHeight), sigma_i, sigma_s)
            methodTimer = time.time() - methodTimer
            self.histogramService.saveHistogram(data=data, model=colorModelTag)
            timerTemp = time.time()
            data = colorModel.hslToRgb(data)
            img = Image.fromarray(numpy.asarray(numpy.clip(data, 0, 255), dtype="uint8"))
            methodTimer = time.time() - timerTemp + methodTimer
        with open('{}/temp/log/bilateralFilter.log'
                .format(self.appDir), "a+") as text_file:
            text_file.write("{}: {}\n".format(colorModelTag, methodTimer))
        img.save('{}/temp/processingImage.png'.format(self.appDir))

    @pyqtSlot(str, int, bool, int, int, int)
    def laplacianBlur(self, colorModelTag, currentImageChannelIndex, isOriginalImage,
            filterWidth, filterHeight, sigma):
        """
            Mean filter
        """
        img = self.imageService.openImage(isOriginalImage)
        if img is None:
            return
        methodTimer = time.time()
        if colorModelTag == 'RGB':
            filters.laplacianBlur(colorModelTag, currentImageChannelIndex, img.load(),
                img.size, (filterWidth, filterHeight), sigma)
            methodTimer = time.time() - methodTimer
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
        if colorModelTag == 'YUV':
            colorModel.rgbToYuv(img.load(), img.size)
            filters.laplacianBlur(colorModelTag, currentImageChannelIndex, img.load(),
                img.size, (filterWidth, filterHeight), sigma)
            colorModel.yuvToRgb(img.load(), img.size)
            methodTimer = time.time() - methodTimer
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
        if colorModelTag == 'HSL':
            data = numpy.asarray(img, dtype="float")
            data = colorModel.rgbToHsl(data)
            filters.laplacianBlur(colorModelTag, currentImageChannelIndex, data,
                data.shape, (filterWidth, filterHeight), sigma)
            methodTimer = time.time() - methodTimer
            self.histogramService.saveHistogram(data=data, model=colorModelTag)
            timerTemp = time.time()
            data = colorModel.hslToRgb(data)
            img = Image.fromarray(numpy.asarray(numpy.clip(data, 0, 255), dtype="uint8"))
            methodTimer = time.time() - timerTemp + methodTimer
        with open('{}/temp/log/laplacianBlur.log'.format(self.appDir), "a+") as text_file:
            text_file.write("{}: {}\n".format(colorModelTag, methodTimer))
        img.save('{}/temp/processingImage.png'.format(self.appDir))

    @pyqtSlot(str, int, bool, int, int, int)
    def cleanerFilterByJimCasaburi(self, colorModelTag, currentImageChannelIndex,
            isOriginalImage, filterWidth, filterHeight, threshold):
        """
            Mean filter
        """
        img = self.imageService.openImage(isOriginalImage)
        if img is None:
            return
        methodTimer = time.time()
        if colorModelTag == 'RGB':
            filters.cleanerFilterByJimCasaburi(colorModelTag, currentImageChannelIndex,
                img.load(), img.size, (filterWidth, filterHeight), threshold)
            methodTimer = time.time() - methodTimer
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
        if colorModelTag == 'YUV':
            colorModel.rgbToYuv(img.load(), img.size)
            filters.cleanerFilterByJimCasaburi(colorModelTag, currentImageChannelIndex,
                img.load(), img.size, (filterWidth, filterHeight), threshold)
            colorModel.yuvToRgb(img.load(), img.size)
            methodTimer = time.time() - methodTimer
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
        if colorModelTag == 'HSL':
            data = numpy.asarray(img, dtype="float")
            data = colorModel.rgbToHsl(data)
            filters.cleanerFilterByJimCasaburi(colorModelTag, currentImageChannelIndex,
                data, data.shape, (filterWidth, filterHeight), threshold)
            methodTimer = time.time() - methodTimer
            self.histogramService.saveHistogram(data=data, model=colorModelTag)
            timerTemp = time.time()
            data = colorModel.hslToRgb(data)
            img = Image.fromarray(numpy.asarray(numpy.clip(data, 0, 255), dtype="uint8"))
            methodTimer = time.time() - timerTemp + methodTimer
        with open('{}/temp/log/cleanerFilterByJimCasaburi.log'
                .format(self.appDir), "a+") as text_file:
            text_file.write("{}: {}\n".format(colorModelTag, methodTimer))
        img.save('{}/temp/processingImage.png'.format(self.appDir))

    @pyqtSlot(str, int, bool, int)
    def adaptiveMedianFilter(self, colorModelTag, currentImageChannelIndex,
            isOriginalImage, filterSize):
        """
            Adaptive mean filter
        """
        img = self.imageService.openImage(isOriginalImage)
        if img is None:
            return
        methodTimer = time.time()
        if colorModelTag == 'RGB':
            r, g, b = img.split()
            if currentImageChannelIndex == 0:
                r = adaptiveFilter.adpmedf(r, img.size, filterSize)
                g = adaptiveFilter.adpmedf(g, img.size, filterSize)
                b = adaptiveFilter.adpmedf(b, img.size, filterSize)
            if currentImageChannelIndex == 1:
                r = adaptiveFilter.adpmedf(r, img.size, filterSize)
            if currentImageChannelIndex == 2:
                g = adaptiveFilter.adpmedf(g, img.size, filterSize)
            if currentImageChannelIndex == 3:
                b = adaptiveFilter.adpmedf(b, img.size, filterSize)
            img = Image.merge("RGB", (r, g, b))
            methodTimer = time.time() - methodTimer
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
        if colorModelTag == 'YUV':
            colorModel.rgbToYuv(img.load(), img.size)
            r, g, b = img.split()
            if currentImageChannelIndex == 0:
                r = adaptiveFilter.adpmedf(r, img.size, filterSize)
                g = adaptiveFilter.adpmedf(g, img.size, filterSize)
                b = adaptiveFilter.adpmedf(b, img.size, filterSize)
            if currentImageChannelIndex == 1:
                r = adaptiveFilter.adpmedf(r, img.size, filterSize)
            if currentImageChannelIndex == 2:
                g = adaptiveFilter.adpmedf(g, img.size, filterSize)
            if currentImageChannelIndex == 3:
                b = adaptiveFilter.adpmedf(b, img.size, filterSize)
            img = Image.merge("RGB", (r, g, b))
            colorModel.yuvToRgb(img.load(), img.size)
            methodTimer = time.time() - methodTimer
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
        if colorModelTag == 'HSL':
            data = numpy.asarray(img, dtype="float")
            data = colorModel.rgbToHsl(data)
            r = data[:, :, 0]
            g = data[:, :, 1]
            b = data[:, :, 2]
            if currentImageChannelIndex == 0:
                r = adaptiveFilter.adpmedf(r, img.size, filterSize)
                g = adaptiveFilter.adpmedf(g, img.size, filterSize)
                b = adaptiveFilter.adpmedf(b, img.size, filterSize)
            if currentImageChannelIndex == 1:
                r = adaptiveFilter.adpmedf(r, img.size, filterSize)
            if currentImageChannelIndex == 2:
                g = adaptiveFilter.adpmedf(g, img.size, filterSize)
            if currentImageChannelIndex == 3:
                b = adaptiveFilter.adpmedf(b, img.size, filterSize)
            data = numpy.dstack((r, g, b))
            methodTimer = time.time() - methodTimer
            self.histogramService.saveHistogram(data=img, model=colorModelTag)
            timerTemp = time.time()
            data = colorModel.hslToRgb(data)
            img = Image.fromarray(numpy.asarray(numpy.clip(data, 0, 255), dtype="uint8"))
            methodTimer = time.time() - timerTemp + methodTimer
        with open('{}/temp/log/adaptiveMedianFilter.log'
                .format(self.appDir), "a+") as text_file:
            text_file.write("{}: {}\n".format(colorModelTag, methodTimer))
        img.save('{}/temp/processingImage.png'.format(self.appDir))

