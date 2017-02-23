
function showConfirm() {
    if (confirm("Are you sure") == false) {
        window.location="list_students.html";
    }
    // else{
    //     window.location="remove_student.html";
    // }
}

function checkSubmit(e) {
   if(e && e.keyCode == 13) {
      window.location="main.html";
       // document.forms[0].submit();
   }
}

function markAttendance1() {

    var src_str = document.getElementById("attendanceIcon1").src;
    if (src_str.endsWith("green.png")) {
        document.getElementById("attendanceIcon1").src="img/yellow.png";
    }
    else if (src_str.endsWith("yellow.png")) {
        document.getElementById("attendanceIcon1").src = "img/red.png";
    }
    else if (src_str.endsWith("red.png")) {
        document.getElementById("attendanceIcon1").src = "img/green.png";
    }
}

function markAttendance2() {

    var src_str = document.getElementById("attendanceIcon2").src;
    if (src_str.endsWith("green.png")) {
        document.getElementById("attendanceIcon2").src="img/yellow.png";
    }
    else if (src_str.endsWith("yellow.png")) {
        document.getElementById("attendanceIcon2").src = "img/red.png";
    }
    else if (src_str.endsWith("red.png")) {
        document.getElementById("attendanceIcon2").src = "img/green.png";
    }
}

function markCheckpoint1() {

    var src_str = document.getElementById("checkpointIcon1").src;
    if (src_str.endsWith("green.png")) {
        document.getElementById("checkpointIcon1").src="img/yellow.png";
    }
    else if (src_str.endsWith("yellow.png")) {
        document.getElementById("checkpointIcon1").src = "img/red.png";
    }
    else if (src_str.endsWith("red.png")) {
        document.getElementById("checkpointIcon1").src = "img/green.png";
    }
}

function markCheckpoint2() {

    var src_str = document.getElementById("checkpointIcon2").src;
    if (src_str.endsWith("green.png")) {
        document.getElementById("checkpointIcon2").src="img/yellow.png";
    }
    else if (src_str.endsWith("yellow.png")) {
        document.getElementById("checkpointIcon2").src = "img/red.png";
    }
    else if (src_str.endsWith("red.png")) {
        document.getElementById("checkpointIcon2").src = "img/green.png";
    }
}

function gradeSubmission() {
    var person = prompt("Enter grade: ", "");
    if (person != null) {
        document.getElementById("graded").innerText = "Assignment graded: " + person;
    }
}

function addToTeam(val) {
    document.getElementById("added_to_team").innerText = "Student [name, surname] added to: " + val;
    }