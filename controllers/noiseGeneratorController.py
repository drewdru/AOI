"""
    @package noiseGeneratorController
    Controller for qml noiseGenerator
"""
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import random
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

from imageProcessor import colorModel, noiseGenerator, colorHistogram
from services import histogramService
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtQml import QJSValue
from PIL import Image

class NoiseGeneratorController(QObject):
    """ Controller for color corrector view """
    def __init__(self):
        QObject.__init__(self)
        self.appDir = os.getcwd()
        self.histogramService = histogramService.HistogramService()

    def openImage(self, isOriginalImage):
        """ Open image for processing

            @param isOriginalImage: The value for choose original or processing Image
        """
        try:
            if isOriginalImage:
                img = Image.open('{}/temp/inImage.png'.format(self.appDir))
            else:
                img = Image.open('{}/temp/processingImage.png'.format(self.appDir))
            return img.convert(mode='RGB')
        except Exception:
            return None

    @pyqtSlot(str, int, int, bool)
    def addImpulsNoise(self, colorModelTag, impulseNoise, noiseLevel, isOriginalImage):
        """ Change color model and channels

            @param colorModelTag: The color model tag
            @param currentImageChannelIndex: The index of current image channel
        """
        img = self.openImage(isOriginalImage)
        if img is None:
            return
        if colorModelTag == 'RGB':
            noiseGenerator.impulsNoise(img.load(),
                img.size,
                colorModelTag,
                impulseNoise,
                noiseLevel)
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
        if colorModelTag == 'YUV':
            colorModel.rgbToYuv(img.load(), img.size)
            noiseGenerator.impulsNoise(img.load(),
                img.size,
                colorModelTag,
                impulseNoise,
                noiseLevel)
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
        if colorModelTag == 'HSL':
            data = np.asarray(img, dtype="float")
            data = colorModel.rgbToHsl(data)
            noiseGenerator.impulsNoise(data,
                data.shape,
                colorModelTag,
                impulseNoise,
                noiseLevel)
            self.histogramService.saveHistogram(data=data, model=colorModelTag)
            data = colorModel.hslToRgb(data)
            img = Image.fromarray(np.asarray(np.clip(data, 0, 255), dtype="uint8"))

        img.save('{}/temp/processingImage.png'.format(self.appDir))




    
    


