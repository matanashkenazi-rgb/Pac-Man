import arcade

from coin import Coin
from ghost import Ghost
from wall import Wall
from player import Pacman

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Pacman - Arcade"
TILE_SIZE = 32


with open("map.txt", "r") as mapFile:
    strMap = mapFile.read()
    LEVEL_MAP = strMap.split("\n")

class PacmanGame(arcade.View):
    def __init__(self):
        super().__init__()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.ghost_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.player = None
        self.game_over = False
        self.start_x = 0
        self.start_y = 0

    def setup(self):

        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.ghost_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.game_over = False

        for row_idx, row in enumerate(LEVEL_MAP):
            for col_idx, cell in enumerate(row):
                x = col_idx * TILE_SIZE + TILE_SIZE / 2
                y = (len(LEVEL_MAP) - row_idx - 1) * TILE_SIZE + TILE_SIZE / 2

                if cell == "#":
                    self.wall_list.append(Wall(x, y))
                elif cell == ".":
                    self.coin_list.append(Coin(x, y))
                elif cell == "G":
                    self.ghost_list.append(Ghost(x, y))
                    self.coin_list.append(Coin(x, y))
                elif cell == "P":
                    self.start_x = x
                    self.start_y = y
                    self.player = Pacman(x, y)
                    self.player_list.append(self.player)

    def on_draw(self):
        self.clear()
        self.wall_list.draw()
        self.coin_list.draw()
        self.ghost_list.draw()
        self.player_list.draw()
        arcade.draw_text(f"score: {self.player.score}, lives: {self.player.lives}", TILE_SIZE, WINDOW_HEIGHT - TILE_SIZE)
        if self.game_over:
           arcade.draw_text(f"Game over. tap space to restart. ", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

    def on_update(self, delta_time):

        player = self.player_list[0]
        if player.lives == 0:
            self.game_over = True
            return

        # check collision with ghost and walls
        old_x = self.player.center_x
        old_y = self.player.center_y

        self.player.move()

        if player.collides_with_list(self.wall_list):
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
        coins = arcade.check_for_collision_with_list(self.player, self.coin_list)
        for coin in coins:
            self.player.score += coin.value
            coin.remove_from_sprite_lists()


        # 5. check collision with player and ghost.
        if player.collides_with_list(self.ghost_list):
            self.player.center_x = self.start_x
            self.player.center_y = self.start_y
            player.lives -= 1

    def on_key_press(self, key, modifiers):
        if self.game_over and key == arcade.key.SPACE:
            self.setup()

        # Move
        player = self.player_list[0]

        if key == arcade.key.UP:
            player.change_y = 1
        elif key == arcade.key.DOWN:
            player.change_y = -1
        elif key == arcade.key.RIGHT:
            player.change_x = 1
        elif key == arcade.key.LEFT:
            player.change_x = -1

    def on_key_release(self, key, modifiers):
        player = self.player_list[0]
        if key == arcade.key.UP or key == arcade.key.DOWN:
            player.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            player.change_x = 0