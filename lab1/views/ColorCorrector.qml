import QtQuick 2.6
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.1
import QtQuick.Controls.Material 2.1
import "../JS/colorCorrector.js" as ColorCorrector

Item {
    Material.theme: Material.Dark
    Material.accent: Material.Red

    id: firstPage
    ColumnLayout {
        id: preferenceColorPanel

        anchors.fill: parent
        
        anchors.margins: 10
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
                ColorCorrector.toGrayscale(isOriginalImage.checked)
                drawer.updateProcessingImage()
                preferenceColorPanel.enabled = true
            }
        }
        Slider {
            id: hueSlider
            Layout.fillWidth: true
            from: 0
            value: 0
            to: 360
            stepSize: 1.0
            onValueChanged: {
                Slider.running = true
                preferenceColorPanel.enabled = false
                ColorCorrector.changeHue(value, isOriginalImage.checked)
                preferenceColorPanel.enabled = true
                Slider.running = false
                drawer.updateProcessingImage()
            }
            background: Rectangle {
                Image {
                    width: parent.width
                    height: parent.height
                    source: "file:./image/slider.png"
                }
            }
            handle: Rectangle {
                x: parent.visualPosition * (parent.availableWidth + 10) - 10
                y: parent.topPadding + parent.availableHeight / 2 - height / 2
                implicitWidth: 20
                implicitHeight: 20
                radius: 10
                color: if (parent.pressed) {
                    "#f0f0f0"
                } else if (parent.enabled) {
                    "#f6f6f6"
                } else {
                    "#aaf6f6f6"
                }
                border.color: "#bdbebf"
            }
            ToolTip {
                visible: parent.pressed
                text: qsTr("Hue is " + parent.valueAt(parent.position).toFixed(1))
            }
        }
    }
}