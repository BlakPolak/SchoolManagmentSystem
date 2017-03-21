import datetime
import sqlite3
from models.student_statistic import StudentStatistic
from models.graded_assignment import gradedAssignment
from models.team import Team
from models.assignment import Assignment
from models.gradeable_submissions import GradeableSubmissions
from models.checkpoints_stats_for_mentors import CheckpointStatsForMentors
from models.grade_stats_for_mentors import GradeStatsForMentors
from models.submission import Submission
from models.checkpoint_assignment import CheckpointAssignment
from models.student_grades import StudentGrades
from models.gradeable_checkpoint_submission import GradeableCheckpointSubmission
from models.db_alchemy import *
from main import db


class User:
    """
        Base class creates user object

        Args:
            name: check_if_correct(name, str)
            surname: check_if_correct(surname, str)
            gender: gender
            birth_date: birth_date
            email:
            login:login
            password: check_if_correct(password, str)
    """

    path = "db/program.db"

    def __init__(self, _id, name, surname, gender, birth_date, email, login, password, user_type):
        """
        Initialize user object

        Args:
            name: check_if_correct(name, str)
            surname: check_if_correct(surname, str)
            gender: gender
            birth_date: birth_date
            email:
            login:login
            password: check_if_correct(password, str)
        """
        self._id = _id
        self.name = name             #self.check_if_correct(name, str)
        self.surname = surname         #self.check_if_correct(surname, str)
        self.gender = gender
        self.birth_date = birth_date
        self.email = email
        self.login = login
        self.password = password  #self.check_if_correct(password, str)
        self.user_type = user_type

    # @classmethod
    # def get_user(cls, login, password):
    #     """ On successful authentication returns User or Manager object
    #         Args:
    #             login (str): login of the user
    #             password (str): password of the user
    #         Returns:
    #             User (obj): if authentication passed
    #             None: if authentication fails
    #     """
    #     conn = sqlite3.connect(User.path)
    #     cursor = conn.execute("SELECT * FROM user")
    #     for row in cursor.fetchall():
    #         if row[6] == login and row[7] == password:
    #             conn.close()
    #             if row[8] == "manager":
    #                 return Manager(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
    #             elif row[8] == "student":
    #                 return Student(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
    #             elif row[8] == "employee":
    #                 return Employee(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
    #             elif row[8] == "mentor":
    #                 return Mentor(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
    #     conn.close()
    #     return None


    @classmethod
    def get_user(cls, login, password):
        """ On successful authentication returns User or Manager object
            Args:
                login (str): login of the user
                password (str): password of the user
            Returns:
                User (obj): if authentication passed
                None: if authentication fails
        """
        user = db.session.query(UserDb).filter_by(login=login, password=password).first()
        if user.user_type == "student":
            return Student(user.id, user.name, user.surname, user.gender, user.birth_date, user.email, user.login,
                           user.password, user.user_type)
        elif user.user_type == "manager":
            return Manager(user.id, user.name, user.surname, user.gender, user.birth_date, user.email, user.login,
                           user.password, user.user_type)
        elif user.user_type == "employee":
            return Employee(user.id, user.name, user.surname, user.gender, user.birth_date, user.email, user.login,
                           user.password, user.user_type)
        elif user.user_type == "mentor":
            return Mentor(user.id, user.name, user.surname, user.gender, user.birth_date, user.email, user.login,
                           user.password, user.user_type)
        else:
            return None


