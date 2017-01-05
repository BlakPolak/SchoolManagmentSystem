class Shape:
    """
    This is a abstract class representing geometrical shape.
    """

    def get_area():
        """
        Calculates shape's area.

        Returns:
            float: area of the shape
        """
        pass

    def get_perimeter():
        """
        Calculates shape's perimeter.

        Returns:
            float: perimeter of the shape
        """
        pass

    def __str__():
        """
        Returns information about the shape as string.

        Returns:
            str: information bout shape
        """
        pass

    @classmethod
    def get_area_formula(cls):
        """
        Returns formula for the area of the shape as a string.

        Returns:
            str: area formula
        """
        pass

    @classmethod
    def get_perimeter_formula(cls):
        """
        Returns formula for the perimeter of the shape as a string.

        Returns:
            str: perimeter formula
        """
        pass

class Circle(Shape):
    pass

class Triangle(Shape):
    pass

class EquilateralTriangle(Triangle):
    pass

class Rectangle(Shape):
    pass

class Square(Rectangle):
    pass

class RegularPentagon(Shape):
    pass

class ShapeList:
    pass
