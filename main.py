"""
    @package main
    Run PyQt app
"""

import sys
import os

from PyQt5.QtQml import QQmlEngine
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQuick import QQuickView
from PyQt5.QtGui import QIcon

from controllers.mainController import MainController
from controllers.colorCorrectorController import ColorCorrectorController

if __name__ == '__main__':
    # Create main app
    myApp = QApplication(sys.argv)
    myApp.setWindowIcon(QIcon('./image/icon.png'))

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
    appDir = os.getcwd()
    context.setContextProperty('appDir', appDir)

    colorCorrectorController = ColorCorrectorController()
    context.setContextProperty('colorCorrectorController', colorCorrectorController)

    # Show the View
    appView.setSource(QUrl('./views/main.qml'))
    appView.show()

    # Execute the Application and Exit
    myApp.exec_()
    sys.exit()
