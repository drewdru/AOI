import QtQuick 2.6
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.1
import QtQuick.Controls.Material 2.1
import "../components"

Drawer {
    id: drawer

    Material.theme: Material.Dark
    Material.accent: Material.Red
    // color: Material.color(Material.BlueGrey)

    width: parent.width/2
    // height: parent.height

    signal showColorCorrectorDrawer()
    signal showNoiseGeneratorDrawer()

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
        anchors.margins: 10
        ColumnLayout {
            id: preferenceColorPanel
            width: drawer.width - 20

            Button {
                id: colorCorrectorButton
                Layout.fillWidth: true  
                text: qsTr("View color corrector methods")
                onClicked: drawer.showColorCorrectorDrawer()
            }
            Button {
                id: noiseGeneratorButton
                Layout.fillWidth: true  
                text: qsTr("View image noise generators")
                onClicked: drawer.showNoiseGeneratorDrawer()
            }  
        }
    }
}