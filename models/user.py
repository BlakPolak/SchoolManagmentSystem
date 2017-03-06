import datetime
import sqlite3

from models import ui


class User:
    """
        Base class creates user object

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
    def __init__(self, _id, name, surname, gender, birth_date, email, login, password):
        """
        Initialize user object

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
        self._id = _id
        self.name = self.check_if_correct(name, str)
        self.surname = self.check_if_correct(surname, str)
        self.check_gender(gender)
        self.gender = gender
        self.date_validate(birth_date)
        self.birth_date = birth_date
        self.email = email
        self.login = login
        self.password = self.check_if_correct(password, str)

    @staticmethod
    def check_if_correct(validate, check_type):
        """
        Checks if variable is expected type and convert it to integer type if it contains just digits

        Args:
            validate: variable to check
            check_type: expected type of variable

        Returns:
            validated variable
        """
        if type(validate) != check_type:
            raise TypeError("Wrong format for: " + str(validate))
        elif type(validate) == check_type:
            if validate.isdigit():
                validate = int(validate)
                return validate
            elif all(i.isalpha() or i.isspace() for i in validate):
                return validate
            else:
                raise TypeError("Wrong format for: " + str(validate))

    def check_gender(self, gender):
        """
        Checks if variable is correct type of gender, if not - it raises an error

        Args:
            gender: variable to check

        Returns:
            None
        """
        gender_list = ['male', 'female', 'not sure']
        if gender.lower() not in gender_list:
            raise NameError('Gender should be: male, female, not sure')

    def date_validate(self, birth_date):
        """
        Checks if data format is correct

        Args:
            birth_date: variable to check

        Returns:
         True if data format is correct
        """
        if datetime.datetime.strptime(birth_date, '%Y-%m-%d').strftime('%Y-%m-%d'):
            return True


