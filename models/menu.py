from models import user, ui


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
                    assignment = user_signed_in.list_assignments_to_submit()
                    ui.Ui.print_table(assignment, ['Index', 'Assignment name', 'Assignment type',
                                                                                    'Delivery date'])
                    user_signed_in.submit_assignment(assignment)
                elif menu.option == "3":
                    team = user_signed_in.find_student_team()
                    teammates = user_signed_in.find_students_teammates(team)
                    group_submission = user_signed_in.list_group_assignment()
                    ui.Ui.print_table(group_submission, ['Index', 'Assignment name', 'Assignment type',
                                                                                    'Delivery date'])
                    user_signed_in.add_group_assignment(teammates, group_submission)
                elif menu.option == "4":
                    ui.Ui.print_table(user_signed_in.check_my_attendance(), ['Attendance in %'])
                elif menu.option == "0":
                    return "exit"
        elif type(user_signed_in) == user.Employee:
            while True:
                menu = MenuEmployee()
                menu.handle_menu()
                if menu.option == "1":
                    ui.Ui.print_table(user_signed_in.list_students(), ["Index", "Name", "Surname"])
                elif menu.option == "2":
                    ui.Ui.print_table(user_signed_in.view_student_details(), ["Index", "Name", "Surname",
                                                                                          "Gender", "Date of birth",
                                                                                          "Email", "Login", "Password"])
                elif menu.option == "0":
                    return "exit"
        elif type(user_signed_in) == user.Manager:
            while True:
                menu = MenuManager()
                menu.handle_menu()
                if menu.option == "1":
                    ui.Ui.print_table(user_signed_in.list_mentors(), ["Index", "Name", "Surname"])
                elif menu.option == "2":
                    ui.Ui.print_table(user_signed_in.view_mentors_details(), ["Index", "Name", "Surname",
                                                                                          "Gender", "Birth date",
                                                                                          "Mail", "Login", "Password"])
                elif menu.option == "3":
                    ui.Ui.print_table(user_signed_in.list_students(), ["Index", "Name", "Surname"])
                elif menu.option == "4":
                    ui.Ui.print_table(user_signed_in.view_student_details(), ["Index", "Name", "Surname",
                                                                                          "Gender", "Birth date",
                                                                                          "Mail", "Login", "Password"])
                elif menu.option == "5":
                    user_signed_in.add_mentor()
                elif menu.option == "6":
                    ui.Ui.print_table(user_signed_in.list_mentors(), ["Index", "Name", "Surname"])
                    user_signed_in.remove_mentor()
                elif menu.option == "7":
                    ui.Ui.print_table(user_signed_in.list_mentors(), ["Index", "Name", "Surname"])
                    user_signed_in.edit_mentor()
                elif menu.option == "8":
                    ui.Ui.print_table(user_signed_in.list_students(), ["Index", "Name", "Surname"])
                    signed_user = user_signed_in.average_grade_for_student()
                    if signed_user:
                        ui.Ui.print_table(signed_user, ["Name", "Surname", "Average grade"])
                elif menu.option == "9": #card stats for mentor
                    signed_user = user_signed_in.which_mentor_is_a_monster()
                    if signed_user:
                        ui.Ui.print_table(signed_user, ["Name and Surname", "Red cards", "Yellow cards", "Green cards"])
                elif menu.option == "10": #card stats for mentor
                    signed_user = user_signed_in.grades_stats_for_mentors()
                    if signed_user:
                        ui.Ui.print_table(signed_user, ["Name", "Surname", "Number of graded assignments",
                                                        "Average rating of mentor"])
                elif menu.option == "11": #full stats for student
                    ui.Ui.print_table(user_signed_in.list_students(), ["Index", "Name", "Surname"])
                    signed_user = user_signed_in.full_stats_for_student()
                    if signed_user:
                        ui.Ui.print_table(signed_user, ["Name", "Surname", "Amount of graded assignments",
                                                        "Average Grade"])
                elif menu.option == "0":
                    return "exit"
        elif type(user_signed_in) == user.Mentor:
            while True:
                menu = MenuMentor()
                menu.handle_menu()
                if menu.option == "1":
                    user_signed_in.check_attendance()
                elif menu.option == "2":
                    ui.Ui.print_table(user_signed_in.list_students(), ["Index", "Name", "Surname"])
                elif menu.option == "3":
                    ui.Ui.print_table(user_signed_in.view_student_details(), ["Index", "Name", "Surname",
                                                                                          "Gender", "Date of birth",
                                                                                          "Email", "Login", "Password"])
                elif menu.option == "4":
                    user_signed_in.add_student()
                elif menu.option == "5":
                    ui.Ui.print_table(user_signed_in.list_students(), ["Index", "Name", "Surname"])
                    user_signed_in.remove_student()
                elif menu.option == "6":
                    ui.Ui.print_table(user_signed_in.list_students(), ["Index", "Name", "Surname"])
                    user_signed_in.edit_student()
                elif menu.option == "7":
                    user_signed_in.add_assignment()
                elif menu.option == "8":
                    print_submissions = user_signed_in.show_submissions_to_grade()
                    if print_submissions is not None:
                        ui.Ui.print_table(print_submissions,
                                          ["Index", "Assignment", "Delivery date", "Student name", "Student surname", "Submition date"])
                        user_signed_in.grade_submission()
                elif menu.option == "9":
                    ui.Ui.print_table(user_signed_in.list_teams(), ["Index", "Team", "Name", "Surname"])

                elif menu.option == "10":
                    ui.Ui.print_table(user_signed_in.list_teams(), ["Index", "Team", "Name", "Surname"])
                    user_signed_in.add_team()
                elif menu.option == "11":
                    ui.Ui.print_table(user_signed_in.list_checkpoint_assignments(), ["Index", "Name", "Assignments"])
                    checkpoint_assignment_id = user_signed_in.get_checkpoint_id()
                    ui.Ui.print_table(user_signed_in.list_students_simple_view(), ["Index", "Name", "Surname"])
                    user_signed_in.add_checkpoint_submission(checkpoint_assignment_id)
                elif menu.option == "12":
                    ui.Ui.print_table(user_signed_in.list_students_simple_view(), ["Index", "Name", "Surname"])
                    stats_table = user_signed_in.check_student_performance()
                    ui.Ui.print_table(stats_table, ["Name", "Surname", "Avg presence", "Avg grades", "Yellow cards", "Red cards"])
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