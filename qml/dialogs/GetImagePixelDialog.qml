import QtQuick 2.6
import QtQuick.Controls 2.1
import QtQuick.Dialogs 1.2
import QtQuick.Layouts 1.3
import QtQuick.Controls.Material 2.1
import QtQuick.Window 2.0

import QtQml.Models 2.1

Dialog {
    id: spinboxDialog
    modality: Qt.WindowModal

    Material.theme: Material.Dark
    Material.accent: Material.Red
    width: 600
    height: 600

    contentItem: Rectangle {
        color: 'white'
        Flickable {
            focus: true
            anchors.fill: parent
            contentWidth: preferenceColorPanel.width
            contentHeight: preferenceColorPanel.height
            // contentY : 20
            boundsBehavior: Flickable.StopAtBounds
            
            // Keys.onUpPressed: verticalScrollBar.decrease()
            // Keys.onDownPressed: verticalScrollBar.increase()

            // Keys.onLeftPressed: horizontalScrollBar.decrease()
            // Keys.onRightPressed: horizontalScrollBar.increase()

            ScrollBar.vertical: ScrollBar {
                id: verticalScrollBar
                Binding {
                    target: verticalScrollBar
                    property: "active"
                    value: verticalScrollBar.hovered
                }
            }
            ScrollBar.horizontal: ScrollBar {
                id: horizontalScrollBar
                Binding {
                    target: horizontalScrollBar
                    property: "active"
                    value: horizontalScrollBar.hovered
                }
            }
            
            Image {
                id: photoPreview
                cache: false
                // // width: parent.width/2 - 10
                // Layout.fillWidth: true
                // Layout.fillHeight: true
                fillMode : "PreserveAspectFit"
                source: appDir + "/temp/inImage.png"
                MouseArea {
                    id: selectArea;
                    anchors.fill: parent;
                    onPressed: {
                        
                        console.log("x: ", mouse.x )
                        console.log("y: ", mouse.y )
                    }
                }
            }
        }
    }
}
