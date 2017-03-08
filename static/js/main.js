function assignTeam(team_name) {
    var student_id = document.getElementById("student_id").value;
    // alert(team_name+student_id);
    window.location = Flask.url_for("assign_student_to_team", {"student_id": student_id, "team_name": team_name});
    return false
}


// function ShowStudentStatistics() {
//     var date_from = document.getElementById("date_from");
//     var date_to = document.getElementById("date_to");
//     if (date_from && date_to) {
//         window.location = Flask.url_for("view_student_statistics", {"date_from": date_from, "date_to": date_to})
//     }
//     return false
// }

function showConfirm() {
    if (confirm("Are you sure") == false) {
        window.location=Flask.url_for("list_students");
        return false
    }
    else{
    }
}
//
// function checkSubmit(e) {
//    if(e && e.keyCode == 13) {
//       window.location="main.html";
//        // document.forms[0].submit();
//    }
// }
//
// function markAttendance1() {
//     var src_str = document.getElementById("attendanceIcon1").src;
//     if (src_str.endsWith("green.png")) {
//         document.getElementById("attendanceIcon1").src = "img/yellow.png";
//
//     }
//     else if (src_str.endsWith("yellow.png")) {
//         document.getElementById("attendanceIcon1").src = "img/red.png";
//     }
//     else if (src_str.endsWith("red.png")) {
//         document.getElementById("attendanceIcon1").src = "img/green.png";
//     }
//
//     var radioObj = document.radio1.present;
//     for (var i = 0; i < radioObj.length; i++) {
//         if (radioObj[i].value == "late" && src_str.endsWith("green.png")) {
//             radioObj[i].checked = true;
//         }
//         else if (radioObj[i].value == "absent" && src_str.endsWith("yellow.png")) {
//             radioObj[i].checked = true;
//         }
//         else if (radioObj[i].value == "present" && src_str.endsWith("red.png")) {
//             radioObj[i].checked = true;
//         }
//     }
// }
// function markAttendance2() {
//
//     var src_str = document.getElementById("attendanceIcon2").src;
//     if (src_str.endsWith("green.png")) {
//         document.getElementById("attendanceIcon2").src="img/yellow.png";
//     }
//     else if (src_str.endsWith("yellow.png")) {
//         document.getElementById("attendanceIcon2").src = "img/red.png";
//     }
//     else if (src_str.endsWith("red.png")) {
//         document.getElementById("attendanceIcon2").src = "img/green.png";
//     }
//
//     var radioObj = document.radio2.present;
//     for (var i = 0; i < radioObj.length; i++) {
//         if (radioObj[i].value == "late" && src_str.endsWith("green.png")) {
//             radioObj[i].checked = true;
//         }
//         else if (radioObj[i].value == "absent" && src_str.endsWith("yellow.png")) {
//             radioObj[i].checked = true;
//         }
//         else if (radioObj[i].value == "present" && src_str.endsWith("red.png")) {
//             radioObj[i].checked = true;
//         }
//     }
// }
//
// function markCheckpoint1() {
//
//     var src_str = document.getElementById("checkpointIcon1").src;
//     if (src_str.endsWith("green.png")) {
//         document.getElementById("checkpointIcon1").src="img/yellow.png";
//     }
//     else if (src_str.endsWith("yellow.png")) {
//         document.getElementById("checkpointIcon1").src = "img/red.png";
//     }
//     else if (src_str.endsWith("red.png")) {
//         document.getElementById("checkpointIcon1").src = "img/green.png";
//     }
//     var radioObj = document.radio1.card;
//     for (var i = 0; i < radioObj.length; i++) {
//         if (radioObj[i].value == "yellow" && src_str.endsWith("green.png")) {
//             radioObj[i].checked = true;
//         }
//         else if (radioObj[i].value == "red" && src_str.endsWith("yellow.png")) {
//             radioObj[i].checked = true;
//         }
//         else if (radioObj[i].value == "green" && src_str.endsWith("red.png")) {
//             radioObj[i].checked = true;
//         }
//     }
// }
//
// function markCheckpoint2() {
//
//     var src_str = document.getElementById("checkpointIcon2").src;
//     if (src_str.endsWith("green.png")) {
//         document.getElementById("checkpointIcon2").src="img/yellow.png";
//     }
//     else if (src_str.endsWith("yellow.png")) {
//         document.getElementById("checkpointIcon2").src = "img/red.png";
//     }
//     else if (src_str.endsWith("red.png")) {
//         document.getElementById("checkpointIcon2").src = "img/green.png";
//     }
//     var radioObj = document.radio2.card;
//     for (var i = 0; i < radioObj.length; i++) {
//         if (radioObj[i].value == "yellow" && src_str.endsWith("green.png")) {
//             radioObj[i].checked = true;
//         }
//         else if (radioObj[i].value == "red" && src_str.endsWith("yellow.png")) {
//             radioObj[i].checked = true;
//         }
//         else if (radioObj[i].value == "green" && src_str.endsWith("red.png")) {
//             radioObj[i].checked = true;
//         }
//     }
// }
//
// function gradeSubmission() {
//     var person = prompt("Enter grade: ", "");
//     if (person != null) {
//         document.getElementById("graded").innerText = "Assignment graded: " + person;
//     }
// }
//
// function addToTeam(val) {
//     document.getElementById("added_to_team").innerText = "Student [name, surname] added to: " + val;
//     }