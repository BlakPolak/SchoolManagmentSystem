from flask import Flask, render_template, request, url_for, redirect, session, g, flash
from models.user import User
from models.data import Data
from models.attendance import Attendance
from models.submission import Submission
from flask_jsglue import JSGlue
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
    return render_template("mentor.html", logged_user=g.logged_user)

@app.route("/student")
def student():
    return render_template("student.html", logged_user=g.logged_user)

@app.route("/view_my_attendance")
def view_my_attendance():
    return render_template("view_my_attendance.html", attendance=g.logged_user.check_my_attendance(), logged_user=g.logged_user)

@app.route("/list_assignment")
def list_assignment():
    return render_template("list_assignment.html", assignment_list=g.logged_user.check_my_attendance(),
                           logged_user=g.logged_user)

@app.route("/employee")
def employee():
    return render_template("employee.html", logged_user=g.logged_user)

@app.route("/manager")
def manager():
    return render_template("manager.html", logged_user=g.logged_user)

@app.route("/list_students")
def list_students():
    return render_template("list_students.html", list_of_students=g.logged_user.get_students(), logged_user=g.logged_user)


@app.route("/list_mentors")
def list_mentors():
    return render_template("list_mentors.html", list_of_mentors=g.logged_user.list_mentors(), logged_user=g.logged_user)

@app.route('/edit_mentor')
def edit_mentor():
    print ('I am in edit mentor')

@app.route('/list_students_employee')
def list_students_employee():
    return render_template('list_students_employee.html', list_of_students=g.logged_user.get_students(), logged_user=g.logged_user)

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
