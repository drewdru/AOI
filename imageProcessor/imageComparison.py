"""
    @package imageСomparison
    Image Сomparison
"""
import sys
import os
import numpy
import matplotlib.pyplot as plt
import random
import time

import math
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

from imageFilters import filters, adaptiveFilter
from imageProcessor import colorModel, histogramService, imageService
from PyQt5.QtCore import QCoreApplication, QDir 
from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtQml import QJSValue
from PIL import Image

def getImages():
    imageServices = imageService.ImageService()
    imgOriginal = imageServices.openImage(True)
    imgProcessed = imageServices.openImage(False)
    if imgOriginal is None or imgProcessed is None:
        return None, None

    imgOriginal = numpy.asarray(imgOriginal, dtype="float")
    imgProcessed = numpy.asarray(imgProcessed, dtype="float")
    return imgOriginal, imgProcessed

def calculateMSE():
    """
        Calculate PSNR
    """
    imgOriginal, imgProcessed = getImages()
    if imgOriginal is None: 0

    mse = numpy.mean((imgOriginal - imgProcessed) ** 2)
    return mse

def calculatePSNR():
    """
        Calculate PSNR
    """
    mse = calculateMSE()
    if mse == 0:
        return (100, 0)
    PIXEL_MAX = 255.0
    psnr = 20 * math.log10(PIXEL_MAX / math.sqrt(mse))
    return (mse, psnr)

def rmsDifference():
    """
        Calculate root mean square difference of two images
    """
    imgOriginal, imgProcessed = getImages()
    if imgOriginal is None: 0
    return numpy.sqrt(numpy.mean(numpy.square(imgOriginal - imgProcessed)))


def calculateImageDifference(colorModelTag, logFile):
    mse, psnr = calculatePSNR()
    rms = rmsDifference()

    with open(logFile, "a+") as text_file:
        if colorModelTag is not None:
            text_file.write("MSE: {}: {}\n".format(colorModelTag, mse))
            text_file.write("PSNR: {}: {}\n".format(colorModelTag, psnr))
            text_file.write("RMS: {}: {}\n".format(colorModelTag, rms))
        else:
            text_file.write("MSE: {}\n".format(mse))
            text_file.write("PSNR: {}\n".format(psnr))
            text_file.write("RMS: {}\n".format(rms))


