import math

class Shape:
    """
    This is a abstract class representing geometrical shape.
    """

    def __init__(self):
        """
        Constructs Shape object

        Raises:
            ValueError: If any of the parameters is below 0.
        """
        pass

    def get_area(self):
        """
        Calculates shape's area.

        Returns:
            float: area of the shape
        """
        pass

    def get_perimeter(self):
        """
        Calculates shape's perimeter.

        Returns:
            float: perimeter of the shape
        """
        pass

    def __str__(self):
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

    area_formula = 'pi * r^2'
    perimeter_formula = '2 * pi * r'

    def __init__(self, r):
        """
        Constructs Circle object

        Raises:
            ValueError: If any of the parameters is below 0.
        """
        if not float(r) or float(r) < 0:
            raise ValueError('Radius has to be a number greater than 0')
        self.r = float(r)


    def get_area(self):
        """
        Calculates Circle area.

        Returns:
            float: area of the shape
        """
        area = math.pi * self.r**2

        return area

    def get_perimeter(self):
        """
        Calculates circle perimeter.

        Returns:
            float: perimeter of the shape
        """
        perimeter = 2 * math.pi * self.r
        return perimeter

    def __str__(self):
        """
        Returns information about the circle as string.

        Returns:
            str: information bout shape
        """
        return 'Circle: r = {}'.format(self.r)

    @classmethod
    def get_area_formula(cls):
        """
        Returns formula for the area of the shape as a string.

        Returns:
            str: area formula
        """
        return cls.area_formula

    @classmethod
    def get_perimeter_formula(cls):
        """
        Returns formula for the perimeter of the shape as a string.

        Returns:
            str: perimeter formula
        """
        return cls.perimeter_formula



class Triangle(Shape):

    area_formula = 'sqrt*(s*(s-a)*(s-b)*(s-c))   where: s = (a+b+c)/2'
    perimeter_formula = 'a + b + c'

    def __init__(self, a, b, c):
        """
        Constructs triangle object

        Raises:
            ValueError: If any of the parameters is below 0.
        """
        for parameter in [a, b, c]:
            if not float(parameter) or float(parameter) < 0:
                raise ValueError('Sides length have to be a number greater than 0')
            self.a = float(a)
            self.b = float(b)
            self.c = float(c)
        if not a + b > c and not a + c > b and not b + c > a :
            raise ValueError('Remember! To create a triangle the sum of the two sides have to be greater than the third')


    def get_area(self):
        """
        Calculates triangle area.

        Returns:
            float: area of the triangle
        """
        s = (self.a + self.b + self.c) / 2

        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))

    def get_perimeter(self):
        """
        Calculates triangle perimeter.

        Returns:
            float: perimeter of the triangle
        """
        return self.a + self.b + self.c

    def __str__(self):
        """
        Returns information about the triangle as string.

        Returns:
            str: information bout triangle
        """
        return 'Triangle: a = {}, b = {}, c = {}'.format(self.a, self.b, self.c)

    @classmethod
    def get_area_formula(cls):
        """
        Returns formula for the area of the shape as a string.

        Returns:
            str: area formula
        """
        return cls.area_formula

    @classmethod
    def get_perimeter_formula(cls):
        """
        Returns formula for the perimeter of the shape as a string.

        Returns:
            str: perimeter formula
        """
        return cls.perimeter_formula


class EquilateralTriangle(Triangle):

    def __init__(self, a):
        """
        Constructs triangle object

        Raises:
            ValueError: If any of the parameters is below 0.
        """
        Triangle.__init__(self, a, a, a)



class Rectangle(Shape):

    area_formula = 'a * b'
    perimeter_formula = '2a + 2b'

    def __init__(self, a, b):
        """
        Constructs rectangle object

        Raises:
            ValueError: If any of the parameters is below 0.
        """
        for parameter in [a, b]:
            if not float(parameter) or float(parameter) < 0:
                raise ValueError('Sides length have to be a number greater than 0')
        self.a = float(a)
        self.b = float(b)


    def get_area(self):
        """
        Calculates rectangle area.

        Returns:
            float: area of the triangle
        """
        return self.a * self.b

    def get_perimeter(self):
        """
        Calculates rectangle perimeter.

        Returns:
            float: perimeter of the triangle
        """
        return 2 * self.a + 2 * self.b

    def __str__(self):
        """
        Returns information about the rectangle as string.

        Returns:
            str: information bout triangle
        """
        return 'Rectangle: a = {}, b = {}'.format(self.a, self.b)

    @classmethod
    def get_area_formula(cls):
        """
        Returns formula for the area of the rectangle as a string.

        Returns:
            str: area formula
        """
        return cls.area_formula

    @classmethod
    def get_perimeter_formula(cls):
        """
        Returns formula for the perimeter of the rectangle as a string.

        Returns:
            str: perimeter formula
        """
        return cls.perimeter_formula


