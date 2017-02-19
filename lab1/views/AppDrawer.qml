import QtQuick 2.6
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.1
import QtQuick.Controls.Material 2.1

Drawer {
    id: drawer

    Material.theme: Material.Dark
    Material.accent: Material.Red
    // color: Material.color(Material.BlueGrey)

    width: parent.width/2
    height: parent.height

    signal updateProcessingImage()
    
    TabBar {
        id: tabBar
        width: parent.width
        // currentIndex: view.currentIndex
        TabButton {
            text: qsTr("ColorCorrector")
            onClicked: {tabBar.currentIndex = 0}
        }
        TabButton {
            text: qsTr("Discover")
            onClicked: {tabBar.currentIndex = 1}
        }
        TabButton {
            text: qsTr("Activity")
            onClicked:{tabBar.currentIndex = 2}
        }
    }

    StackLayout {
        id: view
        anchors.fill: parent
        y: parent.height
        height: parent.height - y

        currentIndex: tabBar.currentIndex

        ColorCorrector {}
        Item {
            id: discoverTab
        }
        Item {
            id: activityTab
        }
    }

    // IS MOBILE:
    // SwipeView {
    //     id: view

    //     currentIndex: tabBar.currentIndex
    //     anchors.fill: parent
    //     y: parent.height
    //     height: parent.height - y
        
    //     ColorCorrector {}
    //     Item {
    //         id: secondPage
    //     }
    //     Item {
    //         id: thirdPage
    //     }
    // }

    PageIndicator {
        id: indicator

        count: view.count
        currentIndex: view.currentIndex

        anchors.bottom: view.bottom
        anchors.horizontalCenter: parent.horizontalCenter
    }

    
}