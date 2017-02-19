import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

from imageProcessor import colorModel

from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtQml import QJSValue
from PIL import Image

import numpy


class IceController(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.callback = []

    def dump(self):
        print('Dump was called')
        #print('Callback is %s' % self.callback)
        #print(dir(self.callback))
        #print('Callback is callable %s' % self.callback.isCallable)
        #print('Callback is callable %s' % self.callback.isCallable())
        for c in self.callback:
            c.call([QJSValue('IT IS A TEST RESPONSE')])
        self.callback = []

    def openImage(self, isOriginalImage):
        try:
            if isOriginalImage:
                img = Image.open('inImage.png')
            else:
                img = Image.open('processingImage.png')
            return img.convert(mode='RGB')
        except:
            return None

    @pyqtSlot(str, 'QJSValue')
    def enqueue(self, command, callback):
        print('Enqueuing function of %s' % command)
        #print('Test callback is %s' % callback)
        #print('Callback is callable?:  %s' % callback.isCallable())
        self.callback.append(QJSValue(callback))
        #self.callback = callback
        #self.dump()

    @pyqtSlot()
    def processResponses(self):
        print('processing responses')
        self.dump()

    @pyqtSlot()
    def loadProcessingImage(self):
        try:
            img = Image.open('inImage.png')
            img.save('processingImage.png')
        except:
            pass

    @pyqtSlot(str)
    def openFile(self, file):
        try:
            img = Image.open(file)
            img.save('inImage.png')
        except:
            pass

    @pyqtSlot(str)
    def saveFile(self, file):
        try:
            img = Image.open('processingImage.png')
            img.save(str)
        except:
            pass

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

    @pyqtSlot(str)
    def log(self, s):
        print(s)
