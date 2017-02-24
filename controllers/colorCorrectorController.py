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

    def saveHistogram(self, img=None, data=None, model='RGB'):
        if not img is None:
            histogram1, histogram2, histogram3 = colorHistogram.getHistogramImage(
                img.load(), img.size)
        elif not data is None:
            histogram1, histogram2, histogram3 = colorHistogram.getHistogramArray(
                data)
        else: return

        QCoreApplication.processEvents()
        # print(histogram1.shape)
        plt.hist(np.arange(histogram1.shape[0]), weights=histogram1, facecolor='r', alpha=0.75)
        plt.title('Histogram {}'.format(model[0]))
        plt.savefig('hist1.png')
        np.save('hist1', histogram1)
        plt.close('all')

        QCoreApplication.processEvents()
        plt.hist(np.arange(histogram2.shape[0]), weights=histogram2, facecolor='g', alpha=0.75)
        plt.title('Histogram {}'.format(model[1]))
        plt.savefig('hist2.png')
        np.save('hist2', histogram2)
        plt.close('all')

        QCoreApplication.processEvents()
        plt.hist(np.arange(histogram3.shape[0]), weights=histogram3, facecolor='b', alpha=0.75)
        plt.title('Histogram {}'.format(model[2]))
        plt.savefig('hist3.png')
        np.save('hist3', histogram3)
        plt.close('all')

        self.showHistogram(1, model='HSL')

    def pltProcessEvents(self):
        QCoreApplication.processEvents()

    def showHistogram(self, channelId, model='RGB'):
        try:
            if channelId == 0:
                histogram = np.load('hist1.npy')
                facecolor = 'r'
            elif channelId == 1:
                histogram = np.load('hist2.npy')
                facecolor = 'g'
            elif channelId == 2:
                histogram = np.load('hist3.npy')
                facecolor = 'b'
            else: return
        except FileNotFoundError:
            return

        plt.close('all')

        fig, ax = plt.subplots()
        ax.set_xlabel('Color')
        ax.set_ylabel('Frequency')
        ax.grid(True)
        ax.set_title('Histogram {}'.format(model[channelId]))
        ax.hist(np.arange(histogram.shape[0]), weights=histogram, facecolor=facecolor, alpha=0.75)
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


