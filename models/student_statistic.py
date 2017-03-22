class StudentStatistic:
    """ Class creates Student Statistics object """


    def __init__(self, id, student_name, student_surname, avg_days, grades_avg, yellow_cards, red_cards, green_cards):
        """
        Initialize object args
        Args:   id: number
                student_name: str
                student_surname: str
                avg_days: number (int)
                grades_avg: number (int)
                yellow_cards : number (int)
                red_cards: number (int)
        Returns: None
        """

        self.id = id
        self.student_name = student_name
        self.student_surname = student_surname
        self.avg_days = avg_days
        self.grades_avg = grades_avg
        self.yellow_cards = yellow_cards
        self.red_cards = red_cards
        self.green_cards = green_cards
