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

from imageFilters import filters
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
        filters.meanFilter(img.load(), img.size, (filterWidth, filterHeight))
        with open('{}/temp/log/meanFilter.log'.format(self.appDir), "a+") as text_file:
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
        filters.medianFilter(img.load(), img.size, (filterWidth, filterHeight))
        with open('{}/temp/log/medianFilter.log'.format(self.appDir), "a+") as text_file:
            text_file.write("{}\n".format(time.time() - start_time))
        self.histogramService.saveHistogram(img=img)
        img.save('{}/temp/processingImage.png'.format(self.appDir))

    @pyqtSlot(bool, int, int)
    def gaussianBlur(self, isOriginalImage, filterWidth, filterHeight):
        """
            Mean filter
        """
        img = self.imageService.openImage(isOriginalImage)
        if img is None:
            return
        start_time = time.time()
        filters.gaussianBlur(img.load(), img.size, (filterWidth, filterHeight))
        with open('{}/temp/log/gaussianBlur.log'.format(self.appDir), "a+") as text_file:
            text_file.write("{}\n".format(time.time() - start_time))
        self.histogramService.saveHistogram(img=img)
        img.save('{}/temp/processingImage.png'.format(self.appDir))

    @pyqtSlot(bool, int, int, int, int)
    def bilateralFilter(self, isOriginalImage, filterWidth, filterHeight, sigma_i, sigma_s):
        """
            Mean filter
        """
        img = self.imageService.openImage(isOriginalImage)
        if img is None:
            return
        start_time = time.time()
        filters.bilateralFilter(img.load(), img.size, (filterWidth, filterHeight), sigma_i, sigma_s)
        with open('{}/temp/log/bilateralFilter.log'.format(self.appDir), "a+") as text_file:
            text_file.write("{}\n".format(time.time() - start_time))
        self.histogramService.saveHistogram(img=img)
        img.save('{}/temp/processingImage.png'.format(self.appDir))

    @pyqtSlot(bool, int, int, int)
    def laplacianBlur(self, isOriginalImage, filterWidth, filterHeight, sigma):
        """
            Mean filter
        """
        img = self.imageService.openImage(isOriginalImage)
        if img is None:
            return
        start_time = time.time()
        filters.laplacianBlur(img.load(), img.size, (filterWidth, filterHeight), sigma)
        with open('{}/temp/log/laplacianBlur.log'.format(self.appDir), "a+") as text_file:
            text_file.write("{}\n".format(time.time() - start_time))
        self.histogramService.saveHistogram(img=img)
        img.save('{}/temp/processingImage.png'.format(self.appDir))

    @pyqtSlot(bool, int, int, int)
    def cleanerFilterByJimCasaburi(self, isOriginalImage, filterWidth, filterHeight, threshold):
        """
            Mean filter
        """
        img = self.imageService.openImage(isOriginalImage)
        if img is None:
            return
        start_time = time.time()
        filters.cleanerFilterByJimCasaburi(img.load(), img.size, (filterWidth, filterHeight), threshold)
        with open('{}/temp/log/cleanerFilterByJimCasaburi.log'.format(self.appDir), "a+") as text_file:
            text_file.write("{}\n".format(time.time() - start_time))
        self.histogramService.saveHistogram(img=img)
        img.save('{}/temp/processingImage.png'.format(self.appDir))

