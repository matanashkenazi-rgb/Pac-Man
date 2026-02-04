import arcade
import random

class Ghost(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.texture = arcade.make_circle_texture(30, arcade.color.RED)
        self.center_x = x
        self.center_y = y
        self.speed = 1
        self.change_x = 0
        self.change_y = 0
        self.time_left = 0

    def pick_new_direction(self):
        directions = [(1,0), (-1,0), (0,1), (0,-1)]
        self.change_x, self.change_y = random.choice(directions)
        self.time_left = random.uniform(0.5, 1.5)

    def update(self, delta_time):
        self.time_left -= delta_time
        if self.time_left <= 0:
            self.pick_new_direction()

        self.center_x += self.change_x * self.speed
        self.center_y += self.change_y * self.speed
