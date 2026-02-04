import arcade

class Coin(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.value = 10
        self.texture = arcade.make_circle_texture(8, arcade.color.YELLOW)
        self.center_x = x
        self.center_y = y