class Employee(User):
    """Class creates object employee"""
    def __init__(self, _id, name, surname, gender, birth_date, email, login, password, user_type):
        """
        Initialize employee object that inherits from User class

        Args:
            name: check_if_correct(name, str)
            surname: check_if_correct(surname, str)
            gender: gender
            birth_date: birth_date
            email:
            login:login
            password: check_if_correct(password, str)
        """
        super().__init__(_id, name, surname, gender, birth_date, email, login, password, user_type)

    def get_students(self):
        """
        Return student list to display

        Returns:
                student list
        """
        students = db.session.query(UserDb).filter_by(user_type="student").all()
        return students

    def get_student(self, id):
        """
        Return student list to display

        Returns:
                student list
        """
        student = db.session.query(UserDb).filter_by(id=id).first()
        return student

    def list_students_simple_view(self):
        """
        Return student list to display

        Returns:
                student list
        """
        student_list = []
        data = sqlite3.connect(User.path)
        cursor = data.cursor()
        cursor.execute("SELECT * FROM `User` WHERE User_type='student'")
        students = cursor.fetchall()
        for student in students:
            student_list.append([student[0], student[1], student[2]])
        data.close()
        return student_list

    def view_student_details(self):
        """
        Returns students details list to display

            Returns:

                student detail list
        """
        student_list = []
        data = sqlite3.connect(User.path)
        cursor = data.cursor()
        cursor.execute("SELECT * FROM `User` WHERE User_type='student'")
        students = cursor.fetchall()
        n = 1
        for student in students:
            student_list.append([str(n) + ".", student[1], student[2], student[3],
                                 student[4], student[5], student[6], student[7]])
            n += 1
        data.close()
        return student_list


class Student(User):
    """Class creates object student"""
    def __init__(self, _id, name, surname, gender, birth_date, email, login, password, user_type):
        """
        Initialize student object that inherits from User class

       Args:
            name: check_if_correct(name, str)
            surname: check_if_correct(surname, str)
            gender: gender
            birth_date: birth_date
            email:
            login:login
            password: check_if_correct(password, str)
        """
        super().__init__(_id, name, surname, gender, birth_date, email, login, password, user_type)
        self.my_submissions_list = []

    def view_my_grades(self):
        """
        Method display list of submitted assignment with grades

        Return:
            table submitted assignment with grades

        """
        data = sqlite3.connect(User.path)
        cursor = data.cursor()
        cursor.execute("SELECT assignment.name, submission.grade FROM assignment INNER JOIN submission "
                       "ON submission.ID_assignment = assignment.ID WHERE ID_Student=?", (self._id, ))
        grades = cursor.fetchall()
        student_all_grades = []
        for row in grades:
            assignment_name = row[0]
            assignment_grade = row[1]
            student_grade = gradedAssignment(assignment_name, assignment_grade)
            student_all_grades.append(student_grade)
        data.close()
        return student_all_grades

    def list_assignments_to_submit(self):
        """
        Method returns list of all student submission

        Return:
            list not submitted assignment

        """
        data = sqlite3.connect(User.path)
        cursor = data.cursor()
        cursor.execute("select * from assignment where ID not in "
                       "(select id_assignment from submission where id_student=?) AND type='individual';", (self._id,))
        assignments = cursor.fetchall()
        assignments_to_submit = []
        for row in assignments:
            assignment_id = row[0]
            assignment_name = row[1]
            assignment_type = row[2]
            assignment_max_points = row[3]
            assignment_delivery_date = row[4]
            assignment_content = row[5]
            assignment = Assignment(assignment_id, assignment_name, assignment_type, assignment_max_points, assignment_delivery_date, assignment_content)
            assignments_to_submit.append(assignment)
        data.close()
        return assignments_to_submit

    def submit_assignment(self, result, id_assignment):
        """
        Method allows student to submit assignment

        Args:
            assignment, result

        """
        data = sqlite3.connect(User.path)
        cursor = data.cursor()
        submission_date = datetime.date.today()
        id_student = self._id
        cursor.execute("INSERT INTO `Submission` (`ID_Student`, `ID_Assignment`,`Result`, `Submittion_date`) "
                       "VALUES (?, ?, ?, ?)", (id_student, id_assignment, result, submission_date))
        data.commit()
        data.close()

    def list_group_assignment(self):
        """
        Method returns list of all group submission

        Return:
            list assignment for group

        """
        data = sqlite3.connect(User.path)
        cursor = data.cursor()
        cursor.execute("select * from assignment where ID not in "
                       "(select id_assignment from submission where id_student=?) And type='group';", (self._id,))
        assignments = cursor.fetchall()
        group_assignments_to_submit = []
        for row in assignments:
            assignment_id = row[0]
            assignment_name = row[1]
            assignment_type = row[2]
            assignment_max_points = row[3]
            assignment_delivery_date = row[4]
            assignment_content = row[5]
            assignment = Assignment(assignment_id, assignment_name, assignment_type, assignment_max_points,
                                    assignment_delivery_date, assignment_content)
            group_assignments_to_submit.append(assignment)
        data.close()
        return group_assignments_to_submit

    def find_student_team(self):
        """
        Method returns team name for logged student

        Return:
            team name as list

        """
        data = sqlite3.connect(User.path)
        cursor = data.cursor()
        cursor.execute("SELECT `Team_Name` FROM `Teams` WHERE ID_Student=?", (self._id,))
        teams = cursor.fetchall()
        data.commit()
        data.close()
        team = teams[0][0]
        return team

    def find_students_teammates(self):
        """
        Method returns all students from the same team

        Return:
            list student teammates.py

        """
        data = sqlite3.connect(User.path)
        cursor = data.cursor()
        cursor.execute("SELECT Id_Student FROM `Teams` WHERE Team_name=?", (self.find_student_team(),))
        teammates = cursor.fetchall()
        teammates_list = []
        for mate in teammates:
            teammates_list.append(mate[0])
        data.commit()
        data.close()
        return teammates_list

    def add_group_assignment(self, id_assignment, result):
        """
        Method allows student to submit assignment for each team member

        Args:
            teammates.py, group_submission

        """
        data = sqlite3.connect(User.path)
        cursor = data.cursor()
        submission_date = datetime.date.today()
        for teammate in self.find_students_teammates():
            cursor.execute("INSERT INTO `Submission` (`ID_Student`, `ID_Assignment`,`Result`, `Submittion_date`) "
                           "VALUES (?, ?, ?, ?)", (teammate, id_assignment, result, submission_date))
        data.commit()
        data.close()

    def check_my_attendance(self):
        """
        Method allows student to check attendance level in %

        Return:
            percent of attendance

        """
        student_id = self._id
        data = sqlite3.connect(User.path)
        cursor = data.cursor()
        cursor.execute("SELECT COUNT(Presence) FROM `Attendance` WHERE ID_Student=?"
                       "AND `Presence`= 0", (student_id,))
        presence = cursor.fetchall()
        number_of_presence = float(presence[0][0])
        cursor.execute("SELECT COUNT(Presence) FROM `Attendance`")
        number_of_days = cursor.fetchall()
        days = float(number_of_days[0][0])
        attendance_in_percent = (number_of_presence / days) * 100
        data.commit()
        data.close()
        return round(attendance_in_percent)


