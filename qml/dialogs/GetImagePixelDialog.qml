import QtQuick 2.6
import QtQuick.Controls 2.1
import QtQuick.Dialogs 1.2
import QtQuick.Layouts 1.3
import QtQuick.Controls.Material 2.1
import QtQuick.Window 2.0

import QtQml.Models 2.1

Dialog {
    id: getPixelDialog
    modality: Qt.WindowModal
    // modality: Qt.NonModal

    Material.theme: Material.Dark
    Material.accent: Material.Red
    width: 600
    height: 600
    property string xPix: '0'
    property string yPix: '0'

    title: "Please get pixel"
    standardButtons: StandardButton.Ok | StandardButton.Cancel

    // signal test()
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
                fillMode : "PreserveAspectFit"
                source: appDir + "/temp/inImage.png"
                MouseArea {
                    id: selectArea;
                    anchors.fill: parent;
                    onPressed: {
                        getPixelDialog.xPix = mouse.x
                        getPixelDialog.yPix = mouse.y
                        getPixelDialog.click(StandardButton.Ok)
                        // getPixelDialog.close()
                        // getPixelDialog.test()
                    }
                }
            }
        }
    }
}
