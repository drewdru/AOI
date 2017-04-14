import QtQuick 2.6
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.1
import QtQuick.Controls.Material 2.1
import QtQuick.Dialogs 1.0
import "../components"
import "../dialogs"

GroupBox {
    title: 'Morphology mask settings'
    Layout.fillWidth: true

    property int maskWidh: mask_widh.text
    property int maskHeight: mask_height.text

    ColumnLayout {
        RowLayout {
            Label {
                text: qsTr("Mask width:")
            }
            TextField {
                id: mask_widh
                text: qsTr("3")
                Layout.fillWidth: true
                validator: IntValidator{}
                inputMethodHints: Qt.ImhDigitsOnly
                background: Rectangle {
                    radius: 2
                    border.color: "#333"
                    border.width: 1
                }
            }
            Label {
                text: qsTr("Mask height:")
            }
            TextField {
                id: mask_height
                text: qsTr("3")
                Layout.fillWidth: true
                validator: IntValidator{}
                inputMethodHints: Qt.ImhDigitsOnly
                background: Rectangle {
                    radius: 2
                    border.color: "#333"
                    border.width: 1
                }
            }
        }
        Button {
            text: qsTr("Change mask")
            width: parent.width
            onClicked: {
                morphologyController.createMaskList(mask_widh.text, mask_height.text)
                maskDialog.open()
            }
        }
    }

    MaskDialog {
        visible: false
        id: maskDialog
        apertureWidth: parseInt(mask_widh.text)
        apertureHeight: parseInt(mask_height.text)
    }
}