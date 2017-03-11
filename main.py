"""
    @package main
    Run PyQt app
"""

import sys
import os

from PyQt5.QtQml import QQmlEngine
from PyQt5.QtCore import QUrl, QDir 
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQuick import QQuickView
from PyQt5.QtGui import QIcon

from controllers.mainController import MainController
from controllers.noiseGeneratorController import NoiseGeneratorController
from controllers.colorCorrectorController import ColorCorrectorController
from controllers.filtersController import FiltersController

if __name__ == '__main__':
    # Create main app
    myApp = QApplication(sys.argv)
    myApp.setWindowIcon(QIcon('./images/icon.png'))

    # Create a View and set its properties
    appView = QQuickView()
    appView.setMinimumHeight(640)
    appView.setMinimumWidth(1024)
    appView.setTitle('Lab1')

    engine = appView.engine()
    engine.quit.connect(myApp.quit)
    context = engine.rootContext()

    # add controllers
    mainController = MainController()
    context.setContextProperty('PyConsole', mainController)
    context.setContextProperty('mainController', mainController)
    # appDir = os.getcwd()
    # print(QDir.currentPath())
    appDir = 'file:///' + QDir.currentPath()
    # print(appDir)
    # # print('appDir:', appDir)
    # appDir = 'file:///h:/QtDocuments/AOI'
    # print(appDir)
    context.setContextProperty('appDir', appDir)

    colorCorrectorController = ColorCorrectorController()
    context.setContextProperty('colorCorrectorController', colorCorrectorController)

    noiseGeneratorController = NoiseGeneratorController()
    context.setContextProperty('noiseGeneratorController', noiseGeneratorController)

    filtersController = FiltersController()
    context.setContextProperty('filtersController', filtersController)

    # Show the View
    appView.setSource(QUrl('./qml/main.qml'))
    appView.show()

    # Execute the Application and Exit
    myApp.exec_()
    sys.exit()
