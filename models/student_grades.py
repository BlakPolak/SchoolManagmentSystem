class StudentGrades:
    """ Class creates Student Grades object """
    def __init__(self, name, surname, number_of_grades, average_grade):
        """
        Initialize object args
        Args:
                name: str
                surname: str
                number_of_grades: number (int)
                number_of_grades: number (int)
                average_grade : number (int)
        Returns: None
        """
        self.name = name
        self.surname = surname
        self.number_of_grades = number_of_grades
        self.average_grade = average_grade
