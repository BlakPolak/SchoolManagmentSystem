from flask import Flask, render_template, request, url_for, redirect, session, g, flash
from models.user import *
from flask_jsglue import JSGlue
# from models.user import User
from flask_sqlalchemy import SQLAlchemy

import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.getcwd() + '/db/program.db'
db = SQLAlchemy(app)
app.secret_key = os.urandom(24)
jsglue = JSGlue(app)


@app.before_request
def before_request():
    """ Check if session for user is still up, assign current user object to global g
    """
    setattr(g, 'logged_user', None)
    if "login" in session:
        g.logged_user = app.config.logged_user


@app.route("/")
@app.route("/index")
def index():
    """ App root. Depending on type of user routes him for expected view
    """
    if g.logged_user is not None:
        if g.logged_user.user_type == "student":
            return redirect(url_for("student"))
        elif g.logged_user.user_type == "employee":
            return redirect(url_for("employee"))
        if g.logged_user.user_type == "mentor":
            return redirect(url_for("mentor"))
        else:
            return redirect(url_for("manager"))
    else:
        return redirect(url_for("login"))


@app.route("/mentor")
def mentor():
    """Show menu for mentor user"""
    return render_template("mentor.html")


@app.route("/student")
def student():
    """Show menu for student user"""
    return render_template("student.html", logged_user=g.logged_user)


@app.route("/view_my_grades")
def view_my_grades():
    """Show grades for logged student"""
    return render_template("view_my_grades.html", student_grades=g.logged_user.view_my_grades(), logged_user=g.logged_user)


@app.route("/view_my_attendance")
def view_my_attendance():
    """ Show percent attendance for logged student"""
    return render_template("view_my_attendance.html", attendance=g.logged_user.check_my_attendance(), logged_user=g.logged_user)


@app.route("/list_assignment")
def list_assignment():
    """Shows list of individual assignment stored in the database"""
    return render_template("list_assignment.html", assignment_list=g.logged_user.list_assignments_to_submit(), logged_user=g.logged_user)


@app.route("/list_group_assignment")
def list_group_assignment():
    """Shows list of group assignment stored in the database"""
    return render_template("list_group_assignment.html", group_assignment=g.logged_user.list_group_assignment(), logged_user=g.logged_user)


@app.route("/submit_assignment/<assignment_id>", methods=["POST", "GET"])
def submit_assignment(assignment_id):
    """Student provide result for submission"""
    assignment = Assignment.get_assignment_by_id(g.logged_user, assignment_id)
    if request.method == "POST":
        result = request.form["result"]
        id_assignment = assignment.id
        g.logged_user.submit_assignment(result, id_assignment)
        return redirect(url_for("list_assignment"))
    return render_template("submit_assignment.html", assignment=assignment)


@app.route("/submit_group_assignment/<assignment_id>", methods=["POST", "GET"])
def submit_group_assignment(assignment_id):
    """Student provide result for group submission"""
    assignment = Assignment.get_assignment_by_id(g.logged_user, assignment_id)
    if request.method == "POST":
        result = request.form["result"]
        id_assignment = assignment_id
        g.logged_user.add_group_assignment(id_assignment, result)
        return redirect(url_for("list_group_assignment"))
    return render_template("submit_group_assignment.html", group_assignment=g.logged_user.list_group_assignment(),
                           logged_user=g.logged_user, assignment=assignment)


@app.route("/employee")
def employee():
    """Show menu for employee user"""
    return render_template("employee.html", logged_user=g.logged_user)


@app.route("/manager")
def manager():
    """Show menu for manager user"""
    return render_template("manager.html", logged_user=g.logged_user)


@app.route("/list_students")
def list_students():
    """Shows list of students stored in the database"""
    return render_template("list_students_mentor.html", list_of_students=g.logged_user.get_students())


@app.route("/add_new_student", methods=["POST", "GET"])
def add_new_student():
    """Create new student"""
    if request.method == "POST":
        name = request.form["name"]
        surname = request.form["surname"]
        gender = request.form["gender"]
        birthdate = request.form["birthdate"]
        email = request.form["email"]
        login = request.form["login"]
        password = request.form["password"]
        new_student = g.logged_user.add_student(name, surname, gender, birthdate, email, login, password)
        flash("Student was added: " + new_student.name + " " + new_student.surname, "alert alert-success text-centered")
        return redirect(url_for("list_students"))
    return render_template("add_new_student.html")


