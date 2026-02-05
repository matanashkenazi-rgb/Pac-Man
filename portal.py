import arcade

class Portal(arcade.Sprite):
    """PortalGate"""

    def __init__(self, x, y):
        super().__init__()
        self.texture = arcade.make_circle_texture(10, arcade.color.RED)
        self.width = self.texture.width
        self.height = self.texture.height
        self.center_x = x
        self.center_y = y

