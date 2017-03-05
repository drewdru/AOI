import QtQuick 2.6
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.1
import QtQuick.Controls.Material 2.1
import QtQuick.Dialogs 1.0
import "../components"

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
            // Layout.fillWidth: true
            width: secondPage.width
            CheckBox {
                id: isOriginalImage
                checked: true
                text: qsTr("Use original image")
            }
            GroupBox {
                // anchors.fill: parent
                Layout.fillWidth: true
                title: qsTr("Image noise")
                ColumnLayout {
                    anchors.fill: parent
                    RowLayout {
                        Label {
                            text: qsTr("Noise level")
                        }
                        Slider {
                            id: noiseLevelBalance
                            from: 0
                            value: 50                            
                            to: 100
                            Layout.fillWidth: true
                            ToolTip {
                                visible: parent.pressed
                                text: qsTr("Noise level is " + parent.valueAt(parent.position).toFixed(1) + "%")
                            }
                        }
                    }
                    RowLayout {
                        Label {
                            text: "Impulse noise:"
                        }
                        Slider {
                            id: impulseNoiseBalance
                            from: 0
                            value: 0                            
                            to: 100
                            Layout.fillWidth: true
                            onValueChanged: {
                                secondPage.enabled = false
                                noiseGeneratorController.addImpulsNoise(colorModelSelector.colorModelTag, colorModelSelector.currentImageChannelIndex, value, noiseLevelBalance.value, isOriginalImage.checked)
                                secondPage.enabled = true
                                secondPage.updateProcessingImage()
                            }
                            ToolTip {
                                visible: parent.pressed
                                text: {
                                    qsTr("Min color channel value is " + parent.valueAt(parent.position).toFixed(1) + "%")
                                }
                            }
                        }
                        // Label {
                        //     text: "Black"
                        // }
                    }
                    RowLayout {
                        Label {
                            text: qsTr("Additive noise")
                        }
                        Slider {
                            id: additiveNoiseBalance
                            from: 0
                            value: 50                            
                            to: 100
                            Layout.fillWidth: true
                            onValueChanged: {
                                secondPage.enabled = false
                                noiseGeneratorController.addAdditiveNoise(colorModelSelector.colorModelTag, colorModelSelector.currentImageChannelIndex, value, noiseLevelBalance.value, isOriginalImage.checked)
                                secondPage.enabled = true
                                secondPage.updateProcessingImage()
                            }
                            ToolTip {
                                visible: parent.pressed
                                text: qsTr("Max deviation is " + parent.valueAt(parent.position).toFixed(1) + "%")
                            }
                        }
                    }
                    GroupBox {
                        Layout.fillWidth: true
                        ColumnLayout {
                            Label {
                                text: qsTr("Multiplicative noise")
                            }
                            RowLayout {
                                Label {
                                    text: qsTr("Kmin:\t")
                                }
                                TextField {
                                    id: kmin
                                    text: qsTr("0")
                                    Layout.fillWidth: true
                                    validator: IntValidator{}
                                    inputMethodHints: Qt.ImhFormattedNumbersOnly
                                    background: Rectangle {
                                        radius: 2
                                        border.color: "#333"
                                        border.width: 1
                                    }
                                }
                            }
                            RowLayout {
                                Label {
                                    text: qsTr("Kmax:\t")
                                }
                                TextField {
                                    id: kmax
                                    text: qsTr("1")
                                    Layout.fillWidth: true
                                    validator: IntValidator{}
                                    inputMethodHints: Qt.ImhFormattedNumbersOnly
                                    background: Rectangle {
                                        radius: 2
                                        border.color: "#333"
                                        border.width: 1
                                    }
                                }
                            }
                            Button {
                                text: qsTr("add multiplicative noise")
                                width: parent.width
                                onClicked: {
                                    secondPage.enabled = false
                                    noiseGeneratorController.addMultiplicativeNoise(colorModelSelector.colorModelTag, colorModelSelector.currentImageChannelIndex, kmin.text, kmax.text, noiseLevelBalance.value, isOriginalImage.checked)
                                    secondPage.enabled = true
                                    secondPage.updateProcessingImage()
                                }
                            }
                        }
                    }
                }
            }
            ColorModelSelector {
                id: colorModelSelector
            }
        }
    }
}