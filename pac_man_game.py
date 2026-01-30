import arcade
from wall import Wall
from coin import Coin
from ghost import Ghost
from pacman import Pacman

LEVEL_MAP = [
    "###########",
    "#P....G...#",
    "#.........#",
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
        self.lives = 3
        self.speed = 2
        self.score = 0
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
                    self.player = Pacman(x,y)
                    self.start_x = x
                    self.start_y = y
                    self.player_list.append(self.player)
                if LEVEL_MAP[row_idx][col_idx] == "G":
                    self.ghost_list.append(Ghost(x,y))
    def on_draw(self):

        self.clear()
        arcade.set_background_color(arcade.color.BLACK)

        self.wall_list.draw()
        self.coin_list.draw()
        self.ghost_list.draw()
        self.player_list.draw()

        arcade.draw_text(f"score: {self.score}",TILE_SIZE, WINDOW_HEIGHT - 20, arcade.color.WHITE)
        arcade.draw_text(f"lives: {self.lives}", TILE_SIZE, WINDOW_HEIGHT - 60,arcade.color.WHITE)

        if self.game_over:
            arcade.draw_text("GAME OVER", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, arcade.color.RED)



    def on_update(self, delta_time):
        if self.game_over == True:
            return

        #player movment and collision
        temperary_x = self.player.center_x
        temperary_y = self.player.center_y
        self.player.move()
        self.player_list.update()
        
        #wall collision
        if arcade.check_for_collision_with_list(self.player, self.wall_list):
            self.player.center_x = temperary_x
            self.player.center_y = temperary_y
        
        for i in self.ghost_list:
            T_x = i.center_x
            T_y = i.center_y
            if arcade.check_for_collision_with_list(i, self.wall_list):
                i.center_x = T_x
                i.center_y = T_y
                
        #coin collision
        coins_hit = arcade.check_for_collision_with_list(self.player, self.coin_list)
        if len(coins_hit) > 0:
            self.score += len(coins_hit)
        for coin in coins_hit:
            coin.remove_from_sprite_lists()
            
        #ghost collision
        ghosts_hit = arcade.check_for_collision_with_list(self.player, self.ghost_list)
        if len(ghosts_hit) > 0:
            self.lives -= 1
            self.player.center_x = self.start_x
            self.player.center_y = self.start_y
        if self.lives <= 0:
            self.game_over = True
        
    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.setup()
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

