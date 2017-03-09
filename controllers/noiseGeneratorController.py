"""
    @package noiseGeneratorController
    Controller for qml noiseGenerator
"""
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import random
import time

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

from imageProcessor import colorModel, noiseGenerator, colorHistogram
from imageProcessor import histogramService, imageService
from PyQt5.QtCore import QCoreApplication, QDir 
from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtQml import QJSValue
from PIL import Image

class NoiseGeneratorController(QObject):
    """ Controller for color corrector view """
    def __init__(self):
        QObject.__init__(self)
        self.appDir = QDir.currentPath()
        self.histogramService = histogramService.HistogramService()
        self.imageService = imageService.ImageService()

    @pyqtSlot(str, int, int, int, bool)
    def addImpulsNoise(self, colorModelTag, currentImageChannelIndex, impulseNoise, noiseLevel, isOriginalImage):
        """ Change color model and channels

            @param colorModelTag: The color model tag
            @param currentImageChannelIndex: The index of current image channel
        """
        img = self.imageService.openImage(isOriginalImage)
        if img is None:
            return
        start_time = time.time()
        if colorModelTag == 'RGB':
            noiseGenerator.impulsNoise(img.load(),
                img.size,
                colorModelTag,
                currentImageChannelIndex,
                impulseNoise,
                noiseLevel)
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
        if colorModelTag == 'YUV':
            colorModel.rgbToYuv(img.load(), img.size)
            noiseGenerator.impulsNoise(img.load(),
                img.size,
                colorModelTag,
                currentImageChannelIndex,
                impulseNoise,
                noiseLevel)
            colorModel.yuvToRgb(img.load(), img.size)
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
        if colorModelTag == 'HSL':
            data = np.asarray(img, dtype="float")
            data = colorModel.rgbToHsl(data)
            noiseGenerator.impulsNoise(data,
                data.shape,
                colorModelTag,
                currentImageChannelIndex,
                impulseNoise,
                noiseLevel)
            self.histogramService.saveHistogram(data=data, model=colorModelTag)
            data = colorModel.hslToRgb(data)
            img = Image.fromarray(np.asarray(np.clip(data, 0, 255), dtype="uint8"))        
        with open('{}/temp/addImpulsNoise{}.log'.format(self.appDir, colorModelTag), "a+") as text_file:
            text_file.write("{}\n".format(time.time() - start_time))

        img.save('{}/temp/processingImage.png'.format(self.appDir))

    @pyqtSlot(str, int, int, int, bool)
    def addAdditiveNoise(self, colorModelTag, currentImageChannelIndex, deviation, noiseLevel, isOriginalImage):
        """ Change color model and channels

            @param colorModelTag: The color model tag
            @param currentImageChannelIndex: The index of current image channel
        """
        img = self.imageService.openImage(isOriginalImage)
        if img is None:
            return
        start_time = time.time()
        if colorModelTag == 'RGB':
            noiseGenerator.additiveNoise(img.load(),
                img.size,
                colorModelTag,
                currentImageChannelIndex,
                deviation,
                noiseLevel)
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
        if colorModelTag == 'YUV':
            colorModel.rgbToYuv(img.load(), img.size)
            noiseGenerator.additiveNoise(img.load(),
                img.size,
                colorModelTag,
                currentImageChannelIndex,
                deviation,
                noiseLevel)
            colorModel.yuvToRgb(img.load(), img.size)
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
        if colorModelTag == 'HSL':
            data = np.asarray(img, dtype="float")
            data = colorModel.rgbToHsl(data)
            noiseGenerator.additiveNoise(data,
                data.shape,
                colorModelTag,
                currentImageChannelIndex,
                deviation,
                noiseLevel)
            self.histogramService.saveHistogram(data=data, model=colorModelTag)
            data = colorModel.hslToRgb(data)
            img = Image.fromarray(np.asarray(np.clip(data, 0, 255), dtype="uint8"))        
        with open('{}/temp/addAdditiveNoise{}.log'.format(self.appDir, colorModelTag), "a+") as text_file:
            text_file.write("{}\n".format(time.time() - start_time))

        img.save('{}/temp/processingImage.png'.format(self.appDir))

    @pyqtSlot(str, int, int, int, int, bool)
    def addMultiplicativeNoise(self, colorModelTag, currentImageChannelIndex, kmin, kmax, noiseLevel, isOriginalImage):
        """ Change color model and channels

            @param colorModelTag: The color model tag
            @param currentImageChannelIndex: The index of current image channel
        """
        img = self.imageService.openImage(isOriginalImage)
        if img is None:
            return
        start_time = time.time()
        if colorModelTag == 'RGB':
            noiseGenerator.multiplicativeNoise(img.load(),
                img.size,
                colorModelTag,
                currentImageChannelIndex,
                kmin,
                kmax,
                noiseLevel)
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
            colorModel.yuvToRgb(img.load(), img.size)
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
        if colorModelTag == 'HSL':
            data = np.asarray(img, dtype="float")
            data = colorModel.rgbToHsl(data)
            noiseGenerator.multiplicativeNoise(data,
                data.shape,
                colorModelTag,
                currentImageChannelIndex,
                kmin,
                kmax,
                noiseLevel)
            self.histogramService.saveHistogram(data=data, model=colorModelTag)
            data = colorModel.hslToRgb(data)
            img = Image.fromarray(np.asarray(np.clip(data, 0, 255), dtype="uint8"))        
        with open('{}/temp/addMultiplicativeNoise{}.log'.format(self.appDir, colorModelTag), "a+") as text_file:
            text_file.write("{}\n".format(time.time() - start_time))


        img.save('{}/temp/processingImage.png'.format(self.appDir))
