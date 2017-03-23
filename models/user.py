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
from sqlalchemy import and_



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
        student_all_grades = db.session.query(AssignmentDb, SubmissionDb)\
            .join(SubmissionDb, SubmissionDb.id_assignment == AssignmentDb.id)\
            .filter(SubmissionDb.id_student == self._id).all()
        return student_all_grades

    def list_assignments_to_submit(self):
        """
        Method returns list of all student submission

        Return:
            list not submitted assignment

        """
        assignments = db.session.query(AssignmentDb)\
            .outerjoin(SubmissionDb)\
            .filter(AssignmentDb.type == 'individual')\
            .filter(SubmissionDb.id_assignment==None).all()
        return assignments

    def submit_assignment(self, result, id_assignment):
        """
        Method allows student to submit assignment

        Args:
            assignment, result

        """

        submission = db.session.query(SubmissionDb)\
            .filter_by(id_student=self._id, id_assignment=id_assignment).first()
        submission.result = result
        db.session.add(submission)
        db.session.commit()

    def list_group_assignment(self):
        """
        Method returns list of all group submission

        Return:
            list assignment for group

        """
        group_assignments_to_submit = db.session.query(AssignmentDb) \
            .outerjoin(SubmissionDb) \
            .filter(AssignmentDb.type == 'group') \
            .filter(SubmissionDb.id_assignment == None).all()
        return group_assignments_to_submit

    def find_student_team(self):
        """
        Method returns team name for logged student

        Return:
            team name as list

        """
        team = db.session.query(TeamDb)\
            .filter_by(id_student=self._id).first()
        return team

    def find_students_teammates(self):
        """
        Method returns all students from the same team

        Return:
            list student teammates

        """
        teammates_list = db.session.query(TeamDb)\
            .filter_by(name=self.find_student_team().name).all()
        return teammates_list

    def add_group_assignment(self, id_assignment, result):
        """
        Method allows student to submit assignment for each team member

        Args:
            teammates.py, group_submission

        """
        submission_date = datetime.date.today()
        for teammate in self.find_students_teammates():
            submission = SubmissionDb(id_student=teammate.id_student, result=result, id_assignment=id_assignment, date=submission_date)
            db.session.add(submission)
            db.session.commit()

    def check_my_attendance(self):
        """
        Method allows student to check attendance level in %

        Return:
            percent of attendance

        """
        presence = db.session.query(func.count(AttendanceDb.presence)).filter(AttendanceDb.id_student == self._id, AttendanceDb.presence == 1).all()
        days = db.session.query(func.count(AttendanceDb.presence)).filter(AttendanceDb.id_student == self._id).all()
        presence = presence[0][0]
        days = days[0][0]
        attendance_in_percent = (presence/days)*100
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

    def add_checkpoint(self, name, assignment):
        new_checkpoint = CheckpointAssignmentDb(name=name, assignment=assignment)
        db.session.add(new_checkpoint)
        db.session.commit()
        students = db.session.query(UserDb).filter_by(user_type='student').all()
        for student in students:
            new_submission = CheckpointSubmissionDb(id_assignment=new_checkpoint.id, id_student=student.id)
            db.session.add(new_submission)
        db.session.commit()

    def get_student_checkpoint_submission(self, checkpoint_submission_id):
        submission = db.session.query(CheckpointSubmissionDb).filter_by(id=checkpoint_submission_id).first()
        return submission


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

        team_list = db.session.query(TeamDb, UserDb).outerjoin(UserDb, UserDb.id == TeamDb.id_student)\
            .order_by(TeamDb.name).all()
        return team_list


    def get_teams_for_student(self):
        """
        Method allows mentor to list teams

        Args:
            None
        Return:
             None
        """
        team_list = db.session.query(TeamDb, UserDb).outerjoin(UserDb, UserDb.id == TeamDb.id_student)\
            .order_by(TeamDb.name).group_by(TeamDb.name).all()
        return team_list

    def add_to_team(self, student_id, team_name):
        """
        Method allows mentor assign student to team

        Args:
            None
        Return:
             None
        """
        student_in_team = db.session.query(TeamDb).filter_by(id_student=student_id).first()
        if student_in_team:
            db.session.delete(student_in_team)
        # assign_student = db.session.query(TeamDb).filter_by(id_student=student_id, name=team_name).first()
        assigned_student = TeamDb(id_student=student_id, name=team_name)
        db.session.add(assigned_student)
        db.session.commit()
        return assigned_student

    def add_team(self, name):
        """
         Method allows mentor to add new team

         Args:
             name
         Return:
             None
         """

        new_team = TeamDb(name=name, id_student='')
        db.session.add(new_team)
        db.session.commit()
        return new_team



    def remove_team(self, team_name):
        """
        Method allows mentor to remove team

        Args:
            team name
        Return:
            None
        """

        db.session.query(TeamDb).filter_by(name=team_name).delete()
        db.session.commit()


    def remove_student_from_team(self, student_id):
        """
        Method allows mentor to remove team

        Args:
            team name
        Return:
            None
        """
        db.session.query(TeamDb).filter_by(id_student=student_id).delete()
        db.session.commit()


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
        submissions = db.session.query(CheckpointSubmissionDb).\
            filter((CheckpointSubmissionDb.card == '') | CheckpointSubmissionDb.card.is_(None)).all()
        return submissions


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

    @staticmethod
    def get_mentor_by_id(id):
        """
        Method return mentor by id

        Args: mentor_id

        Return:
             object Mentor
        """

        mentor = db.session.query(UserDb).filter_by(id=id).first()
        return mentor



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