class Mentor(Employee):
    """Class creates object mentor"""
    def __init__(self, _id, name, surname, gender, birth_date, email, login, password, user_type):
        """
        Initialize mentor object that inherits from User class

        Args:
            name: check_if_correct(name, str)
            surname: check_if_correct(surname, str)
            check_gender: gender
            gender: gender
            date_validate: birth_date
            birth_date: birth_date
            email:
            login:login
            password: check_if_correct(password, str)
        """
        super().__init__(_id, name, surname, gender, birth_date, email, login, password, user_type)

    def add_student(self, name, surname, gender, birthdate, email, login, password):
        """
        Method allows mentor to add student to students list

        Args:
            name, surname, gender, birthdate, email, login, password
        Return:
             UserDB object
        """
        new_student = UserDb(name=name, surname=surname, gender=gender, birth_date=birthdate,
                                email=email, login=login, password=password, user_type="student")
        db.session.add(new_student)
        db.session.commit()
        return new_student

    def remove_student(self, student_id):
        """
        Method allows mentor remove students from students list

        Args:
            student id
        Return:
             None
        """

        user = db.session.query(UserDb).filter_by(id=student_id).first()
        db.session.delete(user)
        db.session.commit()

    def save_attendance(self, attendance_list):
        """
        Method allows mentor to save checked attendance

        Args:
            attendance list
        Return:
            True if attendance checked first time today
            False if attendance already checked today
        """
        data = sqlite3.connect(User.path)
        for index, item in enumerate(attendance_list):
            if item[1] == "present":
                attendance_list[index][1] = 1
            elif item[1] == "absent":
                attendance_list[index][1] = 0
            else:
                attendance_list[index][1] = 2
        cursor = data.cursor()
        cursor.execute("select * from Attendance where date=?", (str(datetime.date.today()),))
        rows = cursor.fetchall()
        if len(rows) > 0:
            return False
        for row in attendance_list:
            cursor.execute("insert into Attendance (ID_Student, Date, Presence) values(?, ?, ?)", (row[0], str(datetime.date.today()), row[1]))
        data.commit()
        data.close()
        return True




    def update_student(self, student_id, name, surname, gender, birthdate, email, login, password):
        """
        Method allows mentor edit students specific data

        Args:
            None
        Return:
             None
        """
        user = db.session.query(UserDb).filter_by(id=student_id).first()
        user.name = name
        user.surname = surname
        user.gender = gender
        user.birth_date = birthdate
        user.email = email
        user.login = login
        user.password = password
        db.session.commit()
        return user

    def get_submissions_to_grade(self):
        """
        Method allows mentor show submissions to grade

        Args:
            None
        Return:
             List of lists with submissions to grade
        """
        return_list = []
        data = sqlite3.connect(User.path)
        cursor = data.cursor()
        submissions_not_graded = cursor.execute(
                            "SELECT Submission.id, Assignment.ID, Assignment.Name, Assignment.delivery_date, User.Name, User.Surname, Submission.Submittion_date "
                            "FROM Submission "
                            "LEFT JOIN Assignment ON Assignment.ID=Submission.ID_Assignment "
                            "INNER JOIN User ON user.ID=Submission.ID_Student "
                            "WHERE Submission.Grade IS NULL OR Submission.Grade=''").fetchall()

        if len(submissions_not_graded) == 0:
            return None
        for submission in submissions_not_graded:
            return_list.append(GradeableSubmissions(submission[1], submission[2], submission[3],
                                submission[4], submission[5], submission[6], submission[0]))
        data.close()
        return return_list

    def get_submission(self, submission_id):
        """
        Method allows mentor to get one submission

        Args:
            submission id
        Return:
            one submission
        """
        data = sqlite3.connect(User.path)
        cursor = data.cursor()
        cursor.execute("select * from Submission where ID=?", (submission_id,))
        row = cursor.fetchone()
        if row:
            submission = Submission(row[2], row[1], row[5], row[3], row[4], row[0])
        data.close()
        return submission


    def get_checkpoint_submissions_to_grade(self, checkpoint_assignment_id):
        """
        Method allows mentor to get checkpoint submmision to grade

        Args:
            checkpoint assignment id
        Return:
             submission list
        """
        submission_list = []
        data = sqlite3.connect(User.path)
        cursor = data.cursor()
        cursor.execute("select Checkpoint_submittion.id, Checkpoint_assignment.name, user.Name, user.Surname "
                       "from Checkpoint_submittion "
                       "inner join User on user.ID=Checkpoint_submittion.ID_Student "
                       "inner join Checkpoint_assignment on Checkpoint_assignment.ID=Checkpoint_submittion.ID_Assignment"
                       " where (checkpoint_submittion.card='' or checkpoint_submittion.card is null) "
                       "and checkpoint_submittion.id_assignment=?", (checkpoint_assignment_id,))
        rows = cursor.fetchall()
        if rows:
            for row in rows:
                submission_list.append(GradeableCheckpointSubmission(row[0], row[1], row[2], row[3]))
        data.close()
        return submission_list


    def grade_checkpoint_submission(self, list_of_notes):
        """
        Method allows mentor to grade checkpoint submission

        Args:
            list of notes
        Return:
             submission list
        """
        submission_list = []
        data = sqlite3.connect(User.path)
        cursor = data.cursor()
        for row in list_of_notes:
            cursor.execute("update Checkpoint_submittion set card=?, Date=?, ID_Mentor=? "
                           "where id=?", (row[1], str(datetime.date.today()), self._id, row[0]))
        data.commit()
        data.close()
        return submission_list



    def grade_submission(self, assignment_id, grade):
        """
        Method allows mentor grade students submitted assignment

        Args:
            None
        Return:
             None
        """
        data = sqlite3.connect(User.path)
        cursor = data.cursor()
        cursor.execute("UPDATE Submission SET Grade=? WHERE ID=?", (grade, assignment_id))
        data.commit()
        data.close()

    def get_teams(self):
        """
        Method allows mentor to list teams

        Args:
            None
        Return:
             None
        """
        team_list = []
        data = sqlite3.connect(User.path)
        cursor = data.cursor()
        # cursor.execute("SELECT user.id, team_name, name, surname FROM teams "
        #                "LEFT JOIN user ON teams.id_student=user.id ORDER BY team_name")
        cursor.execute("SELECT user.id, team_name, name, surname FROM teams "
                       "LEFT JOIN user ON teams.id_student=user.id order by team_name")
        teams = cursor.fetchall()
        for team in teams:
            team_list.append(Team(team[0], team[1], team[2], team[3]))
        data.close()
        return team_list


    def get_teams_for_student(self):
        """
        Method allows mentor to list teams

        Args:
            None
        Return:
             None
        """
        team_list = []
        data = sqlite3.connect(User.path)
        cursor = data.cursor()
        # cursor.execute("SELECT user.id, team_name, name, surname FROM teams "
        #                "LEFT JOIN user ON teams.id_student=user.id ORDER BY team_name")
        cursor.execute("SELECT user.ID, team_name, name, surname FROM teams "
                       "LEFT JOIN user ON teams.id_student=user.id group by Team_Name order by team_name")
        teams = cursor.fetchall()
        for team in teams:
            team_list.append(Team(team[0], team[1], team[2], team[3]))
        data.close()
        return team_list

    def add_to_team(self, student_id, team_name):
        data = sqlite3.connect(User.path)
        cursor = data.cursor()
        cursor.execute("SELECT * FROM teams WHERE ID_Student=?", (student_id,)) # check if student already is in team
        team_row = cursor.fetchone()
        if team_row:
            cursor.execute("DELETE FROM teams WHERE ID_Student=?", (student_id,))
        cursor.execute("INSERT INTO teams (ID_Student, Team_name) VALUES (?, ?)", (student_id, team_name))
        data.commit()
        data.close()

    def add_team(self, new_team):
        data = sqlite3.connect(User.path)
        cursor = data.cursor()
        cursor.execute("SELECT * FROM teams WHERE Team_Name=?", (new_team,)) # check if student already is in team
        team_row = cursor.fetchone()
        if team_row:
            data.close()
            return None
        cursor.execute("INSERT INTO teams (Team_name, ID_Student) VALUES (?, ?)", (new_team, "<empty>"))
        data.commit()
        data.close()

    def remove_team(self, team_name):
        """
        Method allows mentor to remove team

        Args:
            team name
        Return:
            None
        """
        data = sqlite3.connect(User.path)
        cursor = data.cursor()
        cursor.execute("delete FROM teams WHERE Team_Name=?", (team_name,))
        data.commit()
        data.close()

    def get_assignments(self):
        """
        Method allows mentor to get list of all assignments

        Args:
          None
        Return:
          list of assignments
        """

        list_of_assignments = []
        data = sqlite3.connect(User.path)
        cursor = data.cursor()
        cursor.execute("select * from Assignment")
        for row in cursor.fetchall():
            new_assignment = Assignment(row[0], row[1], row[2], row[3], row[4], row[5])
            list_of_assignments.append(new_assignment)
        data.close()
        return list_of_assignments

    def get_assignment(self, assignment_id):
        """
        Method allows mentor to get assignment by id

        Args:
          assignment id
        Return:
          assignment
        """
        data = sqlite3.connect(User.path)
        cursor = data.cursor()
        cursor.execute("select * from Assignment where ID=?", (assignment_id,))
        row = cursor.fetchone()
        if row:
            assignment = Assignment(row[0], row[1], row[2], row[3], row[4], row[5])
        data.close()
        return assignment

    def remove_assignment(self, assignment_id):
        """
        Method allows mentor to remove assignment

        Args:
            None
        Return:
            None
        """
        data = sqlite3.connect(User.path)
        cursor = data.cursor()
        cursor.execute("delete from  Assignment where ID=?", (assignment_id,))
        data.commit()
        data.close()


    def update_assignment(self, assignment_id, name, type, max_points, delivery_date, content):
        """
         Method allows mentor to update assignment

         Args:
             None
         Return:
             None
         """
        data = sqlite3.connect(User.path)
        cursor = data.cursor()
        cursor.execute("update Assignment set Name=?, Type=?, Max_points=?, Delivery_date=?, "
                       " Content=? where ID=?", (name, type, max_points, delivery_date, content, assignment_id))
        data.commit()
        data.close()


    def add_new_assignment(self, name, type, max_points, delivery_date, content):
        """
        Method allows mentor to add new assignment

        Args:
            None
        Return:
            None
        """
        data = sqlite3.connect(User.path)
        cursor = data.cursor()
        cursor.execute("insert into Assignment (Name, Type, Max_points, Delivery_date, "
                       " Content) values(?, ?, ?, ?, ?)", (name, type, max_points, delivery_date, content))
        data.commit()
        data.close()


    def get_checkpoints_for_submission(self):
        """
        Method allows mentor to get checkpoints for submission

        Args:
            None
        Return:
             list of checkpoint submissions
        """
        list_of_checkpoint_submissions = []
        data = sqlite3.connect(User.path)
        cursor = data.cursor()
        cursor.execute("select user.id from user where user.id not in (select id_student from checkpoint_submittion) and user.user_type='student'")
        students_ids_without_submissions = cursor.fetchall()
        cursor.execute("select id from Checkpoint_assignment")
        assignments = cursor.fetchall()
        for student_id in students_ids_without_submissions:
            for assignment in assignments:
                cursor.execute("insert into Checkpoint_submittion (ID_Student, ID_Assignment) values (?, ?)", (student_id[0], assignment[0]))
        data.commit()
        cursor.execute("SELECT * FROM Checkpoint_assignment"
                       " where Checkpoint_assignment.id in (select ID_Assignment from Checkpoint_submittion"
                       " where card='' or card is null group by ID_Assignment)")

        rows = cursor.fetchall()
        if rows:
            for row in rows:
                list_of_checkpoint_submissions.append(CheckpointAssignment(row[0], row[1], row[2]))
        return list_of_checkpoint_submissions

    def get_submissions_for_checkpoint(self):
        """
        Method allows mentor to get submissions for checkpoints

        Args:
            None
        Return:
             list of checkpoint submissions
        """
        list_of_checkpoint_submissions = []
        data = sqlite3.connect(User.path)
        cursor = data.cursor()
        cursor.execute("SELECT * FROM Checkpoint_submittion, Checkpoint_assignment"
                       " where Checkpoint_submittion.ID_Assignment in (select ID_Assignment from Checkpoint_submittion"
                       " where card='' or card is null)")

        rows = cursor.fetchall()
        if rows:
            for row in rows:
                list_of_checkpoint_submissions.append(CheckpointAssignment(row[0], row[1], row[2]))
        return list_of_checkpoint_submissions


    def get_checkpoint_assignments(self):
        """
        Method allows mentor to list checkpoint assignments

        Args:
            None
        Return:
             None
        """
        checkpoint_assignments_list = []
        data = sqlite3.connect(User.path)
        cursor = data.cursor()
        cursor.execute("SELECT * FROM Checkpoint_assignment")
        assignments = cursor.fetchall()
        n = 1
        for assignment in assignments:
            if assignment[2] == None:
                checkpoint_assignments_list.append([str(n) + ".", assignment[1], ''])

            else:
                checkpoint_assignments_list.append([str(n) + ".", assignment[1], assignment[2]])
            n += 1
        data.close()
        return checkpoint_assignments_list

    def get_checkpoint_id(self):
        """
        Returns id of checkpoint

        Args:
            None
        Return:
             id of checkpoint
        """
        choosed_checkpoint = ui.Ui.get_inputs([""], "Choose checkpoint to grade student")
        data = sqlite3.connect(User.path)
        cursor = data.cursor()
        cursor.execute("SELECT * FROM Checkpoint_assignment")
        checkpoint = cursor.fetchall()
        checkpoint_id = checkpoint[int(choosed_checkpoint[0]) - 1][0]
        data.close()
        return checkpoint_id


    def check_student_performance(self, student_id, date_from, date_to):
        """
        Method allows mentor to check performance of particular student by showing hes statistics

        Args:
            student_id, data_from, data_to
        Return:
             None
        """
        data = sqlite3.connect(User.path)
        cursor = data.cursor()
        cursor.execute("SELECT name, surname FROM user where ID=?", (student_id,))
        _data = cursor.fetchone()
        student_name = _data[0]
        student_surname = _data[1]

        cursor.execute("SELECT * FROM attendance where id_student=? AND date BETWEEN ? AND ?",
                       (student_id, date_from, date_to))
        _data = cursor.fetchall()
        all_days = 0
        days_in_school = 0
        for item in _data:
            all_days += 1
            if item[3] == "1":
                days_in_school += 1
        if all_days == 0:
            avg_days = 0
        else:
            avg_days = round(days_in_school/all_days, 2)

        cursor.execute("SELECT Grade FROM Submission where id_student=? AND Submittion_date BETWEEN ? AND ?",
                       (student_id, date_from, date_to))
        _data = cursor.fetchall()
        grades_quantity = 0
        grades_sum = 0
        for item in _data:
            grades_quantity += 1
            grades_sum += int(item[0])
        if grades_quantity:
            grades_avg = round(grades_sum/grades_quantity, 2)
        else:
            grades_avg = 0

        cursor.execute("SELECT Card FROM Checkpoint_submittion where id_student=? AND date BETWEEN ? AND ?",
                       (student_id, date_from, date_to))
        _data = cursor.fetchall()
        yellow_cards = 0
        red_cards = 0
        for item in _data:
            if item[0] == "yellow":
                yellow_cards += 1
            elif item[0] == "red":
                red_cards += 1

        student_statistics = StudentStatistic(student_id, student_name, student_surname, avg_days,
                                      grades_avg, yellow_cards, red_cards)
        data.close()
        return student_statistics

    def edit_mentor(self):
        """
        Method allows manager to edit mentor specific data

        Return:
             None
        """
        data = sqlite3.connect(User.path)
        cursor = data.cursor()
        cursor.execute("UPDATE `User` SET `Name`=?, `Surname`=?, `Gender`=?, "
                       "`Birth_date`=?,`Email`=?, `Login`=?, `Password`=?"
                       " WHERE `ID`=?",
                       (self.name, self.surname, self.gender, self.birth_date, self.email, self.login, self.password, self._id))
        data.commit()
        data.close()

    @classmethod
    def get_mentor_by_id(cls, id):
        """
        Method return mentor by id

        Args: mentor_id

        Return:
             object Mentor
        """
        data = sqlite3.connect(User.path)
        cursor = data.cursor()
        cursor.execute("SELECT * FROM `User` WHERE ID = ?;", (id,))
        mentor = cursor.fetchone()  # jak nie będzie działało to może fetchall i wtedy row = mentor[0]
        if mentor:
            return cls(mentor[0], mentor[1], mentor[2], mentor[3], mentor[4],
                       mentor[5], mentor[6], mentor[7], mentor[8])


