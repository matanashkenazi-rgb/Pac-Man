import arcade

TILE_SIZE = 32

class Wall(arcade.Sprite):

    def __init__(self, center_x, center_y):
        super().__init__()
        
        # sprite properties
        self.texture = arcade.make_soft_square_texture(20, arcade.color.BLUE)
        self.center_x = center_x
        self.center_y = center_y
        self.width = self.texture.width
        self.height = self.texture.height