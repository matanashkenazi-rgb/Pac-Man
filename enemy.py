from character import Character
import random
import time

class Enemy(Character):

    def __init__(self, x, y):
        super().__init__(x, y, 100)
        self.direction_change_to_time = 0

    def pick_new_direction(self):

        kivoonim = [(0, 1), (0, 1), (1, 0), (1, 0), (1, 1)]
        random_index = random.randint(0, len(kivoonim))
        self.x_change = kivoonim[random_index][0]
        self.y_change = kivoonim[random_index][1]
        self.direction_change_to_time = random.uniform(0.3, 1.0)

    def update(self, deltat_time):
        while self.direction_change_to_time > 0:
            time.sleep(deltat_time)
            self.direction_change_to_time -= deltat_time
        self.pick_new_direction()

        self.center_x = self.x_change * self.speed
        self.center_y = self.y_change * self.speed
