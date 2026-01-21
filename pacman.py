import arcade

TILE_SIZE = 32

class Pacman(arcade.Sprite):

    def __init__(self, x, y):

        super().__init__()
        self.lives = 3
        self.score = 0

        # sprite properties
        self.texture = arcade.make_circle_texture(TILE_SIZE - 2, arcade.color.YELLOW)
        self.change_x = x
        self.change_y = y
        self.width = self.texture.width
        self.height = self.texture.height

    def move(self):
        self.center_x = self.change_y * self.speed
        self.center_y = self.change_y * self.speed