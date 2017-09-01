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
    // color: Material.color(Material.BlueGrey)

    width: parent.width/2
    // height: parent.height

    signal showColorCorrectorDrawer()
    signal showNoiseGeneratorDrawer()
    signal showFiltersDrawer()
    signal showBinarizeDrawer()
    signal showMorphologyDrawer()
    signal showSegmentationDrawer()
    signal updateProcessingImage()

    Flickable {
        focus: true
        anchors.fill: parent
        contentWidth: preferenceColorPanel.width
        contentHeight: preferenceColorPanel.height
        // contentY : 20
        boundsBehavior: Flickable.StopAtBounds
        

        Keys.onUpPressed: verticalScrollBar.decrease()
        Keys.onDownPressed: verticalScrollBar.increase()

        ScrollBar.vertical: ScrollBar {
            id: verticalScrollBar
            Binding {
                target: verticalScrollBar
                property: "active"
                value: verticalScrollBar.hovered
            }
        }
        anchors.margins: 10
        ColumnLayout {
            id: preferenceColorPanel
            width: drawer.width - 20
            CheckBox {
                id: isExpert
                checked: false
                text: qsTr("Expert mode")
            }
            GroupBox {
                id: userMode
                visible: !isExpert.checked
                title: 'User mode'
                Layout.fillWidth: true
                ColumnLayout {
                    width: drawer.width - 50
                    Button {
                        text: qsTr("Detect road lane")
                        width: parent.width
                        onClicked: {
                            userMode.enabled = false
                            segmentationController.detectRoadLane('RGB', 0, true)
                            userMode.enabled = true
                            drawer.updateProcessingImage()
                        }
                    }
                }
            }
            
            GroupBox {
                visible: isExpert.checked
                title: 'Expert mode'
                Layout.fillWidth: true
                ColumnLayout {
                    width: drawer.width - 45
                    GroupBox {
                        Layout.fillWidth: true
                        ColumnLayout {
                            width: drawer.width - 70
                            Button {
                                id: colorCorrectorButton
                                Layout.fillWidth: true
                                text: qsTr("View color corrector methods")
                                onClicked: drawer.showColorCorrectorDrawer()
                            }
                            Button {
                                id: filterButton
                                Layout.fillWidth: true  
                                text: qsTr("View image filters")
                                onClicked: drawer.showFiltersDrawer()
                            }
                            Button {
                                id: binarizeButton
                                Layout.fillWidth: true  
                                text: qsTr("View Binarize methods")
                                onClicked: drawer.showBinarizeDrawer()
                            }
                            Button {
                                id: morphologyButton
                                Layout.fillWidth: true  
                                text: qsTr("View Edge detection methods")
                                onClicked: drawer.showMorphologyDrawer()
                            }
                            Button {
                                id: segmentationButton
                                Layout.fillWidth: true  
                                text: qsTr("View Detect road lane method")
                                onClicked: drawer.showSegmentationDrawer()
                            }
                        }
                    }
                    GroupBox {
                        Layout.fillWidth: true
                        ColumnLayout {
                            width: drawer.width - 70
                            Button {
                                id: noiseGeneratorButton
                                Layout.fillWidth: true  
                                text: qsTr("View image noise generators")
                                onClicked: drawer.showNoiseGeneratorDrawer()
                            }
                        }
                    }
                }
            }
        }
    }
}