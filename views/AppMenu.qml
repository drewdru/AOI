import QtQuick 2.7
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.1
import QtQuick.Dialogs 1.2
import "../JS/main.js" as App

Item {
    id: menuWrapper
    
    property bool isDrawerVisible: false
    signal showDrawer()
    signal hideDrawer()
    signal updateImages()
    
    Shortcut {
        sequence: "Ctrl+Q"
        onActivated: Qt.quit()
    }
    Shortcut {
        sequence: "Ctrl+O"
        onActivated: fileOpenDialog.open()
    }
    FileDialog {
        id: fileOpenDialog
        title: qsTr("Open a file")
        folder: "../"
        onAccepted: {
            App.openFile(fileOpenDialog.fileUrls)
            menuWrapper.updateImages()
        }
    }
    FileDialog {
        id: fileSaveDialog
        title: qsTr("Save as...")
        folder: "../"
        selectExisting: false
        onAccepted: {
            App.saveFile(fileSaveDialog.fileUrls)
            menuWrapper.updateImages()
        }
    }
    ToolBar {
        id: myTopMenu
        x: 0
        y: 0
        width: parent.width
        RowLayout {
            ToolButton { 
                onClicked:{                    
                    if (menuWrapper.isDrawerVisible)
                        menuWrapper.hideDrawer()
                    else
                        menuWrapper.showDrawer()
                }
                background: Rectangle {
                    implicitWidth: 40
                    implicitHeight: 40
                    color: {
                        if (parent.down)
                            Qt.darker("#33333333", parent.enabled && (parent.checked || parent.highlighted) ? 1.5 : 1.0)
                        else
                            Qt.darker("#00FFFFFF", parent.enabled && (parent.checked || parent.highlighted) ? 1.5 : 1.0)

                    }
                    opacity: enabled ? 1 : 0.3
                    Image {
                        anchors.margins: 5
                        id: photoPreview                        
                        anchors.fill: parent
                        fillMode : "PreserveAspectFit"
                        source: appDir + "/image/burger.png"
                    }
                }
            }
            ToolButton { 
                text: "File"
                hoverEnabled: true
                onClicked: menu.open()
                Menu {
                    y: myTopMenu.height
                    id: menu
                    MenuItem {
                        text: "Open"
                        onTriggered: fileOpenDialog.open()
                    }
                    MenuItem {
                        text: "Save As..."
                        onTriggered: fileSaveDialog.open()
                    }
                    MenuItem {
                        text: "Exit"
                        onTriggered: Qt.quit()
                    }
                }
            }
        }
    }
}