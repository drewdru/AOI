import QtQuick 2.6
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.1
import QtQuick.Controls.Material 2.1
import "../JS/colorCorrector.js" as ColorCorrector

ColumnLayout {
    id: colorModelSelector
    property string colorModelTag: "RGB"
    property int currentImageChannelIndex: 0
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
                        colorModelSelector.colorModelTag = text
                        colorModelSelector.onColororModelorChannelChange()
                    }
                }
                RadioButton {
                    id: isYuvModel
                    text: qsTr("YUV")
                    onClicked: {
                        colorModelSelector.colorModelTag = text
                        colorModelSelector.onColororModelorChannelChange()
                    }
                }
            }
        }
        GroupBox {
            Layout.fillWidth: true
            title: qsTr("Choose color channel")
            ColumnLayout {
                RadioButton {
                    id: isFirstImageChannel
                    checked: true
                    text: {
                        if (isRgbModel.checked)
                            qsTr("R")
                        else if (isYuvModel.checked)
                            qsTr("Y")
                    }
                    onClicked: {
                        colorModelSelector.currentImageChannelIndex = 0
                        colorModelSelector.onColororModelorChannelChange()
                    }
                }
                RadioButton {
                    id: isSecondImageChannel
                    text: {
                        if (isRgbModel.checked)
                            qsTr("G")
                        else if (isYuvModel.checked)
                            qsTr("U")
                    }
                    onClicked: {
                        colorModelSelector.currentImageChannelIndex = 1
                        colorModelSelector.onColororModelorChannelChange()
                    }
                }
                RadioButton {
                    id: isThirdImageChannel
                    text: {
                        if (isRgbModel.checked)
                            qsTr("B")
                        else if (isYuvModel.checked)
                            qsTr("V")
                    }
                    onClicked: {
                        colorModelSelector.currentImageChannelIndex = 2
                        colorModelSelector.onColororModelorChannelChange()
                    }
                }
            }
        }
    }
    function onColororModelorChannelChange() {
        ColorCorrector.changeColorModel(
            colorModelSelector.colorModelTag,
            colorModelSelector.currentImageChannelIndex
        )
        colorModelSelector.updateProcessingImage()
    }
}

