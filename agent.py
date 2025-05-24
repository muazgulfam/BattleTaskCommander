class Agent:
    def __init__(self, id, role, x, y, health = 80):
        self.id = id
        self.role = role
        self.x = x
        self.y = y
        self.state = 'Idle'
        self.health = health
        self.energy = 100
        self.task = None
