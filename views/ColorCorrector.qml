import QtQuick 2.6
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.1
import QtQuick.Controls.Material 2.1
import "../JS/colorCorrector.js" as ColorCorrector

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
            ColorModelGroupBox {
                onUpdateProcessingImage: firstPage.updateProcessingImage()
            }
            
            // GroupBox {
            //     title: "Use color model"
            // }
            Button {
                id: grayscaleButton
                text: qsTr("Grayscale")
                onClicked: {
                    preferenceColorPanel.enabled = false
                    ColorCorrector.toGrayscale(isOriginalImage.checked)
                    firstPage.updateProcessingImage()
                    preferenceColorPanel.enabled = true
                }
            }
            Label {
                text: "1232"
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
                    firstPage.updateProcessingImage()
                }
                background: Rectangle {
                    Image {
                        width: parent.width
                        height: parent.height
                        source: "file:../image/slider.png"
                    }
                }
                handle: Rectangle {
                    x: parent.visualPosition * (parent.availableWidth - 5)
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
}