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

    def list_students(self):
        pass

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

    def add_mentor(self):
        pass

    def remove_mentor(self):
        pass

    def edit_mentor(self):
        pass

    def list_mentors(self, organisation):
        for mentor in organisation.mentors_list:
            print(mentor.name, mentor.surname)


    def view_mentors_details(self):
        pass
