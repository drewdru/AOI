"""
    @package mainController
    main.qml controller
"""
import sys
import os
import time
import numpy
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

from imageProcessor import colorModel
from PyQt5.QtCore import QObject, pyqtSlot, QDir, QCoreApplication
from PyQt5.QtQml import QJSValue
from PIL import Image

class MainController(QObject):
    """ Controller for main view """
    def __init__(self):
        QObject.__init__(self)
        self.callback = []
        self.appDir = QDir.currentPath()

    def dump(self):
        """ Return to callbacks """
        print('Dump was called')
        for c in self.callback:
            c.call([QJSValue('IT IS A TEST RESPONSE')])
        self.callback = []

    @pyqtSlot(str, 'QJSValue')
    def enqueue(self, command, callback):
        """ Add an item of data awaiting processing to a queue of such items

            @param command: The tag of command
            @param callback: The callback function
        """
        self.callback.append(QJSValue(callback))

    @pyqtSlot()
    def processResponses(self):
        """ Processing responses """
        self.dump()

    @pyqtSlot()
    def loadProcessingImage(self):
        """ Replace processingImage.png """
        try:
            img = Image.open('{}/temp/inImage.png'.format(self.appDir))
            img.save('{}/temp/processingImage.png'.format(self.appDir))
        except Exception as error:
            print(error)

    @pyqtSlot(str)
    def openFile(self, file):
        """ Copy image to inImage.png

            @param file: The path to file
        """
        try:
            print('openFile:', file)
            img = Image.open(file)
            img.save('{}/temp/inImage.png'.format(self.appDir))
        except:
            pass
        while True:
            if os.path.exists('{}/temp/inImage.png'.format(self.appDir)):
                try:
                    os.rename('{}/temp/inImage.png'.format(self.appDir),
                            '{}/temp/inImage.png'.format(self.appDir) + "_")
                    os.rename('{}/temp/inImage.png'.format(self.appDir) + "_",
                            '{}/temp/inImage.png'.format(self.appDir))
                    break
                except OSError as e:
                    print(e)

    @pyqtSlot(str)
    def saveFile(self, file):
        """ Copy processingImage.png to file

            @param file: The path to file
        """
        try:
            img = Image.open('{}/temp/processingImage.png'.format(self.appDir))
            img.save(file)
        except:
            pass

    # @pyqtSlot()
    # def getLastMethodWorkTime(self):
    #     return 25

    @pyqtSlot('QJSValue')
    def getLastMethodWorkMetrics(self, callback):
        max_mtime = 0
        for dirname, subdirs, files in os.walk('{}/temp/log'.format(self.appDir)):
            for fname in files:
                full_path = os.path.join(dirname, fname)
                mtime = os.stat(full_path).st_mtime
                if mtime > max_mtime:
                    max_mtime = mtime
                    max_dir = dirname
                    max_file = fname

        methodTime = methodMSE = methodPSNR = methodRMS = 0
        with open('{}/{}'.format(max_dir, max_file), 'r') as fileStream:
            for textLine in fileStream.readlines():
                if 'Timer: ' in textLine:
                    methodTime = textLine.replace('Timer: ', '')
                if 'MSE: ' in textLine:
                    methodMSE = textLine.replace('MSE: ', '')
                if 'PSNR: ' in textLine:
                    methodPSNR = textLine.replace('PSNR: ', '')
                if 'RMS: ' in textLine:
                    methodRMS = textLine.replace('RMS: ', '')
                if 'Segments count: ' in textLine:
                    segmentCount = textLine.replace('Segments count: ', '')
                if 'Sum of similar: ' in textLine:
                    sumOfSimilar = textLine.replace('Sum of similar: ', '')
                if 'Sum of coinciding: ' in textLine:
                    sumOfCoinciding = textLine.replace('Sum of coinciding: ', '')
                if 'Area: ' in textLine:
                    methodArea = textLine.replace('Area: ', '')
                if 'Perimetr: ' in textLine:
                    methodPerimetr = textLine.replace('Perimetr: ', '')
                if 'Center of mass: ' in textLine:
                    methodCenterOfMass = textLine.replace('Center of mass: ', '')
                if 'Compactness: ' in textLine:
                    methodCompactness = textLine.replace('Compactness: ', '')
        responseText = '<h1>{}</h1><h2>Timer(seconds):</h2>{}'.format(
            max_file.replace('.log', ''),
            methodTime)
        if methodMSE:
            responseText = '{}<h2>MSE:</h2>{}'.format(responseText, methodMSE)
        if methodPSNR:
            responseText = '{}<h2>PSNR:</h2>{}'.format(responseText, methodPSNR)
        if methodRMS:
            responseText = '{}<h2>RMS:</h2>{}'.format(responseText, methodRMS)
        if segmentCount:
            responseText = '{}<h2>Segments count:</h2>{}'.format(responseText, segmentCount)
        if sumOfSimilar:
            responseText = '{}<h2>Sum of similar:</h2>{}'.format(responseText, sumOfSimilar)
        if sumOfCoinciding:
            responseText = '{}<h2>Sum of coinciding:</h2>{}'.format(responseText, sumOfCoinciding)
        if methodArea:
            responseText = '{}<h2>Area:</h2>{}'.format(responseText, methodArea)
        if methodPerimetr:
            responseText = '{}<h2>Perimetr:</h2>{}'.format(responseText, methodPerimetr)
        if methodCenterOfMass:
            responseText = '{}<h2>Center of mass:</h2>{}'.format(responseText, methodCenterOfMass)
        if methodCompactness:
            responseText = '{}<h2>Compactness:</h2>{}'.format(responseText, methodCompactness)
        if callback.isCallable():
            callback.call([QJSValue(responseText)])

    @pyqtSlot(str)
    def log(self, s):
        """ PyConsole
            @param s: The string
        """
        print(s)
