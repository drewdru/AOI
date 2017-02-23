import QtQuick 2.6
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.1
import QtQuick.Controls.Material 2.1
// import QtQuick.Controls.Styles 1.4
// import QtQuick.Controls 2.1
import "../JS/main.js" as App

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
}