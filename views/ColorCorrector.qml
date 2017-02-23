import QtQuick 2.6
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.1
import QtQuick.Controls.Material 2.1
Item {
    id: firstPage

    Material.theme: Material.Dark
    Material.accent: Material.Red

    signal updateProcessingImage()

    anchors.fill: parent        
    anchors.margins: 10

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
            // Layout.fillWidth: true
            width: firstPage.width
            CheckBox {
                id: isOriginalImage
                checked: true
                text: qsTr("Use original image")
            }    
            Button {
                id: grayscaleButton
                text: qsTr("Grayscale")
                onClicked: {
                    preferenceColorPanel.enabled = false
                    colorCorrectorController.toGrayscale(isOriginalImage.checked)
                    firstPage.updateProcessingImage()
                    preferenceColorPanel.enabled = true
                }
            }
            RowLayout {
                Label {
                    text: qsTr("Hue:")
                }
                HueSlider {
                    isOriginalImage: isOriginalImage.checked
                    onUpdateProcessingImage: firstPage.updateProcessingImage()
                }    
            }
            
            ColorModelGroupBox {
                isOriginalImage: isOriginalImage.checked
                onUpdateProcessingImage: firstPage.updateProcessingImage()
            }        
        }
    }
}