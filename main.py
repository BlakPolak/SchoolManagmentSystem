from flask import Flask, render_template, request, url_for, redirect, session, g, flash
from models.user import *
from flask_jsglue import JSGlue
from models.user import User
from models.data import Data
from models.attendance import Attendance
from models.submission import Submission
import os

app = Flask(__name__)
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
    return render_template("mentor.html")


@app.route("/student")
def student():
    return render_template("student.html", logged_user=g.logged_user)


@app.route("/view_my_grades")
def view_my_grades():
    return render_template("view_my_grades.html", student_grades=g.logged_user.view_my_grades(), logged_user=g.logged_user)


@app.route("/view_my_attendance")
def view_my_attendance():
    return render_template("view_my_attendance.html", attendance=g.logged_user.check_my_attendance(), logged_user=g.logged_user)


@app.route("/list_assignment")
def list_assignment():
    return render_template("list_assignment.html", assignment_list=g.logged_user.list_assignments_to_submit(),
                           logged_user=g.logged_user)

@app.route("/employee")
def employee():
    return render_template("employee.html", logged_user=g.logged_user)

@app.route("/manager")
def manager():
    return render_template("manager.html", logged_user=g.logged_user)

@app.route("/list_students")
def list_students():
    return render_template("list_students.html", list_of_students=g.logged_user.get_students())

@app.route("/add_new_student", methods=["POST", "GET"])
def add_new_student():
    if request.method == "POST":
        name = request.form["name"]
        surname = request.form["surname"]
        gender = request.form["gender"]
        birthdate = request.form["birthdate"]
        email = request.form["email"]
        login = request.form["login"]
        password = request.form["password"]
        g.logged_user.add_student(name, surname, gender, birthdate, email, login, password)
        return redirect(url_for("list_students"))
    return render_template("add_new_student.html")

@app.route("/edit_student", methods=["POST", "GET"])
def edit_student():
    if request.method == "POST":
        student_id = request.form["student_id"]
        name = request.form["name"]
        surname = request.form["surname"]
        gender = request.form["gender"]
        birthdate = request.form["birthdate"]
        email = request.form["email"]
        login = request.form["login"]
        password = request.form["password"]
        g.logged_user.update_student(student_id, name, surname, gender, birthdate, email, login, password)
        return redirect(url_for("list_students"))
    student_id = request.args["student_id"]
    student = g.logged_user.get_student(student_id)
    return render_template("edit_student.html", student=student)

@app.route("/remove_student")
def remove_student():
    student_id = request.args["student_id"]
    g.logged_user.remove_student(student_id)
    return redirect("list_students")

@app.route("/add_to_team")
def add_to_team():
    student_id = request.args["student_id"]
    return redirect(url_for("teams_for_student", student_id=student_id))

@app.route("/teams_for_student")
def teams_for_student():
    student_id = request.args["student_id"]
    list_of_teams = g.logged_user.get_teams()
    return render_template("team_names.html", list_of_teams=list_of_teams, student_id=student_id)

@app.route("/assign_student_to_team")
def assign_student_to_team():
    student_id = request.args["student_id"]
    team_name = request.args["team_name"]
    g.logged_user.add_to_team(student_id, team_name)
    return redirect(url_for("list_students"))

@app.route("/add_new_team", methods=["POST", "GET"])
def add_new_team():
    if request.method == "POST":
        new_team = request.form["name"]
        g.logged_user.add_team(new_team)
        return redirect(url_for("list_teams"))
    return render_template("add_new_team.html")

@app.route("/remove_team")
def remove_team():
    team_name = request.args["team_name"]
    g.logged_user.remove_team(team_name)
    return redirect(url_for("list_teams"))


@app.route("/view_student_details")
def view_student_details():
    student = g.logged_user.get_student(request.args["id"])
    return render_template("view_student_details.html", logged_user=g.logged_user, student=student)

@app.route("/view_student_statistics", methods=["POST", "GET"])
def view_student_statistics():
    if request.method == "POST":
        if request.form["date_from"] and request.form["date_to"]:
            student_statistics = g.logged_user.check_student_performance(request.form["student_id"], request.form["date_from"], request.form["date_to"])
            return render_template("view_student_statistics.html",
                                   date_from=request.form["date_from"], date_to=request.form["date_to"],
                                   logged_user=g.logged_user, student_statistics=student_statistics, student_id=request.form["student_id"])
    return render_template("view_student_statistics.html", logged_user=g.logged_user, student_id=request.args["student_id"])


@app.route("/list_teams", methods=["POST", "GET"])
def list_teams():
    list_of_teams = g.logged_user.get_teams()
    return render_template("list_teams.html", list_of_teams=list_of_teams)


@app.route("/list_mentors")
def list_mentors():
    return render_template("list_mentors.html", list_of_mentors=g.logged_user.list_mentors(), logged_user=g.logged_user)


@app.route("/list_students_manager")
def list_students_manager():
    return render_template("list_students_manager.html", list_of_students=g.logged_user.get_students(), logged_user=g.logged_user)


@app.route('/student_statistic_manager/<int:student_id>')
def student_statistic_manager(student_id):
    return render_template('student_statistic_manager.html', stats=g.logged_user.full_stats_for_students(student_id), logged_user=g.logged_user, student_id=student_id)


@app.route('/average_grades_manager')
def average_grades_manager():
    return render_template('average_grades_manager.html', grades=g.logged_user.average_grade_for_student(), logged_user=g.logged_user)


@app.route('/edit_mentor/<mentor_id>', methods=["POST", "GET"])
def edit_mentor(mentor_id):
    if request.method == "POST":
        new_name = request.form["name"]
        new_surname= request.form["surname"]
        new_gender = request.form["gender"]
        new_birthdate = request.form["birthdate"]
        new_email = request.form["email"]
        new_login = request.form["login"]
        new_password = request.form["password"]

        mentor_to_edit = Mentor.get_mentor_by_id(mentor_id)

        mentor_to_edit.name = new_name
        mentor_to_edit.surname = new_surname
        mentor_to_edit.gender = new_gender
        mentor_to_edit.birth_date = new_birthdate
        mentor_to_edit.email = new_email
        mentor_to_edit.login = new_login
        mentor_to_edit.password = new_password
        mentor_to_edit.edit_mentor()
        return redirect(url_for('list_mentors'))

    if request.method == "GET":
        mentor_to_edit = Mentor.get_mentor_by_id(mentor_id)
        return render_template("edit_mentor.html", logged_user=g.logged_user, mentor_id=mentor_id, mentor=mentor_to_edit)

@app.route('/add_new_mentor', methods=["POST", "GET"])
def add_new_mentor():
    if request.method == "POST":
            name = request.form["name"]
            surname = request.form["surname"]
            gender = request.form["gender"]
            birthdate = request.form["birthdate"]
            email = request.form["email"]
            login = request.form["login"]
            password = request.form["password"]
            g.logged_user.add_mentor(name, surname, gender, birthdate, email, login, password)
            return redirect(url_for("list_mentors"))
    return render_template("add_new_mentor.html")

@app.route("/remove_mentor")
def remove_student():
    mentor_id = request.args["mentor_id"]
    g.logged_user.remove_student(mentor_id)
    return redirect("list_students")

@app.route('/list_students_employee')
def list_students_employee():
    return render_template('list_students_employee.html', list_of_students=g.logged_user.get_students(), logged_user=g.logged_user)


@app.route('/student_details_employee/<student_id>')
def student_details_employee(student_id):
    student = Student.get_mentor_by_id(student_id)
    return render_template('student_details_employee.html', list_of_students=g.logged_user.get_students(), logged_user=g.logged_user)


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
