import arcade
import time
from wall import Wall
from coin import Coin
from coin import SpecialCoin
from ghost import Ghost
from pacman import Pacman

with open("map.txt", "r") as map_file:
    game_map = map_file.read()
    LEVEL_MAP = game_map.split("\n")

with open("general.txt", "r") as general_file:
    general_data = general_file.read()
    data = general_data.split("\n")
    TILE_SIZE = int(data[1])
    WINDOW_WIDTH = int(data[3])
    WINDOW_HEIGHT = int(data[5])

class PacmanGame(arcade.View):
    def __init__(self):
        super().__init__()
        self.power_up_active = False
        self.power_up_end_time = 0
        self.special_coin_list = arcade.SpriteList()
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
        self.power_up_active = False
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.special_coin_list = arcade.SpriteList()  # אתחול מחדש של הרשימה
        self.ghost_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.game_over = False
        for row_idx, row in enumerate(LEVEL_MAP):
            for col_idx, cell in enumerate(row):
                x = col_idx * TILE_SIZE + TILE_SIZE / 2
                y = (len(LEVEL_MAP) - row_idx - 1) * TILE_SIZE + TILE_SIZE / 2

                if LEVEL_MAP[row_idx][col_idx] == "#":
                    self.wall_list.append(Wall(x, y))
                if LEVEL_MAP[row_idx][col_idx] == ".":
                    self.coin_list.append(Coin(x, y))
                if LEVEL_MAP[row_idx][col_idx] == "S":
                    self.special_coin_list.append(SpecialCoin(x, y))  # הוספת מטבע מיוחד
                if LEVEL_MAP[row_idx][col_idx] == "P":
                    self.player = Pacman(x, y)
                    self.start_x = x
                    self.start_y = y
                    self.player_list.append(self.player)
                if LEVEL_MAP[row_idx][col_idx] == "G":
                    self.ghost_list.append(Ghost(x, y))

    def on_draw(self):
        self.clear()
        arcade.set_background_color(arcade.color.BLACK)
        self.special_coin_list.draw()  
        self.wall_list.draw()
        self.coin_list.draw()
        self.ghost_list.draw()
        self.player_list.draw()

        arcade.draw_text(f"score: {self.player.score}", TILE_SIZE, WINDOW_HEIGHT - 20, arcade.color.WHITE)
        arcade.draw_text(f"lives: {self.player.lives}", TILE_SIZE, WINDOW_HEIGHT - 60, arcade.color.WHITE)
        if self.power_up_active:
            arcade.draw_text("POWER UP!", TILE_SIZE, WINDOW_HEIGHT - 100, arcade.color.GREEN)
            arcade.draw_text(f"Time left: {int(self.power_up_end_time - time.time())}s", TILE_SIZE, WINDOW_HEIGHT - 140, arcade.color.GREEN)
        if self.game_over == True:
            arcade.draw_text("GAME OVER", WINDOW_WIDTH / 2, WINDOW_HEIGHT -100, arcade.color.RED)
        if self.player.score == len(self.coin_list) + self.player.score:
            self.game_over = True
            arcade.draw_text("YOU WIN!", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, arcade.color.GREEN)

    def on_update(self, delta_time):
        if self.game_over:
            return

        if self.power_up_active and time.time() > self.power_up_end_time:
            self.power_up_active = False

        # player movement and collision
        temporary_x = self.player.center_x
        temporary_y = self.player.center_y
        self.player.move()
        self.player_list.update()

        # wall collision
        if arcade.check_for_collision_with_list(self.player, self.wall_list):
            self.player.center_x = temporary_x
            self.player.center_y = temporary_y

        # special coin collision
        special_coins_hit = arcade.check_for_collision_with_list(self.player, self.special_coin_list)
        if len(special_coins_hit) > 0:
            self.power_up_active = True
            self.power_up_end_time = time.time() + 5
            for coin in special_coins_hit:
                coin.remove_from_sprite_lists()

        # coin collision
        coins_hit = arcade.check_for_collision_with_list(self.player, self.coin_list)
        if len(coins_hit) > 0:
            self.player.score += len(coins_hit)
        for coin in coins_hit:
            coin.remove_from_sprite_lists()

        # ghost collision
        ghosts_hit = arcade.check_for_collision_with_list(self.player, self.ghost_list)
        if len(ghosts_hit) > 0:
            if self.power_up_active:  # אם הכוח פעיל, הרג את הרוחות
                for ghost in ghosts_hit:
                    ghost.remove_from_sprite_lists()
            else:
                self.player.lives -= 1
                self.player.center_x = self.start_x
                self.player.center_y = self.start_y
        if self.player.lives <= 0:
            self.game_over = True

        # ghost movement
        for ghost in self.ghost_list:
            temp_x = ghost.center_x
            temp_y = ghost.center_y
            ghost.update()

            # wall collision
            if arcade.check_for_collision_with_list(ghost, self.wall_list):
                ghost.center_x = temp_x
                ghost.center_y = temp_y

    def on_key_press(self, key, modifiers):
        if self.game_over and key == arcade.key.SPACE:
            self.setup()
            self.player.lives = 3
            self.player.score = 0
        if key == arcade.key.UP:
            self.player.change_y = 1
            self.player.change_x = 0
        if key == arcade.key.DOWN:
            self.player.change_y = -1
            self.player.change_x = 0
        if key == arcade.key.LEFT:
            self.player.change_x = -1
            self.player.change_y = 0
        if key == arcade.key.RIGHT:
            self.player.change_x = 1
            self.player.change_y = 0

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.change_y = 0
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0