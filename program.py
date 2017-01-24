import user

class Program:

    def __init__(self, employee_csv, students_csv, mentors_csv, managers_csv, assignments_csv):
        self.employee_table = self.import_csv(employee_csv)
        self.students_table = self.import_csv(students_csv)
        self.mentors_table = self.import_csv(mentors_csv)
        self.managers_table = self.import_csv(managers_csv)
        self.assignments_table = self.import_csv(assignments_csv)
        self.employee_list = []
        self.students_list = []
        self.mentors_list = []
        self.managers_list = []
        self.assignments_list = []
        self.initialize_objects()



    def import_csv(self, file_name):
        with open(file_name, "r") as file:
            lines = file.readlines()
        table = [element.replace("\n", "").split(",") for element in lines]
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


