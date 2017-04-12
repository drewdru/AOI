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
from imageBinarize import globalThresholding, localThresholding
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
        globalThresholding.histogramSegmentation(img.load(), img.size, 'otsu', otsu_k)
        methodTimer = time.time() - methodTimer
        logFile = '{}/temp/log/otsuBinarize.log'.format(self.appDir)
        with open(logFile, "a+") as text_file:
            text_file.write("Timer: {}: {}\n".format(colorModelTag, methodTimer))
        img = img.convert(mode='RGB')
        img.save('{}/temp/processingImage.png'.format(self.appDir))
        imageComparison.calculateImageDifference(colorModelTag, logFile)

    @pyqtSlot(str, int, bool, int)
    def histThresholdBinarize(self, colorModelTag, currentImageChannelIndex, isOriginalImage,
            otsu_k):
        """
            Otsu Binarize
        """
        img = self.imageService.openImage(isOriginalImage)
        if img is None:
            return
        img = img.convert(mode='L')
        methodTimer = time.time()
        globalThresholding.histogramSegmentation(img.load(), img.size, 'histPeakValue', otsu_k)
        methodTimer = time.time() - methodTimer
        logFile = '{}/temp/log/histThresholdBinarize.log'.format(self.appDir)
        with open(logFile, "a+") as text_file:
            text_file.write("Timer: {}: {}\n".format(colorModelTag, methodTimer))
        img = img.convert(mode='RGB')
        img.save('{}/temp/processingImage.png'.format(self.appDir))
        imageComparison.calculateImageDifference(colorModelTag, logFile)

