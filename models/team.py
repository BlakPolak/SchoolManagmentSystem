class Team:
    """ This class creates Team object. """
    def __init__(self, student_id, team_name, student_name, student_surname):
        """
        Initialize object args
        Args:
            student_id: number
            team_name: str
            student_name: str
            student_surname: str

        Returns: None
        """
        self.student_id = student_id
        self.team_name = team_name
        self.student_name = student_name
        self.student_surname = student_surname
