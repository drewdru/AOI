"""
    @package colorCorrectorController
    controller for color corrector
"""
import sys
import os
import numpy
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))


from imageProcessor import colorModel
from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtQml import QJSValue
from PIL import Image


class ColorCorrectorController(QObject):
    def openImage(self, isOriginalImage):
        try:
            if isOriginalImage:
                img = Image.open('inImage.png')
            else:
                img = Image.open('processingImage.png')
            return img.convert(mode='RGB')
        except:
            return None

    @pyqtSlot(int, bool)
    def changeHue(self, value, isOriginalImage):
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
        img = self.openImage(isOriginalImage)
        if img is None:
            return
        colorModel.rgbToYuv(img.load(), img.size)
        colorModel.yuvToGrayscaleRgb(img.load(), img.size)
        img.save('processingImage.png')
