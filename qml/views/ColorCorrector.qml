import QtQuick 2.6
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.1
import QtQuick.Controls.Material 2.1
import QtQuick.Dialogs 1.0
import "../components"

Item {
    id: firstPage

    Material.theme: Material.Dark
    Material.accent: Material.Red

    signal updateProcessingImage()

    anchors.fill: parent        
    anchors.margins: 10

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
            width: firstPage.width
            CheckBox {
                id: isOriginalImage
                checked: true
                text: qsTr("Use original image")
            }
            ColorModelBalance {
                id: colorModelBalance
                isOriginalImage: isOriginalImage.checked
                onUpdateProcessingImage: firstPage.updateProcessingImage()
                // onColorModelTagChanged: {
                //     firstPage.colorModelTag = colorModelBalance.colorModelTag
                // }
            }
            Button {
                id: autolevelsButton
                text: qsTr("Autolevels")
                onClicked: {
                    preferenceColorPanel.enabled = false
                    colorCorrectorController.toAutolevels(isOriginalImage.checked)
                    firstPage.updateProcessingImage()
                    preferenceColorPanel.enabled = true
                }
            }   
            Button {
                id: grayscaleButton
                text: qsTr("Grayscale")
                onClicked: {
                    preferenceColorPanel.enabled = false
                    colorCorrectorController.toGrayscale(isOriginalImage.checked)
                    firstPage.updateProcessingImage()
                    preferenceColorPanel.enabled = true
                }
            }    
            Button {
                id: grayWorldButton
                text: qsTr("Gray world")
                onClicked: {
                    preferenceColorPanel.enabled = false
                    colorCorrectorController.toGrayWorld(isOriginalImage.checked)
                    firstPage.updateProcessingImage()
                    preferenceColorPanel.enabled = true
                }
            }   
            Button {
                id: histogramEqualizationButton
                text: qsTr("Histogram equalization")
                onClicked: {
                    preferenceColorPanel.enabled = false
                    colorCorrectorController.histogramEqualization(isOriginalImage.checked)
                    firstPage.updateProcessingImage()
                    preferenceColorPanel.enabled = true
                }
            }
            RowLayout {
                Label {
                    text: qsTr("Gamma:")
                }
                Slider {
                    id: gammaSlider
                    from: 0
                    value: 1                            
                    to: 5
                    Layout.fillWidth: true
                    onValueChanged: {
                        Slider.running = true
                        preferenceColorPanel.enabled = false
                        colorCorrectorController.changeGamma(isOriginalImage.checked, value)
                        preferenceColorPanel.enabled = true
                        Slider.running = false
                        firstPage.updateProcessingImage()
                    }

                    ToolTip {
                        visible: parent.pressed
                        text: qsTr("Max deviation is " + parent.valueAt(parent.position).toFixed(1) + "%")
                    }
                }
            }
            RowLayout {
                Label {
                    text: qsTr("Hue:")
                }
                HueSlider {
                    id: hueSlider
                    isOriginalImage: isOriginalImage.checked
                    // onUpdateProcessingImage: firstPage.updateProcessingImage()

                    onValueChanged: {
                        Slider.running = true
                        preferenceColorPanel.enabled = false
                        colorCorrectorController.changeHue(isOriginalImage.checked, value)
                        preferenceColorPanel.enabled = true
                        Slider.running = false
                        firstPage.updateProcessingImage()
                    }
                }
                // Button {
                //     text: qsTr("Palette")
                //     onClicked: colorDialog.open()
                // }
            }              
        }
    }
}