@app.route("/edit_student", methods=["POST", "GET"])
def edit_student():
    """ Edit selected student data """
    if request.method == "POST":
        student_id = request.form["student_id"]
        name = request.form["name"]
        surname = request.form["surname"]
        gender = request.form["gender"]
        birthdate = request.form["birthdate"]
        email = request.form["email"]
        login = request.form["login"]
        password = request.form["password"]
        student = g.logged_user.update_student(student_id, name, surname, gender, birthdate, email, login, password)
        flash("Student data was updated: "+student.name+" "+student.surname, "alert alert-success text-centered")
        return redirect(url_for("list_students"))
    student_id = request.args["student_id"]
    student = g.logged_user.get_student(student_id)
    return render_template("edit_student.html", student=student)


@app.route("/remove_student")
def remove_student():
    """ Remove selected by id student from database """
    student_id = request.args["student_id"]
    g.logged_user.remove_student(student_id)
    flash("Student was removed", "alert alert-success text-centered")
    return redirect("list_students")


@app.route("/check_students_attendance", methods=["POST", "GET"])
def check_students_attendance():
    """ Checks students attendance i stored it in database """
    if request.method == "POST":
        attendance_list = []
        for key, value in request.form.items():
            attendance_list.append([key, value])
        zm = g.logged_user.save_attendance(attendance_list)
        if not zm:
            flash("You've checked attendance today!", "alert alert-danger text-centered")
        else:
            flash("Attendance done!", "alert alert-success text-centered")
    return render_template("check_students_attendance.html", list_of_students=g.logged_user.get_students())


@app.route("/add_to_team")
def add_to_team():
    """ Add selected student to team """
    student_id = request.args["student_id"]
    return redirect(url_for("teams_for_student", student_id=student_id))


@app.route("/teams_for_student")
def teams_for_student():
    """ Shows teams names from stored in database"""
    student_id = request.args["student_id"]
    list_of_teams = g.logged_user.get_teams_for_student()
    return render_template("team_names.html", list_of_teams=list_of_teams, student_id=student_id)


@app.route("/assign_student_to_team")
def assign_student_to_team():
    """ Assign selected by id student to team """
    student_id = request.args["student_id"]
    team_name = request.args["team_name"]
    g.logged_user.add_to_team(student_id, team_name)
    return redirect(url_for("list_students"))


@app.route("/add_new_team", methods=["POST", "GET"])
def add_new_team():
    """ Add new team name to database """
    if request.method == "POST":
        new_team = request.form["name"]
        g.logged_user.add_team(new_team)
        flash("Team was added", "alert alert-success text-centered")
        return redirect(url_for("list_teams"))
    return render_template("add_new_team.html")


@app.route("/remove_team")
def remove_team():
    """ Remove selected by id team from database """
    team_name = request.args["team_name"]
    g.logged_user.remove_team(team_name)
    flash("Team was removed", "alert alert-success text-centered")
    return redirect(url_for("list_teams"))


@app.route("/list_submissions")
def list_submissions():
    """ List all submissions from database """
    list_of_submissions = g.logged_user.get_submissions_to_grade()
    return render_template("list_submissions.html", list_of_submissions=list_of_submissions)


@app.route("/grade_submission", methods=["POST", "GET"])
def grade_submission():
    """ Grade selected submissions and stored data to database """
    if request.method == "POST":
        grade = request.form["grade"]
        submission_id = request.form["submission_id"]
        g.logged_user.grade_submission(submission_id, grade)
        flash("Submission was graded", "alert alert-success text-centered")
        return redirect(url_for("list_submissions"))
    submission_id = request.args["submission_id"]
    submission = g.logged_user.get_submission(submission_id)
    assignment = g.logged_user.get_assignment(submission.id_assignment)
    return render_template("grade_submission.html", submission=submission, assignment=assignment)


@app.route("/list_checkpoints")
def list_checkpoints():
    """ List all checkpoint assignment from database """
    checkpoints = g.logged_user.get_checkpoints_for_submission()
    return render_template("list_checkpoints_for_submission.html", checkpoints=checkpoints)


