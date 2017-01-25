import user
import ui

class Menu:


    def handle_menu(self):
        NotImplementedError()

    @staticmethod
    def create_menu(user_signed_in, organisation):
        if type(user_signed_in) == user.Student:
            MenuStudent()
        elif type(user_signed_in) == user.Employee:
            MenuEmployee()
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
            MenuMentor()
        return menu

class MenuStudent(Menu):

    def print_menu(self):
        pass

class MenuMentor(Menu):
    def print_menu(self):
        pass

class MenuManager(Menu):
    def __init__(self):
        self.option = None

    def handle_menu(self):
        while not self.option:
            self.option = ui.Ui.handle_manager_menu()





class MenuEmployee(Menu):
    def print_menu(self):
        pass