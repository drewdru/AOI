import QtQuick 2.6
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.1
import QtQuick.Controls.Material 2.1
import "../components"
import "../views"

Drawer {
    id: drawer

    Material.theme: Material.Dark
    Material.accent: Material.Red

    width: parent.width/2

    signal updateProcessingImage()
    signal backClicked()
    
    StackLayout {
        id: view
        Layout.fillWidth: true
        y: tabBar.height + tabBar.y
        height: parent.height - y
        width: parent.width

        currentIndex: tabBar.currentIndex

        Binarize {
            width: drawer.width
            height: drawer.height
            onUpdateProcessingImage: drawer.updateProcessingImage()
        }
    }
    TabBar {
        id: tabBar
        width: parent.width
        TabButton {
            Text {
                text: qsTr("    ← Binarizing")
                color: "white"
            }
            background: Rectangle {                
                anchors.fill: parent                
                color: Qt.lighter("#333333", parent.hovered ? 2 : 1.0)
            }   
            onClicked: drawer.backClicked()
        }
    }
}