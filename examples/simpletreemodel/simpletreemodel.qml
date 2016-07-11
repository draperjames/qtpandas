import QtQuick 2.5
import QtQuick.Controls 1.4

Rectangle {
    width: 480
    height: 640

    TreeView {
        id: treeView
        anchors.fill: parent
        anchors.margins: 6
        anchors.top: parent.top
        anchors.horizontalCenter: parent.horizontalCenter

        model: model

        TableViewColumn {
            title: "Title"
            role: "TitleRole"
            resizable: true
        }

        TableViewColumn {
            title: "Summary"
            role: "SummaryRole"
            resizable: true
        }
    }
}