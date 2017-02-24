"""
    @package colorCorrectorController
    Controller for qml colorCorrector
"""
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import random
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

from imageProcessor import colorModel, colorHistogram
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtQml import QJSValue
from PIL import Image

class ColorCorrectorController(QObject):
    """ Controller for color corrector view """
    def __init__(self):
        QObject.__init__(self)

    def openImage(self, isOriginalImage):
        """ Open image for processing

            @param isOriginalImage: The value for choose original or processing Image
        """
        try:
            if isOriginalImage:
                img = Image.open('inImage.png')
            else:
                img = Image.open('processingImage.png')
            return img.convert(mode='RGB')
        except Exception:
            return None

    def hexToRgb(self, value):
        """Return (red, green, blue) for the color given as #rrggbb."""
        value = value.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

    def rgbToHex(self, red, green, blue):
        """Return color as #rrggbb for the given color values."""
        return '#%02x%02x%02x' % (red, green, blue)

    @pyqtSlot(str, 'QJSValue')
    def getHlsFromHex(self, hexColor, callback):
        color = self.hexToRgb(hexColor)
        color = colorModel.colorRgbToHsl(color[0], color[1], color[2])
        if callback.isCallable():
            callback.call([QJSValue(color[0]), QJSValue(color[1]), QJSValue(color[2])])

    @pyqtSlot(int, bool)
    def changeHue(self, value, isOriginalImage):
        """ Change an image hue

            @param value: The hue value
            @param isOriginalImage: The value for choose original or processing Image
        """
        img = self.openImage(isOriginalImage)
        if img is None:
            return
        data = np.asarray(img, dtype="float")
        data = colorModel.rgbToHsl(data, value)
        self.saveHistogram(data=data, model='HSL')
        data = colorModel.hslToRgb(data)
        img = Image.fromarray(np.asarray(np.clip(data, 0, 255), dtype="uint8"))
        img.save('processingImage.png')

    @pyqtSlot(bool)
    def toGrayscale(self, isOriginalImage):
        """ Convert image to grayscale

            @param isOriginalImage: The value for choose original or processing Image
        """
        img = self.openImage(isOriginalImage)
        if img is None:
            return

        colorModel.rgbToYuv(img.load(), img.size)
        colorModel.yuvToGrayscaleRgb(img.load(), img.size)
        img.save('processingImage.png')
        self.saveHistogram(img=img, model='YUV')

    def savePltHist(self, histogram, title, name, color):
        QCoreApplication.processEvents()
        fig, ax = plt.subplots()
        ax.set_xlabel('Color')
        ax.set_ylabel('Frequency')
        ax.grid(True)
        ax.hist(np.arange(histogram.shape[0]), weights=histogram, facecolor=color, alpha=0.5)
        ax.set_title('Histogram {}'.format(title))
        plt.savefig('{}.png'.format(name))
        np.save(name, histogram)
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
            plt.hist(np.arange(histogram.shape[0]), weights=histogram, facecolor=colors[indx], alpha=0.5)
        plt.savefig('{}.png'.format('hist0'))
        plt.close('all')

    def pltProcessEvents(self):
        QCoreApplication.processEvents()
    
    @pyqtSlot(int, str)
    def showHistogram(self, channelId, model='RGB'):
        try:
            if channelId == 0:
                histogram = []
                histogram.append(np.load('hist1.npy'))
                histogram.append(np.load('hist2.npy'))
                histogram.append(np.load('hist3.npy'))
                facecolor = 'rgb'
            elif channelId == 1:
                histogram = np.load('hist1.npy')
                facecolor = 'r'
            elif channelId == 2:
                histogram = np.load('hist2.npy')
                facecolor = 'g'
            elif channelId == 3:
                histogram = np.load('hist3.npy')
                facecolor = 'b'
            else: return
        except FileNotFoundError:
            return
        QCoreApplication.processEvents()
        plt.close('all')
        if channelId == 0:
            plt.xlabel('Color')
            plt.ylabel('Frequency')
            plt.grid(True)
            plt.title('Histogram {}'.format(model))
            for indx, hist in enumerate(histogram):
                plt.hist(np.arange(hist.shape[0]), weights=hist, facecolor=facecolor[indx], alpha=0.5)
            fig = plt.figure(1)
            timer = fig.canvas.new_timer(interval=3)
            timer.add_callback(self.pltProcessEvents)
            timer.start()
            plt.show()
        else:
            fig, ax = plt.subplots()
            ax.set_xlabel('Color')
            ax.set_ylabel('Frequency')
            ax.grid(True)
            ax.set_title('Histogram {}'.format(model[channelId-1]))
            ax.hist(np.arange(histogram.shape[0]), weights=histogram, facecolor=facecolor, alpha=0.5)
            timer = fig.canvas.new_timer(interval=3)
            timer.add_callback(self.pltProcessEvents)
            timer.start()
            plt.show(fig)


    @pyqtSlot(str, int, bool, int, int, int)
    def changeColorModel(self, colorModelTag,
            currentImageChannelIndex,
            isOriginalImage,
            firstChannel,
            secondChannel,
            thirdChannel):
        """ Change color model and channels

            @param colorModelTag: The color model tag
            @param currentImageChannelIndex: The index of current image channel
        """
        # img = Image.open('inImage.png')
        # img = img.convert(mode='RGB')
        # if img is None:
        #     return
        img = self.openImage(isOriginalImage)
        if img is None:
            return
        if colorModelTag == 'RGB':
            colorModel.changeRgbBalance(img.load(), img.size, firstChannel, secondChannel, thirdChannel)
            self.saveHistogram(img=img)
            if currentImageChannelIndex > 0:
                colorModel.viewRGBChannelByID(img.load(), img.size, currentImageChannelIndex-1)
        if colorModelTag == 'YUV':
            colorModel.rgbToYuv(img.load(), img.size, firstChannel, secondChannel, thirdChannel)
            self.saveHistogram(img=img, model='YUV')
            if currentImageChannelIndex > 0:
                colorModel.viewYUVChannelByID(img.load(), img.size, currentImageChannelIndex-1)
                colorModel.yuvToRgb(img.load(), img.size)

        img.save('processingImage.png')


