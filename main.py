import sys
import os
import time
from geometry import *


def add_shape_menu(shapes):
    choose = int(input("Choose what kind of shape you would like to add.\n"
           "(1) Circle\n"
           "(2) Triangle\n"
           "(3) Equilateral triangle\n"
           "(4) Rectangle\n"
           "(5) Square\n"
           "(6) Regular pentagon\n"
           "(0) Go back to Main Menu.\n"))

    if choose == 1:
        r = input('Radius: ')
        shapes.add_shape(Circle(r))
        print('\nCircle added!')
        time.sleep(2)
        os.system('clear')

    if choose == 2:
        a = input('Length of first side: ')
        b = input('Length of second side: ')
        c = input('Length of third side: ')
        shapes.add_shape(Triangle(a, b, c))
        print('\nTriangle added!')
        time.sleep(2)
        os.system('clear')

    if choose == 3:
        a = input('Length of sides : ')
        shapes.add_shape(EquilateralTriangle(a))
        print('\nEquilateral Triangle added!')
        time.sleep(2)
        os.system('clear')

    if choose == 4:
        a = input('Length of first side: ')
        b = input('Length of second side: ')
        shapes.add_shape(Rectangle(a, b))
        print('\nRectangle added!')
        time.sleep(2)
        os.system('clear')

    if choose == 5:
        a = input('Length of sides : ')
        shapes.add_shape(Square(a))
        print('\nSquare added!')
        time.sleep(2)
        os.system('clear')

    if choose == 6:
        a = input('Length of sides : ')
        shapes.add_shape(RegularPentagon(a))
        print('\nRegular Pentagon added!')
        time.sleep(2)
        os.system('clear')

    if choose == 0:
        main()

def show_formulas_menu(shapes):
    choose = int(input("Choose what shape formulas would you like to see.\n"
                       "(1) Circle\n"
                       "(2) Triangle\n"
                       "(3) Equilateral triangle\n"
                       "(4) Rectangle\n"
                       "(5) Square\n"
                       "(6) Regular pentagon\n"
                       "(0) Go back to Main Menu.\n"))

    if choose == 1:
        os.system('clear')
        print('Circle perimeter formula:\n')
        print(Circle.get_perimeter_formula())
        print('\nCircle area formula:\n')
        print(Circle.get_area_formula())
        input('\nPress enter to continue')
        os.system('clear')

    if choose == 2:
        os.system('clear')
        print('Triangle perimeter formula:\n')
        print(Triangle.get_perimeter_formula())
        print('\nTriangle area formula:\n')
        print(Triangle.get_area_formula())
        input('\nPress enter to continue')
        os.system('clear')

    if choose == 3:
        os.system('clear')
        print('Equilateral Triangle perimeter formula:\n')
        print(EquilateralTriangle.get_perimeter_formula())
        print('\nEquilateral Triangle area formula:\n')
        print(EquilateralTriangle.get_area_formula())
        input('\nPress enter to continue')
        os.system('clear')

    if choose == 4:
        os.system('clear')
        print('Rectangle perimeter formula:\n')
        print(Rectangle.get_perimeter_formula())
        print('\nRectangle area formula:\n')
        print(Rectangle.get_area_formula())
        input('\nPress enter to continue')
        os.system('clear')

    if choose == 5:
        os.system('clear')
        print('Square perimeter formula:\n')
        print(Square.get_perimeter_formula())
        print('\nSquare area formula:\n')
        print(Square.get_area_formula())
        input('\nPress enter to continue')
        os.system('clear')

    if choose == 6:
        os.system('clear')
        print('Regular Pentagon perimeter formula:\n')
        print(RegularPentagon.get_perimeter_formula())
        print('\nRegular Pentagon area formula:\n')
        print(RegularPentagon.get_area_formula())
        input('\nPress enter to continue')
        os.system('clear')

    if choose == 0:
        main()


def main():

    shapes = ShapeList()  # object containing all shapes added by the user
    while True:
        # TODO: implement user interaction here. You can change the code below

        option = int(input("\tL E A R N   G E O M E T R Y \n"
                       "\tWhat do you want to do?\n"
                       "\n\t(1) Add new shape\n"
                       "\t(2) Show all shapes\n"
                       "\t(3) Show shape with the largest perimeter\n"
                       "\t(4) Show shape with the largest area\n"
                       "\t(5) Show formulas\n"
                       "\t(0) Exit program\n"))
        if option == 1:
            # Add new shape
            os.system('clear')
            add_shape_menu(shapes)

        elif option == 2:
            # Show all shapes
            os.system('clear')
            print(shapes.get_shapes_table())
        elif option == 3:
            # Show shape with the largest perimeter
            os.system('clear')
            print(shapes.get_shapes_table())
            print('\nShape with the largest perimeter:\n')
            print(shapes.get_largest_shape_by_perimeter(), '\n')
            input('\nPress enter to continue')
            os.system('clear')
        elif option == 4:
            # Show shape with the largest area
            os.system('clear')
            print(shapes.get_shapes_table())
            print('\nShape with the largest area:\n')
            print(shapes.get_largest_shape_by_area(), '\n')
            input('\nPress enter to continue')
            os.system('clear')
        elif option == 5:
            # Show formulas
            os.system('clear')
            show_formulas_menu(shapes)
            os.system('clear')
        elif option == 0:
            sys.exit()

if __name__ == "__main__":
    main()
