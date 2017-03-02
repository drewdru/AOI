import QtQuick 2.6
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.1
import QtQuick.Controls.Material 2.1
import QtQuick.Dialogs 1.0

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
                            text: "Impulse noise: White"
                        }
                        Slider {
                            id: impulseNoiseBalance
                            from: 0
                            value: 0                            
                            to: 100
                            onValueChanged: {
                                secondPage.enabled = false
                                noiseGeneratorController.addImpulsNoise(colorModelSelector.colorModelTag, value, noiseLevelBalance.value, isOriginalImage.checked)
                                secondPage.enabled = true
                                secondPage.updateProcessingImage()
                            }
                            Layout.fillWidth: true
                            ToolTip {
                                visible: parent.pressed
                                text: {
                                    qsTr("Black is " + parent.valueAt(parent.position).toFixed(1) + "%")
                                }
                            }
                        }
                        Label {
                            text: "Black"
                        }
                    }
                    RowLayout {
                        Label {
                            text: "Additive noise: -"
                        }
                        ChannelBalanceSlider {
                            id: additive
                            to: 255
                            name: secondPage.colorModelTag
                            onValueChanged: {
                                colorModelBalance.onAllUpdate()
                            }
                        }
                        Label {
                            text: "+"
                        }
                    }
                    RowLayout {
                        Label {
                            text: qsTr("Kmin")
                        }
                        RangeSlider {
                            id: kminKmax
                            from: 0
                            // value: 0                            
                            to: 100
                            // onValueChanged: {
                            //     colorModelBalance.onAllUpdate()
                            // }
                            Layout.fillWidth: true
                            ToolTip {
                                visible: parent.pressed
                                text: qsTr("Noise level is " + parent.valueAt(parent.position).toFixed(1) + "%")
                            }
                        }
                        Label {
                            text: qsTr("Kmax")
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