import os
import sys
from PIL import Image
import threading
import multiprocessing
import math
import numpy

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

from PyQt5.QtCore import QCoreApplication
from imageProcessor import colorHistogram

def avgHistogram(histogram, n):
    for i, hist in enumerate(histogram):
        QCoreApplication.processEvents()
        histogram[i] = histogram[i] / n * i
    return histogram

def normolizeHistogram(histogram):
    for i, hist in enumerate(histogram):
        QCoreApplication.processEvents()
        histogram[i] = histogram[i-1] + histogram[i]
    return histogram

def normolizeChannelColor(maxValue, channelValue, newValue):
    if (channelValue + newValue >= 0) and (channelValue + newValue <= maxValue):
        channelValue += newValue
    elif channelValue + newValue < 0:
        channelValue = 0
    else:
        channelValue = maxValue
    return channelValue

def histogramEqualization(pixels, size):
    N = size[0] * size[1]

    histogram1, histogram2, histogram3 = colorHistogram.getHistogramImage(pixels, size)

    histogram1 = avgHistogram(histogram1, N)
    histogram2 = avgHistogram(histogram2, N)
    histogram3 = avgHistogram(histogram3, N)

    histogramm1 = normolizeHistogram(histogram1)
    histogramm2 = normolizeHistogram(histogram2)
    histogramm3 = normolizeHistogram(histogram3)

    for i in range(size[0]):
        QCoreApplication.processEvents()
        for j in range(size[1]):
            channel1, channel2, channel3 = pixels[i, j]

            maxValue = len(histogramm1) - 1
            value = round(histogramm1[int(channel1)])
            channel1 = normolizeChannelColor(maxValue, channel1, value)

            maxValue = len(histogramm2) - 1
            value = round(histogramm2[int(channel2)])
            channel2 = normolizeChannelColor(maxValue, channel2, value)

            maxValue = len(histogramm3) - 1
            value = round(histogramm3[int(channel3)])
            channel3 = normolizeChannelColor(maxValue, channel3, value)

            pixels[i, j] = (int(channel1), int(channel2), int(channel3))

def gamma(pixels, size, value):
    RampTable = [] #new uchar[256]
    temp = 5.0 if 5.0 <= value else value
    Gam = 0.1 if 0.1 >= temp else temp
    G = 1 / Gam

    for i in range(256):
        temp = (pow(i / 255.0, G) * 255 + 0.5)
        value = 255 if 255 <= temp else int(temp)
        RampTable.append(value)

    for i in range(size[0]):
        QCoreApplication.processEvents()
        for j in range(size[1]):
            channel1, channel2, channel3 = pixels[i, j]
            pixels[i, j] = (RampTable[channel1], RampTable[channel2], RampTable[channel3])

def toGrayWorld(pixels, size):
    avgR = avgG = avgB = avg = 0
    N = size[0] * size[1]

    for i in range(size[0]):
        QCoreApplication.processEvents()
        for j in range(size[1]):
            channel1, channel2, channel3 = pixels[i, j]
            avgR += channel1
            avgG += channel2
            avgB += channel3

    avgR = (avgR)/N;
    avgG = (avgG)/N;
    avgB = (avgB)/N;
    if avgR == 0: avgR = 0.1
    if avgG == 0: avgG = 0.1
    if avgB == 0: avgB = 0.1
    avg = (avgR + avgG + avgB) / 3.0

    for i in range(size[0]):
        QCoreApplication.processEvents()
        for j in range(size[1]):
            channel1, channel2, channel3 = pixels[i, j]

            if (channel1 * avg / avgR) > 255: channel1 = 255
            else: channel1 = (channel1 * avg / avgR)

            if (channel2 * avg / avgR) > 255: channel2 = 255
            else: channel2 = (channel2 * avg / avgR)

            if (channel3 * avg / avgR) > 255: channel3 = 255
            else: channel3 = (channel3 * avg / avgR)

            pixels[i, j] = (int(channel1), int(channel2), int(channel3))

def autolevels(pixels, size):
    channel1, channel2, channel3 = pixels[0, 0]
    minR = maxR = channel1
    minG = maxG = channel2
    minB = maxB = channel3

    for i in range(size[0]):
        QCoreApplication.processEvents()
        for j in range(size[1]):
            channel1, channel2, channel3 = pixels[i, j]

            minR = min(channel1, minR)
            minG = min(channel2, minG)
            minB = min(channel3, minB)

            maxR = max(channel1, maxR)
            maxG = max(channel2, maxG)
            maxB = max(channel3, maxB)

    for i in range(size[0]):
        QCoreApplication.processEvents()
        for j in range(size[1]):
            channel1, channel2, channel3 = pixels[i, j]

            try:
                channel1 = (channel1 - minR)*(255/(maxR - minR))
                channel2 = (channel2 - minG)*(255/(maxG - minG))
                channel3 = (channel3 - minB)*(255/(maxB - minB))
            except ZeroDivisionError:
                pass

            if channel3 > channel1 and channel3 > channel2:
                channel3 = channel2

            pixels[i, j] = (int(channel1), int(channel2), int(channel3))
