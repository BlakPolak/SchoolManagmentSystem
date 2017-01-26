class Attendance:
    """
    This class create object attendance.

    Args: student: stories student object
          date: stories current date
          was_present: stories information about student presence

    """
    def __init__(self, student, date, was_present):
        """
        Initialize object args
            Args:
                student: stories student object
                date: stories current date
                was_present: stories information about student presence
            Returns:
                None
        """
        self.student = student
        self.date = date
        self.was_present = was_present
