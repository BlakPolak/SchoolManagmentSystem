import ui
import assignment
import submission
import datetime
import attendance

class User:
    def __init__(self, name, surname, gender, birth_date, email, login, password):
        self.name = self.check_if_correct(name, str)
        self.surname = self.check_if_correct(surname, str)
        self.check_gender(gender)
        self.gender = gender
        self.date_validate(birth_date)
        self.birth_date = birth_date
        self.email = email  #checking email and login to do in the future
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
            raise TypeError
        elif type(validate) == check_type:
            if validate.isdigit():
                validate = int(validate)
                return validate
            elif all(i.isalpha() or i.isspace() for i in validate):
                return validate
            else:
                raise TypeError

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
            raise TypeError

    def date_validate(self, birth_date):
        try:
            if birth_date != datetime.datetime.strptime(birth_date, '%Y-%m-%d').strftime('%Y-%m-%d'):
                raise ValueError
            return True
        except ValueError:
            return False


class Employee(User):

    def __init__(self, name, surname, gender, birth_date, email, login, password):
        super().__init__(name, surname, gender, birth_date, email, login, password)

    def list_students(self, organisation):
        student_list = []
        n = 1
        while n < len(organisation.students_list):
            for student in organisation.students_list:
                student_list. append([str(n) + ".", student.name, student.surname])
                n += 1
        return student_list

    def view_student_details(self, organisation):
        student_details = []
        for student in organisation.students_list:
            print(student.name, student.surname, student.gender, student.birth_date, student.email, student.login,
                  student.password)


class Student(User):
    def __init__(self, name, surname, gender, birth_date, email, login, password):
        super().__init__(name, surname, gender, birth_date, email, login, password)
        self.my_submissions_list = []

    def __str__(self):
        return self.name+self.surname

    def view_my_grades(self, organisation):
        my_submissions_list = []
        i = 0
        for submission_ in organisation.submissions_list:
            if submission_.student.name == self.name and submission_.student.surname == self.surname:
                if submission_.grade:
                    submission_to_add = [str(i+1), submission_.assignment.name, submission_.grade]
                    my_submissions_list.append(submission_to_add)
                    i += 1
        return my_submissions_list

    def submit_assignment(self, organisation):
        submission_list_done = []
        for submission_ in organisation.submissions_list:
            if submission_.student.name == self.name and submission_.student.surname == self.surname:
                if submission_.grade == "":
                    submission_list_done.append(submission_.assignment) # submission_list_done -
                                                                        # graded assignments of actual student
        final_list = [assignment for assignment in organisation.assignments_list if assignment not in submission_list_done]
        if final_list:
            #ui.Ui.print_menu("Choose assignment to submit", final_list, "Exit")
            table_to_print = []
            id_ = 1
            for assignment in final_list:
                table_to_print.append([str(id_), assignment.name, assignment.max_points,
                                       assignment.delivery_date, assignment.content])
                id_ += 1
            ui.Ui.print_table(table_to_print, ["ID", "Assignment name", "Assignment max points",
                                               "delivery date", "Content"])
            options = ui.Ui.get_inputs(["->"], "")
            if options[0] == "0":
                return
            picked_assignment = final_list[int(options[0]) - 1]
            new_submission = submission.Submission(picked_assignment, self)
            new_submission.provide_result()
            organisation.submissions_list.append(new_submission)
        else:
            print("No assignments left.")
            return


