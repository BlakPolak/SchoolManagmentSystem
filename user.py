import ui
import assignment
import submission
import datetime

class User:
    def __init__(self, name, surname, gender, birth_date, email, login, password):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.birth_date = birth_date
        self.email = email
        self.login = login
        self.password = password

    def validate(self):
        pass

class Employee(User):
    def __init__(self, name, surname, gender, birth_date, email, login, password):
        super().__init__(name, surname, gender, birth_date, email, login, password)

    def list_students(self, organisation):
        for student in organisation.students_list:
            print(student.name, student.surname)

    def view_student_details(self, student):
        pass

class Student(User):
    def __init__(self, name, surname, gender, birth_date, email, login, password):
        super().__init__(name, surname, gender, birth_date, email, login, password)
        self.my_submissions_list = []

    def __str__(self):
        return self.name+self.surname

    def view_my_grades(self):
        pass

    def submit_assignment(self, organisation):
        list_assignment = []
        for assignment in organisation.assignments_list:
            list_assignment.append(str(assignment))
        ui.Ui.print_menu("Choose assignment to submit", list_assignment, "Exit")
        options = ui.Ui.get_inputs(["->"], "")
        picked_assignment = organisation.assignments_list[int(options[0]) - 1]
        new_submission = submission.Submission(picked_assignment)
        new_submission.provide_result()
        organisation.submissions_list.append(new_submission)


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
        attendance_list = []
        i = 0
        for student in organisation.students_list:
            students_list.append(student.surname+" "+student.name)
        options = ui.Ui.get_inputs(students_list, "Starting attendance check (mark 0 for absence, Enter otherwise")
        for student in organisation.students_list:
            attendance_list.append([student, str(datetime.date.today()), options[i]])
            #attendance_list.append([student.name, student.surname, str(datetime.date.today()), options[i]])
            i += 1


    def remove_student(self):
        pass

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
            print("No submission avaible")
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


    def view_mentors_details(self):
        pass
