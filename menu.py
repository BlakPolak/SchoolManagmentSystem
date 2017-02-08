import user
import ui


class Menu:
    """
    This class creates menu object
    """
    def handle_menu(self):
        """Method display menu for signed user"""
        NotImplementedError()

    @staticmethod
    def create_menu(user_signed_in):
        """Method create menu for every user"""
        if type(user_signed_in) == user.Student:
            while True:
                menu = MenuStudent()
                menu.handle_menu()
                if menu.option == "1":
                    ui.Ui.print_table(user_signed_in.view_my_grades(), ['Index', 'Your grade assignments',
                                                                                    'Grade'])
                elif menu.option == "2":
                    user_signed_in.submit_assignment(organisation)
                elif menu.option == "0":
                    return "exit"
        elif type(user_signed_in) == user.Employee:
            while True:
                menu = MenuEmployee()
                menu.handle_menu()
                if menu.option == "1":
                    ui.Ui.print_table(user_signed_in.list_students(organisation), ["Index", "Name", "Surname"])
                elif menu.option == "2":
                    ui.Ui.print_table(user_signed_in.view_student_details(organisation), ["Index", "Name", "Surname",
                                                                                          "Gender", "Date of birth",
                                                                                          "Email", "Login", "Password"])
                elif menu.option == "0":
                    return "exit"
        elif type(user_signed_in) == user.Manager:
            while True:
                menu = MenuManager()
                menu.handle_menu()
                if menu.option == "1":
                    ui.Ui.print_table(user_signed_in.list_mentors(organisation), ["Index", "Name", "Surname"])
                elif menu.option == "2":
                    ui.Ui.print_table(user_signed_in.view_mentors_details(organisation), ["Index", "Name", "Surname",
                                                                                          "Gender", "Birth date",
                                                                                          "Mail", "Login", "Password"])
                elif menu.option == "3":
                    ui.Ui.print_table(user_signed_in.list_students(organisation), ["Index", "Name", "Surname"])
                elif menu.option == "4":
                    ui.Ui.print_table(user_signed_in.view_student_details(organisation), ["Index", "Name", "Surname",
                                                                                          "Gender", "Birth date",
                                                                                          "Mail", "Login", "Password"])
                elif menu.option == "5":
                    user_signed_in.add_mentor(organisation)
                elif menu.option == "6":
                    ui.Ui.print_table(user_signed_in.list_mentors(organisation), ["Index", "Name", "Surname"])
                    user_signed_in.remove_mentor(organisation)
                elif menu.option == "7":
                    ui.Ui.print_table(user_signed_in.list_mentors(organisation), ["Index", "Name", "Surname"])
                    user_signed_in.edit_mentor(organisation)
                elif menu.option == "0":
                    return "exit"
        elif type(user_signed_in) == user.Mentor:
            while True:
                menu = MenuMentor()
                menu.handle_menu()
                if menu.option == "1":
                    user_signed_in.check_attendance(organisation)
                elif menu.option == "2":
                    ui.Ui.print_table(user_signed_in.list_students(organisation), ["Index", "Name", "Surname"])
                elif menu.option == "3":
                    ui.Ui.print_table(user_signed_in.view_student_details(organisation), ["Index", "Name", "Surname",
                                                                                          "Gender", "Date of birth",
                                                                                          "Email", "Login", "Password"])
                elif menu.option == "4":
                    user_signed_in.add_student(organisation)
                elif menu.option == "5":
                    ui.Ui.print_table(user_signed_in.list_students(organisation), ["Index", "Name", "Surname"])
                    user_signed_in.remove_student(organisation)
                elif menu.option == "6":
                    ui.Ui.print_table(user_signed_in.list_students(organisation), ["Index", "Name", "Surname"])
                    user_signed_in.edit_student(organisation)
                elif menu.option == "7":
                    user_signed_in.add_assignment(organisation)
                elif menu.option == "8":
                    user_signed_in.grade_submission(organisation)
                elif menu.option == "0":
                    return "exit"
            return menu


class MenuStudent(Menu):
    """
    This class create student menu object.
    """
    def __init__(self):
        """Initialize object student menu"""
        self.option = None

    def handle_menu(self):
        """Method display menu for signed user"""
        while not self.option:
            self.option = ui.Ui.handle_student_menu()


class MenuMentor(Menu):
    """
    This class create mentor menu object.
    """
    def __init__(self):
        """Initialize object student menu"""
        self.option = None

    def handle_menu(self):
        """Method display menu for signed user"""
        while not self.option:
            self.option = ui.Ui.handle_mentor_menu()


class MenuManager(Menu):
    """
    This class create manager menu object.
    """
    def __init__(self):
        """Initialize object student menu"""
        self.option = None

    def handle_menu(self):
        """Method display menu for signed user"""
        while not self.option:
            self.option = ui.Ui.handle_manager_menu()


class MenuEmployee(Menu):
    """
    This class create employee menu object.
    """
    def __init__(self):
        """Initialize object student menu"""
        self.option = None

    def handle_menu(self):
        """Method display menu for signed user"""
        while not self.option:
            self.option = ui.Ui.handle_employee_menu()