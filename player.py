import arcade

TILE_SIZE = 32

class Pacman(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.texture = arcade.make_circle_texture(30, arcade.color.YELLOW)
        self.center_x = x
        self.center_y = y
        self.change_x = 0
        self.change_y = 0
        self.speed = 2
        self.score = 0
        self.lives = 3

    def move(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
