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

from imageFilters import linearFilters
from imageProcessor import histogramService, imageService
from PyQt5.QtCore import QCoreApplication, QDir 
from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtQml import QJSValue
from PIL import Image

class FiltersController(QObject):
    """ Controller for color corrector view """
    def __init__(self):
        QObject.__init__(self)
        self.appDir = QDir.currentPath()
        self.histogramService = histogramService.HistogramService()
        self.imageService = imageService.ImageService()

    @pyqtSlot(bool, int, int)
    def meanFilter(self, isOriginalImage, filterWidth, filterHeight):
        """
            Mean filter
        """
        img = self.imageService.openImage(isOriginalImage)
        if img is None:
            return
        start_time = time.time()
        linearFilters.meanFilter(img.load(), img.size, (filterWidth, filterHeight))
        with open('{}/temp/meanFilter.log'.format(self.appDir), "a+") as text_file:
            text_file.write("{}\n".format(time.time() - start_time))
        self.histogramService.saveHistogram(img=img)
        img.save('{}/temp/processingImage.png'.format(self.appDir))

    @pyqtSlot(bool, int, int)
    def medianFilter(self, isOriginalImage, filterWidth, filterHeight):
        """
            Mean filter
        """
        img = self.imageService.openImage(isOriginalImage)
        if img is None:
            return
        start_time = time.time()
        linearFilters.medianFilter(img.load(), img.size, (filterWidth, filterHeight))
        with open('{}/temp/medianFilter.log'.format(self.appDir), "a+") as text_file:
            text_file.write("{}\n".format(time.time() - start_time))
        self.histogramService.saveHistogram(img=img)
        img.save('{}/temp/processingImage.png'.format(self.appDir))
