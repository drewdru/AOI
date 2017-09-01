import QtQuick 2.6
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.1
import QtQuick.Controls.Material 2.1

Slider {    
    property string name
    
    id: firstChannelBalance
    value: 0
    stepSize: 1.0
    from: -to
    Layout.fillWidth: true
    ToolTip {
        visible: parent.pressed
        text: qsTr(name + " is " + parent.valueAt(parent.position).toFixed(1))
    }
}