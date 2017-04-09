import math
from PIL import PSDraw
""" Segmentations with histogram """
def getHistogramRGB(img, size):
    """
    @use:
    img = Image.open(filepath)
    img = img.convert(mode='RGB')
    img = img.resize(size, Image.ANTIALIAS)
    histogramR, histogramG, histogramB = get_histogramRGB(img, size)
    """
    histogramR = []
    histogramG = []
    histogramB = []
    for i in range(256):
        histogramR.append(0)
        histogramG.append(0)
        histogramB.append(0)
    for i in range(size[0]):
        for j in range(size[1]):
            r, g, b = img.getpixel((i, j))
            histogramR[r] += 1
            histogramG[g] += 1
            histogramB[b] += 1
    histogram = []
    for i in range(256):
        histogramR[i] /= size[0]*size[1]
        histogramG[i] /= size[0]*size[1]
        histogramB[i] /= size[0]*size[1]
    return histogramR, histogramG, histogramB

def getHistogram(pixels, size):
    histogram = []
    for i in range(256):
        histogram.append(0)
    for i in range(size[0]):
        for j in range(size[1]):
            color = pixels[i, j]
            histogram[color] += 1
    for i in range(256):
        histogram[i] /= size[0]*size[1]
    return histogram

def histogramPeak3(histogram, size, k):
    k /= 256
    peak = []
    lastValue = 0
    maxVal = max(histogram)
    for indx, v in enumerate(histogram):
        if maxVal - v > k:
            peak.append(indx-1)
    return peak

def otsuPeak(histogram, size, k):
    peak = []
    lastValue = 0
    w1 = 0
    w2 = 0
    w = 0
    mu1 = 0
    mu2 = 0
    mu = 0
    for indx, v in enumerate(histogram):
        if (indx <= k):
            w1 += v
        else:
            w2 += v
    for indx, v in enumerate(histogram):
        value = indx*v
        if (indx <= k):
            mu1 += value/w1
        else:
            mu2 += value/w2
        mu += (value/w1 + value/w2)
    nu = (w1*w2*((mu2-mu1)**2))/(mu**2)
    for indx, v in enumerate(histogram):
        if v < nu:
            peak.append(indx-1)
    return peak

def histogramSegmentation(pixels, size, method, k):
    """http://www.ijcset.net/docs/Volumes/volume2issue1/ijcset2012020103.pdf"""
    # pixels = img.load()
    histogram = getHistogram(pixels, size)
    if method == 'otsu':
        peak = otsuPeak(histogram, size, k)
        for i in range(size[0]):
            for j in range(size[1]):
                if pixels[i, j] in peak:
                    pixels[i, j] = 255
                else:
                    pixels[i, j] = 0
        # img.show('histogramPeak')
    if method == 'histPeakValue':
        peak = histogramPeak3(histogram, size, k)
        for i in range(size[0]):
            for j in range(size[1]):
                if pixels[i, j] in peak:
                    pixels[i, j] = 255
                else:
                    pixels[i, j] = 0
        # img.show('histogramPeak3')
