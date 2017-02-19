import QtQuick 2.6
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.1
import QtQuick.Controls.Material 2.1
// import QtQuick.Controls.Styles 1.4
// import QtQuick.Controls 2.1
import "../JS/application.js" as App
// import QtQuick.Dialogs 1.0
// ColorDialog {
//     id: colorDialog
//     title: "Please choose a color"
//     onAccepted: {
//         console.log("You chose: " + colorDialog.color)
//         Qt.quit()
//     }
//     onRejected: {
//         console.log("Canceled")
//         Qt.quit()
//     }
//     Component.onCompleted: visible = true
// }

Rectangle {

    Material.theme: Material.Dark
    Material.accent: Material.Red
    color: Material.color(Material.BlueGrey)

    id: rootWindow    
    anchors.fill: parent    
    width: 300; height: 300    
    // color: "#80000000"

    Component.onCompleted: {
        App.onLoad()
        photoPreview2.source = "file:inImage.png"
        photoPreview2.source = "file:processingImage.png"
    }

    Shortcut {
        sequence: "Ctrl+W"
        onActivated: appMenu.showDrawer()
    }

    AppMenu {
        id: appMenu
        width: parent.width
        height: 20
        onShowDrawer: drawer.open()
        onHideDrawer: drawer.close()
        onUpdateImages: {
            photoPreview.source = "file:processingImage.png"
            photoPreview.source = "file:inImage.png"
            App.loadProcessingImage()
            photoPreview2.source = "file:inImage.png"
            photoPreview2.source = "file:processingImage.png"
        }
    }
    AppDrawer {
        id: drawer
        y: 40
        height: parent.height - y
        onUpdateProcessingImage: {
            photoPreview2.source = "file:inImage.png"
            photoPreview2.source = "file:processingImage.png"
        }
        onOpened: appMenu.isDrawerVisible = true
        onClosed: appMenu.isDrawerVisible = false
        Shortcut {
            sequence: "Ctrl+W"
            onActivated: appMenu.hideDrawer()
        }
    }

    GridLayout
    {
        id:grid
        anchors.fill: parent
        columns: 3
        anchors.margins: 10

        RowLayout {
            Layout.columnSpan: 2
            Image {
                id: photoPreview
                width: parent.width/2 - 10
                Layout.fillWidth: true
                Layout.fillHeight: true
                fillMode : "PreserveAspectFit"
                source: "file:../inImage.png"
            }
            Image {
                id: photoPreview2
                x:photoPreview.width + 10
                width: parent.width / 2
                Layout.fillWidth: true
                Layout.fillHeight: true
                fillMode : "PreserveAspectFit"
                source: "file:../processingImage.png"
            }
        }
        
        // Text {
        //     Layout.columnSpan: 2
        //     Layout.margins: 15
        //     text: qsTr(" ")
        // }
    }

    // ColumnLayout {
    //     id:mainLayout
    //     anchors.fill: parent
    //     anchors.margins: 10

    //     AppMenu {        
    //         Layout.fillWidth: true
    //     }

    //     GroupBox {
    //         Layout.margins: 10
    //         id: rowBox
    //         title: "Row layout"
    //         Layout.fillWidth: true
    //         Layout.alignment : Qt.AlignTop

    //         RowLayout {
    //             id: rowLayout
    //             anchors.fill: parent
    //             TextField {
    //                 placeholderText: "This wants to grow horizontally"
    //                 Layout.fillWidth: true
    //             }
    //             Button {
    //                 text: "Button"
    //             }
    //             Grid {
    //             // Layout.alignment : Qt.AlignTop
    //                 id: colorPicker

    //                 rows: 2; columns: 3; spacing: 3

    //                 Cell { cellColor: "white"; onClicked: helloText.color = cellColor }
    //                 Cell { cellColor: "green"; onClicked: helloText.color = cellColor }
    //                 Cell { cellColor: "blue"; onClicked: helloText.color = cellColor }
    //                 Cell { cellColor: "yellow"; onClicked: helloText.color = cellColor }
    //                 Cell { cellColor: "steelblue"; onClicked: helloText.color = cellColor }
    //                 Cell { cellColor: "black"; onClicked: helloText.color = cellColor }
    //             }
    //         }
    //     }
    //     Text {
    //     // Layout.alignment : Qt.AlignTop
    //         id: helloText
    //         anchors.verticalCenter: parent.verticalCenter
    //         anchors.horizontalCenter: parent.horizontalCenter
    //         text: "Hello World!!!\n Traditional first app using PyQt5"
    //         color: "blue"
    //         font.family: "Helvetica"
    //         font.pointSize: 14
    //         horizontalAlignment: Text.AlignHCenter
    //     }
    // }
}