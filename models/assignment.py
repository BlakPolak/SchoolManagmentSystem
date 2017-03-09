import sqlite3

class Assignment:
    """
    This class creates object assignment.

    Args: name: stories assignment title
          max_points: int
          delivery_date: stories date of delivery
          content: stories content of assignment
    """
    def __init__(self, id, name, type, max_points, delivery_date, content):
        """
        Initialize object args
            Args:
                name: stories assignment title
                max_points: int
                delivery_date: stories date of delivery
                content: stories content of assignment
            Returns:
                None
        """
        self.id = id
        self.name = name
        self.type = type
        self.max_points = max_points
        self.delivery_date = delivery_date
        self.content = content

    def __str__(self):
        """Conversion to string"""
        return self.name+"\t"+self.max_points+"\t"+self.delivery_date+"\t"+self.content


    def get_assignment_by_id(self, id):
        """
        Method returns list of all student submission

        Return:
            list not submitted assignment
        """

        data = sqlite3.connect("db/program.db")
        cursor = data.cursor()
        cursor.execute("SELECT * FROM Assignment WHERE ID='{}'".format(id))
        row = cursor.fetchone()
        assignment = Assignment(row[0], row[1], row[2], row[3], row[4], row[5])
        data.close()
        return assignment
