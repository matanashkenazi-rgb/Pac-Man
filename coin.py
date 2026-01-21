import arcade

TILE_SIZE = 32

class Coin(arcade.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.value = 10

        # sprite properties
        self.texture = arcade.make_circle_texture(5, arcade.color.YELLOW)
        self.center_x = x
        self.center_y = y
        self.width = self.texture.width
        self.height = self.texture.height