class Mentor(Employee):
    def __init__(self, name, surname, gender, birth_date, email, login, password):
        super().__init__(name, surname, gender, birth_date, email, login, password)

    def add_student(self, organisation):
        options = ui.Ui.get_inputs(["Name", "Surname", "Gender", "Birth date", "Email", "Login",
                                    "Password"], "Provide information about new student")
        new_student = Student(options[0], options[1], options[2], options[3], options[4], options[5],
                            options[6])
        organisation.students_list.append(new_student)
        print("Student was added.")

    def check_attendance(self, organisation):
        students_list = []
        #attendance_list = []
        i = 0
        for student in organisation.students_list:
            students_list.append(student.surname+" "+student.name)
        options = ui.Ui.get_inputs(students_list, "Starting attendance check (mark 0 for absence, Enter otherwise")
        for student in organisation.students_list:
            new_attendance = attendance.Attendance(student, str(datetime.date.today()), options[i])
            #organisation.attendance_list.append([student, str(datetime.date.today()), options[i]])
            organisation.attendance_list.append(new_attendance)
            i += 1

    def remove_student(self, organisation):  # add funcionality
        self.list_students(organisation)
        options = ui.Ui.get_inputs([""], "Enter number to erase student from database")
        del organisation.students_list[int(options[0]) - 1]
        print("Student was erased.")
        #self.list_mentors(organisation)

    def edit_student(self, organisation):
        self.list_students(organisation)
        options = ui.Ui.get_inputs([""], "Enter number to edit student's data")
        student = organisation.students_list[int(options[0]) - 1]
        options = ui.Ui.get_inputs(["Name", "Surname", "Gender", "Birth date", "Email", "Login",
                                    "Password"], "Edit information about student")
        student.name = options[0]
        student.surname = options[1]
        student.gender = options[2]
        student.birth_date = options[3]
        student.email = options[4]
        student.login = options[5]
        student.password = options[6]
        print("Update completed")
        self.list_students(organisation)

    def grade_submission(self, organisation):
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
        ui.Ui.print_menu("Choose submission to grade", list_submission, "Exit")
        options = ui.Ui.get_inputs(["->"], "")
        picked_submission = organisation.submissions_list[int(options[0])+i]
        options = ui.Ui.get_inputs(["Enter grade for this submission"], "")
        picked_submission.grade = options[0]

    def add_assignment(self, organisation):
        options = ui.Ui.get_inputs(["Name", "Max. points to receive", "Delivery date", "Content"],
                                    "Provide information about new assignment")
        new_assignment = assignment.Assignment(options[0], options[1], options[2], options[3])
        organisation.assignments_list.append(new_assignment)

class Manager(Employee):
    def __init__(self, name, surname, gender, birth_date, email, login, password):
        super().__init__(name, surname, gender, birth_date, email, login, password)

    def add_mentor(self, organisation):
        #ui.Ui.print_menu()
        options = ui.Ui.get_inputs(["Name", "Surname", "Gender", "Birth date", "Email", "Login",
                                    "Password"], "Provide information about new mentor")
        new_mentor = Mentor(options[0], options[1], options[2], options[3], options[4], options[5],
                            options[6])
        organisation.mentors_list.append(new_mentor)
        print("Mentor was added.")

    def remove_mentor(self, organisation):
        self.list_mentors(organisation)
        options = ui.Ui.get_inputs([""], "Enter number to erase mentor from database")
        del organisation.mentors_list[int(options[0]) - 1]
        print("Mentor was erased.")
        #self.list_mentors(organisation)

    def edit_mentor(self, organisation):
        self.list_mentors(organisation)
        options = ui.Ui.get_inputs([""], "Enter number to edit mentor's data")
        mentor = organisation.mentors_list[int(options[0]) - 1]
        options = ui.Ui.get_inputs(["Name", "Surname", "Gender", "Birth date", "Email", "Login",
                                    "Password"], "Edit information about mentor")
        mentor.name = options[0]
        mentor.surname = options[1]
        mentor.gender = options[2]
        mentor.birth_date = options[3]
        mentor.email = options[4]
        mentor.login = options[5]
        mentor.password = options[6]
        print("Update completed")
        self.list_mentors(organisation)

    def list_mentors(self, organisation):
        i = 0
        for mentor in organisation.mentors_list:
            i += 1
            print(str(i), mentor.name, mentor.surname)

    def view_mentors_details(self, organisation):
        for mentor in organisation.mentors_list:
            print(mentor.name, mentor.surname, mentor.gender, mentor.birth_date, mentor.email, mentor.login,
                  mentor.password)
