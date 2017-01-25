import ui
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

    def choose_assignment(self):
        pass

    def view_my_grades(self):
        pass

    def submit_assignment(self):
        pass


class Mentor(Employee):
    def __init__(self, name, surname, gender, birth_date, email, login, password):
        super().__init__(name, surname, gender, birth_date, email, login, password)

    def add_student(self):
        pass

    def remove_student(self):
        pass

    def edit_student(self):
        pass

    def grade_submission(self):
        pass

    def add_assignment(self):
        pass

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
