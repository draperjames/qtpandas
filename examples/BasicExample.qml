import QtQuick 2.5
// import QtQuick.Window 2.2
import QtQuick.Controls 1.4

Rectangle {
    width: 480
    height: 640

//     TextField {
//         id: edit
// 
//         placeholderText: "Filter.."
// 
//         anchors.top: parent.top
//         anchors.left: parent.left
//         anchors.right: parent.right
// 
//         anchors.margins: 10
// 
// //         onTextChanged: qmodel.setFilterFixedString(text)
//     }
    
    Button{
        id: edit
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right

        anchors.margins: 10
        text : "About"
        onClicked: {
            print('Hello')
        }
    }
    Rectangle {
        color: "red"
        radius: 2

        anchors.top: edit.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.margins: 5

        TableView {
            id: myTableView
            anchors.fill: parent
            anchors.margins: 5
            model: dataFrameModel

            TableViewColumn {
                role: "columnA"
                title: "A"
                width: 100
//                 delegate: Text {text: model.columnA}
            }
            TableViewColumn {
                role: "columnB"
                title: "B"
                width: 100
            }
            TableViewColumn {
                role: "columnC"
                title: "C"
                width: 100
            }
        }
    }

}