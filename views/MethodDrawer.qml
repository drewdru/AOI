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
    // height: parent.height

    signal updateProcessingImage()


    StackLayout {
        id: view
        Layout.fillWidth: true
        y: tabBar.height + tabBar.y
        height: parent.height - y
        width: parent.width

        currentIndex: tabBar.currentIndex

        ColorCorrector {
            id: colorCorrectorId
            width: drawer.width
            height: drawer.height
            onUpdateProcessingImage: drawer.updateProcessingImage()
            // onColorModelTagChanged: {
            //     imageNoiseId.colorModelTag = colorCorrectorId.colorModelTag
            // }
        }
        NoiseGenerator {
            id: imageNoiseId
            // colorModelTag: colorCorrectorId.colorModelTag
            width: drawer.width
            height: drawer.height
            onUpdateProcessingImage: drawer.updateProcessingImage()
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
                text: qsTr("Image noise")
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