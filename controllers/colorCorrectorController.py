"""
    @package colorCorrectorController
    Controller for qml colorCorrector
"""
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import random
import time
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

from imageProcessor import colorModel, colorHistogram, colorCorrector
from imageProcessor import histogramService, imageService
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtQml import QJSValue
from PIL import Image

class ColorCorrectorController(QObject):
    """ Controller for color corrector view """
    def __init__(self):
        QObject.__init__(self)
        self.appDir = os.getcwd()
        self.histogramService = histogramService.HistogramService()
        self.imageService = imageService.ImageService()

    def hexToRgb(self, value):
        """Return (red, green, blue) for the color given as #rrggbb."""
        value = value.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

    def rgbToHex(self, red, green, blue):
        """Return color as #rrggbb for the given color values."""
        return '#%02x%02x%02x' % (red, green, blue)

    @pyqtSlot(str, 'QJSValue')
    def getHslFromHex(self, hexColor, callback):
        color = self.hexToRgb(hexColor)
        print(color)
        color = colorModel.colorRgbToHsl(color[0], color[1], color[2])
        print((color[0], color[1], color[2]))
        if callback.isCallable():
            callback.call([QJSValue(color[0]), QJSValue(color[1]), QJSValue(color[2])])
    
    @pyqtSlot(bool, int, int, int)
    def changeHueByPallet(self, isOriginalImage, hValue=0, sValue=0, lValue=0):
        self.changeHue(self, isOriginalImage, hValue=hValue, sValue=sValue, lValue=lValue)

    @pyqtSlot(bool, int)
    def changeHue(self, isOriginalImage, value=None, hValue=0, sValue=0, lValue=0):
        """ Change an image hue

            @param value: The hue value
            @param isOriginalImage: The value for choose original or processing Image
        """
        img = self.imageService.openImage(isOriginalImage)
        if img is None:
            return
        start_time = time.time()
        data = np.asarray(img, dtype="float")
        data = colorModel.rgbToHsl(data, value=value, hValue=hValue, sValue=sValue, lValue=lValue)
        print("--- %s seconds ---" % (time.time() - start_time))
        self.histogramService.saveHistogram(data=data, model='HSL')
        data = colorModel.hslToRgb(data)
        img = Image.fromarray(np.asarray(np.clip(data, 0, 255), dtype="uint8"))
        img.save('{}/temp/processingImage.png'.format(self.appDir))

    @pyqtSlot(bool)
    def toGrayscale(self, isOriginalImage):
        """ Convert image to grayscale

            @param isOriginalImage: The value for choose original or processing Image
        """
        img = self.imageService.openImage(isOriginalImage)
        if img is None:
            return

        colorModel.rgbToYuv(img.load(), img.size)
        colorModel.yuvToGrayscaleRgb(img.load(), img.size)
        img.save('{}/temp/processingImage.png'.format(self.appDir))
        self.histogramService.saveHistogram(img=img, model='RGB')

    def pltProcessEvents(self):
        QCoreApplication.processEvents()

    @pyqtSlot(int)
    def showHistogram(self, channelId):
        try:
            if channelId == 0:
                histograms = []
                histograms.append(np.load('{}/temp/hist1.npy'.format(self.appDir)))
                histograms.append(np.load('{}/temp/hist2.npy'.format(self.appDir)))
                histograms.append(np.load('{}/temp/hist3.npy'.format(self.appDir)))
                facecolor = 'rgb'
            elif channelId == 1:
                histogram = np.load('{}/temp/hist1.npy'.format(self.appDir))
                facecolor = 'r'
            elif channelId == 2:
                histogram = np.load('{}/temp/hist2.npy'.format(self.appDir))
                facecolor = 'g'
            elif channelId == 3:
                histogram = np.load('{}/temp/hist3.npy'.format(self.appDir))
                facecolor = 'b'
            else: return
        except FileNotFoundError:
            return
        try:
            with open('{}/temp/temp.config'.format(self.appDir), "r") as text_file:
                model = text_file.read()
        except FileNotFoundError:
            model = "RGB"
        QCoreApplication.processEvents()
        plt.close('all')
        if channelId == 0:
            plt.xlabel('Color')
            plt.ylabel('Frequency')
            plt.grid(True)
            plt.title('Histogram {}'.format(model))
            for indx, hist in enumerate(histograms):
                plt.hist(np.arange(hist.shape[0]),
                    weights=hist,
                    facecolor=facecolor[indx],
                    alpha=0.5)
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
            ax.set_title('Histogram {}'.format(model[channelId - 1]))
            ax.hist(np.arange(histogram.shape[0]),
                weights=histogram,
                facecolor=facecolor,
                alpha=0.5)
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
        img = self.imageService.openImage(isOriginalImage)
        if img is None:
            return
        if colorModelTag == 'RGB':
            colorModel.changeRgbBalance(img.load(),
                img.size,
                firstChannel,
                secondChannel,
                thirdChannel)
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
            if currentImageChannelIndex > 0:
                colorModel.viewRGBChannelByID(img.load(),
                    img.size,
                    currentImageChannelIndex - 1)
        if colorModelTag == 'YUV':
            colorModel.rgbToYuv(img.load(),
                img.size,
                firstChannel,
                secondChannel,
                thirdChannel)
            self.histogramService.saveHistogram(img=img, model=colorModelTag)
            if currentImageChannelIndex > 0:
                colorModel.viewYUVChannelByID(img.load(),
                    img.size,
                    currentImageChannelIndex - 1)
                colorModel.yuvToRgb(img.load(), img.size)
        if colorModelTag == 'HSL':
            data = np.asarray(img, dtype="float")
            data = colorModel.rgbToHsl(data,
                None,
                firstChannel,
                secondChannel,
                thirdChannel)
            self.histogramService.saveHistogram(data=data, model=colorModelTag)
            data = colorModel.hslToRgb(data)
            img = Image.fromarray(np.asarray(np.clip(data, 0, 255), dtype="uint8"))

        img.save('{}/temp/processingImage.png'.format(self.appDir))

    @pyqtSlot(bool)
    def histogramEqualization(self, isOriginalImage):
        """
            Normolize image histograms
        """
        img = self.imageService.openImage(isOriginalImage)
        if img is None:
            return
        colorCorrector.histogramEqualization(img.load(), img.size)
        self.histogramService.saveHistogram(img=img)
        img.save('{}/temp/processingImage.png'.format(self.appDir))

    @pyqtSlot(bool, float)
    def changeGamma(self, isOriginalImage, value):
        """
            Change image gamma
        """
        img = self.imageService.openImage(isOriginalImage)
        if img is None:
            return
        colorCorrector.gamma(img.load(), img.size, value)
        self.histogramService.saveHistogram(img=img)
        img.save('{}/temp/processingImage.png'.format(self.appDir))

    @pyqtSlot(bool)
    def toGrayWorld(self, isOriginalImage):
        """
            Convert image to gray world

            @param isOriginalImage: The value for choose original or processing Image
        """
        img = self.imageService.openImage(isOriginalImage)
        if img is None:
            return
        colorCorrector.toGrayWorld(img.load(), img.size)
        self.histogramService.saveHistogram(img=img)
        img.save('{}/temp/processingImage.png'.format(self.appDir))

    @pyqtSlot(bool)
    def toAutolevels(self, isOriginalImage):
        """
            Convert image to autolevels

            @param isOriginalImage: The value for choose original or processing Image
        """
        img = self.imageService.openImage(isOriginalImage)
        if img is None:
            return
        colorCorrector.autolevels(img.load(), img.size)
        self.histogramService.saveHistogram(img=img)
        img.save('{}/temp/processingImage.png'.format(self.appDir))