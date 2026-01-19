from character import Character

class Player(Character):

    def __init__(self, x, y):
        super().__init__(x, y, 100)
        self.score = 0
        self.lives = 3

    def move(self):
        self.center_x = self.x_change * self.speed
        self.center_y = self.y_change * self.speed