class Manager(Employee):
    """Class creates object mentor"""
    def __init__(self, _id, name, surname, gender, birth_date, email, login, password, user_type):
        """
        Initialize mentor object that inherits from User class

        Args:
            name: check_if_correct(name, str)
            surname: check_if_correct(surname, str)
            check_gender: gender
            gender: gender
            date_validate: birth_date
            birth_date: birth_date
            email:
            login:login
            password: check_if_correct(password, str)
        """
        super().__init__(_id, name, surname, gender, birth_date, email, login, password, user_type)


    def add_mentor(self, name, surname, gender, birthdate, email, login, password):
        """
        Method allows manager to add mentor to mentors list
        Args:
            name, surname, gender, birthdate, email, login, password
        Return:
             None
        """
        data = sqlite3.connect(User.path)
        cursor = data.cursor()
        cursor.execute("INSERT INTO `User` (`Name`, `Surname`, `Gender`, `Birth_date`, `Email`, `Login`, `Password`, `User_type`) "
                       "VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (name, surname, gender, birthdate, email, login, password, "mentor"))
        data.commit()
        data.close()
        print("Mentor was added.")


    def remove_mentor(self, mentor_id):
        """
        Method allows manager to remove mentor from mentors list

        Args:
            mentor id
        Return:
             None
        """

        data = sqlite3.connect(User.path)
        cursor = data.cursor()
        cursor.execute("DELETE FROM User WHERE ID=?", (mentor_id,))
        data.commit()
        data.close()


    @staticmethod
    def list_mentors():
        """
        Method allows manager to list all mentor from list

        Return:
             mentor_list
        """
        mentor_list = []
        data = sqlite3.connect(User.path)
        cursor = data.cursor()
        cursor.execute("SELECT * FROM `User` WHERE User_type='mentor'")
        mentors = cursor.fetchall()
        for mentor in mentors:
            mentor_list.append(Mentor(mentor[0], mentor[1], mentor[2], mentor[3], mentor[4],
                                      mentor[5], mentor[6], mentor[7], mentor[8]))
        data.close()
        return mentor_list


    @staticmethod
    def which_mentor_is_a_monster():
        """
        Method display checkpoint cards statistics of mentors


        Return:
           list with card statistics

        """
        checkpoint_stats_list = []
        cards_statistics = {}
        mentors = []
        data = sqlite3.connect(User.path)
        cursor = data.cursor()
        cards = cursor.execute("SELECT `Name`, `Surname`, `Card` "
                               "FROM `Checkpoint_submittion` "
                               "INNER JOIN `User` ON Checkpoint_submittion.ID_Mentor = User.ID ")
        cards = cards.fetchall()
        for row in cards:
            name_surname = str(row[0]) + ' ' + str(row[1])
            cards_statistics[name_surname] = [0, 0, 0] #Cards [red,yellow,green] # row[1]- surname change for name,surname or ID_Mentor
            mentors.append(name_surname)
        mentors = list(set(mentors))
        for mentor in mentors:
            for row in cards:
                if str(row[0]) + ' ' + str(row[1]) == mentor:
                    if str(row[2]) == 'red':
                        cards_statistics[mentor][0] += 1
                    if str(row[2]) == 'yellow':
                        cards_statistics[mentor][1] += 1
                    if str(row[2]) == 'green':
                        cards_statistics[mentor][2] += 1
        for key, value in cards_statistics.items():
            statistic_for_mentor = CheckpointStatsForMentors(key, value[0], value[1], value[2])
            checkpoint_stats_list.append(statistic_for_mentor)
        data.commit()
        data.close()
        return checkpoint_stats_list

    @staticmethod
    def grades_stats_for_mentors():
        """
         Method display how many assignment mentor graded and what is his average grade

         Args:
             None

         Return:
            list with grade statistics

        """
        grades_statistics = []
        data = sqlite3.connect(User.path)
        cursor = data.cursor()
        grades = cursor.execute("SELECT  `Name`, `Surname`, COUNT(`Grade`), AVG(`Grade`)"
                                            "FROM `Submission` INNER JOIN `User` ON `Submission`.ID_Mentor = User.ID"
                                            " GROUP BY `Name`")

        grades = grades.fetchall()
        for row in grades:
            grades_statistics.append(GradeStatsForMentors(row[0], row[1], row[2], row[3]))
        return grades_statistics


    def full_stats_for_student(self, student_id):
        """
         Method display how statistics for students

         Args:
             student id


         Return:
            list with grade statistics

        """

        data = sqlite3.connect(User.path)
        cursor = data.cursor()
        grades = cursor.execute("SELECT  `Name`, `Surname`, COUNT(`Grade`), AVG(`Grade`)"
                                "FROM `Submission` INNER JOIN `User` ON `Submission`.ID_Student = User.ID"
                                " WHERE ID_Student = ?", (student_id,))
        grades = grades.fetchall()
        student_grades = StudentGrades(grades[0][0], grades[0][1], grades[0][2], grades[0][3])
        return student_grades