class Square(Rectangle):

    area_formula = 'a^2'
    perimeter_formula = '4a'

    def __init__(self, a):
        """
        Constructs triangle object

        Raises:
            ValueError: If any of the parameters is below 0.
        """
        Rectangle.__init__(self, a, a)

    def __str__(self):
        """
        Returns information about the shape as string.
        Returns:
            str: information about shape
        """
        return 'Square, a = {}'.format(self.a)

    @classmethod
    def get_area_formula(cls):
        """
        Returns formula for the area of the shape as a string.
        Returns:
            str: area formula
        """
        return cls.area_formula

    @classmethod
    def get_perimeter_formula(cls):
        """
        Returns formula for the perimeter of the shape as a string.
        Returns:
            str: perimeter formula
        """
        return cls.perimeter_formula


class RegularPentagon(Shape):

    area_formula = '(a^2*sqrt(5(5+2sqrt(5))))/4'
    perimeter_formula = '5a'

    def __init__(self, a):
        """
        Constructs RegularPentagon object

        Raises:
            ValueError: If any of the parameters is below 0.
        """
        if not float(a) or float(a) < 0:
            raise ValueError('Sides length have to be a number greater than 0')
        self.a = float(a)

    def get_area(self):
        """
        Calculates rectangle area.

        Returns:
            float: area of the triangle
        """
        return (self.a**2 * math.sqrt(5 * (5 + 2 * math.sqrt(5)))) / 4

    def get_perimeter(self):
        """
        Calculates rectangle perimeter.

        Returns:
            float: perimeter of the triangle
        """
        return 5 * self.a

    def __str__(self):
        """
        Returns information about the rectangle as string.

        Returns:
            str: information bout triangle
        """
        return 'Regular Pentagon: a = {}'.format(self.a)

    @classmethod
    def get_area_formula(cls):
        """
        Returns formula for the area of the rectangle as a string.

        Returns:
            str: area formula
        """
        return cls.area_formula

    @classmethod
    def get_perimeter_formula(cls):
        """
        Returns formula for the perimeter of the rectangle as a string.

        Returns:
            str: perimeter formula
        """
        return cls.perimeter_formula


class ShapeList:

    def __init__(self, shapes=None):
        if shapes is None:
            shapes = []
        if type(shapes) != list:
            raise TypeError('Should be list')
        self.shapes = shapes

    def add_shape(self, shape):
        if isinstance(shape, Shape):
            self.shapes.append(shape)
        else:
            raise TypeError('{} has not Shape class as it\'s ancestor.'.format(shape))

    def get_shapes_table(self):
        title_list = ['idx', 'Class', '__str__', 'Perimeter', 'Formula', 'Area', 'Formula']
        column_width = list()
        new_table = ''
        table = []

        for i, shape in enumerate(self.shapes):
            table.append([str(i+1), str(shape.__class__.__name__), shape.__str__(), str(round(shape.get_perimeter(), 2)),
                         str(shape.get_perimeter_formula()), str(round(shape.get_area(), 2)), str(shape.get_area_formula())])

        for i, title in enumerate(title_list):
            column_width.append(len(title))

        for items in table:
            for i, item in enumerate(items):
                try:
                    if column_width[i] < len(str(item)):
                        column_width[i] = len(str(item))
                except:
                    column_width.append(len(str(item)))

        table_size = 1
        for dash in column_width:
            table_size += (dash + 3)

        new_table += '-' * table_size + '\n'

        for iterator, title in enumerate(title_list):
            if iterator == 0:
                new_table += '|'
            new_table += ' {:{width}} |'.format(title, width=column_width[iterator])

        new_table += '\n' + '-' * table_size + '\n'

        for items in table:
            for iterator, item in enumerate(items):
                if iterator == 0:
                    new_table += '|'
                new_table += ' {:{width}} |'.format(item, width=column_width[iterator])
            new_table += '\n'

        new_table += '-' * table_size
        return new_table

    def get_largest_shape_by_perimeter(self):
        """Returns shape with largest perimeter or None if there is no list."""
        if len(self.shapes) == 0:
            return None

        largest_by_perimeter = self.shapes[0]
        for shape in self.shapes:
            if shape.get_perimeter() > largest_by_perimeter.get_perimeter():
                largest_by_perimeter = shape
        return largest_by_perimeter

    def get_largest_shape_by_area(self):
        """Returns shape with largest area or None if there is no list. """
        if len(self.shapes) == 0:
            return None

        largest_by_area = self.shapes[0]
        for shape in self.shapes:
            if shape.get_area() > largest_by_area.get_area():
                largest_by_area = shape
        return largest_by_area