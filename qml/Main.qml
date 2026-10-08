import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: root
    visible: true
    width: 1180
    height: 780
    minimumWidth: 850
    minimumHeight: 620
    title: "لغتي — تعلم العربية والإنجليزية"
    color: "#F4F7FB"

    LayoutMirroring.enabled: true
    LayoutMirroring.childrenInherit: true

    property string page: "languages"
    property string selectedLanguage: "ar"
    property int selectedLevel: 0
    property var selectedLesson: ({})
    property var levelRows: []
    property var lessonRows: []

    function chooseLanguage(code) {
        selectedLanguage = code
        levelRows = appBackend.levels(code)
        page = "levels"
    }

    function openLevel(level) {
        selectedLevel = level
        lessonRows = appBackend.lessons(level, selectedLanguage)
        page = "stages"
    }

    function openLesson(id) {
        selectedLesson = appBackend.lesson(id)
        page = "lesson"
    }

    function goBack() {
        if (page === "lesson") page = "stages"
        else if (page === "stages") page = "levels"
        else page = "languages"
    }

    Rectangle {
        anchors.fill: parent
        color: root.color

        ColumnLayout {
            anchors.fill: parent
            spacing: 0

            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 82
                color: "white"
                border.color: "#E5EAF1"

                RowLayout {
                    anchors.fill: parent
                    anchors.margins: 22
                    spacing: 14

                    Button {
                        visible: root.page !== "languages"
                        text: "رجوع"
                        onClicked: root.goBack()
                    }

                    Text {
                        text: "لغتي ✨"
                        font.pixelSize: 27
                        font.bold: true
                        color: "#27364B"
                    }

                    Item { Layout.fillWidth: true }

                    Text {
                        text: "⭐ " + appBackend.xp + " نقطة"
                        font.pixelSize: 16
                        font.bold: true
                        color: "#23607A"
                    }
                    Text {
                        text: appBackend.completedLessons + " درس مكتمل"
                        font.pixelSize: 16
                        color: "#53657A"
                    }
                }
            }

            StackLayout {
                Layout.fillWidth: true
                Layout.fillHeight: true
                currentIndex: ["languages", "levels", "stages", "lesson"].indexOf(root.page)

                Item {
                    ScrollView {
                        anchors.fill: parent
                        contentWidth: availableWidth
                        ColumnLayout {
                            width: Math.min(parent.width - 48, 1000)
                            anchors.horizontalCenter: parent.horizontalCenter
                            spacing: 22

                            Text {
                                Layout.fillWidth: true
                                text: "اختر اللغة التي تريد تعلمها"
                                horizontalAlignment: Text.AlignHCenter
                                font.pixelSize: 32
                                font.bold: true
                                color: "#24364B"
                            }
                            Text {
                                Layout.fillWidth: true
                                text: "لكل لغة مستويات متدرجة، وفي كل مستوى مراحل تدريبية."
                                horizontalAlignment: Text.AlignHCenter
                                font.pixelSize: 19
                                color: "#65758A"
                            }

                            RowLayout {
                                Layout.fillWidth: true
                                spacing: 20

                                Rectangle {
                                    Layout.fillWidth: true
                                    Layout.preferredHeight: 250
                                    radius: 28
                                    color: "white"
                                    border.color: "#E1E8F0"
                                    ColumnLayout {
                                        anchors.centerIn: parent
                                        spacing: 12
                                        Text { text: "🇸🇦"; font.pixelSize: 52; Layout.alignment: Qt.AlignHCenter }
                                        Text { text: "اللغة العربية"; font.pixelSize: 25; font.bold: true; color: "#27364B"; Layout.alignment: Qt.AlignHCenter }
                                        Text { text: "حروف وأصوات وقراءة وكتابة"; font.pixelSize: 16; color: "#65758A"; Layout.alignment: Qt.AlignHCenter }
                                        Button {
                                            text: "ابدأ العربية"
                                            Layout.alignment: Qt.AlignHCenter
                                            onClicked: root.chooseLanguage("ar")
                                        }
                                    }
                                    MouseArea {
                                        anchors.fill: parent
                                        z: -1
                                        onClicked: root.chooseLanguage("ar")
                                    }
                                }

                                Rectangle {
                                    Layout.fillWidth: true
                                    Layout.preferredHeight: 250
                                    radius: 28
                                    color: "white"
                                    border.color: "#E1E8F0"
                                    ColumnLayout {
                                        anchors.centerIn: parent
                                        spacing: 12
                                        Text { text: "🇬🇧"; font.pixelSize: 52; Layout.alignment: Qt.AlignHCenter }
                                        Text { text: "اللغة الإنجليزية"; font.pixelSize: 25; font.bold: true; color: "#27364B"; Layout.alignment: Qt.AlignHCenter }
                                        Text { text: "حروف وأصوات وكلمات وقراءة وكتابة"; font.pixelSize: 16; color: "#65758A"; Layout.alignment: Qt.AlignHCenter }
                                        Button {
                                            text: "ابدأ الإنجليزية"
                                            Layout.alignment: Qt.AlignHCenter
                                            onClicked: root.chooseLanguage("en")
                                        }
                                    }
                                    MouseArea {
                                        anchors.fill: parent
                                        z: -1
                                        onClicked: root.chooseLanguage("en")
                                    }
                                }
                            }
                        }
                    }
                }

                Item {
                    ScrollView {
                        anchors.fill: parent
                        contentWidth: availableWidth
                        ColumnLayout {
                            width: Math.min(parent.width - 48, 1050)
                            anchors.horizontalCenter: parent.horizontalCenter
                            spacing: 16

                            Text {
                                text: root.selectedLanguage === "ar" ? "مستويات اللغة العربية" : "مستويات اللغة الإنجليزية"
                                font.pixelSize: 30
                                font.bold: true
                                color: "#24364B"
                            }
                            Text {
                                text: "اختر المستوى، ثم اتبع مراحله بالترتيب."
                                font.pixelSize: 17
                                color: "#65758A"
                            }

                            Repeater {
                                model: root.levelRows
                                delegate: Rectangle {
                                    Layout.fillWidth: true
                                    Layout.preferredHeight: 104
                                    radius: 20
                                    color: "white"
                                    border.color: "#E1E8F0"

                                    RowLayout {
                                        anchors.fill: parent
                                        anchors.margins: 18
                                        spacing: 16
                                        Rectangle {
                                            width: 54
                                            height: 54
                                            radius: 17
                                            color: "#EAF3FF"
                                            Text {
                                                anchors.centerIn: parent
                                                text: (modelData.level + 1).toString()
                                                font.pixelSize: 22
                                                font.bold: true
                                                color: "#3367A8"
                                            }
                                        }
                                        ColumnLayout {
                                            Layout.fillWidth: true
                                            Text {
                                                text: modelData.title
                                                font.pixelSize: 20
                                                font.bold: true
                                                color: "#27364B"
                                            }
                                            Text {
                                                text: modelData.lessonCount + " مراحل تعليمية في هذا المستوى"
                                                font.pixelSize: 15
                                                color: "#65758A"
                                            }
                                            Text {
                                                text: modelData.goal
                                                font.pixelSize: 13
                                                color: "#718096"
                                                elide: Text.ElideRight
                                            }
                                        }
                                        Button {
                                            text: "افتح المستوى"
                                            onClicked: root.openLevel(modelData.level)
                                        }
                                    }
                                }
                            }
                        }
                    }
                }

                Item {
                    ScrollView {
                        anchors.fill: parent
                        contentWidth: availableWidth
                        ColumnLayout {
                            width: Math.min(parent.width - 48, 1050)
                            anchors.horizontalCenter: parent.horizontalCenter
                            spacing: 15

                            Text {
                                text: "مراحل المستوى " + (root.selectedLevel + 1) + ": "
                                      + (root.levelRows[root.selectedLevel] ? root.levelRows[root.selectedLevel].title : "")
                                font.pixelSize: 28
                                font.bold: true
                                color: "#24364B"
                            }
                            Text {
                                text: root.levelRows[root.selectedLevel] ? root.levelRows[root.selectedLevel].goal : "اتبع المراحل بالترتيب، من الاستماع إلى التطبيق."
                                font.pixelSize: 17
                                color: "#65758A"
                            }

                            Repeater {
                                model: root.lessonRows
                                delegate: Rectangle {
                                    Layout.fillWidth: true
                                    Layout.preferredHeight: 105
                                    radius: 20
                                    color: "white"
                                    border.color: modelData.done ? "#9BD5B2" : "#E1E8F0"
                                    RowLayout {
                                        anchors.fill: parent
                                        anchors.margins: 18
                                        spacing: 15
                                        Rectangle {
                                            width: 52
                                            height: 52
                                            radius: 17
                                            color: modelData.done ? "#E7F7ED" : "#F0F4FA"
                                            Text {
                                                anchors.centerIn: parent
                                                text: modelData.stage.toString()
                                                font.pixelSize: 21
                                                font.bold: true
                                                color: modelData.done ? "#27834E" : "#53657A"
                                            }
                                        }
                                        ColumnLayout {
                                            Layout.fillWidth: true
                                            Text {
                                                text: (root.selectedLanguage === "ar" ? "المرحلة " : "Stage ")
                                                      + modelData.stage + ": " + modelData.stageTitle
                                                font.pixelSize: 19
                                                font.bold: true
                                                color: "#27364B"
                                            }
                                            Text {
                                                text: modelData.stageDescription
                                                font.pixelSize: 15
                                                color: "#65758A"
                                            }
                                        }
                                        Text {
                                            text: modelData.done ? "✓ مكتمل" : ""
                                            font.pixelSize: 15
                                            color: "#27834E"
                                        }
                                        Button {
                                            text: "ابدأ"
                                            onClicked: root.openLesson(modelData.id)
                                        }
                                    }
                                }
                            }

                            Text {
                                visible: root.lessonRows.length === 0
                                text: "لا توجد دروس لهذا المستوى حتى الآن."
                                font.pixelSize: 18
                                color: "#65758A"
                            }
                        }
                    }
                }

                Item {
                    ScrollView {
                        anchors.fill: parent
                        contentWidth: availableWidth
                        ColumnLayout {
                            width: Math.min(parent.width - 48, 1000)
                            anchors.horizontalCenter: parent.horizontalCenter
                            spacing: 18

                            Text {
                                Layout.fillWidth: true
                                text: "المرحلة التعليمية: " + (root.selectedLesson.stageTitle || "الدرس")
                                wrapMode: Text.WordWrap
                                font.pixelSize: 29
                                font.bold: true
                                color: "#24364B"
                            }
                            Rectangle {
                                Layout.fillWidth: true
                                radius: 24
                                color: "white"
                                border.color: "#E1E8F0"
                                ColumnLayout {
                                    anchors.fill: parent
                                    anchors.margins: 24
                                    spacing: 14
                                    Text {
                                        text: root.selectedLesson.goal || root.selectedLesson.stageDescription || ""
                                        font.pixelSize: 20
                                        font.bold: true
                                        color: "#3367A8"
                                    }
                                    Text {
                                        Layout.fillWidth: true
                                        text: root.selectedLesson.body || ""
                                        wrapMode: Text.WordWrap
                                        font.pixelSize: 18
                                        color: "#40536A"
                                    }
                                    Button {
                                        text: "🎧 استمع إلى التدريب الصوتي"
                                        enabled: (root.selectedLesson.audioUrl || "").length > 0
                                        onClicked: Qt.openUrlExternally(root.selectedLesson.audioUrl)
                                    }
                                    Text {
                                        visible: (root.selectedLesson.audioUrl || "").length === 0
                                        text: "لا يوجد ملف صوتي لهذا المستوى بعد."
                                        font.pixelSize: 14
                                        color: "#7A8797"
                                    }
                                }
                            }

                            Text {
                                text: "كلمات المرحلة"
                                font.pixelSize: 23
                                font.bold: true
                                color: "#27364B"
                            }
                            Repeater {
                                model: root.selectedLesson.words || []
                                delegate: Rectangle {
                                    Layout.fillWidth: true
                                    Layout.preferredHeight: 88
                                    radius: 18
                                    color: "white"
                                    border.color: "#E7ECF2"
                                    RowLayout {
                                        anchors.fill: parent
                                        anchors.margins: 17
                                        Text {
                                            text: modelData.text
                                            font.pixelSize: 22
                                            font.bold: true
                                            color: "#27364B"
                                        }
                                        Item { Layout.fillWidth: true }
                                        Text {
                                            text: modelData.meaning
                                            font.pixelSize: 16
                                            color: "#65758A"
                                        }
                                    }
                                }
                            }

                            Text {
                                text: "مشاهد الدرس المرئي (النص)"
                                font.pixelSize: 23
                                font.bold: true
                                color: "#27364B"
                            }
                            Text {
                                Layout.fillWidth: true
                                text: "هذه خطة المشاهد والحوار؛ ملف الفيديو المتحرك غير مرفق حاليًا."
                                wrapMode: Text.WordWrap
                                font.pixelSize: 14
                                color: "#7A8797"
                            }
                            Repeater {
                                model: root.selectedLesson.videoScenes || []
                                delegate: Rectangle {
                                    Layout.fillWidth: true
                                    Layout.preferredHeight: 88
                                    radius: 18
                                    color: "white"
                                    border.color: "#E7ECF2"
                                    ColumnLayout {
                                        anchors.fill: parent
                                        anchors.margins: 15
                                        Text {
                                            text: modelData.order + ". " + modelData.character
                                            font.pixelSize: 15
                                            font.bold: true
                                            color: "#3367A8"
                                        }
                                        Text {
                                            Layout.fillWidth: true
                                            text: modelData.dialogue || modelData.action
                                            wrapMode: Text.WordWrap
                                            font.pixelSize: 16
                                            color: "#40536A"
                                        }
                                    }
                                }
                            }

                            Button {
                                text: "أنهيت المرحلة"
                                Layout.preferredHeight: 52
                                onClicked: {
                                    appBackend.completeLesson(root.selectedLesson.id, 100)
                                    root.lessonRows = appBackend.lessons(root.selectedLevel, root.selectedLanguage)
                                    root.page = "stages"
                                }
                            }
                        }
                    }
                }
            }

            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 54
                color: "white"
                border.color: "#E5EAF1"
                Text {
                    anchors.centerIn: parent
                    text: "تعلّم خطوة بخطوة • العربية والإنجليزية"
                    font.pixelSize: 14
                    color: "#718096"
                }
            }
        }
    }
}