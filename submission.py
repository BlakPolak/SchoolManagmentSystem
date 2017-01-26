import ui
import datetime


class Submission:

    def __init__(self, assignment, student, submission_date="", result="", grade=""):
        self.result = result
        self.grade = grade
        self.submission_date = datetime.date.today()
        self.assignment = assignment
        self.student = student

    def __str__(self):
        return self.assignment.name+"\t"+self.grade+"\t"+self.result

    def provide_result(self):
        options = ui.Ui.get_inputs(["->"], "Write your assignment solution")
        self.result = options[0]