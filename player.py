from charachter import Character

class Player(Character):
    """פקמן – השחקן."""

    def __init__(self, x, y):
        super().__init__(speed=2.5, x=x, y=y)

        self.lives = 3
        self.score = 0

    def move(self):
        self.center_x += self.change_x * self.speed
        self.center_y += self.change_y * self.speed
