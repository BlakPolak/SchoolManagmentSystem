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
from sqlalchemy.sql import func
from main import db
from sqlalchemy.sql import func



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
        if user:
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
                students list
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
        student_all_grades = db.session.query(AssignmentDb, SubmissionDb).join(SubmissionDb, SubmissionDb.id_assignment == AssignmentDb.id).filter(SubmissionDb.id_student == self._id).all()
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
        assignments_ids = db.session.query(CheckpointAssignmentDb.id).all()
        for id in assignments_ids:
            new_submission = CheckpointSubmissionDb(id_student=new_student.id, id_assignment=id[0], card='')
            db.session.add(new_submission)
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
        for index, item in enumerate(attendance_list):
            if item[1] == "present":
                attendance_list[index][1] = 1
            elif item[1] == "absent":
                attendance_list[index][1] = 0
            else:
                attendance_list[index][1] = 2
        today = datetime.date.today()
        todays_attendance = db.session.query(AttendanceDb).filter_by(date=today).all()
        if todays_attendance:
            return False
        for row in attendance_list:
            att = AttendanceDb(id_student=row[0], date=today, presence=row[1])
            db.session.add(att)
        db.session.commit()
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
        submissions = db.session.query(SubmissionDb.id, AssignmentDb.id, AssignmentDb.name, AssignmentDb.delivery_date,
                                       UserDb.name, UserDb.surname, SubmissionDb.date).filter(
                                        AssignmentDb.id == SubmissionDb.id_assignment, UserDb.id == SubmissionDb.id_student,
                                        (SubmissionDb.grade == "") | (SubmissionDb.grade.is_(None))
                                        ).all()
        for submission in submissions:
            return_list.append(GradeableSubmissions(submission[1], submission[2], submission[3],
                                submission[4], submission[5], submission[6], submission[0]))
        return return_list

    def get_submission(self, submission_id):
        """
        Method allows mentor to get one submission

        Args:
            submission id
        Return:
            one submission
        """
        submission = db.session.query(SubmissionDb).filter_by(id=submission_id).first()
        return submission

    def get_student_checkpoint_submission(self, checkpoint_submission_id):
        submission = db.session.query(CheckpointSubmissionDb).filter_by(id=checkpoint_submission_id).first()
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


    def grade_checkpoint_submission(self, submission_id, card):
        """
        Method allows mentor to grade checkpoint submission

        Args:
            list of notes
        Return:
             submission list
        """
        submission = db.session.query(CheckpointSubmissionDb).filter_by(id=submission_id).first()
        submission.card = card
        db.session.commit()



    def grade_submission(self, submission_id, grade):
        """
        Method allows mentor grade students submitted assignment

        Args:
            None
        Return:
             None
        """
        submission = self.get_submission(submission_id)
        submission.grade = grade
        db.session.commit()

    def get_teams(self):
        """
        Method allows mentor to list teams

        Args:
            None
        Return:
             None
        """

        team_list = db.session.query(TeamDb, UserDb).join(UserDb, UserDb.id == TeamDb.id_student).all()
        # team_list = db.session.query(TeamDb).all()
        print(team_list)
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

        list_of_assignments = db.session.query(AssignmentDb).all()
        return list_of_assignments

    def get_assignment(self, assignment_id):
        """
        Method allows mentor to get assignment by id

        Args:
          assignment id
        Return:
          assignment
        """
        assignment = db.session.query(AssignmentDb).filter_by(id=assignment_id).first()
        return assignment

    def remove_assignment(self, assignment_id):
        """
        Method allows mentor to remove assignment

        Args:
            None
        Return:
            None
        """
        db.session.query(AssignmentDb).filter_by(id=assignment_id).delete()


    def update_assignment(self, assignment_id, name, type, max_points, delivery_date, content):
        """
         Method allows mentor to update assignment

         Args:
             None
         Return:
             None
         """

        assignment = self.get_assignment(assignment_id)
        assignment.name = name
        assignment.type = type
        assignment.max_points = max_points
        assignment.delivery_date = delivery_date
        assignment.content = content
        db.session.commit()
        return assignment


    def add_new_assignment(self, name, type, max_points, delivery_date, content):
        """
        Method allows mentor to add new assignment

        Args:
            None
        Return:
            None
        """
        new_assignment = AssignmentDb(name=name, type=type, max_points=max_points, delivery_date=delivery_date, content=content)
        db.session.add(new_assignment)
        db.session.commit()
        return new_assignment

    def get_checkpoints_for_submission(self):
        """
        Method allows mentor to get checkpoints for submission

        Args:
            None
        Return:
             list of checkpoint submissions
        """
        submissions = db.session.query(CheckpointSubmissionDb).filter_by(card='').all()
        # a = submissions[0].student

        # list_of_checkpoint_submissions = []
        # data = sqlite3.connect(User.path)
        # cursor = data.cursor()
        # cursor.execute("select user.id from user where user.id not in (select id_student from checkpoint_submittion) and user.user_type='student'")
        # students_ids_without_submissions = cursor.fetchall()
        # cursor.execute("select id from Checkpoint_assignment")
        # assignments = cursor.fetchall()
        # for student_id in students_ids_without_submissions:
        #     for assignment in assignments:
        #         cursor.execute("insert into Checkpoint_submittion (ID_Student, ID_Assignment) values (?, ?)", (student_id[0], assignment[0]))
        # data.commit()
        # cursor.execute("SELECT * FROM Checkpoint_assignment"
        #                " where Checkpoint_assignment.id in (select ID_Assignment from Checkpoint_submittion"
        #                " where card='' or card is null group by ID_Assignment)")
        #
        # rows = cursor.fetchall()
        # if rows:
        #     for row in rows:
        #         list_of_checkpoint_submissions.append(CheckpointAssignment(row[0], row[1], row[2]))
        return submissions

    # def get_submissions_for_checkpoint(self):
    #     """
    #     Method allows mentor to get submissions for checkpoints
    #
    #     Args:
    #         None
    #     Return:
    #          list of checkpoint submissions
    #     """
    #     list_of_checkpoint_submissions = []
    #     data = sqlite3.connect(User.path)
    #     cursor = data.cursor()
    #     cursor.execute("SELECT * FROM Checkpoint_submittion, Checkpoint_assignment"
    #                    " where Checkpoint_submittion.ID_Assignment in (select ID_Assignment from Checkpoint_submittion"
    #                    " where card='' or card is null)")
    #
    #     rows = cursor.fetchall()
    #     if rows:
    #         for row in rows:
    #             list_of_checkpoint_submissions.append(CheckpointAssignment(row[0], row[1], row[2]))
    #     return list_of_checkpoint_submissions

    #
    # def get_checkpoint_assignments(self):
    #     """
    #     Method allows mentor to list checkpoint assignments
    #
    #     Args:
    #         None
    #     Return:
    #          None
    #     """
    #     checkpoint_assignments_list = []
    #     data = sqlite3.connect(User.path)
    #     cursor = data.cursor()
    #     cursor.execute("SELECT * FROM Checkpoint_assignment")
    #     assignments = cursor.fetchall()
    #     n = 1
    #     for assignment in assignments:
    #         if assignment[2] == None:
    #             checkpoint_assignments_list.append([str(n) + ".", assignment[1], ''])
    #
    #         else:
    #             checkpoint_assignments_list.append([str(n) + ".", assignment[1], assignment[2]])
    #         n += 1
    #     data.close()
    #     return checkpoint_assignments_list

    # def get_checkpoint_id(self):
    #     """
    #     Returns id of checkpoint
    #
    #     Args:
    #         None
    #     Return:
    #          id of checkpoint
    #     """
    #     choosed_checkpoint = ui.Ui.get_inputs([""], "Choose checkpoint to grade student")
    #     data = sqlite3.connect(User.path)
    #     cursor = data.cursor()
    #     cursor.execute("SELECT * FROM Checkpoint_assignment")
    #     checkpoint = cursor.fetchall()
    #     checkpoint_id = checkpoint[int(choosed_checkpoint[0]) - 1][0]
    #     data.close()
    #     return checkpoint_id


    def check_student_performance(self, student_id, date_from, date_to):
        """
        Method allows mentor to check performance of particular student by showing hes statistics

        Args:
            student_id, data_from, data_to
        Return:
             None
        """

        student = db.session.query(UserDb).filter_by(id=student_id).first()
        avg_days = db.session.query(func.avg(AttendanceDb.presence)).\
            filter(AttendanceDb.id_student==student_id, AttendanceDb.date.between(date_from, date_to)).all()[0][0]
        avg_grades = db.session.query(func.avg(SubmissionDb.grade)).\
            filter(SubmissionDb.id_student==student_id, SubmissionDb.date.between(date_from, date_to)).all()[0][0]
        cards = db.session.query(CheckpointSubmissionDb.card).\
            filter(CheckpointSubmissionDb.id_student==student_id, CheckpointSubmissionDb.date.between(date_from, date_to)).all()
        yellow_cards = 0
        red_cards = 0
        green_cards = 0
        for card in cards:
            if card[0] == "yellow":
                yellow_cards += 1
            elif card[0] == "red":
                red_cards += 1
            elif card[0] == "green":
                green_cards += 1
        student_statistics = StudentStatistic(student.id, student.name, student.surname, avg_days,
                                      avg_grades, yellow_cards, red_cards, green_cards)
        print()
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
        mentor = UserDb(name=name, surname=surname, gender=gender, birth_date=birthdate, email=email, login=login, password=password, user_type="mentor")
        db.session.add(mentor)
        db.session.commit()


    def remove_mentor(self, mentor_id):
        """
        Method allows manager to remove mentor from mentors list

        Args:
            mentor id
        Return:
             None
        """
        mentor = db.session.query(UserDb).filter_by(id=mentor_id).first()
        db.session.delete(mentor)
        db.session.commit()


    @staticmethod
    def list_mentors():
        """
        Method allows manager to list all mentor from list

        Return:
             mentor_list
        """
        mentors = db.session.query(UserDb).filter_by(user_type="mentor").all()
        return mentors


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
        cards = db.session.query(UserDb.name, UserDb.surname, CheckpointSubmissionDb.card).filter_by(id=CheckpointSubmissionDb.id_mentor).all()
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
        grades = db.session.query(UserDb, func.count(SubmissionDb.grade), func.avg(SubmissionDb.grade)).filter_by(id=SubmissionDb.id_mentor).all()
        return grades


    def full_stats_for_student(self, student_id):
        """
         Method display how statistics for students

         Args:
             student id


         Return:
            list with grade statistics

        """
        grades = db.session.query(UserDb, func.count(SubmissionDb.grade), func.avg(SubmissionDb.grade)).filter(UserDb.id == SubmissionDb.id_student, UserDb.id == student_id).all()
        return grades
