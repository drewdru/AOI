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
            ColorModelSelector {
                id: colorModelSelector
            }
            GroupBox {
                title: 'Global threshold'
                Layout.fillWidth: true
                ColumnLayout {
                    RowLayout {
                        Label {
                            text: qsTr("k:")
                        }
                        TextField {
                            id: global_threshold_k
                            text: qsTr("116")
                            Layout.fillWidth: true
                            validator: DoubleValidator{locale: DoubleValidator.StandardNotation}
                            inputMethodHints: Qt.ImhDigitsOnly
                            background: Rectangle {
                                radius: 2
                                border.color: "#333"
                                border.width: 1
                            }
                        }
                    }

                    RowLayout {
                        Button {
                            text: qsTr("Otsu")
                            width: parent.width
                            onClicked: {
                                secondPage.enabled = false
                                binarizeController.otsuBinarize(colorModelSelector.colorModelTag, colorModelSelector.currentImageChannelIndex, isOriginalImage.checked, global_threshold_k.text)
                                secondPage.enabled = true
                                secondPage.updateProcessingImage()
                            }
                        }
                        Button {
                            text: qsTr("Threshold by histogram")
                            width: parent.width
                            onClicked: {
                                secondPage.enabled = false
                                binarizeController.histThresholdBinarize(colorModelSelector.colorModelTag, colorModelSelector.currentImageChannelIndex, isOriginalImage.checked, global_threshold_k.text)
                                secondPage.enabled = true
                                secondPage.updateProcessingImage()
                            }
                        }
                    }
                }
            }
            GroupBox {
                title: 'Local threshold'
                Layout.fillWidth: true
                ColumnLayout {
                    RowLayout {
                        Label {
                            text: qsTr("Aperture width:")
                        }
                        TextField {
                            id: aperture_width
                            text: qsTr("3")
                            Layout.fillWidth: true
                            validator: DoubleValidator{locale: DoubleValidator.StandardNotation}
                            inputMethodHints: Qt.ImhDigitsOnly
                            background: Rectangle {
                                radius: 2
                                border.color: "#333"
                                border.width: 1
                            }
                        }
                        Label {
                            text: qsTr("height:")
                        }
                        TextField {
                            id: aperture_height
                            text: qsTr("3")
                            Layout.fillWidth: true
                            validator: DoubleValidator{locale: DoubleValidator.StandardNotation}
                            inputMethodHints: Qt.ImhDigitsOnly
                            background: Rectangle {
                                radius: 2
                                border.color: "#333"
                                border.width: 1
                            }
                        }
                    }

                    RowLayout {
                        Button {
                            text: qsTr("Bersen's binarize")
                            width: parent.width
                            onClicked: {
                                secondPage.enabled = false
                                binarizeController.bernsenBinarize(colorModelSelector.colorModelTag, colorModelSelector.currentImageChannelIndex, isOriginalImage.checked, aperture_width.text, aperture_height.text)
                                secondPage.enabled = true
                                secondPage.updateProcessingImage()
                            }
                        }
                        Button {
                            text: qsTr("Niblack's binarize")
                            width: parent.width
                            onClicked: {
                                secondPage.enabled = false
                                binarizeController.niblackBinarize(colorModelSelector.colorModelTag, colorModelSelector.currentImageChannelIndex, isOriginalImage.checked, aperture_width.text, aperture_height.text)
                                secondPage.enabled = true
                                secondPage.updateProcessingImage()
                            }
                        }
                    }
                }
            }
        }
    }
}