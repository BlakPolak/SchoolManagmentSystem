import sys
from geometry import *


def main():

    shapes = ShapeList()  # object containing all shapes added by the user
    while True:
        # TODO: implement user interaction here. You can change the code below
        option = input("Select an option: ")
        if option == "1":
            # Add new shape
            pass
        elif option == "2":
            # Show all shapes
            pass
        elif option == "3":
            # Show shape with the largest perimeter
            pass
        elif option == "4":
            # Show shape with the largest area
            pass
        elif option == "5":
            # Show formulas
            pass
        elif option == "0":
            sys.exit()

if __name__ == "__main__":
    main()
