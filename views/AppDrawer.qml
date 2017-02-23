import QtQuick 2.6
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.1
import QtQuick.Controls.Material 2.1

import QtQuick.Dialogs 1.0

Drawer {
    id: drawer

    Material.theme: Material.Dark
    Material.accent: Material.Red
    // color: Material.color(Material.BlueGrey)

    width: parent.width/2
    height: parent.height

    signal updateProcessingImage()

    // ColorDialog {
    //     id: colorDialog
    //     title: "Please choose a color"
    //     onAccepted: {
    //         console.log("You chose: " + colorDialog.color)
    //         // Qt.quit()
    //     }
    //     onRejected: {
    //         console.log("Canceled")
    //         // Qt.quit()
    //     }
    //     Component.onCompleted: visible = true
    // }
    

    StackLayout {
        id: view
        Layout.fillWidth: true
        y: tabBar.height + tabBar.y
        height: parent.height - y
        width: parent.width

        currentIndex: tabBar.currentIndex

        ColorCorrector {
            width: drawer.width
            height: drawer.height
            onUpdateProcessingImage: drawer.updateProcessingImage()
        }
        Item {
            id: discoverTab
        }
        Item {
            id: activityTab
        }
    }
    TabBar {
        id: tabBar
        width: parent.width
            TabButton {
                text: qsTr("Color corrector")
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
    // PageIndicator {
    //     id: indicator

    //     count: view.count
    //     currentIndex: view.currentIndex

    //     anchors.bottom: view.bottom
    //     anchors.horizontalCenter: parent.horizontalCenter
    // }

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

    
}