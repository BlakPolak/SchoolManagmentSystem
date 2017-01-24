import unittest
import math
from geometry import *


class CircleTester(unittest.TestCase):

    def test_constructor(self):
        c = Circle(3)
        self.assertEqual(c.r, 3, "Wrong radius")

    def test_value_error(self):
        with self.assertRaises(ValueError,
                               msg="Circle cannot have negative radius"):
            Circle(-1)

    def test_area(self):
        r = 3
        c = Circle(r)
        area = math.pi * r ** 2
        self.assertEqual(c.get_area(), area)

    def test_perimeter(self):
        r = 3
        c = Circle(r)
        perimeter = 2 * math.pi * r
        self.assertEqual(c.get_perimeter(), perimeter)


class TriangleTester(unittest.TestCase):

    def test_constructor(self):
        t = Triangle(2, 4, 5)
        self.assertEqual((t.a, t.b, t.c), (2, 4, 5))

    def test_value_error(self):
        with self.assertRaises(ValueError):
            Triangle(-1, 1, 1)

    def test_area(self):
        a = 2
        b = 4
        c = 5
        t = Triangle(a, b, c)
        s = (a+b+c)/2
        area = math.sqrt(s*(s-a)*(s-b)*(s-c))
        self.assertEqual(t.get_area(), area)

    def test_perimeter(self):
        a = 2
        b = 4
        c = 5
        t = Triangle(a, b, c)
        perimeter = a + b + c
        self.assertEqual(t.get_perimeter(), perimeter)


class EquilateralTriangleTester(unittest.TestCase):

    def test_constructor(self):
        t = EquilateralTriangle(2)
        self.assertEqual((t.a, t.b, t.c), (2, 2, 2))

    def test_value_error(self):
        with self.assertRaises(ValueError):
            EquilateralTriangle(-1)

    def test_area(self):
        a = b = c = 2
        t = EquilateralTriangle(a)
        s = (a+b+c)/2
        area = math.sqrt(s*(s-a)*(s-b)*(s-c))
        self.assertEqual(t.get_area(), area)

    def test_perimeter(self):
        a = 2
        t = EquilateralTriangle(a)
        perimeter = 3*a
        self.assertEqual(t.get_perimeter(), perimeter)


class RectangleTester(unittest.TestCase):

    def test_constructor(self):
        r = Rectangle(2, 3)
        self.assertEqual((r.a, r.b), (2, 3))

    def test_value_error(self):
        with self.assertRaises(ValueError):
            Rectangle(-1, 1)

    def test_area(self):
        a = 2
        b = 3
        r = Rectangle(a, b)
        area = a * b
        self.assertEqual(r.get_area(), area)

    def test_perimeter(self):
        a = 2
        b = 3
        r = Rectangle(a, b)
        perimeter = 2*a + 2*b
        self.assertEqual(r.get_perimeter(), perimeter)


class SquareTester(unittest.TestCase):

    def test_constructor(self):
        s = Square(2)
        self.assertEqual((s.a, s.b), (2, 2))

    def test_value_error(self):
        with self.assertRaises(ValueError):
            Square(-1)
            Square(-90)

    def test_area(self):
        a = 2
        s = Square(a)
        area = a**2
        self.assertEqual(s.get_area(), area)

    def test_perimeter(self):
        a = 2
        s = Square(a)
        perimeter = a*4
        self.assertEqual(s.get_perimeter(), perimeter)


class RegularPentagonTester(unittest.TestCase):

    def test_constructor(self):
        p = RegularPentagon(2)
        self.assertEqual(p.a, 2)

    def test_value_error(self):
        with self.assertRaises(ValueError):
            RegularPentagon(-1)
            RegularPentagon(-90)

    def test_area(self):
        a = 2
        p = RegularPentagon(a)
        area = a**2 * math.sqrt(5*(5+2*math.sqrt(5)))/4
        self.assertEqual(p.get_area(), area)

    def test_perimeter(self):
        a = 2
        p = RegularPentagon(a)
        perimeter = 5*a
        self.assertEqual(p.get_perimeter(), perimeter)


class ShapeListTester(unittest.TestCase):

    def test_constructor(self):
        sl = ShapeList()
        self.assertIsInstance(sl.shapes, list)

    def test_add_shape(self):
        sl = ShapeList()
        c = Circle(2)
        sl.add_shape(c)
        self.assertEqual(sl.shapes[0], c)

    def test_type_error(self):
        sl = ShapeList()
        with self.assertRaises(TypeError, msg="Test dupy się nie powiódł ;("):
            sl.add_shape("dupa")

    def test_shapes_table(self):
        sl = ShapeList()
        s = Square(4)
        sl.add_shape(s)
        self.assertIsInstance(sl.get_shapes_table(), str)

    def test_largest_perimeter(self):
        sl = ShapeList()
        p = RegularPentagon(3)
        s = Square(5)
        t = Triangle(2, 4, 5)
        c = Circle(3)
        sl.add_shape(p)
        sl.add_shape(s)
        sl.add_shape(t)
        sl.add_shape(c)
        self.assertEqual(sl.get_largest_shape_by_perimeter(), s)

    def test_largest_area(self):
        sl = ShapeList()
        p = RegularPentagon(3)
        s = Square(5)
        t = Triangle(2, 4, 5)
        c = Circle(3)
        sl.add_shape(p)
        sl.add_shape(s)
        sl.add_shape(t)
        sl.add_shape(c)
        self.assertEqual(sl.get_largest_shape_by_area(), c)


def main():
    unittest.main(verbosity=2)

if __name__ == '__main__':
    main()
