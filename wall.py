import arcade

class Wall(arcade.Sprite):
    """קיר – חוסם תנועה."""

    def __init__(self, x, y):

        super().__init__()
        self.texture = arcade.make_soft_square_texture(32, arcade.color.BLUE)
        self.width = self.texture.width
        self.height = self.texture.height
        self.lives = 3
        self.score = 0
        self.center_x = x
        self.center_y = y