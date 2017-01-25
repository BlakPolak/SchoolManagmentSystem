import user
import ui

class Menu:


    def handle_menu(self):
        NotImplementedError()

    @staticmethod
    def create_menu(user_signed_in, organisation):
        if type(user_signed_in) == user.Student:
            menu = MenuStudent()
            menu.handle_menu()
            if menu.option == "1":
                user_signed_in.view_my_grades(organisation)
            elif menu.option == "2":
                user_signed_in.submit_assignment()
        elif type(user_signed_in) == user.Employee:
            menu = MenuEmployee()
            menu.handle_menu()
            if menu.option == "1":
                user_signed_in.list_students(organisation)
            elif menu.option == "2":
                user_signed_in.view_student_details(organisation)
        elif type(user_signed_in) == user.Manager:
            menu = MenuManager()
            menu.handle_menu()
            if menu.option == "1":
                user_signed_in.list_mentors(organisation)
            elif menu.option == "2":
                user_signed_in.list_students(organisation)
            elif menu.option == "3":
                user_signed_in.add_mentor(organisation)
            elif menu.option == "4":
                user_signed_in.remove_mentor(organisation)
            elif menu.option == "5":
                user_signed_in.edit_mentor(organisation)
        elif type(user_signed_in) == user.Mentor:
            menu = MenuMentor()
            menu.handle_menu()
            if menu.option == "1":
                user_signed_in.check_attendance(organisation)
            elif menu.option == "2":
                user_signed_in.list_students(organisation)
            elif menu.option == "3":
                user_signed_in.view_student_details(organisation)
            elif menu.option == "4":
                user_signed_in.add_student(organisation)
            elif menu.option == "5":
                user_signed_in.edit_student(organisation)
            elif menu.option == "6":
                user_signed_in.submit_assignment(organisation)
            elif menu.option == "7":
                user_signed_in.grade_assignment()

        return menu

class MenuStudent(Menu):
    def __init__(self):
        self.option = None

    def print_menu(self):
        pass

    def handle_menu(self):
        while not self.option:
            self.option = ui.Ui.handle_student_menu()

class MenuMentor(Menu):
    def __init__(self):
        self.option = None

    def handle_menu(self):
        while not self.option:
            self.option = ui.Ui.handle_mentor_menu()

class MenuManager(Menu):
    def __init__(self):
        self.option = None

    def handle_menu(self):
        while not self.option:
            self.option = ui.Ui.handle_manager_menu()





class MenuEmployee(Menu):
    def __init__(self):
        self.option = None

    def handle_menu(self):
        while not self.option:
            self.option = ui.Ui.handle_employee_menu()