import QtQuick 2.6
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.1
import QtQuick.Controls.Material 2.1
import "../components"
import "../views"

Drawer {
    id: drawer

    Material.theme: Material.Dark
    Material.accent: Material.Red

    // width: parent.width/2

    signal updateHistograms()

    onUpdateHistograms: {
        hist0.source = appDir + "/images/clearHist.png"
        hist1.source = appDir + "/images/clearHist.png"
        hist2.source = appDir + "/images/clearHist.png"
        hist3.source = appDir + "/images/clearHist.png"
        
        hist0.source = appDir + "/temp/hist0.png"
        hist1.source = appDir + "/temp/hist1.png"
        hist2.source = appDir + "/temp/hist2.png"
        hist3.source = appDir + "/temp/hist3.png"
    }

    RowLayout {
        anchors.fill: parent
        ColumnLayout {
            Image {
                id: hist0
                Layout.fillWidth: true
                Layout.fillHeight: true
                fillMode : "PreserveAspectFit"
                source: appDir + "/temp/hist0.png"
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        colorCorrectorController.showHistogram(0)
                    }
                }
            }
        }
        ColumnLayout {
            Image {
                id: hist1
                Layout.fillWidth: true
                Layout.fillHeight: true
                fillMode : "PreserveAspectFit"
                source: appDir + "/temp/hist1.png"
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        colorCorrectorController.showHistogram(1)              
                    }
                }
            }
        }
        ColumnLayout {
            Image {
                id: hist2
                Layout.fillWidth: true
                Layout.fillHeight: true
                fillMode : "PreserveAspectFit"
                source: appDir + "/temp/hist2.png"
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        colorCorrectorController.showHistogram(2)  
                    }
                }
            }
        }
        ColumnLayout {
            Image {
                id: hist3
                Layout.fillWidth: true
                Layout.fillHeight: true
                fillMode : "PreserveAspectFit"
                source: appDir + "/temp/hist3.png"
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        colorCorrectorController.showHistogram(3)  
                    }
                }
            }
        }
    }
}