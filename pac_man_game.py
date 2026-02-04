import random

import arcade
from wall import Wall
from coin import Coin
from ghost import Ghost
from pacman import Pacman

COLORS = [arcade.color.RED, arcade.color.GREEN, arcade.color.BLUE, arcade.color.ORANGE, arcade.color.PURPLE, arcade.color.PINK]
LEVEL_MAP = [
    "###########",
    "#P...#...G#",
    "#.###.#.#.#",
    "#...#.....#",
    "###.#.###.#",
    "#.........#",
    "#.###.###.#",
    "#G.......G#",
    "###########",
]

TILE_SIZE = 32
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

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
        self.game_over = False
        for row_idx, row in enumerate(LEVEL_MAP):
            for col_idx, cell in enumerate(row):
                x = col_idx * TILE_SIZE + TILE_SIZE / 2
                y = (len(LEVEL_MAP) - row_idx - 1) * TILE_SIZE + TILE_SIZE / 2

                if LEVEL_MAP[row_idx][col_idx] == "#":
                    self.wall_list.append(Wall(x,y))
                if LEVEL_MAP[row_idx][col_idx] == ".":
                    self.coin_list.append(Coin(x, y))
                if LEVEL_MAP[row_idx][col_idx] == "P":
                    self.start_x = x
                    self.start_y = y
                    self.player = Pacman(x,y)
                    self.player_list.append(self.player)
                if LEVEL_MAP[row_idx][col_idx] == "G":
                    self.ghost_list.append(Ghost(x,y, random.choice(COLORS)))
    def on_draw(self):

        self.clear()
        arcade.set_background_color(arcade.color.BLACK)

        self.wall_list.draw()
        self.coin_list.draw()
        self.ghost_list.draw()
        self.player_list.draw()

        arcade.draw_text(f"Score: {self.player.score}",TILE_SIZE, WINDOW_HEIGHT - 20, arcade.color.WHITE)
        arcade.draw_text(f"Lives: {self.player.lives}", TILE_SIZE, WINDOW_HEIGHT - 60,arcade.color.WHITE)

        if self.game_over:
            arcade.draw_text("GAME OVER", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, arcade.color.RED)


    def on_update(self, delta_time):
        if self.game_over:
            return

        #Pacman

        back_up_x = self.player.center_x
        back_up_y = self.player.center_y

        self.player.move()
        if self.player.collides_with_list(self.wall_list):
            self.player.center_x = back_up_x
            self.player.center_y = back_up_y

        #Ghosts
        for ghost in self.ghost_list:
            back_up_x = ghost.center_x
            back_up_y = ghost.center_y
            ghost.update(delta_time)
            if arcade.check_for_collision_with_list(ghost, self.wall_list):
                ghost.center_x = back_up_x
                ghost.center_y = back_up_y

        #Coins
        coins = arcade.check_for_collision_with_list(self.player, self.coin_list)
        for coin in coins:
            self.player.score += coin.value
            coin.remove_from_sprite_lists()

        #Hit Ghost
        if self.player.collides_with_list(self.ghost_list):
            self.player.lives-=1
            self.player.center_x = self.start_x
            self.player.center_y = self.start_y
            self.player.speed = 1

        #Check game over
        if self.player.lives == 0:
            self.game_over = True


    def on_key_press(self, key, modifiers):
        if self.game_over and key == arcade.key.SPACE:
            self.setup()
        #Move

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