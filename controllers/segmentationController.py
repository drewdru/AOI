"""
    @package segmentationController
    Controller for qml Segmentation
"""
import sys
import os
import numpy
import matplotlib.pyplot as plt
import random
import time
import math
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

from imageProcessor import colorModel, histogramService, imageService, imageComparison
from imageSegmentation import segmentation
from imageFilters import filters
from PyQt5.QtCore import QCoreApplication, QDir 
from PyQt5.QtCore import QObject, pyqtSlot, QVariant #, QVariantList
from PyQt5.QtQml import QJSValue
from PIL import Image, ImageChops

class SegmentationController(QObject):
    """ Controller for binarize view """
    def __init__(self):
        QObject.__init__(self)
        self.appDir = QDir.currentPath()
        self.histogramService = histogramService.HistogramService()
        self.imageService = imageService.ImageService()

        self.maskList = []
        self.createMaskList(3, 3)

    @pyqtSlot(int, int)
    def createMaskList(self, apertureWidth, apertureHeight):
        if len(self.maskList) ==  apertureHeight and len(self.maskList) > 0:
            if len(self.maskList[0]) == apertureWidth:
                return
        self.maskList = []
        for height in range(apertureHeight):
            modelRow = []
            for width in range(apertureWidth):
                modelRow.append(False)
            self.maskList.append(modelRow)

    @pyqtSlot(int, int, bool)
    def updateCellMaskList(self, y, x, value):
        self.maskList[x][y] = value
