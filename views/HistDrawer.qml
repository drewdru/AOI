import QtQuick 2.6
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.1
import QtQuick.Controls.Material 2.1

Drawer {
    id: drawer

    Material.theme: Material.Dark
    Material.accent: Material.Red
    // color: Material.color(Material.BlueGrey)

    width: parent.width/2
    // height: parent.height

    signal updateHistograms()

    onUpdateHistograms: {
        hist0.source = "file:hist3.png"
        hist1.source = "file:hist2.png"
        hist2.source = "file:hist1.png"
        hist3.source = "file:hist0.png"
        hist0.source = "file:hist0.png"
        hist1.source = "file:hist1.png"
        hist2.source = "file:hist2.png"
        hist3.source = "file:hist3.png"
    }

    RowLayout {
        anchors.fill: parent
        ColumnLayout {
            Label {
                text: "Histogram RGB"
                anchors.horizontalCenter: parent.horizontalCenter
            }
            Image {
                id: hist0
                Layout.fillWidth: true
                Layout.fillHeight: true
                fillMode : "PreserveAspectFit"
                source: "file:../hist0.png"
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        colorCorrectorController.showHistogram(0, "RGB")
                    }
                }
            }
        }
        ColumnLayout {
            Label {
                text: "Histogram R"
                anchors.horizontalCenter: parent.horizontalCenter
            }
            Image {
                id: hist1
                Layout.fillWidth: true
                Layout.fillHeight: true
                fillMode : "PreserveAspectFit"
                source: "file:../hist1.png"
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        colorCorrectorController.showHistogram(1, "RGB")              
                    }
                }
            }
        }
        ColumnLayout {
            Label {
                text: "Histogram G"
                anchors.horizontalCenter: parent.horizontalCenter
            }
            Image {
                id: hist2
                Layout.fillWidth: true
                Layout.fillHeight: true
                fillMode : "PreserveAspectFit"
                source: "file:../hist2.png"
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        colorCorrectorController.showHistogram(2, "RGB")  
                    }
                }
            }
        }
        ColumnLayout {
            Label {
                text: "Histogram B"
                anchors.horizontalCenter: parent.horizontalCenter
            }
            Image {
                id: hist3
                Layout.fillWidth: true
                Layout.fillHeight: true
                fillMode : "PreserveAspectFit"
                source: "file:../hist3.png"
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        colorCorrectorController.showHistogram(3, "RGB")  
                    }
                }
            }
        }
    }
}