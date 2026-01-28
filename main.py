from pac_man_game import PacmanGame
import arcade

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

def main():



    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
    game = PacmanGame()
    game.setup()
    window.show_view(game)
    arcade.run()

if __name__ == "__main__":
    main()