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
                current_object = LEVEL_MAP[row_idx][col_idx]

                if current_object is Coin:
                    current_object = Coin(x, y)
                    self.coin_list.append(current_object)

                elif current_object is Ghost:
                    current_object = Ghost(x, y)
                    self.ghost_list.append(current_object)

                elif current_object is Pacman:
                    current_object = Pacman(x, y)
                    self.player_list.append(current_object)

                # if it is a wall
                else:
                    current_object = Wall(x, y)
                    self.wall_list.append(current_object)

    def on_draw(self):
        self.wall_list.draw()
        self.coin_list.draw()
        self.ghost_list.draw()
        self.player_list.draw()