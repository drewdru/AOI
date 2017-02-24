import QtQuick 2.6
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.1
import QtQuick.Controls.Material 2.1
import QtQuick.Dialogs 1.0

Item {
    id: firstPage

    Material.theme: Material.Dark
    Material.accent: Material.Red

    signal updateProcessingImage()

    anchors.fill: parent        
    anchors.margins: 10

    ColorDialog {
        id: colorDialog
        title: "Please choose a color"
        onAccepted: {
            firstPage.enabled = false
            colorCorrectorController.getHlsFromHex(colorDialog.color,
                function test(hue, saturation, lightness) {
                    colorCorrectorController.changeHue(hue, isOriginalImage.checked)
            });
            firstPage.updateProcessingImage()
            firstPage.enabled = true
        }
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
            width: firstPage.width
            CheckBox {
                id: isOriginalImage
                checked: true
                text: qsTr("Use original image")
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
                        colorCorrectorController.changeHue(value, isOriginalImage.checked)
                        preferenceColorPanel.enabled = true
                        Slider.running = false
                        firstPage.updateProcessingImage()
                    }
                }
                Button {
                    text: qsTr("Palette")
                    onClicked: colorDialog.open()
                }
            }
            
            ColorModelGroupBox {
                isOriginalImage: isOriginalImage.checked
                onUpdateProcessingImage: firstPage.updateProcessingImage()
            }        
        }
    }
}