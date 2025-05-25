class Agent:
    def __init__(self, id, role, x, y, health = 80, stamina=100, speed=1.0):
        self.id = id
        self.role = role
        self.x = x
        self.y = y
        self.state = 'Idle'
        self.health = health
        self.stamina = stamina
        self.speed = speed
        self.task = None
