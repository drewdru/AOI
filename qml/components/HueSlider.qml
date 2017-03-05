import QtQuick 2.6
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.1
import QtQuick.Controls.Material 2.1

Slider {
    signal updateProcessingImage()

    property bool isOriginalImage
    id: hueSlider
    Layout.fillWidth: true
    from: 0
    value: 0
    to: 360
    stepSize: 1.0
    background: Rectangle {
        Image {
            width: parent.width
            height: parent.height
            source: appDir + "/images/slider.png"
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