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
            // GroupBox {
            //     Layout.fillWidth: true
            //     ColumnLayout {
            //         Label {
            //             text: qsTr("Mean filter")
            //         }
            RowLayout {
                Label {
                    text: qsTr("Filter width:\t")
                }
                TextField {
                    id: filterWidth
                    text: qsTr("7")
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
                    text: qsTr("Filter height:\t")
                }
                TextField {
                    id: filterHeight
                    text: qsTr("7")
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
                    filtersController.meanFilter(colorModelSelector.colorModelTag, colorModelSelector.currentImageChannelIndex, isOriginalImage.checked, filterWidth.text, filterHeight.text)
                    secondPage.enabled = true
                    secondPage.updateProcessingImage()
                }
            }
            Button {
                text: qsTr("Median filter")
                width: parent.width
                onClicked: {
                    secondPage.enabled = false
                    filtersController.medianFilter(colorModelSelector.colorModelTag, colorModelSelector.currentImageChannelIndex, isOriginalImage.checked, filterWidth.text, filterHeight.text)
                    secondPage.enabled = true
                    secondPage.updateProcessingImage()
                }
            }
            Button {
                text: qsTr("Gaussian blur")
                width: parent.width
                onClicked: {
                    secondPage.enabled = false
                    filtersController.gaussianBlur(colorModelSelector.colorModelTag, colorModelSelector.currentImageChannelIndex, isOriginalImage.checked, filterWidth.text, filterHeight.text)
                    secondPage.enabled = true
                    secondPage.updateProcessingImage()
                }
            }
            GroupBox {
                Layout.fillWidth: true
                ColumnLayout {
                    // id: preferenceColorPanel
                    Layout.fillWidth: true
                    RowLayout {
                        Label {
                            text: qsTr("sigma:")
                        }
                        TextField {
                            id: sigma
                            text: qsTr("2")
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
                        text: qsTr("Laplacian blur")
                        width: parent.width
                        onClicked: {
                            secondPage.enabled = false
                            filtersController.laplacianBlur(colorModelSelector.colorModelTag, colorModelSelector.currentImageChannelIndex, isOriginalImage.checked, filterWidth.text, filterHeight.text, sigma.text)
                            secondPage.enabled = true
                            secondPage.updateProcessingImage()
                        }
                    }
                }
            }
            GroupBox {
                Layout.fillWidth: true
                ColumnLayout {
                    // id: preferenceColorPanel
                    Layout.fillWidth: true
                    RowLayout {
                        Label {
                            text: qsTr("sigma i:")
                        }
                        TextField {
                            id: sigma_i
                            text: qsTr("12")
                            Layout.fillWidth: true
                            validator: IntValidator{}
                            inputMethodHints: Qt.ImhFormattedNumbersOnly
                            background: Rectangle {
                                radius: 2
                                border.color: "#333"
                                border.width: 1
                            }
                        }
                        Label {
                            text: qsTr("sigma s:")
                        }
                        TextField {
                            id: sigma_s
                            text: qsTr("16")
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
                        text: qsTr("Bilateral filter")
                        width: parent.width
                        onClicked: {
                            secondPage.enabled = false
                            filtersController.bilateralFilter(colorModelSelector.colorModelTag, colorModelSelector.currentImageChannelIndex, isOriginalImage.checked, filterWidth.text, filterHeight.text, sigma_i.text, sigma_s.text)
                            secondPage.enabled = true
                            secondPage.updateProcessingImage()
                        }
                    }
                }
            }
            RowLayout {
                Label {
                    text: qsTr("Threshold:\t")
                }
                TextField {
                    id: thresholdHeight
                    text: qsTr("50")
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
                text: qsTr("2D Cleaner Filter By Jim Casaburi")
                width: parent.width
                onClicked: {
                    secondPage.enabled = false
                    filtersController.cleanerFilterByJimCasaburi(colorModelSelector.colorModelTag, colorModelSelector.currentImageChannelIndex, isOriginalImage.checked, filterWidth.text, filterHeight.text, thresholdHeight.text)
                    secondPage.enabled = true
                    secondPage.updateProcessingImage()
                }
            }

            RowLayout {
                Label {
                    text: qsTr("filterSize:\t")
                }
                TextField {
                    id: adaptiveMedianFilterSize
                    text: qsTr("7")
                    Layout.fillWidth: true
                    validator: IntValidator{}
                    inputMethodHints: Qt.ImhFormattedNumbersOnly
                    background: Rectangle {
                        radius: 2
                        border.color: "#333"
                        border.width: 1
                    }
                }
                Button {
                    text: qsTr("Adaptive median filter")
                    width: parent.width
                    onClicked: {
                        secondPage.enabled = false
                        filtersController.adaptiveMedianFilter(colorModelSelector.colorModelTag, colorModelSelector.currentImageChannelIndex, isOriginalImage.checked, adaptiveMedianFilterSize.text)
                        secondPage.enabled = true
                        secondPage.updateProcessingImage()
                    }
                }
            }

            ColorModelSelector {
                id: colorModelSelector
            }
        }
    }
}