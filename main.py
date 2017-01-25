import program
import user
import ui
import menu


def main():

    codecool = program.Program("csv_lists/employee_list.csv",
                               "csv_lists/students_list.csv",
                               "csv_lists/mentors_list.csv",
                               "csv_lists/managers_list.csv",
                               "csv_lists/assignments_list.csv")

    user_signed_in = None
    while not user_signed_in:
        user_signed_in = ui.Ui.get_login(codecool)
        while True:
            if user_signed_in:
                print("Welcome "+user_signed_in.name)
                user_menu = menu.Menu.create_menu(user_signed_in, codecool)




            else:
                print("Wrong login input. Please try again.")


if __name__ == "__main__":
    main()