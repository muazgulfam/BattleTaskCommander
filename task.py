class Task:
    def __init__(self, id, type, x, y, urgency = 5):
        self.id = id
        self.type = type
        self.x = x
        self.y = y
        self.urgency = urgency
        self.assigned = False
