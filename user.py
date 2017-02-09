import ui
import sqlite3
import data
import assignment
import submission
import datetime
import attendance
import data
import sqlite3


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

            Args:
                organisation

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


    def view_student_details(self):
        """
        Returns students details list to display

            Args:
                organisation

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

        Args:
            organisation

        Return:
            list of submitted assignment with grades

        """
        student_id = self._id
        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        cursor.execute("SELECT Grade FROM `Submission` WHERE ID_Student='{}'".format(student_id))
        grades = cursor.fetchall()
        # print(grades)
        data.commit()
        data.close()
        return grades

    def submit_assignment(self):
        """
        Method allows student to submit assignment

        Args:
            organisation

        Return:
            list of submitted assignment

        """

        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        cursor.execute("INSERT INTO `Assignment` (`ID`, `Name`, `Type`, `Max_points`, `Delivery_date`, `Content`) "
                       "VALUES ('{}', '{}', '{}', '{}', '{}', '{}')"
                       .format(options[0], options[1], options[2], options[3],
                               options[4], option[5]))
        submission = cursor.fetchall()
        data.commit()
        data.close()
        #
        # submission_list_done = []
        # for submission_ in organisation.submissions_list:
        #     if submission_.student.name == self.name and submission_.student.surname == self.surname:
        #         if submission_.grade == "":
        #             submission_list_done.append(submission_.assignment) # submission_list_done -
        #                                                                 # graded assignments of actual student
        # final_list = [assignment for assignment in organisation.assignments_list if assignment not in submission_list_done]
        # if final_list:
        #     table_to_print = []
        #     id_ = 1
        #     for assignment in final_list:
        #         table_to_print.append([str(id_), assignment.name, assignment.max_points,
        #                                assignment.delivery_date, assignment.content])
        #         id_ += 1
        #     ui.Ui.print_table(table_to_print, ["ID", "Assignment name", "Assignment max points",
        #                                        "delivery date", "Content"])
        #     options = ui.Ui.get_inputs(["->"], "")
        #     if options[0] == "0":
        #         return
        #     picked_assignment = final_list[int(options[0]) - 1]
        #     new_submission = submission.Submission(picked_assignment, self)
        #     new_submission.provide_result()
        #     organisation.submissions_list.append(new_submission)
        # else:
        #     print("No assignments left.")
        return


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
            organisation
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
            organisation
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
            cursor.execute("""INSERT INTO attendance (ID_Student, Date, Presence) VALUES ({}, {}, {})""".format(ids[i], str(datetime.date.today()), presence))
            i += 1
        data.commit()
        data.close()
        print("Checking attendance finished")

    def remove_student(self):
        """
        Method allows mentor remove students from students list

        Args:
            organisation
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
            organisation
        Return:
             None
        """
        self.list_students()
        choosed_student = ui.Ui.get_inputs([""], "Enter number to edit student's data")
        if choosed_student[0] == "0" or int(choosed_student[0]) > len(self.list_students()):
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
        Method allows mentor grade students submitted assignment

        Args:
            organisation
        Return:
             None
        """
        return_list = []
        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        submissions_not_graded = cursor.execute(
"SELECT Assignment.ID, Assignment.Name, Assignment.delivery_date, User.Name, User.Surname, Submission.Submittion_date "
"FROM Submission "
"INNER JOIN Assignment ON Assignment.ID=Submission.ID "
"INNER JOIN User ON user.ID=Submission.ID_Student "
"WHERE Submission.Grade IS NULL").fetchall()
        if len(submissions_not_graded) == 0:
            print("No submissions to grade")
            return None
        for submission in submissions_not_graded:
            return_list.append([submission[0], submission[1], submission[2],
                                submission[3], submission[4], submission[5]])
        data.close()
        return return_list

    def grade_submission(self):
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
        Method allows mentor add new assignment to assignment list

        Args:
            organisation
        Return:
             None
        """
        options = ui.Ui.get_inputs(["Name", "Type", "Max. points to receive", "Delivery date", "Content"],
                                    "Provide information about new assignment")
        # if options[0].isalpha() and options[1].isdigit():
        #     if options[2].isalpha():
        #         print('\nData format: YYYY-MM-DD\n')
        #         return
        # else:
        #     print('\nWrong input!\nName: only letters\nMax Points: only numbers\nData should have format: YYYY-MM-DD\n')
        #     return

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
        team_list = []
        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        cursor.execute("SELECT team_name, name, surname FROM teams "
                       "INNER JOIN user ON teams.id_student=user.id ORDER BY team_name")
        teams = cursor.fetchall()
        n = 1
        for team in teams:
            team_list.append([str(n) + ".", team[0], team[1], team[2]])
            n += 1
        data.close()
        return team_list


    def add_team(self):
        choosed_student_and_team = ui.Ui.get_inputs(["Enter number to add student to team: ", "Team name for student: "], "")
        if int(choosed_student_and_team[0]) < 0 or int(choosed_student_and_team[0]) > len(self.list_students()):
            print("There is no such student number on the list")
            return

        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        cursor.execute("SELECT * FROM `user` WHERE `user_type`='student'")
        students = cursor.fetchall()
        student_to_add_id = students[int(choosed_student_and_team[0]) - 1][0] #id student to add to team
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

    def list_students_with_card(self):
        """
        Return student list to display

            Args:
                organisation

            Returns:

                student list
        """
        student_list = []
        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        cursor.execute("SELECT user.name, user.surname, Checkpoint_submittion.Card, Checkpoint_assignment.Name"
                       " FROM User "
                       "INNER JOIN Checkpoint_submittion INNER JOIN Checkpoint_assignment "
                       "ON user.User_type='student'")
        students = cursor.fetchall()
        n = 1
        for student in students:
            student_list.append([str(n) + ".", student[0], student[1], student[2], student[3]])
            n += 1
        data.close()
        return student_list




    def list_checkpoint_assignments(self):
        checkpoint_assignments_list = []
        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        cursor.execute("SELECT * FROM Checkpoint_assignment")
        assignments = cursor.fetchall()
        n = 1
        for assignment in assignments:
            checkpoint_assignments_list.append([str(n) + ".", assignment[1], assignment[2]])
            n += 1
        data.close()
        return checkpoint_assignments_list

    def get_checkpoint_id(self):
        choosed_checkpoint = ui.Ui.get_inputs([""], "Choose checkpoint to grade student")
        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        cursor.execute("SELECT * FROM Checkpoint_assignment")
        checkpoint = cursor.fetchall()
        checkpoint_id = checkpoint[int(choosed_checkpoint[0]) - 1][0]
        data.close()
        return checkpoint_id

    def add_checkpoint_submission(self, checkpoint_assignment_id):
        choosed_student = ui.Ui.get_inputs(
            [""], "Choose student to add checkpoint results")
        if int(choosed_student[0]) < 0 or int(choosed_student[0]) > len(self.list_students()):
            print("There is no such student number on the list")
            return
        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        cursor.execute("SELECT * FROM `user` WHERE `user_type`='student'")
        students = cursor.fetchall()
        student_to_add_id = students[int(choosed_student[0]) - 1][0]  # id student choosed

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

    def add_mentor(self):
        """
        Method allows manager to add mentor to mentors list

        Args:
            organisation
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

    def remove_mentor(self):
        """
        Method allows manager to remove mentor from mentors list

        Args:
            organisation
        Return:
             None
        """
        options = ui.Ui.get_inputs([""], "Enter number to erase mentor from database")

        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        records = cursor.execute("SELECT COUNT(`Name`) FROM `User` WHERE `User_Type` = 'mentor'")
        records = records.fetchall()
        number_of_records = int(records[0][0])

        if int(options[0]) < 0 or int(options[0]) > number_of_records:
            print("There is no such mentor number on the list")
            return


        #     mydata = c.execute('DELETE FROM Zoznam WHERE Name=?', (data3,))
        # data = sqlite3.connect("program.db")
        # cursor = data.cursor()
        # cursor.execute("DELETE FROM `User` WHERE Name = '{}' and Surname= '{}'").format(options[0], options[1])
        # data.commit()
        # data.close()

        cursor.execute("SELECT * FROM `User` WHERE `User_type`='mentor'")
        mentors = cursor.fetchall()
        mentor_name = mentors[int(options[0]) - 1][1]
        mentor_surname = mentors[int(options[0]) - 1][2]
        print(mentor_name, mentor_surname)
        cursor.execute("DELETE FROM `User` WHERE `Name`='{}' AND `Surname`='{}'"
                       .format(mentor_name, mentor_surname))
        data.commit()
        data.close()
        print("Mentor was erased.")

    def edit_mentor(self, organisation):
        """
        Method allows manager to edit mentor specific data

        Args:
            organisation
        Return:
             None
        """

        mentor_to_update = ui.Ui.get_inputs([""], "Enter number to edit mentor's data")

        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        records = cursor.execute("SELECT COUNT(`Name`) FROM `User` WHERE `User_Type` = 'mentor'")
        records = records.fetchall()
        number_of_records = int(records[0][0])

        if int(mentor_to_update[0]) < 1 or int(mentor_to_update[0]) > number_of_records:
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

    def list_mentors(self):
        """
        Method allows manager to list all mentor from list

        Args:
            organisation
        Return:
             None
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


    def view_mentors_details(self):
        """
        Returns mentors details list to display

        Args:
            organisation

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

    def average_grade_for_student(self):
        """
                Method display list of grades for choosen student

                Args:
                    organisation

                Return:
                    list of submitted assignment with grades

                """
        options = ui.Ui.get_inputs([""], "Enter the number of student to see his assessment")

        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        records = cursor.execute("SELECT COUNT(`Name`) FROM `User` WHERE `User_Type` = 'mentor'")
        records = records.fetchall()
        number_of_records = int(records[0][0])

        if int(options[0]) < 0 or int(options[0]) > number_of_records:
            print("There is no such student on the list")
            return

        # mydata = c.execute('DELETE FROM Zoznam WHERE Name=?', (data3,))
        # data = sqlite3.connect("program.db")
        # cursor = data.cursor()
        # cursor.execute("DELETE FROM `User` WHERE Name = '{}' and Surname= '{}'").format(options[0], options[1])
        # data.commit()
        # data.close()

        cursor.execute("SELECT * FROM `User` WHERE `User_type`='student'")
        students = cursor.fetchall()
        student_id = students[int(options[0]) - 1][0]
        cursor.execute("SELECT AVG(Grade) FROM `Submission` WHERE `ID_Student`='{}'"
                       .format(student_id))
        data.commit()
        data.close()
        print("Mentor was erased.")
    def full_stats(self):
        pass