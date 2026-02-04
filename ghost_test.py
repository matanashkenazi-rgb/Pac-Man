import arcade

class Ghost(arcade.Sprite):
    """Pac-Man-style ghost drawn directly, dynamic color."""

    def __init__(self, x, y, color=arcade.color.RED):
        super().__init__()
        self.center_x = x
        self.center_y = y
        self.width = 40
        self.height = 40
        self.color = color

    def draw(self):
        w = self.width
        h = self.height
        x = self.center_x
        y = self.center_y

        # Ghost body (ellipse)
        arcade.draw_ellipse_filled(x, y, w, h*0.8, self.color)

        # Feet (3 triangles)
        foot_width = w / 5
        for i in range(3):
            fx = x - w/2 + foot_width/2 + i * foot_width * 2
            arcade.draw_triangle_filled(
                fx, y - h*0.4,
                fx + foot_width, y - h*0.4,
                fx + foot_width/2, y - h*0.25,
                self.color
            )

        # Eyes
        eye_radius = w*0.1
        eye_offset_x = w*0.15
        eye_y = y + h*0.1
        arcade.draw_circle_filled(x - eye_offset_x, eye_y, eye_radius, arcade.color.WHITE)
        arcade.draw_circle_filled(x + eye_offset_x, eye_y, eye_radius, arcade.color.WHITE)

        # Pupils
        pupil_radius = eye_radius / 2
        arcade.draw_circle_filled(x - eye_offset_x, eye_y, pupil_radius, arcade.color.BLUE)
        arcade.draw_circle_filled(x + eye_offset_x, eye_y, pupil_radius, arcade.color.BLUE)


# ------------------ Test ------------------

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(400, 400, "Pac-Man Ghost Example")
        arcade.set_background_color(arcade.color.BLACK)
        self.ghost_list = []

        # Create ghosts of different colors
        self.ghost_list.append(Ghost(100, 200, arcade.color.RED))
        self.ghost_list.append(Ghost(200, 200, arcade.color.PINK))
        self.ghost_list.append(Ghost(300, 200, arcade.color.CYAN))
        self.ghost_list.append(Ghost(150, 100, arcade.color.ORANGE))

    def on_draw(self):
        arcade.start_render()  # Only here
        for ghost in self.ghost_list:
            ghost.draw()


if __name__ == "__main__":
    game = MyGame()
    arcade.run()