class Employee(User):
    """Class creates object employee"""
    def __init__(self, _id, name, surname, gender, birth_date, email, login, password):
        """
        Initialize employee object that inherits from User class

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
        super().__init__(_id, name, surname, gender, birth_date, email, login, password)

    def list_students(self):
        """
        Return student list to display

        Returns:
                student list
        """
        student_list = []
        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        cursor.execute("SELECT * FROM `User` WHERE User_type='student'")
        students = cursor.fetchall()
        n = 1
        for student in students:
            student_list.append([str(n) + ".", student[1], student[2]])
            n += 1
        data.close()
        return student_list


    def list_students_simple_view(self):
        """
        Return student list to display

        Returns:
                student list
        """
        student_list = []
        data = sqlite3.connect("program.db")
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
        data = sqlite3.connect("program.db")
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
    def __init__(self, _id, name, surname, gender, birth_date, email, login, password):
        """
        Initialize student object that inherits from User class

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
        super().__init__(_id, name, surname, gender, birth_date, email, login, password)
        self.my_submissions_list = []

    def __str__(self):
        return self.name+self.surname

    def view_my_grades(self):
        """
        Method display list of submitted assignment with grades

        Return:
            table submitted assignment with grades

        """
        grades_for_view = []
        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        cursor.execute("SELECT assignment.name, submission.grade FROM assignment INNER JOIN submission "
                       "ON submission.ID_assignment = assignment.ID WHERE ID_Student='{}'".format(self._id))
        grades = cursor.fetchall()
        n = 1
        for grade in grades:
            grades_for_view.append([str(n) + ".", grade[0], grade[1]])
            n += 1
        data.commit()
        data.close()
        return grades_for_view

    def list_submissions(self): #to refactor - move to class submission as class method
        """
        Method returns list of all student submission

        Return:
            list submitted assignment

        """
        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        cursor.execute("select ID_Assignment from `Submission` WHERE ID_Student='{}'".format(self._id))
        submissions = cursor.fetchall()
        submissions_list = []
        for element in submissions:
            submissions_list.append(element[0])
        data.close()
        return submissions_list

    def list_assignments_to_submit(self): #to refactor - move to class submission as class method
        """
        Method returns list of all student submission

        Return:
            list not submitted assignment

        """
        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        cursor.execute("SELECT ID, Name, Type, Delivery_date FROM `Assignment`")
        assignments = cursor.fetchall()
        assignments_to_submit = []
        for assignment in assignments:
            if assignment[0] not in self.list_submissions():
                assignments_to_submit.append(list(assignment))
        data.close()
        return assignments_to_submit

    def submit_assignment(self, assignment):
        """
        Method allows student to submit assignment

        Args:
            assignment

        """
        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        if len(assignment) <= 1:
            print("You have no assignment to submitt!")
            return
        assignment_id = ui.Ui.get_inputs([""], "Enter number to choose assignment to submit: ")
        # if assignment_id not in assignment or assignment_id <= 0:
        #     print("Try again with right index!")
        #     return
        result = ui.Ui.get_inputs(["Content"], "Provide information about new assignment")
        submission_date = datetime.date.today()
        cursor.execute("INSERT INTO `Submission` (`ID_Student`, `ID_Assignment`,`Result`, `Submittion_date`) "
                       "VALUES ('{}', '{}', '{}', '{}')".format(self._id, assignment_id[0], result[0], submission_date))
        data.commit()
        data.close()

    def list_group_assignment(self):
        """
        Method returns list of all group submission

        Return:
            list assignment for group

        """
        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        cursor.execute("SELECT ID, Name, Type, Delivery_date FROM `Assignment` WHERE Type='group'")
        group_assignments = cursor.fetchall()
        group_assignments_list = []
        for assignment in group_assignments:
            group_assignments_list.append([assignment[0], assignment[1], assignment[2], assignment[3]])
        data.commit()
        data.close()
        return group_assignments_list

    def find_student_team(self):
        """
        Method returns team name for logged student

        Return:
            team name as list

        """
        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        cursor.execute("SELECT team_name FROM `Teams` WHERE ID_Student='{}'".format(self._id))
        teams = cursor.fetchall()
        data.commit()
        data.close()
        return teams[0][0]

    def find_students_teammates(self, team):
        """
        Method returns all students from the same team

        Return:
            list student teammates

        """
        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        cursor.execute("SELECT Id_Student FROM `Teams` WHERE Team_name='{}'".format(team))
        teammates = cursor.fetchall()
        teammates_list = []
        for mate in teammates:
            teammates_list.append(mate[0])
        data.commit()
        data.close()
        return teammates_list

    def add_group_assignment(self, teammates, group_submission):
        """
        Method allows student to submit assignment for each team member

        Args:
            teammates, group_submission

        """
        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        if len(group_submission) <= 1:
            print("You have no assignment to submitt!")
            return
        assignment_id = ui.Ui.get_inputs([""], "Enter number to choose assignment to submit: ")
        result = ui.Ui.get_inputs(["Content"], "Provide information about new assignment")
        submission_date = datetime.date.today()
        for row in teammates:
            cursor.execute("INSERT INTO `Submission` (`ID_Student`, `ID_Assignment`,`Result`, `Submittion_date`) "
                           "VALUES ('{}', '{}', '{}', '{}')".format(row, assignment_id[0], result[0], submission_date))
        data.commit()
        data.close()

    def check_my_attendance(self):
        """
        Method allows student to check attendance level in %

        Return:
            percent of attendance

        """
        student_id = self._id
        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        cursor.execute("SELECT COUNT(Presence) FROM `Attendance` WHERE ID_Student='{}'"
                       "AND `Presence`= 0".format(student_id))
        presence = cursor.fetchall()
        number_of_presence = float(presence[0][0])
        cursor.execute("SELECT COUNT(Presence) FROM `Attendance`")
        number_of_days = cursor.fetchall()
        days = float(number_of_days[0][0])
        if days == 0:
            print("No attendance!")
            return
        # TODO: new validation
        percent_of_attendance = (number_of_presence / days) * 100
        percent_of_attendance_list =[]
        percent_of_attendance_list.append([percent_of_attendance])
        data.commit()
        data.close()
        return percent_of_attendance_list


