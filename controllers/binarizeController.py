"""
    @package binarizeController
    Controller for qml Binarize
"""
import sys
import os
import numpy
import matplotlib.pyplot as plt
import random
import time
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

from imageProcessor import histogramService, imageService, imageComparison
from imageBinarize import globalThresholding, histogramBinarize
from PyQt5.QtCore import QCoreApplication, QDir 
from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtQml import QJSValue
from PIL import Image

class BinarizeController(QObject):
    """ Controller for binarize view """
    def __init__(self):
        QObject.__init__(self)
        self.appDir = QDir.currentPath()
        self.histogramService = histogramService.HistogramService()
        self.imageService = imageService.ImageService()

    @pyqtSlot(str, int, bool, int)
    def otsuBinarize(self, colorModelTag, currentImageChannelIndex, isOriginalImage,
            otsu_k):
        """
            Otsu Binarize
        """
        img = self.imageService.openImage(isOriginalImage)
        if img is None:
            return
        img = img.convert(mode='L')
        methodTimer = time.time()
        histogramBinarize.histogramSegmentation(img.load(), img.size, 'otsu', otsu_k)
        # if colorModelTag == 'RGB':
        #     filters.meanFilter(colorModelTag, currentImageChannelIndex, img.load(),
        #         img.size, (filterWidth, filterHeight))
        #     methodTimer = time.time() - methodTimer
        #     self.histogramService.saveHistogram(img=img, model=colorModelTag)
        # if colorModelTag == 'YUV':
        #     colorModel.rgbToYuv(img.load(), img.size)
        #     filters.meanFilter(colorModelTag, currentImageChannelIndex, img.load(),
        #         img.size, (filterWidth, filterHeight))
        #     colorModel.yuvToRgb(img.load(), img.size)
        #     methodTimer = time.time() - methodTimer
        #     self.histogramService.saveHistogram(img=img, model=colorModelTag)
        # if colorModelTag == 'HSL':
        #     data = numpy.asarray(img, dtype="float")
        #     data = colorModel.rgbToHsl(data)
        #     filters.meanFilter(colorModelTag, currentImageChannelIndex, data,
        #         data.shape, (filterWidth, filterHeight))
        #     methodTimer = time.time() - methodTimer
        #     self.histogramService.saveHistogram(data=data, model=colorModelTag)
        #     timerTemp = time.time()
        #     data = colorModel.hslToRgb(data)
        #     img = Image.fromarray(numpy.asarray(numpy.clip(data, 0, 255), dtype="uint8"))
        #     methodTimer = time.time() - timerTemp + methodTimer

        logFile = '{}/temp/log/meanFilter.log'.format(self.appDir)
        with open(logFile, "a+") as text_file:
            text_file.write("Timer: {}: {}\n".format(colorModelTag, methodTimer))
        img = img.convert(mode='RGB')
        img.save('{}/temp/processingImage.png'.format(self.appDir))
        imageComparison.calculateImageDifference(colorModelTag, logFile)

