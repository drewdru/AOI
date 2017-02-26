import QtQuick 2.6
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.1
import QtQuick.Controls.Material 2.1

ColumnLayout {
    id: colorModelBalance
    property string colorModelTag: "RGB"
    property int currentImageChannelIndex: 0
    property bool isOriginalImage
    signal updateProcessingImage()
    
    // anchors.fill: parent
    
    ColumnLayout {
        GroupBox {
            // anchors.fill: parent
            Layout.fillWidth: true
            title: qsTr("Choose color model")
            ColumnLayout {
                RadioButton {
                    id: isRgbModel
                    checked: true
                    text: qsTr("RGB")
                    onClicked: {
                        onUpdateColorModel(text, "R", "G", "B", 255, 255, 255)
                    }
                }
                RadioButton {
                    id: isYuvModel
                    text: qsTr("YUV")
                    onClicked: onUpdateColorModel(text, "Y", "U", "V", 255, 128, 128)
                }
                RadioButton {
                    id: isHslModel
                    text: qsTr("HSL")
                    onClicked: onUpdateColorModel(text, "H", "S", "L", 360, 100, 100)
                }
            }
        }
        GroupBox {
            Layout.fillWidth: true
            title: qsTr("Choose color channel")
            ColumnLayout {
                RadioButton {
                    id: isAllImageChannel
                    checked: true
                    text: qsTr("RGB")
                    onClicked: {
                        colorModelBalance.currentImageChannelIndex = 0
                        colorModelBalance.onAllUpdate()
                    }
                }
                RadioButton {
                    id: isFirstImageChannel
                    text: qsTr("R")
                    onClicked: {
                        colorModelBalance.currentImageChannelIndex = 1
                        colorModelBalance.onAllUpdate()
                    }
                }
                RadioButton {
                    id: isSecondImageChannel
                    text: qsTr("G")
                    onClicked: {
                        colorModelBalance.currentImageChannelIndex = 2
                        colorModelBalance.onAllUpdate()
                    }
                }
                RadioButton {
                    id: isThirdImageChannel
                    text: qsTr("B")
                    onClicked: {
                        colorModelBalance.currentImageChannelIndex = 3
                        colorModelBalance.onAllUpdate()
                    }
                }
            }
        }
        GroupBox {
            // anchors.fill: parent
            Layout.fillWidth: true
            title: qsTr("Color balance")
            ColumnLayout {
                anchors.fill: parent
                RowLayout {
                    Label {
                        text: isFirstImageChannel.text
                    }
                    ChannelBalanceSlider {
                        id: firstChannelBalance
                        to: 255
                        name: isFirstImageChannel.text
                        onValueChanged: {
                            colorModelBalance.onAllUpdate()
                        }
                    }
                }
                RowLayout {
                    Label {
                        text: isSecondImageChannel.text
                    }
                    ChannelBalanceSlider {
                        id: secondChannelBalance
                        to: 255
                        name: isSecondImageChannel.text
                        onValueChanged: {
                            colorModelBalance.onAllUpdate()
                        }
                    }
                }
                RowLayout {
                    Label {
                        text: isThirdImageChannel.text
                    }
                    ChannelBalanceSlider {
                        id: thirdChannelBalance
                        to: 255
                        name: isThirdImageChannel.text
                        onValueChanged: {
                            colorModelBalance.onAllUpdate()
                        }
                    }
                }
            }
        }
    }
    function onAllUpdate() {
        colorModelBalance.enabled = false
        colorCorrectorController.changeColorModel(
            colorModelBalance.colorModelTag,
            colorModelBalance.currentImageChannelIndex,
            isOriginalImage,
            firstChannelBalance.value,
            secondChannelBalance.value,
            thirdChannelBalance.value
        )
        colorModelBalance.updateProcessingImage()
        colorModelBalance.enabled = true
    }
    function onUpdateColorModel(text,
            firstChannel,
            secondChannel,
            thirdChannel,
            firstChannelValue,
            secondChannelValue,
            thirdChannelValue) {
        colorModelBalance.colorModelTag = text
        isAllImageChannel.text = text
        isAllImageChannel.checked = true
        colorModelBalance.currentImageChannelIndex = 0

        isFirstImageChannel.text = firstChannel
        isSecondImageChannel.text = secondChannel
        isThirdImageChannel.text = thirdChannel

        firstChannelBalance.to = firstChannelValue
        secondChannelBalance.to = secondChannelValue
        thirdChannelBalance.to = thirdChannelValue

        colorModelBalance.onAllUpdate()
        isAllImageChannel.checked = true
    }
}

