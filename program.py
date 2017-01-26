import user
import assignment
import submission
import attendance
import datetime

class Program:

    def __init__(self, employee_csv, students_csv, mentors_csv, managers_csv, assignments_csv,
                 submissions_csv, attendance_csv):
        self.employee_table = self.import_csv(employee_csv)
        self.students_table = self.import_csv(students_csv)
        self.mentors_table = self.import_csv(mentors_csv)
        self.managers_table = self.import_csv(managers_csv)
        self.assignments_table = self.import_csv(assignments_csv)
        self.submissions_table = self.import_csv(submissions_csv)
        self.attendance_table = self.import_csv(attendance_csv)
        self.employee_list = []
        self.students_list = []
        self.mentors_list = []
        self.managers_list = []
        self.assignments_list = []
        self.submissions_list = []
        self.attendance_list = []
        self.initialize_objects()


    def import_csv(self, file_name):
        with open(file_name, "r") as file:
            lines = file.readlines()
        table = [element.replace("\n", "").split(";") for element in lines]
        return table


    def write_csv(self, file_name, table):
        with open(file_name, "w") as file:
            for record in table:
                row = ';'.join(record)
                file.write(row + "\n")

    def initialize_objects(self):
        for row in self.employee_table:
            name = row[0]
            surname = row[1]
            gender = row[2]
            birth_date = row[3]
            email = row[4]
            login = row[5]
            password = row[6]
            new_employee = user.Employee(name, surname, gender, birth_date, email, login, password)
            self.employee_list.append(new_employee)

        for row in self.students_table:
            name = row[0]
            surname = row[1]
            gender = row[2]
            birth_date = row[3]
            email = row[4]
            login = row[5]
            password = row[6]
            new_student = user.Student(name, surname, gender, birth_date, email, login, password)
            self.students_list.append(new_student)

        for row in self.mentors_table:
            name = row[0]
            surname = row[1]
            gender = row[2]
            birth_date = row[3]
            email = row[4]
            login = row[5]
            password = row[6]
            new_mentor = user.Mentor(name, surname, gender, birth_date, email, login, password)
            self.mentors_list.append(new_mentor)

        for row in self.managers_table:
            name = row[0]
            surname = row[1]
            gender = row[2]
            birth_date = row[3]
            email = row[4]
            login = row[5]
            password = row[6]
            new_manager = user.Manager(name, surname, gender, birth_date, email, login, password)
            self.managers_list.append(new_manager)

        for row in self.assignments_table:
            name = row[0]
            max_points = row[1]
            delivery_date = row[2]
            content = row[3]
            new_assignment = assignment.Assignment(name, max_points, delivery_date, content)
            self.assignments_list.append(new_assignment)

        assignment_related = None
        for row in self.submissions_table:
            assignment_name_related = row[0]
            for assignment_ in self.assignments_list:
                if assignment_.name == assignment_name_related:
                    assignment_related = assignment_
                    break
            if assignment_related:
                student_name = row[1]
                student_surname = row[2]
                submission_date = row[3]
                result = row[4]
                grade = row[5]
                for student in self.students_list:
                    if student.name == student_name:
                        if student.surname == student_surname:
                            student_to_append= student
                if assignment_related:
                    new_submission = submission.Submission(assignment_related, student_to_append, submission_date, result, grade)
                    self.submissions_list.append(new_submission)

        for row in self.attendance_table:
            student_name_related = row[0]
            student_surname_related = row[1]
            for student in self.students_list:
                if student.name == student_name_related:
                    if student.surname == student_surname_related:
                        student_related = student
                        break
            date = row[2]
            was_present = row[3]
            new_attendance = attendance.Attendance(student_related, date, was_present)
            self.attendance_list.append(new_attendance)

    def export_data(self):
        employee_table = []
        students_table = []
        mentors_table = []
        managers_table = []
        assignments_table = []
        submissions_table = []
        attendance_table = []

        for employee in self.employee_list:
            row = [employee.name, employee.surname, employee.gender, employee.birth_date, employee.email,
                   employee.login, employee.password]
            employee_table.append(row)

        for mentor in self.mentors_list:
            row = [mentor.name, mentor.surname, mentor.gender, mentor.birth_date, mentor.email,
                   mentor.login, mentor.password]
            mentors_table.append(row)

        for student in self.students_list:
            row = [student.name, student.surname, student.gender, student.birth_date, student.email,
                   student.login, student.password]
            students_table.append(row)

        for manager in self.managers_list:
            row = [manager.name, manager.surname, manager.gender, manager.birth_date, manager.email,
                   manager.login, manager.password]
            managers_table.append(row)

        for assignment in self.assignments_list:
            row = [assignment.name, assignment.max_points, assignment.delivery_date, assignment.content]
            assignments_table.append(row)

        for submission in self.submissions_list:
            row = [submission.assignment.name, submission.student.name, submission.student.surname,
                   str(submission.submission_date), str(submission.result), str(submission.grade)]
            submissions_table.append(row)

        for attendance in self.attendance_list:
            row = [attendance.student.name, attendance.student.surname, str(attendance.date), attendance.was_present]
            attendance_table.append(row)

        self.write_csv("csv_lists/employee_list.csv", employee_table)
        self.write_csv("csv_lists/students_list.csv", students_table)
        self.write_csv("csv_lists/mentors_list.csv", mentors_table)
        self.write_csv("csv_lists/managers_list.csv", managers_table)
        self.write_csv("csv_lists/assignments_list.csv", assignments_table)
        self.write_csv("csv_lists/submissions_list.csv", submissions_table)
        self.write_csv("csv_lists/attendance_list.csv", attendance_table)
