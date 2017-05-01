import QtQuick 2.6
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.1
import QtQuick.Controls.Material 2.1
import QtQuick.Dialogs 1.0
import "../components"
import "../dialogs"

Item {
    id: secondPage

    property string colorModelTag: "RGB"

    Material.theme: Material.Dark
    Material.accent: Material.Red

    signal updateProcessingImage()

    anchors.fill: parent        
    anchors.margins: 10

    onColorModelTagChanged: {
        console.log(secondPage.colorModelTag)
    }

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

        ColumnLayout {
            id: preferenceColorPanel
            Layout.fillWidth: true
            width: secondPage.width
            CheckBox {
                id: isOriginalImage
                checked: true
                text: qsTr("Use original image")
            }
            ColorModelSelector {
                id: colorModelSelector
            }
            // MorphologySettings {
            //     id: morphSet
            // }
            GetImagePixelDialog {
                visible: false
                id: getImagePixelDialog
            }
            Button {
                text: qsTr("Get pixel position")
                width: parent.width
                onClicked: {
                //     morphologyController.createMaskList(mask_widh.text, mask_height.text)
                //     maskDialog.open()
                    getImagePixelDialog.open()
                }
            }
            GroupBox {
                title: 'Efficient Graph-Based Image Segmentation'
                Layout.fillWidth: true
                ColumnLayout {
                    RowLayout {
                        Label {
                            text: qsTr("sigma:")
                        }
                        TextField {
                            id: sigma
                            text: qsTr("0.5")
                            Layout.fillWidth: true
                            validator: DoubleValidator{locale: DoubleValidator.StandardNotation}
                            inputMethodHints: Qt.ImhDigitsOnly
                            background: Rectangle {
                                radius: 2
                                border.color: "#333"
                                border.width: 1
                            }
                        }
                    }
                    RowLayout {
                        Label {
                            text: qsTr("Neighborhood size:")
                        }
                        TextField {
                            id: neighborhood
                            text: qsTr("4")
                            Layout.fillWidth: true
                            validator: DoubleValidator{locale: DoubleValidator.StandardNotation}
                            inputMethodHints: Qt.ImhDigitsOnly
                            background: Rectangle {
                                radius: 2
                                border.color: "#333"
                                border.width: 1
                            }
                        }
                    }
                    RowLayout {
                        Label {
                            text: qsTr("K:")
                        }
                        TextField {
                            id: k
                            text: qsTr("500")
                            Layout.fillWidth: true
                            validator: DoubleValidator{locale: DoubleValidator.StandardNotation}
                            inputMethodHints: Qt.ImhDigitsOnly
                            background: Rectangle {
                                radius: 2
                                border.color: "#333"
                                border.width: 1
                            }
                        }
                    }
                    RowLayout {
                        Label {
                            text: qsTr("min_comp_size:")
                        }
                        TextField {
                            id: min_comp_size
                            text: qsTr("50")
                            Layout.fillWidth: true
                            validator: DoubleValidator{locale: DoubleValidator.StandardNotation}
                            inputMethodHints: Qt.ImhDigitsOnly
                            background: Rectangle {
                                radius: 2
                                border.color: "#333"
                                border.width: 1
                            }
                        }
                    }
                    Button {
                        text: qsTr("Segmentate")
                        width: parent.width
                        onClicked: {
                            secondPage.enabled = false
                            segmentationController.EfficientGraphBasedImageSegmentation(colorModelSelector.colorModelTag, colorModelSelector.currentImageChannelIndex, isOriginalImage.checked, sigma.text, neighborhood.text, k.text, min_comp_size.text)
                            secondPage.enabled = true
                            secondPage.updateProcessingImage()
                        }
                    }
                }                
            }
            Button {
                text: qsTr("Detect road lane")
                width: parent.width
                onClicked: {
                    secondPage.enabled = false
                    segmentationController.detectRoadLane(colorModelSelector.colorModelTag, colorModelSelector.currentImageChannelIndex, isOriginalImage.checked)
                    secondPage.enabled = true
                    secondPage.updateProcessingImage()
                }
            }
        }
    }
}