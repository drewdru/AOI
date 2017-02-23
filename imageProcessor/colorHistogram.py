import numpy
from PyQt5.QtCore import QCoreApplication
def getHistogramImage(pixels, size):
    """
    @use:
    img = Image.open(filepath)
    img = img.convert(mode='RGB')
    img = img.resize(size, Image.ANTIALIAS)
    histogramR, histogramG, histogramB = get_histogramRGB(img, size)
    """
    histogram1 = numpy.zeros(256)
    histogram2 = numpy.zeros(256)
    histogram3 = numpy.zeros(256)
    for i in range(size[0]):
        QCoreApplication.processEvents()
        for j in range(size[1]):
            channel1, channel2, channel3 = pixels[i, j]
            histogram1[channel1] += 1
            histogram2[channel2] += 1
            histogram3[channel3] += 1
    return histogram1, histogram2, histogram3

def getHistogramArray(npPixels):
    histogram1 = numpy.zeros(361)
    histogram2 = numpy.zeros(101)
    histogram3 = numpy.zeros(101)
    for i, pixels in enumerate(npPixels):
        QCoreApplication.processEvents()
        for j, pixel in enumerate(pixels):
            channel1, channel2, channel3 = pixel
            histogram1[int(channel1)] += 1
            histogram2[int(channel2)] += 1
            histogram3[int(channel3)] += 1
    return histogram1, histogram2, histogram3