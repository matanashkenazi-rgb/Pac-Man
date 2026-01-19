from charachter import Character
import random

class Enemy(Character):
    """רוח שנעה בצורה רנדומלית."""

    def __init__(self, x, y):
        super().__init__(speed=2.0, x=x, y=y)

        # כל כמה זמן מחליפים כיוון
        self.time_to_change_direction = 0.0

    def pick_new_direction(self):
        """בחירת כיוון חדש רנדומלי."""
        directions = [
            (1, 0),   # ימין
            (-1, 0),  # שמאל
            (0, 1),   # למעלה
            (0, -1),  # למטה
            (0, 0),   # לעמוד
        ]
        self.change_x, self.change_y = random.choice(directions)
        self.time_to_change_direction = random.uniform(0.3, 1.0)

    def update(self, delta_time=1/60):
        """עדכון תנועת הרוח."""
        self.time_to_change_direction -= delta_time

        if self.time_to_change_direction <= 0:
            self.pick_new_direction()

        self.center_x += self.change_x * self.speed
        self.center_y += self.change_y * self.speed
