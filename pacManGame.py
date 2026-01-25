import arcade

from coin import Coin
from ghost import Ghost
from wall import Wall
from pacman import Pacman

# מפה לדוגמה: # = קיר, . = מטבע, P = פקמן, G = רוח, רווח = כלום

LEVEL_MAP = [
    "###########",
    "#P....G...#",
    "#.........#",
    "###########",
]

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Pacman - Arcade"
TILE_SIZE = 32

class PacmanGame(arcade.View):

    def __init__(self):
        super().__init__()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.ghost_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.player = None
        self.game_over = False
        self.background_color = arcade.color.BLACK
        self.start_x = 0
        self.start_y = 0

    def setup(self):

        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.ghost_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()

        for row_idx, row in enumerate(LEVEL_MAP):
            for col_idx, cell in enumerate(row):

                x = col_idx * TILE_SIZE + TILE_SIZE / 2
                y = (len(LEVEL_MAP) - row_idx - 1) * TILE_SIZE + TILE_SIZE / 2

                if cell == ".":
                    current_object = Coin(x, y)
                    self.coin_list.append(current_object)

                elif cell == "G":
                    current_object = Ghost(x, y)
                    self.ghost_list.append(current_object)

                elif cell == "P":
                    current_object = Pacman(x, y)
                    self.player_list.append(current_object)

                # if it is a wall
                else:
                    current_object = Wall(x, y)
                    self.wall_list.append(current_object)

    def on_draw(self):

        self.clear()
        arcade.set_background_color(arcade.color.BLACK)

        self.wall_list.draw()
        self.coin_list.draw()
        self.ghost_list.draw()
        self.player_list.draw()

        arcade.draw_text("Score: 0",TILE_SIZE, WINDOW_HEIGHT - 20, arcade.color.WHITE)
        arcade.draw_text("Lives: 3", TILE_SIZE, WINDOW_HEIGHT - 60,arcade.color.WHITE)

        if self.game_over:
            arcade.draw_text("GAME OVER", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, arcade.color.RED)