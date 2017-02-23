"""
    @package colorCorrectorController
    Controller for qml colorCorrector
"""
import sys
import os
import numpy
import random
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

from imageProcessor import colorModel
from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtQml import QJSValue
from PIL import Image


class ColorCorrectorController(QObject):
    """ Controller for color corrector view """

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
        data = numpy.asarray(img, dtype="float")
        data = colorModel.rgbToHsl(data, value)
        data = colorModel.hslToRgb(data)
        img = Image.fromarray(numpy.asarray(numpy.clip(data, 0, 255), dtype="uint8"))
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
            if currentImageChannelIndex > 0:
                colorModel.viewRGBChannelByID(img.load(), img.size, currentImageChannelIndex-1)
        if colorModelTag == 'YUV':
            colorModel.rgbToYuv(img.load(), img.size, firstChannel, secondChannel, thirdChannel)
            if currentImageChannelIndex > 0:
                colorModel.viewYUVChannelByID(img.load(), img.size, currentImageChannelIndex-1)
                colorModel.yuvToRgb(img.load(), img.size)

        img.save('processingImage.png')


