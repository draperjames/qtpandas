import QtQuick 2.5
import QtQuick.Controls 1.4

Rectangle {
    width: 480
    height: 640

    TreeView {
        id: fsView
        anchors.fill: parent
        anchors.margins: 6
        anchors.top: parent.top
        anchors.horizontalCenter: parent.horizontalCenter

        model: fsmodel

        TableViewColumn {
            title: "Name"
            role: "fileName"
            resizable: true
        }
    }
}