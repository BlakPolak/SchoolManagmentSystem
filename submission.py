import ui
import datetime


class Submission:
    """
    This class creates submissions.
    """

    def __init__(self, assignment, student, submission_date="", result="", grade=""):
        """
        Initialize object args
        Args:   assignment: name of assignment(str)
                student: student it belongs to(str)
                submission_date: when it was submitted(str)
                result: the answer(str)
                grade: number (int)
        Returns: None
        """
        self.result = result
        self.grade = grade
        self.submission_date = datetime.date.today()
        self.assignment = assignment
        self.student = student

    def __str__(self):
        """
        Returns string with data.
        """
        return self.assignment.name+"\t"+self.grade+"\t"+self.result

    def provide_result(self):
        """
        Assigns the value to variable result.
        """
        options = ui.Ui.get_inputs(["->"], "Write your assignment solution: ")
        self.result = options[0]