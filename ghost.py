import arcade
import random
import time
import arcade

TILE_SIZE = 32

class Ghost(arcade.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.direction_change_to_time = 0

        # sprite properties
        self.texture = arcade.make_circle_texture(TILE_SIZE - 2, arcade.color.RED)
        self.change_x = x
        self.change_y = y
        self.width = self.texture.width
        self.height = self.texture.height

    def pick_new_direction(self):

        kivoonim = [(0, 1), (0, 1), (1, 0), (1, 0), (1, 1)]
        random_index = random.randint(0, len(kivoonim))
        self.change_x = kivoonim[random_index][0]
        self.change_y = kivoonim[random_index][1]
        self.direction_change_to_time = random.uniform(0.3, 1.0)

    def update(self, deltat_time):
        while self.direction_change_to_time > 0:
            time.sleep(deltat_time)
            self.direction_change_to_time -= deltat_time
        self.pick_new_direction()

        self.center_x = self.change_x * self.speed
        self.center_y = self.change_y * self.speed
