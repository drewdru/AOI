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
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtQml import QJSValue
from PIL import Image

class NoiseGeneratorController(QObject):
    """ Controller for color corrector view """
    def __init__(self):
        QObject.__init__(self)
        self.appDir = os.getcwd()

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
            self.saveHistogram(img=img, model=colorModelTag)
        if colorModelTag == 'YUV':
            colorModel.rgbToYuv(img.load(), img.size)
            noiseGenerator.impulsNoise(img.load(),
                img.size,
                colorModelTag,
                impulseNoise,
                noiseLevel)
            self.saveHistogram(img=img, model=colorModelTag)
        if colorModelTag == 'HSL':
            data = np.asarray(img, dtype="float")
            data = colorModel.rgbToHsl(data)
            noiseGenerator.impulsNoise(data,
                data.shape,
                colorModelTag,
                impulseNoise,
                noiseLevel)
            self.saveHistogram(data=data, model=colorModelTag)
            data = colorModel.hslToRgb(data)
            img = Image.fromarray(np.asarray(np.clip(data, 0, 255), dtype="uint8"))

        img.save('{}/temp/processingImage.png'.format(self.appDir))


    def savePltHist(self, histogram, title, name, color):
        QCoreApplication.processEvents()
        fig, ax = plt.subplots()
        ax.set_xlabel('Color')
        ax.set_ylabel('Frequency')
        ax.grid(True)
        ax.hist(np.arange(histogram.shape[0]),
            weights=histogram,
            facecolor=color,
            alpha=0.5)
        ax.set_title('Histogram {}'.format(title))
        plt.savefig('{}/temp/{}.png'.format(self.appDir, name))
        np.save('{}/temp/{}'.format(self.appDir, name), histogram)
        plt.close('all')

    def saveHistogram(self, img=None, data=None, model='RGB'):
        if not img is None:
            histogram1, histogram2, histogram3 = colorHistogram.getHistogramImage(
                img.load(), img.size)
        elif not data is None:
            histogram1, histogram2, histogram3 = colorHistogram.getHistogramArray(
                data)
        else: return

        self.savePltHist(histogram1, model[0], 'hist1', 'r')
        self.savePltHist(histogram2, model[1], 'hist2', 'g')
        self.savePltHist(histogram3, model[2], 'hist3', 'b')

        QCoreApplication.processEvents()
        plt.xlabel('Color')
        plt.ylabel('Frequency')
        plt.grid(True)
        plt.title('Histogram {}'.format(model))
        colors = 'rgb'
        for indx, histogram in enumerate([histogram1, histogram2, histogram3]):
            plt.hist(np.arange(histogram.shape[0]),
                weights=histogram,
                facecolor=colors[indx],
                alpha=0.5)
        plt.savefig('{}/temp/{}.png'.format(self.appDir, 'hist0'))
        plt.close('all')

        with open('{}/temp/temp.config'.format(self.appDir), "w") as text_file:
            text_file.write(model)
    


