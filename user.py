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
        cursor = data.Data.init_db()
        cursor.execute("SELECT * FROM `User` WHERE User_type='student'")
        students = cursor.fetchall()
        n = 1
        for student in students:
            student_list.append([str(n) + ".", student[1], student[2]])
            n += 1
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
        cursor = data.Data.init_db()
        cursor.execute("SELECT * FROM `User` WHERE User_type='student'")
        students = cursor.fetchall()
        n = 1
        for student in students:
            student_list.append([str(n) + ".", student[1], student[2], student[3],
                                 student[4], student[5], student[6], student[7]])
            n += 1
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
        grades_for_view = []
        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        cursor.execute("SELECT Grade FROM `Submission` WHERE ID_Student='{}'".format(self._id))
        grades = cursor.fetchall()
        n = 0
        for grade in grades:
            grades_for_view.append(grade)
            n += 1
        data.commit()
        data.close()
        return grades_for_view

    def list_submissions(self): #to refactor - move to class submission as class method
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
            organisation

        Return:
            list of submitted assignment

        """
        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        if len(assignment) <= 1:
            print("You have no assignment to submitt!")
            return
        assignment_id = ui.Ui.get_inputs([""], "Enter number to choose assignment to submit: ")
        # TODO: validate index from user input
        result = ui.Ui.get_inputs(["Content"], "Provide information about new assignment")
        submission_date = datetime.date.today()
        cursor.execute("INSERT INTO `Submission` (`ID_Student`, `ID_Assignment`,`Result`, `Submittion_date`) "
                       "VALUES ('{}', '{}', '{}', '{}')".format(self._id, assignment_id[0], result[0], submission_date))
        data.commit()
        data.close()

    def list_group_assignment(self):
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


    def add_group_assignment(self, group_assignment):
        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        if len(group_assignment) <= 1:
            print("You have no assignment to submitt!")
            return
        assignment_id = ui.Ui.get_inputs([""], "Enter number to choose assignment to submit: ")
        # TODO: validate index from user input
        result = ui.Ui.get_inputs(["Content"], "Provide information about new assignment")
        submission_date = datetime.date.today()
        cursor.execute("INSERT INTO `Submission` (`ID_Student`, `ID_Assignment`,`Result`, `Submittion_date`) "
                       "VALUES ('{}', '{}', '{}', '{}')".format(self._id, assignment_id[0], result[0], submission_date))
        data.commit()
        data.close()
        pass

    def check_my_attendance(self):
        student_id = self._id
        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        cursor.execute("SELECT COUNT(Presence) FROM `Attendance` WHERE ID_Student='{}' AND `Presence`= NULL".format(student_id))
        presence = cursor.fetchall()
        number_of_presence = float(presence[0][0])
        cursor.execute("SELECT COUNT(Presence) FROM `Attendance`")
        number_of_days = cursor.fetchall()
        days = float(number_of_days[0][0])
        percent_of_attendance = str((number_of_presence/days)*100)
        percent_of_attendance_list =[]
        percent_of_attendance_list.append(percent_of_attendance)
        # print(percent_of_attendance_list)
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

    def check_attendance(self, organisation):
        """
        Method allows mentor check students attendance

        Args:
            organisation
        Return:
             None
        """
        students_list = []
        i = 0
        for student in organisation.students_list:
            students_list.append(student.surname+" "+student.name)
        options = ui.Ui.get_inputs(students_list, "Starting attendance check (mark 0 for absence, Enter otherwise)")

        for student in organisation.students_list:
            new_attendance = attendance.Attendance(student, str(datetime.date.today()), options[i])
            organisation.attendance_list.append(new_attendance)
            i += 1

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

    def grade_submission(self):
        """
        Method allows mentor grade students submitted assignment

        Args:
            organisation
        Return:
             None
        """
        list_submission = []
        i = -1
        for submission_ in organisation.submissions_list:
            if not submission_.grade:
                list_submission.append(submission_)
            else:
                i += 1
        if not list_submission:
            print("No submission available")
            return
        table_to_print = []
        id_ = 1
        for submission_ in list_submission:
            table_to_print.append([str(id_), submission_.assignment.name, submission_.result])
            id_ += 1
        ui.Ui.print_table(table_to_print, ["ID", "Assignment name", "Submission result"])
        options = ui.Ui.get_inputs(["->"], "")
        if options[0].isalpha() or int(options[0]) > len(list_submission):
            print("There is no such number of assignment on list")
            return
        if options[0] == "0":
            return
        picked_submission = list_submission[int(options[0])-1]
        options = ui.Ui.get_inputs(["Enter grade for this submission: "], "")
        if options[0].isalpha() or int(options[0]) < 0 or int(options[0]) > 5:
            print("Grade can be only number in range 0-5")
            return
        picked_submission.grade = options[0]

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

        if int(options[0]) < 0 or int(options[0]) > number_of_records-1:
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
        cursor.execute("DELETE FROM `User` WHERE `Name`='{}' AND `Surname`='{}'"
                       .format(mentor_name, mentor_surname))
        data.commit()
        data.close()
        print("Mentor was erased.")

    def edit_mentor(self):
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
        options = ui.Ui.get_inputs([""], "Enter the number of student to see his average grade")

        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        records = cursor.execute("SELECT COUNT(`Name`) FROM `User` WHERE `User_Type` = 'mentor'")
        records = records.fetchall()
        number_of_records = int(records[0][0])

        if int(options[0]) < 1 or int(options[0]) > number_of_records-1:
            print("There is no such student on the list")
            return

        # mydata = c.execute('DELETE FROM Zoznam WHERE Name=?', (data3,))
        # data = sqlite3.connect("program.db")
        # cursor = data.cursor()
        # cursor.execute("DELETE FROM `User` WHERE Name = '{}' and Surname= '{}'").format(options[0], options[1])
        # data.commit()
        # data.close()
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


    def full_stats(self):
        pass