@app.route("/grade_checkpoint", methods=["GET", "POST"])
def grade_checkpoint():
    """ Grade checkpoint submissions """
    if request.method == "POST":
        submission_id = request.form['submission_id']
        card = request.form['card']
        g.logged_user.grade_checkpoint_submission(submission_id, card)
        flash("Checkpoint submissions were graded", "alert alert-success text-centered")
        return redirect(url_for("list_checkpoints"))
    checkpoint_submission_id = request.args["checkpoint_submission_id"]
    submission = g.logged_user.get_student_checkpoint_submission(checkpoint_submission_id)
    return render_template("grade_checkpoint_submissions.html", submission=submission)


@app.route("/view_student_details")
def view_student_details():
    """ List all personal data about student from database """
    student = g.logged_user.get_student(request.args["id"])
    return render_template("view_student_details.html", logged_user=g.logged_user, student=student)


@app.route("/view_student_statistics", methods=["POST", "GET"])
def view_student_statistics():
    """ List all statistic data about student from database """
    if request.method == "POST":
        if request.form["date_from"] and request.form["date_to"]:
            student_statistics = g.logged_user.check_student_performance(request.form["student_id"], request.form["date_from"], request.form["date_to"])
            return render_template("view_student_statistics.html",
                                   date_from=request.form["date_from"], date_to=request.form["date_to"],
                                   logged_user=g.logged_user, student_statistics=student_statistics, student_id=request.form["student_id"])
    return render_template("view_student_statistics.html", logged_user=g.logged_user, student_id=request.args["student_id"])


@app.route("/list_teams", methods=["POST", "GET"])
def list_teams():
    """ List all teams from database """
    list_of_teams = g.logged_user.get_teams()
    return render_template("list_teams.html", list_of_teams=list_of_teams)


@app.route("/list_mentors_assignments")
def list_mentors_assignments():
    """ List all assignment from database """
    list_of_assignments = g.logged_user.get_assignments()
    return render_template("list_mentors_assignments.html", list_of_assignments=list_of_assignments)


@app.route("/edit_assignment", methods=["GET", "POST"])
def edit_assignment():
    """ Edit assignment create by mentor user """
    if request.method == "POST":
        assignment_id = request.form["assignment_id"]
        name = request.form["name"]
        type = request.form["type"]
        max_points = request.form["max_points"]
        delivery_date = request.form["date"]
        content = request.form["content"]
        if g.logged_user.update_assignment(assignment_id, name, type, max_points, delivery_date, content):
            flash("Assignment was updated", "alert alert-success text-centered")
        else:
            flash("Error during updating assignment", "alert alert-fail text-centered")
        return redirect(url_for("list_mentors_assignments"))
    assignment_id = request.args["assignment_id"]
    assignment = g.logged_user.get_assignment(assignment_id)
    return render_template("edit_assignment.html", assignment=assignment)


@app.route("/remove_assignment")
def remove_assignment():
    """ Remove assignment from assignment table in database """
    assignment_id = request.args["assignment_id"]
    g.logged_user.remove_assignment(assignment_id)
    flash("Assignment was removed", "alert alert-success text-centered")
    return redirect(url_for("list_mentors_assignments"))


@app.route("/add_new_assignment", methods=["POST", "GET"])
def add_new_assignment():
    """ Add new assignment to database """
    if request.method == "POST":
        name = request.form["name"]
        type = request.form["type"]
        max_points = request.form["max_points"]
        delivery_date = request.form["date"]
        content = request.form["content"]
        if g.logged_user.add_new_assignment(name, type, max_points, delivery_date, content):
            return redirect(url_for("list_mentors_assignments"))
        else:
            flash("Adding assignment has failed", "alert alert-fail text-centered")
    return render_template("add_new_assignment.html")


@app.route("/list_mentors")
def list_mentors():
    """ List all mentors from database """
    return render_template("list_mentors.html", list_of_mentors=g.logged_user.list_mentors(), logged_user=g.logged_user)


@app.route("/list_students_manager")
def list_students_manager():
    """ List all students from database to manager """
    return render_template("list_students_manager.html", list_of_students=g.logged_user.get_students(), logged_user=g.logged_user)


@app.route('/student_statistic_manager/<int:student_id>')
def student_statistic_manager(student_id):
    """ List all students details from database to manager """
    return render_template('student_statistic_manager.html', stats=g.logged_user.full_stats_for_student(student_id), logged_user=g.logged_user)


@app.route('/average_grades_manager/<int:student_id>')
def average_grades_manager(student_id):
    """ List all students statistics from database to manager """
    return render_template('average_grades_manager.html', stats=g.logged_user.full_stats_for_student(student_id), logged_user=g.logged_user)


