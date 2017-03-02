import sys
import os
import numpy as np

from imageProcessor import colorModel, colorHistogram
from PyQt5.QtCore import QCoreApplication, QObject
from PIL import Image

class ImageService(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.appDir = os.getcwd()

    def openImage(self, isOriginalImage):
        """ Open image for processing

            @param isOriginalImage: The value for choose original or processing Image
        """
        try:
            if isOriginalImage:
                img = Image.open('{}/temp/inImage.png'.format(self.appDir))
            else:
                img = Image.open('{}/temp/processingImage.png'.format(self.appDir))
            return img.convert(mode='RGB')
        except Exception as err:
            return None

