class Assignment:
    def __init__(self, name, max_points, delivery_date, content):
        self.name = name
        self.max_points = max_points
        self.delivery_date = delivery_date
        self.content = content

    def __str__(self):
        return self.name+"\t"+self.max_points+"\t"+self.delivery_date+"\t"+self.content
