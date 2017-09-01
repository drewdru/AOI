import QtQuick 2.6
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.1
import QtQuick.Controls.Material 2.1
import QtQuick.Dialogs 1.0
import "../components"

Item {
    id: secondPage

    Material.theme: Material.Dark
    Material.accent: Material.Red

    anchors.fill: parent
    anchors.margins: 10
    
    function updateMetrics() {        
        mainController.getLastMethodWorkMetrics(function setMethodWorkTime(text) {
            methodWorkMetrics.text = text
        })
    }

    Flickable {
        id: flick
        anchors.fill: parent
        contentWidth: methodWorkMetrics.width
        contentHeight: methodWorkMetrics.height
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
        Text {
            id: methodWorkMetrics
            width: secondPage.width
            wrapMode: Text.WrapAnywhere
            text: qsTr("Activate any method\t")
        }
    }
}