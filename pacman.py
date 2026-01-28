import arcade

class Pacman(arcade.Sprite):
    """פקמן – השחקן."""

    def __init__(self, x, y):
        super().__init__()
        self.texture = arcade.make_circle_texture(30, arcade.color.YELLOW)
        self.width = self.texture.width
        self.height = self.texture.height
        self.center_x = x
        self.center_y = y

        self.lives = 3
        self.score = 0

    def move(self):
        self.center_x += self.change_x * self.speed
        self.center_y += self.change_y * self.speed
