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
    // color: Material.color(Material.BlueGrey)

    width: parent.width/2

    signal updateProcessingImage()
    signal backClicked()
    
    // property int lastTab: 1
    // onOpened: {
    //     tabBar.currentIndex = drawer.lastTab
    // }
    // Component.onCompleted: {
    //     tabBar.currentIndex = drawer.lastTab
    // }

    StackLayout {
        id: view
        Layout.fillWidth: true
        y: tabBar.height + tabBar.y
        height: parent.height - y
        width: parent.width

        currentIndex: tabBar.currentIndex

        // Item {
        //     id: backTab
        // }
        Filters {
            width: drawer.width
            height: drawer.height
            onUpdateProcessingImage: drawer.updateProcessingImage()
        }
        // NonLinerFilters {
        //     width: drawer.width
        //     height: drawer.height
        //     onUpdateProcessingImage: drawer.updateProcessingImage()
        // }
    }
    TabBar {
        id: tabBar
        width: parent.width
        TabButton {
            Text {
                text: qsTr("    ← Filters")
                color: "white"
            }
            background: Rectangle {                
                anchors.fill: parent                
                color: Qt.lighter("#333333", parent.hovered ? 2 : 1.0)
            }   
            onClicked: drawer.backClicked()
        }
        // TabButton {
        //     text: qsTr("← Back")
        //     onClicked: {
        //         tabBar.currentIndex = drawer.lastTab
        //         drawer.backClicked()
        //     }
        // }
        // TabButton {
        //     text: qsTr("Liner")
        //     onClicked: {
        //         tabBar.currentIndex = 1
        //         drawer.lastTab = 1
        //     }
        // }
        // TabButton {
        //     text: qsTr("Non-linear")
        //     onClicked: {
        //         tabBar.currentIndex = 2
        //         drawer.lastTab = 2
        //     }
        // }
    }
}