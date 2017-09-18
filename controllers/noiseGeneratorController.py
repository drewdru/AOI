"""
    @package noiseGeneratorController
    Controller for qml noiseGenerator
"""
import sys
import os
import numpy
import matplotlib.pyplot as plt
import random
import time

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

from imageProcessor import colorModel, noiseGenerator, colorHistogram
from imageProcessor import histogramService, imageService, imageComparison
from PyQt5.QtCore import QCoreApplication, QDir 
from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtQml import QJSValue
from PIL import Image

class NoiseGeneratorController(QObject):
    """ Controller for color corrector view """
    def __init__(self, appDir=None):
        QObject.__init__(self)
        self.appDir = QDir.currentPath() if appDir is None else appDir
        self.histogramService = histogramService.HistogramService(self.appDir)
        self.imageService = imageService.ImageService(self.appDir)

    @pyqtSlot(str, int, int, int, bool)
    def addImpulsNoise(self, colorModelTag, currentImageChannelIndex, impulseNoise,
            noiseLevel, isOriginalImage):
        """ Change color model and channels

            @param colorModelTag: The color model tag
            @param currentImageChannelIndex: The index of current image channel
        """
        img = self.imageService.openImage(isOriginalImage)
        if img is None:
            return
        methodTimer = time.time()
        if colorModelTag == 'RGB':
            noiseGenerator.impulsNoise(img.load(),
                img.size,
                colorModelTag,
                currentImageChannelIndex,
                impulseNoise,
                noiseLevel)
            methodTimer = time.time() - methodTimer
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
        if colorModelTag == 'YUV':
            colorModel.rgbToYuv(img.load(), img.size)
            noiseGenerator.impulsNoise(img.load(),
                img.size,
                colorModelTag,
                currentImageChannelIndex,
                impulseNoise,
                noiseLevel)
            methodTimer = time.time() - methodTimer
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
            timerTemp = time.time()
            colorModel.yuvToRgb(img.load(), img.size)
            methodTimer = time.time() - methodTimer
        if colorModelTag == 'HSL':
            data = numpy.asarray(img, dtype="float")
            data = colorModel.rgbToHsl(data)
            noiseGenerator.impulsNoise(data,
                data.shape,
                colorModelTag,
                currentImageChannelIndex,
                impulseNoise,
                noiseLevel)
            methodTimer = time.time() - methodTimer
            self.histogramService.saveHistogram(data=data, model=colorModelTag)
            timerTemp = time.time()
            data = colorModel.hslToRgb(data)
            img = Image.fromarray(numpy.asarray(numpy.clip(data, 0, 255), dtype="uint8"))
            methodTimer = time.time() - timerTemp + methodTimer
        logFile = '{}/temp/log/addImpulsNoise.log'.format(self.appDir)
        with open(logFile, "a+") as text_file:
            text_file.write("Timer: {}: {}\n".format(colorModelTag, methodTimer))
        imageComparison.calculateImageDifference(colorModelTag, logFile)
        img.save('{}/temp/processingImage.png'.format(self.appDir))

    @pyqtSlot(str, int, int, int, int, bool)
    def addAdditiveNoise(self, colorModelTag, currentImageChannelIndex,
            kmin, kmax, noiseLevel, isOriginalImage):
        """ Change color model and channels

            @param colorModelTag: The color model tag
            @param currentImageChannelIndex: The index of current image channel
        """
        img = self.imageService.openImage(isOriginalImage)
        if img is None:
            return
        methodTimer = time.time()
        if colorModelTag == 'RGB':
            noiseGenerator.additiveNoise(img.load(),
                img.size,
                colorModelTag,
                currentImageChannelIndex,
                kmin, kmax,
                noiseLevel)
            methodTimer = time.time() - methodTimer
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
        if colorModelTag == 'YUV':
            colorModel.rgbToYuv(img.load(), img.size)
            noiseGenerator.additiveNoise(img.load(),
                img.size,
                colorModelTag,
                currentImageChannelIndex,
                kmin, kmax,
                noiseLevel)
            methodTimer = time.time() - methodTimer
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
            timerTemp = time.time()
            colorModel.yuvToRgb(img.load(), img.size)
            methodTimer = time.time() - methodTimer
        if colorModelTag == 'HSL':
            data = numpy.asarray(img, dtype="float")
            data = colorModel.rgbToHsl(data)
            noiseGenerator.additiveNoise(data,
                data.shape,
                colorModelTag,
                currentImageChannelIndex,
                kmin, kmax,
                noiseLevel)
            methodTimer = time.time() - methodTimer
            self.histogramService.saveHistogram(data=data, model=colorModelTag)
            timerTemp = time.time()
            data = colorModel.hslToRgb(data)
            img = Image.fromarray(numpy.asarray(numpy.clip(data, 0, 255), dtype="uint8"))
            methodTimer = time.time() - timerTemp + methodTimer
        logFile = '{}/temp/log/addAdditiveNoise.log'.format(self.appDir)
        with open(logFile, "a+") as text_file:
            text_file.write("Timer: {}: {}\n".format(colorModelTag, methodTimer))
        imageComparison.calculateImageDifference(colorModelTag, logFile)
        img.save('{}/temp/processingImage.png'.format(self.appDir))

    @pyqtSlot(str, int, int, int, int, bool)
    def addMultiplicativeNoise(self, colorModelTag, currentImageChannelIndex,
            kmin, kmax, noiseLevel, isOriginalImage):
        """ Change color model and channels

            @param colorModelTag: The color model tag
            @param currentImageChannelIndex: The index of current image channel
        """
        img = self.imageService.openImage(isOriginalImage)
        if img is None:
            return
        methodTimer = time.time()
        if colorModelTag == 'RGB':
            noiseGenerator.multiplicativeNoise(img.load(),
                img.size,
                colorModelTag,
                currentImageChannelIndex,
                kmin,
                kmax,
                noiseLevel)
            methodTimer = time.time() - methodTimer
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
        if colorModelTag == 'YUV':
            colorModel.rgbToYuv(img.load(), img.size)
            noiseGenerator.multiplicativeNoise(img.load(),
                img.size,
                colorModelTag,
                currentImageChannelIndex,
                kmin,
                kmax,
                noiseLevel)
            methodTimer = time.time() - methodTimer
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
            timerTemp = time.time()
            colorModel.yuvToRgb(img.load(), img.size)
            methodTimer = time.time() - methodTimer
        if colorModelTag == 'HSL':
            data = numpy.asarray(img, dtype="float")
            data = colorModel.rgbToHsl(data)
            noiseGenerator.multiplicativeNoise(data,
                data.shape,
                colorModelTag,
                currentImageChannelIndex,
                kmin,
                kmax,
                noiseLevel)
            methodTimer = time.time() - methodTimer
            self.histogramService.saveHistogram(data=data, model=colorModelTag)
            timerTemp = time.time()
            data = colorModel.hslToRgb(data)
            img = Image.fromarray(numpy.asarray(numpy.clip(data, 0, 255), dtype="uint8"))
            methodTimer = time.time() - timerTemp + methodTimer
        logFile = '{}/temp/log/addMultiplicativeNoise.log'.format(self.appDir)
        with open(logFile, "a+") as text_file:
            text_file.write("Timer: {}: {}\n".format(colorModelTag, methodTimer))
        imageComparison.calculateImageDifference(colorModelTag, logFile)
        img.save('{}/temp/processingImage.png'.format(self.appDir))
