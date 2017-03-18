import QtQuick 2.6
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.1
import QtQuick.Controls.Material 2.1
// import QtQuick.Controls.Styles 1.4
// import QtQuick.Controls 2.1
import "JS/main.js" as App
import "views"
import "drawers"

Rectangle {

    Material.theme: Material.Dark
    Material.accent: Material.Red
    color: Material.color(Material.BlueGrey)

    id: rootWindow    
    anchors.fill: parent    
    width: 300; height: 300    
    // color: "#80000000"

    Component.onCompleted: {
        App.onLoad()
        photoPreview2.source = appDir + "/temp/inImage.png"
        photoPreview2.source = appDir + "/temp/processingImage.png"
        drawerHistogram.updateHistograms()
    }

    FeatureListDrawer {
        id: drawerFeatureList
        height: parent.height
        onOpened: appMenu.isDrawerVisible = true
        onClosed: appMenu.isDrawerVisible = false
        Shortcut {
            sequence: "Ctrl+D"
            onActivated: drawerFeatureList.close()
        }
        Shortcut {
            sequence: "Ctrl+Q"
            onActivated: Qt.quit()
        }
        Shortcut {
            sequence: "Ctrl+W"
            onActivated: rootWindow.viewDrawer('drawerHistogram')
        }
        onShowColorCorrectorDrawer: rootWindow.viewDrawer('drawerColorCorrector')
        onShowNoiseGeneratorDrawer: rootWindow.viewDrawer('drawerNoiseGenerator')
        onShowFiltersDrawer: rootWindow.viewDrawer('drawerFilters')
    }
    NoiseGeneratorDrawer {
        id: drawerNoiseGenerator
        height: parent.height
        onUpdateProcessingImage: rootWindow.updateProcessingImage()
        onOpened: appMenu.isDrawerVisible = true
        onClosed: appMenu.isDrawerVisible = false
        onBackClicked: rootWindow.viewDrawer('drawerFeatureList')
        Shortcut {
            sequence: "Ctrl+D"
            onActivated: rootWindow.viewDrawer('drawerFeatureList')
        }
        Shortcut {
            sequence: "Ctrl+Q"
            onActivated: Qt.quit()
        }
        Shortcut {
            sequence: "Ctrl+W"
            onActivated: rootWindow.viewDrawer('drawerHistogram')
        }
    }
    ColorCorrectorDrawer {
        id: drawerColorCorrector
        height: parent.height
        onUpdateProcessingImage: rootWindow.updateProcessingImage()
        onOpened: appMenu.isDrawerVisible = true
        onClosed: appMenu.isDrawerVisible = false
        onBackClicked: rootWindow.viewDrawer('drawerFeatureList')
        Shortcut {
            sequence: "Ctrl+D"
            onActivated: rootWindow.viewDrawer('drawerFeatureList')
        }
        Shortcut {
            sequence: "Ctrl+Q"
            onActivated: Qt.quit()
        }
        Shortcut {
            sequence: "Ctrl+W"
            onActivated: rootWindow.viewDrawer('drawerHistogram')
        }
    }
    FiltersDrawer {
        id: drawerFilters
        height: parent.height
        onUpdateProcessingImage: rootWindow.updateProcessingImage()
        onOpened: appMenu.isDrawerVisible = true
        onClosed: appMenu.isDrawerVisible = false
        onBackClicked: rootWindow.viewDrawer('drawerFeatureList')
        Shortcut {
            sequence: "Ctrl+D"
            onActivated: rootWindow.viewDrawer('drawerFeatureList')
        }
        Shortcut {
            sequence: "Ctrl+Q"
            onActivated: Qt.quit()
        }
        Shortcut {
            sequence: "Ctrl+W"
            onActivated: rootWindow.viewDrawer('drawerHistogram')
        }
    }

    Shortcut {
        sequence: "Ctrl+W"
        onActivated: rootWindow.viewDrawer('drawerHistogram')
    }
    Shortcut {
        sequence: "Ctrl+D"
        onActivated: rootWindow.viewDrawer('drawerFeatureList')
    }
    HistDrawer {
        id: drawerHistogram
        height: parent.height / 3
        width: parent.width
        edge:Qt.BottomEdge
        onOpened: appMenu.isDrawerVisible = true
        onClosed: appMenu.isDrawerVisible = false
        Shortcut {
            sequence: "Ctrl+W"
            onActivated: drawerHistogram.close()
        }
        Shortcut {
            sequence: "Ctrl+Q"
            onActivated: Qt.quit()
        }
        Shortcut {
            sequence: "Ctrl+D"
            onActivated: rootWindow.viewDrawer('drawerFeatureList')
        }
    }

    GridLayout {
        id:grid
        anchors.fill: parent
        columns: 3
        y: 40
        height: parent.height - y
        anchors.margins: 10

        RowLayout {
            Layout.columnSpan: 2
            Image {
                id: photoPreview
                cache: false
                width: parent.width/2 - 10
                Layout.fillWidth: true
                Layout.fillHeight: true
                fillMode : "PreserveAspectFit"
                source: appDir + "/temp/inImage.png"
            }
            Image {
                id: photoPreview2
                cache: false
                x:photoPreview.width + 10
                width: parent.width / 2
                Layout.fillWidth: true
                Layout.fillHeight: true
                fillMode : "PreserveAspectFit"
                source: appDir + "/temp/processingImage.png"
            }
        }
    }

    AppMenu {
        id: appMenu
        width: parent.width
        height: 20
        
        onShowDrawerFeatureList: rootWindow.viewDrawer('drawerFeatureList')
        onHideDrawerFeatureList: drawerFeatureList.close()

        onShowHistDrawer: rootWindow.viewDrawer('drawerHistogram')
        onHideHistDrawer: drawerHistogram.close()
        
        onUpdateImages: {
            photoPreview.source = appDir + "/temp/processingImage.png"
            photoPreview.source = appDir + "/temp/inImage.png"
            App.loadProcessingImage()
            photoPreview2.source = appDir + "/temp/inImage.png"
            photoPreview2.source = appDir + "/temp/processingImage.png"
            drawerHistogram.updateHistograms()
        }        
        Label {
            id: methodWorkTimer
            anchors.right: parent.right
            // anchors.verticalCenter: parent.bottom
            text: qsTr("Timer\t")
        }
    }

    function updateProcessingImage() {
        photoPreview2.source = appDir + "/images/clearHist.png"
        photoPreview2.source = appDir + "/temp/processingImage.png"
        mainController.getLastMethodWorkTime(function setMethodWorkTime(response) {
            methodWorkTimer.text = 'Timer: ' + response
        })
        drawerHistogram.updateHistograms()
    }
    
    function viewDrawer(drawerName) {
        drawerFeatureList.close()
        drawerColorCorrector.close()
        drawerHistogram.close()
        drawerNoiseGenerator.close()
        drawerFilters.close()
        if (drawerName == 'drawerFeatureList') drawerFeatureList.open()
        if (drawerName == 'drawerColorCorrector') drawerColorCorrector.open()
        if (drawerName == 'drawerHistogram') drawerHistogram.open()
        if (drawerName == 'drawerNoiseGenerator') drawerNoiseGenerator.open()
        if (drawerName == 'drawerFilters') drawerFilters.open()
    }
}