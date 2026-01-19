class Character:
    """מחלקת בסיס לדמויות (פקמן, רוחות)."""

    def __init__(self, speed, x, y):
        self.speed = speed

        self.center_x = x
        self.center_y = y

        self.change_x = 0
        self.change_y = 0