class Mentor(Employee):
    """Class creates object mentor"""
    def __init__(self, _id, name, surname, gender, birth_date, email, login, password):
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
        super().__init__(_id, name, surname, gender, birth_date, email, login, password)

    def add_student(self):
        """
        Method allows mentor to add student to students list

        Args:
            None
        Return:
             None
        """
        options = ui.Ui.get_inputs(["Name", "Surname", "Gender", "Birth date", "Email", "Login",
                                    "Password"], "Provide information about new student")

        if options[0].isalpha() and options[1].isalpha() and options[2] in ['male', 'female', 'not sure']:
            if options[3].isalpha():
                print('Data should have format: YYYY-MM-DD')
                return
        else:
            print('\nWrong input!\nName: only letters\nSurname: only letters\n'
                  'Gender: you can choose only male, female or not sure\nData format: YYYY-MM-DD\n')
            return

        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        cursor.execute("INSERT INTO `User` (`name`, `surname`, `gender`, `birth_date`, `email`, `login`, `password`, `user_type`) "
                       "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"
                       .format(options[0], options[1], options[2], options[3],
                               options[4], options[5], options[6], "student"))
        data.commit()
        data.close()
        print("Student was added.")

    def check_attendance(self):
        """
        Method allows mentor check students attendance

        Args:
            None
        Return:
             None
        """
        students_list = []
        ids = []
        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        cursor.execute("SELECT id, name, surname FROM user WHERE User_type='student'")
        students = cursor.fetchall()
        for student in students:
            students_list.append(student[1]+" "+student[2])
            ids.append(student[0])
        presences = ui.Ui.get_inputs(students_list, "Starting attendance check (mark 0 for absence, 1 for present)")
        i = 0
        for presence in presences:
            cursor.execute("INSERT INTO attendance (ID_Student, Date, Presence) VALUES ('{}', '{}', '{}')"
                           .format(ids[i], str(datetime.date.today()), presence))
            i += 1
        data.commit()
        data.close()
        print("Checking attendance finished")


    def remove_student(self):
        """
        Method allows mentor remove students from students list

        Args:
            None
        Return:
             None
        """
        self.list_students()
        options = ui.Ui.get_inputs([""], "Enter number to erase student from database: ")
        if int(options[0]) < 0 or int(options[0]) > len(self.list_students()):
            print("There is no such student number on the list")
            return

        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        cursor.execute("SELECT * FROM `user` WHERE `user_type`='student'")
        students = cursor.fetchall()
        student_to_erase_name = students[int(options[0])-1][1]
        student_to_erase_surname = students[int(options[0])-1][2]
        print(student_to_erase_name, student_to_erase_surname)
        cursor.execute("DELETE FROM `User` WHERE `name`='{}' AND `surname`='{}'"
                       .format(student_to_erase_name, student_to_erase_surname))
        data.commit()
        data.close()
        print("Student was erased.")


    def edit_student(self):
        """
        Method allows mentor edit students specific data

        Args:
            None
        Return:
             None
        """
        self.list_students()
        choosed_student = ui.Ui.get_inputs([""], "Enter number to edit student's data")
        options = ui.Ui.get_inputs(["Name", "Surname", "Gender", "Birth date", "Email", "Login",
                                    "Password"], "Edit information about student")
        if options[0].isalpha() and options[1].isalpha() and options[2] in ['male', 'female', 'not sure']:
            if options[3].isalpha():
                print('Data should have format: YYYY-MM-DD')
                return
        else:
            print('\nWrong input!\nName: only letters\nSurname: only letters\n'
                  'Gender: you can choose only male, female or not sure\nData format: YYYY-MM-DD\n')
            return
        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        cursor.execute("SELECT * FROM `user` WHERE `user_type`='student'")
        students = cursor.fetchall()
        student_to_edit_name = students[int(choosed_student[0]) - 1][1]
        student_to_edit_surname = students[int(choosed_student[0]) - 1][2]

        cursor.execute(
            "UPDATE `User` SET `name`='{}', `surname`='{}', `gender`='{}', `birth_date`='{}', `email`='{}', `login`='{}', `password`='{}' "
            " WHERE "
            "`name`='{}' AND `surname`='{}'"
            .format(options[0], options[1], options[2], options[3],
                    options[4], options[5], options[6], student_to_edit_name, student_to_edit_surname))
        data.commit()
        data.close()
        print("Update completed")

    def show_submissions_to_grade(self):
        """
        Method allows mentor show submissions to grade

        Args:
            None
        Return:
             List of lists with submissions to grade
        """
        return_list = []
        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        submissions_not_graded = cursor.execute(
"SELECT Assignment.ID, Assignment.Name, Assignment.delivery_date, User.Name, User.Surname, Submission.Submittion_date "
"FROM Submission "
"INNER JOIN Assignment ON Assignment.ID=Submission.ID "
"INNER JOIN User ON user.ID=Submission.ID_Student "
"WHERE Submission.Grade IS NULL OR Submission.Grade=''").fetchall()
        if len(submissions_not_graded) == 0:
            print("No submissions to grade")
            return None
        for submission in submissions_not_graded:
            return_list.append([submission[0], submission[1], submission[2],
                                submission[3], submission[4], submission[5]])
        data.close()
        return return_list

    def grade_submission(self):
        """
        Method allows mentor grade students submitted assignment

        Args:
            None
        Return:
             None
        """
        id_assignment_to_grade = ui.Ui.get_inputs([""], "Choose assignment to grade")
        grade = ui.Ui.get_inputs([""], "Enter grade for assignment")
        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        cursor.execute("UPDATE Submission SET Grade={} WHERE ID={}".format(grade[0], int(id_assignment_to_grade[0])))
        print("Submission graded")
        data.commit()
        data.close()

    def add_assignment(self):
        """
        Method allows mentor add new assignment

        Args:
            None
        Return:
             None
        """
        options = ui.Ui.get_inputs(["Name", "Type", "Max. points to receive", "Delivery date", "Content"],
                                    "Provide information about new assignment")
        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        cursor.execute(
            "INSERT INTO `assignment` (`name`, `type`, `max_points`, `delivery_date`, `content`) "
            "VALUES ('{}', '{}', '{}', '{}', '{}')"
            .format(options[0], options[1], options[2], options[3],
                    options[4]))
        data.commit()
        data.close()
        print("Assignment was added.")

    def list_teams(self):
        """
        Method allows mentor to list teams

        Args:
            None
        Return:
             None
        """
        team_list = []
        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        cursor.execute("SELECT user.id, team_name, name, surname FROM teams "
                       "INNER JOIN user ON teams.id_student=user.id ORDER BY team_name")
        teams = cursor.fetchall()
        for team in teams:
            team_list.append([team[0], team[1], team[2], team[3]])
        data.close()
        return team_list

    def add_team(self):
        choosed_student_and_team = ui.Ui.get_inputs(["Enter number to add student to team: ", "Team name for student: "], "")
        student_to_add_id = int(choosed_student_and_team[0]) # id student to add to team
        data = sqlite3.connect("program.db")
        cursor = data.cursor()

        cursor.execute("SELECT * FROM teams WHERE ID_Student='{}'".format(student_to_add_id)) # check if student already is in team
        team_row = cursor.fetchone()
        if team_row:
            cursor.execute("DELETE FROM teams WHERE ID_Student='{}'"
                           .format(student_to_add_id))

        cursor.execute("INSERT INTO teams (ID_Student, Team_name) VALUES ('{}', '{}')"
                           .format(student_to_add_id, choosed_student_and_team[1]))
        data.commit()
        data.close()
        print("Team updated.")


    def list_checkpoint_assignments(self):
        """
        Method allows mentor to list checkpoint assignments

        Args:
            None
        Return:
             None
        """
        checkpoint_assignments_list = []
        data = sqlite3.connect("program.db")
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
        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        cursor.execute("SELECT * FROM Checkpoint_assignment")
        checkpoint = cursor.fetchall()
        checkpoint_id = checkpoint[int(choosed_checkpoint[0]) - 1][0]
        data.close()
        return checkpoint_id

    def add_checkpoint_submission(self, checkpoint_assignment_id):
        """
        Method allows mentor to add cards to particular student

        Args:
            checkpoint_assignment_id: id of particular assignment
        Return:
             None
        """
        choosed_student = ui.Ui.get_inputs([""], "Choose student to add checkpoint results")
        student_to_add_id = int(choosed_student[0])
        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        card = ui.Ui.get_inputs([""], "Choose card to add (Enter to not assign)")

        cursor.execute("SELECT * FROM Checkpoint_submittion "
                       "WHERE ID_Student='{}' AND ID_Assignment='{}'"
                       .format(student_to_add_id, checkpoint_assignment_id))

        _data = cursor.fetchone()
        if _data is None:
            cursor.execute("INSERT INTO Checkpoint_submittion (ID_Student, Date, Card, ID_Mentor, ID_Assignment) "
                           "VALUES ('{}', '{}', '{}', '{}', '{}')"
                           .format(student_to_add_id, datetime.date.today(), card[0], self._id, checkpoint_assignment_id))
            data.commit()
            print("Checkpoint submission added.")
        else:
            print("Checkpoint already graded.")
        data.close()

    def check_student_performance(self):
        """
        Method allows mentor to check performance of particular student by showing hes statistics

        Args:
            None
        Return:
             None
        """
        return_list = []
        choosed_student = ui.Ui.get_inputs([""], "Choose student to check hes performance")
        student_to_check_id = int(choosed_student[0])
        period = ui.Ui.get_inputs(["Date from", "Date to"], "Enter dates for performance check")
        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        cursor.execute("SELECT name, surname FROM user where ID={}".format(student_to_check_id))
        _data = cursor.fetchone()
        student_name = _data[0]
        student_surname = _data[1]

        cursor.execute("SELECT * FROM attendance where id_student={} AND date BETWEEN '{}' AND '{}'"
                       .format(student_to_check_id, period[0], period[1]))
        _data = cursor.fetchall()
        all_days = 0
        days_in_school = 0
        for item in _data:
            all_days += 1
            if item[3] == "1":
                days_in_school += 1
        avg_days = round(days_in_school/all_days, 2)

        cursor.execute("SELECT Grade FROM Submission where id_student={} AND Submittion_date BETWEEN '{}' AND '{}'"
                       .format(student_to_check_id, period[0], period[1]))
        _data = cursor.fetchall()
        grades_quantity = 0
        grades_sum = 0
        for item in _data:
            grades_quantity += 1
            grades_sum += item[0]
        if grades_quantity:
            grades_avg = round(grades_sum/grades_quantity, 2)
        else:
            grades_avg = 0

        cursor.execute("SELECT Card FROM Checkpoint_submittion where id_student={} AND date BETWEEN '{}' AND '{}'"
                       .format(student_to_check_id, period[0], period[1]))
        _data = cursor.fetchall()
        yellow_cards = 0
        red_cards = 0
        for item in _data:
            if item[0] == "yellow":
                yellow_cards += 1
            elif item[0] == "red":
                red_cards += 1

        return_list.append([student_name, student_surname, avg_days,
                            grades_avg, yellow_cards, red_cards])
        data.close()
        return return_list


