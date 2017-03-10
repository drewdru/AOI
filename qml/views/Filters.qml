import QtQuick 2.6
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.1
import QtQuick.Controls.Material 2.1
import QtQuick.Dialogs 1.0
import "../components"

Item {
    id: secondPage

    property string colorModelTag: "RGB"

    Material.theme: Material.Dark
    Material.accent: Material.Red

    signal updateProcessingImage()

    anchors.fill: parent        
    anchors.margins: 10

    onColorModelTagChanged: {
        console.log(secondPage.colorModelTag)
    }

    Flickable {
        focus: true
        anchors.fill: parent
        contentWidth: preferenceColorPanel.width
        contentHeight: preferenceColorPanel.height
        // contentY : 20
        boundsBehavior: Flickable.StopAtBounds
        

        Keys.onUpPressed: verticalScrollBar.decrease()
        Keys.onDownPressed: verticalScrollBar.increase()

        ScrollBar.vertical: ScrollBar {
            id: verticalScrollBar
            Binding {
                target: verticalScrollBar
                property: "active"
                value: verticalScrollBar.hovered
            }
        }

        ColumnLayout {
            id: preferenceColorPanel
            Layout.fillWidth: true
            width: secondPage.width
            CheckBox {
                id: isOriginalImage
                checked: true
                text: qsTr("Use original image")
            }
            GroupBox {
                Layout.fillWidth: true
                ColumnLayout {
                    Label {
                        text: qsTr("Mean filter")
                    }
                    RowLayout {
                        Label {
                            text: qsTr("filter width:\t")
                        }
                        TextField {
                            id: kmin
                            text: qsTr("3")
                            Layout.fillWidth: true
                            validator: IntValidator{}
                            inputMethodHints: Qt.ImhFormattedNumbersOnly
                            background: Rectangle {
                                radius: 2
                                border.color: "#333"
                                border.width: 1
                            }
                        }
                    }
                    RowLayout {
                        Label {
                            text: qsTr("filter height:\t")
                        }
                        TextField {
                            id: kmax
                            text: qsTr("3")
                            Layout.fillWidth: true
                            validator: IntValidator{}
                            inputMethodHints: Qt.ImhFormattedNumbersOnly
                            background: Rectangle {
                                radius: 2
                                border.color: "#333"
                                border.width: 1
                            }
                        }
                    }
                    Button {
                        text: qsTr("Mean filter")
                        width: parent.width
                        onClicked: {
                            secondPage.enabled = false
                            noiseGeneratorController.addMultiplicativeNoise(colorModelSelector.colorModelTag, colorModelSelector.currentImageChannelIndex, kmin.text, kmax.text, noiseLevelBalance.value, isOriginalImage.checked)
                            secondPage.enabled = true
                            secondPage.updateProcessingImage()
                        }
                    }
                }
            }
        }
    }
}