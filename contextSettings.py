
import sys
import os

from PyQt5.QtCore import QDir 
from controllers.mainController import MainController
from controllers.noiseGeneratorController import NoiseGeneratorController
from controllers.colorCorrectorController import ColorCorrectorController
from controllers.filtersController import FiltersController
from controllers.binarizeController import BinarizeController
from controllers.morphologyController import MorphologyController
from controllers.segmentationController import SegmentationController


def setContext(context):
    # appDir = os.getcwd()
    # print(QDir.currentPath())
    appDir = 'file:///' + QDir.currentPath()
    # print(appDir)
    # # print('appDir:', appDir)
    # appDir = 'file:///h:/QtDocuments/AOI'
    # print(appDir)
    context.setContextProperty('appDir', appDir)

    # add controllers
    mainController = MainController()
    context.setContextProperty('PyConsole', mainController)
    context.setContextProperty('mainController', mainController)

    colorCorrectorController = ColorCorrectorController()
    context.setContextProperty('colorCorrectorController', colorCorrectorController)

    noiseGeneratorController = NoiseGeneratorController()
    context.setContextProperty('noiseGeneratorController', noiseGeneratorController)

    filtersController = FiltersController()
    context.setContextProperty('filtersController', filtersController)

    binarizeController = BinarizeController()
    context.setContextProperty('binarizeController', binarizeController)

    morphologyController = MorphologyController()
    context.setContextProperty('morphologyController', morphologyController)

    segmentationController = SegmentationController()
    context.setContextProperty('segmentationController', segmentationController)