class Manager(Employee):
    """Class creates object mentor"""
    def __init__(self, _id, name, surname, gender, birth_date, email, login, password):
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
        super().__init__(_id, name, surname, gender, birth_date, email, login, password)

    @staticmethod
    def add_mentor():
        """
        Method allows manager to add mentor to mentors list

        Return:
             None
        """
        options = ui.Ui.get_inputs(["Name", "Surname", "Gender", "Birth date", "Email", "Login",
                                    "Password"], "Provide information about new mentor")
        if options[0].isalpha() and options[1].isalpha() and options[2] in ['male', 'female', 'not sure']:
            if options[3].isalpha():
                print('\nData should have format: YYYY-MM-DD\n')
                return
        else:
            print('\nWrong input!\nName: only letters\nSurname: only letters\n'
                  'Gender: you can choose only male, female or not sure\nData should have format: YYYY-MM-DD\n')
            return

        # new_mentor = Mentor(options[0], options[1], options[2], options[3], options[4], options[5],
        #                     options[6])

        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        cursor.execute("INSERT INTO `User`(Name, Surname, Gender, Birth_date, Email, Login, Password, User_type) "
                       "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"
                       .format(options[0], options[1], options[2], options[3],
                               options[4], options[5], options[6], "mentor"))
        data.commit()
        data.close()
        print("Mentor was added.")

    @staticmethod
    def remove_mentor():
        """
        Method allows manager to remove mentor from mentors list

        Return:
             None
        """
        options = ui.Ui.get_inputs([""], "Enter number to erase mentor from database")

        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        records = cursor.execute("SELECT COUNT(`Name`) FROM `User` WHERE `User_Type` = 'mentor'")
        records = records.fetchall()
        number_of_records = int(records[0][0])

        if int(options[0]) < 0 or int(options[0]) > number_of_records-1:
            print("There is no such mentor number on the list")
            return


        cursor.execute("SELECT * FROM `User` WHERE `User_type`='mentor'")
        mentors = cursor.fetchall()
        mentor_name = mentors[int(options[0]) - 1][1]
        mentor_surname = mentors[int(options[0]) - 1][2]
        cursor.execute("DELETE FROM `User` WHERE `Name`='{}' AND `Surname`='{}'"
                       .format(mentor_name, mentor_surname))
        data.commit()
        data.close()
        print("Mentor was erased.")

    @staticmethod
    def edit_mentor():
        """
        Method allows manager to edit mentor specific data

        Return:
             None
        """

        mentor_to_update = ui.Ui.get_inputs([""], "Enter number to edit mentor's data")

        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        records = cursor.execute("SELECT COUNT(`Name`) FROM `User` WHERE `User_Type` = 'mentor'")
        records = records.fetchall()
        number_of_records = int(records[0][0])

        if int(mentor_to_update[0]) < 1 or int(mentor_to_update[0]) > number_of_records-1:
            print("There is no such mentor number on the list")
            return
        options = ui.Ui.get_inputs(["Name", "Surname", "Gender", "Birth date", "Email", "Login",
                                    "Password"], "Edit information about student")
        if options[0].isalpha() and options[1].isalpha() and options[2] in ['male', 'female', 'not sure']:
            if options[3].isalpha():
                print('Data should have format: YYYY-MM-DD')
                return
        else:
            print('\nWrong input!\nName: only letters\nSurname: only letters\n'
                  'Gender: you can choose only male, female or not sure\nData format: YYYY-MM-DD\n')
            return

        cursor.execute("SELECT * FROM `User` WHERE `User_type`='mentor'")
        mentors = cursor.fetchall()
        mentor_to_update_name = mentors[int(mentor_to_update[0]) - 1][1]
        mentor_to_update_surname = mentors[int(mentor_to_update[0]) - 1][2]

        cursor.execute(
            "UPDATE `User` SET `Name`='{}', `Surname`='{}', `Gender`='{}', `Birth_date`='{}',"
            " `Email`='{}', `Login`='{}', `Password`='{}' "
            " WHERE "
            "`Name`='{}' AND `Surname`='{}'"
            .format(options[0], options[1], options[2], options[3],
                    options[4], options[5], options[6], mentor_to_update_name, mentor_to_update_surname ))
        data.commit()
        data.close()
        print("Update completed")

    @staticmethod
    def list_mentors():
        """
        Method allows manager to list all mentor from list

        Return:
             mentor_list
        """
        mentor_list = []
        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        cursor.execute("SELECT * FROM `User` WHERE User_type='mentor'")
        mentors = cursor.fetchall()
        n = 1
        for mentor in mentors:
            mentor_list.append([str(n) + ".", mentor[1], mentor[2]])
            n += 1
        data.commit()
        data.close()
        return mentor_list

    @staticmethod
    def view_mentors_details():
        """
        Returns mentors details list to display

        Returns:

            student detail list
        """
        mentors_details_list = []
        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        cursor.execute("SELECT * FROM `User` WHERE User_type='mentor'")
        mentors = cursor.fetchall()
        n = 1
        for mentor in mentors:
            mentors_details_list.append([str(n) + ".", mentor[1], mentor[2], mentor[3], mentor[4],
                                         mentor[5], mentor[6], mentor[7]])
            n += 1
        data.commit()
        data.close()
        return mentors_details_list

    @staticmethod
    def average_grade_for_student():
        """
        Method display average grade for choosen student


        Return:
            average grade for student

        """
        options = ui.Ui.get_inputs([""], "Enter the number of student to see his average grade")

        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        records = cursor.execute("SELECT COUNT(`Name`) FROM `User` WHERE `User_Type` = 'student'")
        records = records.fetchall()
        number_of_records = int(records[0][0])

        if int(options[0]) < 1 or int(options[0]) > number_of_records:
            print("There is no such student on the list")
            return

        average_grade_list = []
        cursor.execute("SELECT * FROM `User` WHERE `User_type`='student'")
        students = cursor.fetchall()
        student_id = students[int(options[0]) - 1][0]
        student_name = students[int(options[0]) - 1][1]
        student_surname = students[int(options[0]) - 1][2]
        record = cursor.execute("SELECT AVG(Grade) FROM `Submission` WHERE `Grade` IS NOT NULL AND `ID_Student`='{}'"
                       .format(student_id))
        record = record.fetchall()
        average_grade = int(record[0][0])
        average_grade_list.append([student_name, student_surname, average_grade])
        data.commit()
        data.close()
        return average_grade_list


    @staticmethod
    def which_mentor_is_a_monster():
        """
        Method display checkpoint cards statistics of mentors


        Return:
           list with card statistics

       """
        list_to_print = []
        cards_statistics = {}
        mentors = []
        data = sqlite3.connect("program.db")
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
            temp = [key, value[0], value[1], value[2]]
            list_to_print.append(temp)
        data.commit()
        data.close()
        return list_to_print

    @staticmethod
    def grades_stats_for_mentors():
        """
         Method display how many assignment mentor graded and what is his average grade


         Return:
            list with grade statistics

        """
        grades_statistics = []
        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        grades = cursor.execute("SELECT  `Name`, `Surname`, COUNT(`Grade`), AVG(`Grade`)"
                                            "FROM `Submission` INNER JOIN `User` ON `Submission`.ID_Mentor = User.ID"
                                            " GROUP BY `Name`")
        list_to_print = []
        grades = grades.fetchall()
        for row in grades:
            grades_statistics.append(row)
        for row in grades_statistics:
            list_to_print.append([row[0], row[1], row[2], row[3]])
        return list_to_print

    @staticmethod
    def full_stats_for_students():

        student_stats = []
        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        grades = cursor.execute("SELECT  `Name`, `Surname`, COUNT(`Grade`), AVG(`Grade`)"
                                "FROM `Submission` INNER JOIN `User` ON `Submission`.ID_Student = User.ID"
                                " GROUP BY `Name`")
        grades = grades.fetchall()
        for row in grades:
            student_stats.append(row)
        list_to_print = []
        for row in student_stats:
            list_to_print.append([row[0], row[1], row[2], row[3]])
        return list_to_print

        # # TODO: return list with percent of attendance for every student...
        # presence = cursor.execute("SELECT  `Name`, `Surname`, COUNT(CASE WHEN Presence = 1 THEN 1 ELSE NULL END)"
        #                           " FROM `Attendance` "
        #                           "INNER JOIN `User` ON Attendance.ID_Student = User.ID "
        #                           "GROUP BY `Name`")
        # presence = presence.fetchall()
        #
        # percent_of_attendance = []
        #
        # for row in presence:
        #     percent_of_attendance.append(row)
        # print (percent_of_attendance)
        #
        # number_of_all_day = cursor.execute("SELECT  `Name`, `Surname`, COUNT(Presence)"
        #                                     " FROM `Attendance` "
        #                                     "INNER JOIN `User` ON Attendance.ID_Student = User.ID "
        #                                     "GROUP BY `Name`")
        #
        # number_of_all_day = number_of_all_day.fetchall()
        # for number in number_of_all_day:
        #     for index, element in enumerate(percent_of_attendance):
        #         if number[0] == element[0] and number[1] == element[1]:
        #             percent_of_attendance[index][2] = str((element[0][2]/int(number[2])) * 100)
        #
        # print (percent_of_attendance)