@app.route('/edit_mentor/<mentor_id>', methods=["POST", "GET"])
def edit_mentor(mentor_id):
    """ Edit mentors data in database """
    if request.method == "POST":
        mentor_to_edit = Mentor.get_mentor_by_id(mentor_id)
        mentor_to_edit.name = request.form["name"]
        mentor_to_edit.surname = request.form["surname"]
        mentor_to_edit.gender = request.form["gender"]
        mentor_to_edit.birth_date = request.form["birthdate"]
        mentor_to_edit.email = request.form["email"]
        mentor_to_edit.login = request.form["login"]
        mentor_to_edit.password = request.form["password"]
        db.session.commit()
        flash("Mentor updated!", "alert alert-success text-centered")
        return redirect(url_for('list_mentors'))
    if request.method == "GET":
        mentor_to_edit = Mentor.get_mentor_by_id(mentor_id)
        return render_template("edit_mentor.html", logged_user=g.logged_user, mentor_id=mentor_id, mentor=mentor_to_edit)


@app.route('/add_new_mentor', methods=["POST", "GET"])
def add_new_mentor():
    """ Add new mentor to database """
    if request.method == "POST":
            name = request.form["name"]
            surname = request.form["surname"]
            gender = request.form["gender"]
            birthdate = request.form["birthdate"]
            email = request.form["email"]
            login = request.form["login"]
            password = request.form["password"]
            g.logged_user.add_mentor(name, surname, gender, birthdate, email, login, password)
            flash("Mentor added!", "alert alert-success text-centered")
            return redirect(url_for("list_mentors"))
    return render_template("add_new_mentor.html")


@app.route("/remove_mentor")
def remove_mentor():
    """ Remove selected by id mentor from database """
    mentor_id = request.args["mentor_id"]
    g.logged_user.remove_mentor(mentor_id)
    flash("Mentor removed!", "alert alert-success text-centered")
    return redirect("list_mentors")


@app.route("/checkpoint_stats_for_mentors")
def checkpoint_stats_for_mentors():
    """ List all mentor statistic about grades and checkpoint cards """
    list_of_statistics = g.logged_user.which_mentor_is_a_monster()
    return render_template("checkpoint_stats_for_mentors.html", list_of_statistics=list_of_statistics)


@app.route("/grade_stats_for_mentors")
def grade_stats_for_mentors():
    """ List grade statistics for selected mentor """
    list_of_statistics = g.logged_user.grades_stats_for_mentors()
    return render_template("grade_stats_for_mentors.html", list_of_statistics=list_of_statistics)


@app.route('/list_students_employee')
def list_students_employee():
    """ List all students from database to employee """
    return render_template('list_students_employee.html', list_of_students=g.logged_user.get_students(), logged_user=g.logged_user)


@app.route('/view_mentors_details')
def view_mentors_details():
    """ Show all mentor details from database to manager """
    mentor = Mentor.get_mentor_by_id(request.args["id"])
    return render_template("view_mentors_details.html", logged_user=g.logged_user, mentor=mentor)


@app.route('/student_details_employee/<student_id>')
def student_details_employee(student_id):
    """ List all students details from database to manager """
    student = Employee.get_student(g.logged_user, student_id)
    return render_template('student_details_employee.html', list_of_students=g.logged_user.get_students(), logged_user=g.logged_user, student=student)


@app.route("/logout")
def logout():
    """ Log out current user
    """
    session.pop("username", None)
    flash("Logged out successfully", "alert alert-success text-centered")
    return redirect(url_for("login"))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Shows login form if method was GET. Log user if method was POST.
    """
    if request.method == "POST":
        logged_user = User.get_user(request.form["username"], request.form["password"])
        if logged_user:
            session["login"] = logged_user.login
            session["type"] = logged_user.user_type
            app.config.logged_user = logged_user
            flash('You were successfully logged in', "alert alert-success text-centered")
            return redirect(url_for("index"))
        else:
            flash("Your login data was incorrect", "alert alert-danger text-centered")
    return render_template("login.html")


@app.errorhandler(404)
def page_not_found(error):
    """ Basic 404 error handle. Redirect to login page.
    """
    flash("Invalid address: "+str(error), "alert alert-danger text-centered")
    return render_template("login.html")



if __name__ == "__main__":
    app.run(debug=True)
