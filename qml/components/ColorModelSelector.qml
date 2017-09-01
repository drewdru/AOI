import QtQuick 2.6
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.1
import QtQuick.Controls.Material 2.1

ColumnLayout {
    id: colorModelSelector
    property string colorModelTag: "RGB"
    property string channelTag: "RGB"
    property int currentImageChannelIndex: 0
    // property bool isOriginalImage
    signal updateProcessingImage()

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
                        onUpdateColorModel(text, "R", "G", "B")
                    }
                }
                RadioButton {
                    id: isYuvModel
                    text: qsTr("YUV")
                    onClicked: onUpdateColorModel(text, "Y", "U", "V")
                }
                RadioButton {
                    id: isHslModel
                    text: qsTr("HSL")
                    onClicked: onUpdateColorModel(text, "H", "S", "L")
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
                        colorModelSelector.currentImageChannelIndex = 0
                        colorModelSelector.onAllUpdate()
                    }
                }
                RadioButton {
                    id: isFirstImageChannel
                    text: qsTr("R")
                    onClicked: {
                        colorModelSelector.currentImageChannelIndex = 1
                        colorModelSelector.onAllUpdate()
                    }
                }
                RadioButton {
                    id: isSecondImageChannel
                    text: qsTr("G")
                    onClicked: {
                        colorModelSelector.currentImageChannelIndex = 2
                        colorModelSelector.onAllUpdate()
                    }
                }
                RadioButton {
                    id: isThirdImageChannel
                    text: qsTr("B")
                    onClicked: {
                        colorModelSelector.currentImageChannelIndex = 3
                        colorModelSelector.onAllUpdate()
                    }
                }
            }
        }
    }
    function onAllUpdate() {
        colorModelSelector.channelTag = (isAllImageChannel.checked ? isAllImageChannel.text : '') +
            (isFirstImageChannel.checked ? isFirstImageChannel.text : '') +
            (isSecondImageChannel.checked ? isSecondImageChannel.text : '') +
            (isThirdImageChannel.checked ? isThirdImageChannel.text : '');
        
    }
    function onUpdateColorModel(text,
            firstChannel,
            secondChannel,
            thirdChannel) {
        colorModelSelector.colorModelTag = text
        isAllImageChannel.text = text
        isAllImageChannel.checked = true
        colorModelSelector.currentImageChannelIndex = 0

        isFirstImageChannel.text = firstChannel
        isSecondImageChannel.text = secondChannel
        isThirdImageChannel.text = thirdChannel
        colorModelSelector.onAllUpdate()
        isAllImageChannel.checked = true
    }
}

