import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: root
    visible: true
    width: 1280
    height: 800
    minimumWidth: 900
    minimumHeight: 600
    title: "لغتي — رحلة تعلم العربية والإنجليزية"
    layoutDirection: Qt.RightToLeft
    color: "#F7F9FC"

    property string page: "home"
    property int selectedLevel: 0
    property var selectedLesson: ({})
    property var levelRows: []
    property var lessonRows: []
    property var storyRows: []
    property var achievementRows: []

    Component.onCompleted: {
        levelRows = appBackend.levels()
        storyRows = appBackend.stories()
        achievementRows = appBackend.achievements()
    }

    function openLevel(level) {
        selectedLevel=level
        lessonRows=appBackend.lessons(level)
        page="lessons"
    }
    function openLesson(id) {
        selectedLesson=appBackend.lesson(id)
        page="lesson"
    }

    Rectangle {
        anchors.fill: parent
        color: "#F7F9FC"

        ColumnLayout {
            anchors.fill: parent
            spacing: 0

            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 78
                color: "#FFFFFF"
                border.color: "#E8ECF3"

                RowLayout {
                    anchors.fill: parent
                    anchors.margins: 22
                    Text { text: "لغتي ✨"; font.pixelSize: 28; font.bold: true; color: "#27364B" }
                    Item { Layout.fillWidth: true }
                    Rectangle {
                        width: 150; height: 44; radius: 22; color: "#FFF4D8"
                        RowLayout { anchors.fill: parent; anchors.margins: 12
                            Text { text: "🔥 " + appBackend.streak; font.pixelSize: 17; font.bold: true }
                            Text { text: "أيام متتالية"; color: "#6B5B2A" }
                        }
                    }
                    Rectangle {
                        width: 150; height: 44; radius: 22; color: "#EAF7FF"
                        Text { anchors.centerIn: parent; text: "⭐ " + appBackend.xp + " نقطة"; color: "#23607A"; font.bold: true }
                    }
                    Button { text: "⚙️"; onClicked: page="settings" }
                }
            }

            StackLayout {
                id: content
                Layout.fillWidth: true
                Layout.fillHeight: true
                currentIndex: ["home","journey","lessons","lesson","games","stories","progress","parent","settings"].indexOf(root.page)

                Item {
                    ScrollView { anchors.fill: parent
                        ColumnLayout { width: root.width-60; anchors.horizontalCenter: parent.horizontalCenter; spacing: 20
                            Item { Layout.preferredHeight: 20 }
                            Rectangle {
                                Layout.fillWidth: true; Layout.preferredHeight: 210; radius: 30
                                gradient: Gradient { GradientStop { position:0; color:"#E7F6FF" } GradientStop { position:1; color:"#FFF0F7" } }
                                RowLayout { anchors.fill: parent; anchors.margins: 28
                                    ColumnLayout { Layout.fillWidth:true; spacing:10
                                        Text { text:"مرحباً يا " + appBackend.childName + " 👋"; font.pixelSize:30; font.bold:true; color:"#26364A" }
                                        Text { text:"ليان وسامي ينتظرانك في مغامرة اليوم!"; font.pixelSize:20; color:"#53657A" }
                                        Button { text:"🚀 متابعة التعلم"; font.pixelSize:18; onClicked: root.openLevel(0) }
                                    }
                                    Text { text:"👧\n✨\n👦"; font.pixelSize:58; horizontalAlignment:Text.AlignHCenter }
                                }
                            }
                            Text { text:"مهمتك اليوم"; font.pixelSize:24; font.bold:true; color:"#27364B" }
                            RowLayout {
                                Layout.fillWidth:true; spacing:14
                                Repeater { model: appBackend.todayTasks()
                                    delegate: Rectangle { Layout.fillWidth:true; Layout.preferredHeight:125; radius:24; color:"#FFFFFF"; border.color:"#E6EAF1"
                                        ColumnLayout { anchors.centerIn:parent; Text { text:modelData.icon; font.pixelSize:34; Layout.alignment:Qt.AlignHCenter } Text { text:modelData.title; font.pixelSize:17; font.bold:true; Layout.alignment:Qt.AlignHCenter } }
                                    }
                                }
                            }
                            Text { text:"رحلتك التعليمية"; font.pixelSize:24; font.bold:true; color:"#27364B" }
                            Rectangle { Layout.fillWidth:true; Layout.preferredHeight:150; radius:28; color:"#FFFFFF"; border.color:"#E6EAF1"
                                RowLayout { anchors.fill:parent; anchors.margins:22
                                    Text { text:"🏠"; font.pixelSize:38 }
                                    Text { text:"→"; font.pixelSize:30; color:"#9AA7B7" }
                                    Text { text:"🔤"; font.pixelSize:38 }
                                    Text { text:"→"; font.pixelSize:30; color:"#9AA7B7" }
                                    Text { text:"📚"; font.pixelSize:38 }
                                    Text { text:"→"; font.pixelSize:30; color:"#9AA7B7" }
                                    Text { text:"🏆"; font.pixelSize:38 }
                                    Item { Layout.fillWidth:true }
                                    Button { text:"🗺️ فتح الرحلة"; onClicked:page="journey" }
                                }
                            }
                            Text { text:"تعلم العربية والإنجليزية"; font.pixelSize:24; font.bold:true; color:"#27364B" }
                            RowLayout { Layout.fillWidth:true; spacing:14
                                Button { Layout.fillWidth:true; Layout.preferredHeight:70; text:"🇸🇦  العربية"; font.pixelSize:19; onClicked:root.openLevel(0) }
                                Button { Layout.fillWidth:true; Layout.preferredHeight:70; text:"🇬🇧  English"; font.pixelSize:19; onClicked:root.openLevel(0) }
                            }
                        }
                    }
                }

                Item {
                    ScrollView { anchors.fill:parent
                        GridLayout { columns: root.width>1100 ? 4 : 3; width: root.width-60; anchors.horizontalCenter:parent.horizontalCenter; anchors.margins:20; columnSpacing:16; rowSpacing:16
                            Text { Layout.columnSpan:4; text:"🗺️ رحلتك التعليمية"; font.pixelSize:30; font.bold:true; color:"#27364B" }
                            Text { Layout.columnSpan:4; text:"افتح المستوى وتعلم خطوة بخطوة. كل درس يحفظ تقدمك."; font.pixelSize:17; color:"#65758A" }
                            Repeater { model: levelRows
                                delegate: Rectangle { Layout.fillWidth:true; Layout.preferredHeight:150; radius:26; color:"#FFFFFF"; border.color:"#E3E9F1"
                                    ColumnLayout { anchors.fill:parent; anchors.margins:18
                                        Text { text:"⭐ المستوى " + modelData.level; font.pixelSize:22; font.bold:true; color:"#2A3C54" }
                                        Text { text:modelData.level===0 ? "البداية" : "مرحلة جديدة من المغامرة"; color:"#69798D" }
                                        Text { text:"🇸🇦 " + modelData.ar + " درس   🇬🇧 " + modelData.en + " درس"; color:"#53657A" }
                                        Button { text:"دخول المستوى"; onClicked:root.openLevel(modelData.level) }
                                    }
                                }
                            }
                        }
                    }
                }

                Item {
                    ScrollView { anchors.fill:parent
                        ColumnLayout { width:root.width-60; anchors.horizontalCenter:parent.horizontalCenter; spacing:14
                            Text { text:"📚 دروس المستوى " + selectedLevel; font.pixelSize:30; font.bold:true; color:"#27364B" }
                            Repeater { model:lessonRows
                                delegate: Rectangle { Layout.fillWidth:true; Layout.preferredHeight:100; radius:22; color:"#FFFFFF"; border.color:"#E3E9F1"
                                    RowLayout { anchors.fill:parent; anchors.margins:18
                                        Text { text:modelData.language==="ar" ? "🇸🇦" : "🇬🇧"; font.pixelSize:28 }
                                        ColumnLayout { Layout.fillWidth:true
                                            Text { text:modelData.title; font.pixelSize:19; font.bold:true }
                                            Text { text:modelData.skill; color:"#68788B" }
                                        }
                                        Text { text:modelData.done ? "✅ مكتمل" : "▶️ ابدأ"; color:modelData.done ? "#1D8A57" : "#3D6CE7"; font.bold:true }
                                        Button { text:"فتح"; onClicked:root.openLesson(modelData.id) }
                                    }
                                }
                            }
                        }
                    }
                }

                Item {
                    ScrollView { anchors.fill:parent
                        ColumnLayout { width:root.width-60; anchors.horizontalCenter:parent.horizontalCenter; spacing:18
                            Text { text:"🎓 " + (selectedLesson.title || "الدرس"); font.pixelSize:30; font.bold:true; color:"#27364B" }
                            Rectangle { Layout.fillWidth:true; radius:28; color:"#FFFFFF"; border.color:"#E3E9F1"; Layout.preferredHeight:220
                                ColumnLayout { anchors.fill:parent; anchors.margins:25; spacing:12
                                    Text { text:selectedLesson.language==="ar" ? "🇸🇦 العربية" : "🇬🇧 الإنجليزية"; font.pixelSize:18; color:"#64748B" }
                                    Text { text:selectedLesson.skill || ""; font.pixelSize:22; font.bold:true }
                                    Text { text:selectedLesson.body || "هيا نتعلم مع ليان وسامي!"; wrapMode:Text.WordWrap; Layout.fillWidth:true; font.pixelSize:19; color:"#4B5C70" }
                                    Item { Layout.fillHeight:true }
                                    Button { text:"🔊 استمع"; Layout.preferredHeight:52 }
                                }
                            }
                            Text { text:"🧩 كلمات الدرس"; font.pixelSize:24; font.bold:true }
                            RowLayout { Layout.fillWidth:true
                                Repeater { model:selectedLesson.words || []
                                    delegate: Rectangle { Layout.fillWidth:true; Layout.preferredHeight:100; radius:20; color:"#F0F8FF"
                                        ColumnLayout { anchors.centerIn:parent; Text { text:modelData.text; font.pixelSize:25; font.bold:true; Layout.alignment:Qt.AlignHCenter } Text { text:modelData.meaning; color:"#617185"; Layout.alignment:Qt.AlignHCenter } }
                                    }
                                }
                            }
                            Button { text:"⭐ أنهيت الدرس"; Layout.preferredHeight:58; font.pixelSize:19; onClicked:{ appBackend.completeLesson(selectedLesson.id,100); page="progress" } }
                        }
                    }
                }

                Item {
                    ScrollView { anchors.fill:parent
                        ColumnLayout { width:root.width-60; anchors.horizontalCenter:parent.horizontalCenter; spacing:18
                            Text { text:"🎮 العب وتعلم"; font.pixelSize:30; font.bold:true }
                            Text { text:"ألعاب مرتبطة بما تتعلمه حتى يصبح التدريب ممتعاً."; font.pixelSize:17; color:"#65758A" }
                            Repeater { model:[["🧠","ذاكرة الكلمات"],["🔤","صيد الحروف"],["🎧","اسمع واختر"],["🧩","ركّب الكلمة"],["🗣️","تحدث مع سامي"],["🏃","سباق المعرفة"]]
                                delegate: Rectangle { Layout.fillWidth:true; Layout.preferredHeight:95; radius:22; color:"#FFFFFF"; border.color:"#E3E9F1"
                                    RowLayout { anchors.fill:parent; anchors.margins:20; Text { text:modelData[0]; font.pixelSize:35 } Text { text:modelData[1]; font.pixelSize:20; font.bold:true; Layout.fillWidth:true } Button { text:"ابدأ" } }
                                }
                            }
                        }
                    }
                }

                Item {
                    ScrollView { anchors.fill:parent
                        ColumnLayout { width:root.width-60; anchors.horizontalCenter:parent.horizontalCenter; spacing:15
                            Text { text:"📖 القصص التفاعلية"; font.pixelSize:30; font.bold:true }
                            Repeater { model:storyRows
                                delegate: Rectangle { Layout.fillWidth:true; Layout.preferredHeight:110; radius:22; color:"#FFFFFF"; border.color:"#E3E9F1"
                                    RowLayout { anchors.fill:parent; anchors.margins:18; Text { text:"📚"; font.pixelSize:32 } ColumnLayout { Layout.fillWidth:true; Text { text:modelData.title; font.pixelSize:19; font.bold:true } Text { text:"المستوى " + modelData.level; color:"#69798D" } } Button { text:"اقرأ" } }
                                }
                            }
                        }
                    }
                }

                Item {
                    ColumnLayout { anchors.centerIn:parent; spacing:20
                        Text { text:"📊 تقدمي"; font.pixelSize:32; font.bold:true }
                        Text { text:"أنجزت " + appBackend.completedLessons + " درساً"; font.pixelSize:21 }
                        Text { text:"أتقنت " + appBackend.masteredLessons + " درساً"; font.pixelSize:21 }
                        Text { text:"⭐ " + appBackend.xp + " نقطة"; font.pixelSize:21 }
                        Text { text:"🔥 " + appBackend.streak + " يوم متتالٍ"; font.pixelSize:21 }
                    }
                }

                Item {
                    ColumnLayout { anchors.centerIn:parent; spacing:16
                        Text { text:"👨‍👩‍👧 لوحة ولي الأمر"; font.pixelSize:32; font.bold:true }
                        Text { text:"هذه المنطقة مخصصة لمتابعة الطفل وإدارة تجربته."; font.pixelSize:18; color:"#65758A" }
                        Button { text:"تحديث التقرير"; onClicked:{} }
                        Text { text:"الدروس المكتملة: " + appBackend.completedLessons; font.pixelSize:20 }
                        Text { text:"الدروس المتقنة: " + appBackend.masteredLessons; font.pixelSize:20 }
                    }
                }

                Item {
                    ColumnLayout { anchors.centerIn:parent; spacing:18
                        Text { text:"⚙️ الإعدادات"; font.pixelSize:32; font.bold:true }
                        Text { text:"لغتي يعمل دون إنترنت في النواة، ويمكن إضافة المزامنة عند توفر الاتصال."; font.pixelSize:18; color:"#65758A"; wrapMode:Text.WordWrap; Layout.maximumWidth:600 }
                        Button { text:"🏠 العودة للرئيسية"; onClicked:page="home" }
                    }
                }
            }

            Rectangle {
                Layout.fillWidth:true; Layout.preferredHeight:76; color:"#FFFFFF"; border.color:"#E8ECF3"
                RowLayout { anchors.fill:parent; anchors.margins:8; spacing:8
                    Repeater { model:[["🏠","الرئيسية","home"],["🗺️","الرحلة","journey"],["🎮","الألعاب","games"],["📖","القصص","stories"],["📊","تقدمي","progress"],["👨‍👩‍👧","الوالدان","parent"]]
                        delegate:Button { Layout.fillWidth:true; text:modelData[0]+"\n"+modelData[1]; font.pixelSize:15; flat:true; onClicked:root.page=modelData[2] }
                    }
                }
            }
        }
    }
}
