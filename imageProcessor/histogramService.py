import sys
import os
import numpy
import matplotlib.pyplot as plt

from imageProcessor import colorModel, colorHistogram
from PyQt5.QtCore import QCoreApplication, QObject, QDir

class HistogramService(QObject):
    def __init__(self, appDir=None):
        QObject.__init__(self)
        self.appDir = QDir.currentPath() if appDir is None else appDir

    def savePltHist(self, histogram, title, name, color):
        QCoreApplication.processEvents()
        fig, ax = plt.subplots()
        ax.set_title('Histogram {}'.format(title))
        self.setupAx(ax)
        ax.hist(numpy.arange(histogram.shape[0]),
            weights=histogram,
            rwidth=0.1,
            facecolor=color,
            alpha=0.5)
        plt.savefig('{}/temp/{}.png'.format(self.appDir, name))
        numpy.save('{}/temp/{}'.format(self.appDir, name), histogram)
        plt.close('all')

    def saveHistogram(self, img=None, data=None, model='RGB'):
        if not img is None:
            histogram1, histogram2, histogram3 = colorHistogram.getHistogramImage(
                img.load(), img.size)
        elif not data is None:
            histogram1, histogram2, histogram3 = colorHistogram.getHistogramArray(
                data)
        else: return

        self.savePltHist(histogram1, model[0], 'hist1', 'r')
        self.savePltHist(histogram2, model[1], 'hist2', 'g')
        self.savePltHist(histogram3, model[2], 'hist3', 'b')

        QCoreApplication.processEvents()
        fig, ax = plt.subplots()
        ax.set_title('Histogram {}'.format(model))
        self.setupAx(ax)
        colors = 'rgb'
        for indx, histogram in enumerate([histogram1, histogram2, histogram3]):
            ax.hist(numpy.arange(histogram.shape[0]),
                weights=histogram,
                rwidth=0.1,
                facecolor=colors[indx],
                alpha=0.5)
        plt.savefig('{}/temp/{}.png'.format(self.appDir, 'hist0'))
        plt.close('all')

        with open('{}/temp/temp.config'.format(self.appDir), "w") as text_file:
            text_file.write(model)

    def setupAx(self, ax):
        ax.set_xlabel('Color')
        ax.set_ylabel('Frequency')
        ax.grid(True)
        # major ticks every 20, minor ticks every 5
        major_ticks = numpy.arange(0, 360, 20)
        minor_ticks = numpy.arange(0, 360, 1)

        ax.set_xticks(major_ticks)
        ax.set_xticks(minor_ticks, minor=True)

        # and a corresponding grid
        ax.grid(which='both')

        # or if you want differnet settings for the grids:
        ax.grid(which='minor', alpha=0.1)
        ax.grid(which='major', alpha=0.5)
