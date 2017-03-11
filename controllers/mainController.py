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
                    os.rename('{}/temp/inImage.png'.format(self.appDir), '{}/temp/inImage.png'.format(self.appDir)+"_")
                    os.rename('{}/temp/inImage.png'.format(self.appDir)+"_", '{}/temp/inImage.png'.format(self.appDir))
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

    @pyqtSlot(str)
    def log(self, s):
        """ PyConsole

            @param s: The string
        """
        print(s)
