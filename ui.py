import getpass
from data import Data
import user


class Ui:
    """This class create user interface"""
    @staticmethod
    def get_login():
        """Ask user for login and password"""
        _login = input("login: ")
        _password = getpass.getpass("password: ")
        cursor = Data.init_db()
        cursor.execute("SELECT * FROM `User` WHERE Login='{}' AND Password='{}'"
                       .format(_login, _password))
        _user = cursor.fetchone()
        if _user[8] == "mentor":
            mentor = user.Mentor(_user[0], _user[1], _user[2], _user[3], _user[4], _user[5], _user[6], _user[7])
            return mentor
        if _user[8] == "student":
            student = user.Student(_user[0], _user[1], _user[2], _user[3], _user[4], _user[5], _user[6], _user[7])
            return student
        if _user[8] == "manager":
            manager = user.Manager(_user[0], _user[1], _user[2], _user[3], _user[4], _user[5], _user[6], _user[7])
            return manager
        if _user[8] == "employee":
            employee = user.Employee(_user[0], _user[1], _user[2], _user[3], _user[4], _user[5], _user[6], _user[7])
            return employee
        return None

    @staticmethod
    def handle_manager_menu():
        """Method display menu for manager"""
        print("""
               Welcome
               What would you like to do:
               (1) List mentors
               (2) View mentors details
               (3) List students
               (4) View students details
               (5) Add mentor
               (6) Remove mentor
               (7) Edit mentors data
               (8) Show student average grade
               (9) Show mentors checkpoint cards statistics
               (10) Show mentors grades statistics
               (11) Show student stats
               (0) Exit CcMS
            """)
        option = input("Your choice: ")
        return option

    @staticmethod
    def handle_mentor_menu():
        """Method display menu for mentor"""
        print("""
               Welcome
               What would you like to do:
               (1) Check attendance
               (2) List students
               (3) View students details
               (4) Add student
               (5) Remove student
               (6) Edit students data
               (7) Add assignment
               (8) Grade submission
               (9) List teams
               (10) Add student to team
               (11) Add checkpoint submission
               (12) Check student performance
               (0) Exit CcMS
            """)
        option = input("Your choice: ")
        return option

    @staticmethod
    def handle_student_menu():
        """Method display menu for student"""
        print("""
               Welcome
               What would you like to do:
               (1) View my grades
               (2) Submit assignment
               (3) Add group assignment
               (4) Check attendance (%)
               (0) Exit CcMS
            """)
        option = input("Your choice: ")
        return option

    @staticmethod
    def handle_employee_menu():
        """Method display menu for employee"""
        print("""
               Welcome
               What would you like to do:
               (1) List students
               (2) View students details
               (0) Exit CcMS
            """)
        option = input("Your choice: ")
        return option

    @staticmethod
    def get_inputs(list_labels, title):
        """Method ask user for input"""
        inputs = []
        print(title)
        for item in list_labels:
            user_input = input(item + ' ').strip()
            inputs.append(user_input)
        return inputs

    @staticmethod
    def print_menu(title, list_options, exit_message):
        """Display option for user"""
        print(title + ':')
        for i in range(len(list_options)):
            print('  ({}) {}'.format(i + 1, list_options[i]))
        print('  (0) ' + exit_message)

    # @staticmethod
    # def print_list(organisation):
    #     for assignment in organisation.assignments_list:
    #         print(assignment)

    @staticmethod
    def print_table(table, title_list):
        """Display data in formatted table"""
        table.insert(0, title_list)
        for row_index, row in enumerate(table):
            for col_index, col in enumerate(row):
                if (type(col) == float) or (type(col) == int):
                    table[row_index][col_index] = str(col)
                    # table[row_index][col_index] = str("{0:,.2f}".format(col))
        widths = [max(map(len, col)) for col in zip(*table)]
        sum_of_widths = sum(widths) + len(table[0]) * 3 - 1 # len(table[0]) - number of |
        for row in table:
            print("-" * sum_of_widths)
            print("|" + "  ".join((val.rjust(width) + "|" for val, width in zip(row, widths))))
        print("-" * sum_of_widths)
