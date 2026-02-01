import arcade

from coin import Coin
from ghost import Ghost
from wall import Wall
from player import Pacman

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
                    self.player = Pacman(x, y)
                    self.player_list.append(self.player)

                # if it is a wall
                elif cell == "#":
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

    def on_update(self, delta_time):

        if self.game_over:
            return

        # check collision with player and walls
        old_x = self.player.center_x
        old_y = self.player.center_y

        self.player.update(delta_time)

        if arcade.check_for_collision_with_list(self.player, self.wall_list):
            self.player.center_x = old_x
            self.player.center_y = old_y

        # check collision with ghost and walls
        for ghost in self.ghost_list:
            old_x = ghost.center_x
            old_y = ghost.center_y

            ghost.update(delta_time)
            if ghost.collides_with_list(self.wall_list):
                ghost.center_x = old_x
                ghost.center_y = old_y

        # 4. check collision with player and coins
        coins_to_remove = arcade.check_for_collision_with_list(self.player, self.coin_list)

        for coin in coins_to_remove:
            coin.remove_from_sprite_lists()
            self.player.score += coin.value

        # 5. check collision with player and ghost.
        for ghost in self.ghost_list:
            old_x = ghost.center_x
            old_y = ghost.center_y

            if arcade.check_for_collision(self.player, ghost):
                ghost.center_x = old_x
                ghost.center_y = old_y
                self.player.lives -= 1

    def on_key_press(self, key, modifiers):

        if key == arcade.key.SPACE:
            self.setup()

        if key == arcade.key.UP:
            self.player.change_y = 1

        if key == arcade.key.DOWN:
            self.player.change_y = -1

        if key == arcade.key.LEFT:
            self.player.change_x = -1

        if key == arcade.key.RIGHT:
            self.player.change_x = 1

    def on_key_release(self, key, modifiers):

        if key in (arcade.key.UP, arcade.key.DOWN):
            self.player.change_y = 0

        if key in (arcade.key.LEFT, arcade.key.RIGHT):
            self.player.change_x = 0