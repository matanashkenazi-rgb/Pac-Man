import arcade


class Coin(arcade.Sprite):
    """מטבע לאיסוף."""

    def __init__(self, x, y):
        super().__init__()
        self.texture = arcade.make_circle_texture(10, arcade.color.YELLOW)
        self.width = self.texture.width
        self.height = self.texture.height
        self.center_x = x
        self.center_y = y
        self.value = 10