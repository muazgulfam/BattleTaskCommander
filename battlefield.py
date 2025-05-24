class Battlefield:
    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        self.grid = [['.' for _ in range(width)] for _ in range(height)]

    def place_entity(self, x, y, entity):
        self.grid[y][x] = 'A' if hasattr(entity, 'health') else 'T'

    def display(self):
        print("Battlefield Grid:")
        for row in self.grid:
            print(' '.join(row))
