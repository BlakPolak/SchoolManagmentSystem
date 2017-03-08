class Assignment:
    """
    This class creates object assignment.

    Args: name: stories assignment title
          max_points: int
          delivery_date: stories date of delivery
          content: stories content of assignment
    """
    def __init__(self, name, max_points, delivery_date, type, content):
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
        self.name = name
        self.max_points = max_points
        self.delivery_date = delivery_date
        self.type = type
        self.content = content

    def __str__(self):
        """Conversion to string"""
        return self.name+"\t"+self.max_points+"\t"+self.delivery_date+"\t"+self.content
