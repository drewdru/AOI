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


    property int apertureWidth: 3
    property int apertureHeight: 3

    property ObjectModel test: itemModel
    // onButtonClicked: {
    //     console.log(itemModel.get(0).Row)
    //     // test = grid
    // }
    width: 50 * apertureWidth
    height: 50 * apertureHeight

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
            

            ColumnLayout {
                id: preferenceColorPanel
                Layout.fillWidth: true
                Layout.fillHeight: true
                // width: secondPage.width
                Grid {
                    id: grid
                    anchors.fill: parent
                    columns: 1
                    Repeater {
                        model: itemModel
                    }
                }
            }
        }
    }

    ObjectModel {
        id: itemModel
        Repeater {
            model: apertureHeight
            Row {
                property int heightRepeatRow: index
                
                // Component.onCompleted: console.log("index: ", index)
                
                Repeater {
                    model: apertureWidth
                    Rectangle { 
                        property int heightRepeat: heightRepeatRow
                        property int widthRepeat: index
                        border.width: 1
                        border.color: 'red'
                        height: 50
                        width: 50
                        color: "#ffffff"
                        // NO://get value CellMaskList
                        
                        MouseArea {
                            anchors.fill: parent
                            cursorShape: Qt.PointingHandCursor
                            hoverEnabled: true
                            onEntered: {}
                            onExited: {}
                            onWheel: {}
                            onClicked: {
                                console.log(widthRepeat)
                                console.log(heightRepeat)
                                binarizeController.updateCellMaskList(widthRepeat, heightRepeat, parent.color == '#00aa00' ? false : true)
                                parent.color = parent.color == '#00aa00' ? '#ffffff' : '#00aa00'
                            }
                        }
                    }
                }
            }
        }
    }
}
