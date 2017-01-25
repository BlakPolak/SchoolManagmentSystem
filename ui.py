import getpass


class Ui:
    @staticmethod
    def get_login(organisation):
        login = input("Type login: ")
        password = getpass.getpass("Type password: ")
        for manager in organisation.managers_list:
            if login == manager.login:
                if password == manager.password:
                    return manager

        for mentor in organisation.mentors_list:
            if login == mentor.login:
                if password == mentor.password:
                    return mentor

        for student in organisation.students_list:
            if login == student.login:
                if password == student.password:
                    return student

        for employee in organisation.employee_list:
            if login == employee.login:
                if password == employee.password:
                    return employee
        return None

    @staticmethod
    def handle_manager_menu():
        print("""
           Welcome
           What would you like to do:
           (1) List mentors
           (2) List students
           (3) Add mentor
           (4) Remove mentor
           (5) Edit mentor
           (0) Exit CcMS
        """)
        option = input("Your choice: ")
        return option

    @staticmethod
    def get_inputs(list_labels, title):
        inputs = []
        print(title)
        for item in list_labels:
            user_input = input(item + ' ').strip()
            inputs.append(user_input)
        return inputs

    @staticmethod
    def print_menu(title, list_options, exit_message):
        print(title + ':')
        for i in range(len(list_options)):
            print('  ({}) {}'.format(i + 1, list_options[i]))
        print('  (0) ' + exit_message)

    def print_table(table, title_list):
        table.insert(0, title_list)
        for row_index, row in enumerate(table):
            for col_index, col in enumerate(row):
                if (type(col) == float) or (type(col) == int):
                    table[row_index][col_index] = str("{0:,.2f}".format(col))
        widths = [max(map(len, col)) for col in zip(*table)]
        sum_of_widths = sum(widths) + len(table[0]) * 3 - 1 # len(table[0]) - number of |
        for row in table:
            print("-" * sum_of_widths)
            print("|" + "  ".join((val.rjust(width) + "|" for val, width in zip(row, widths))))
        print("-" * sum_of_widths)

