import arcade
from pacManGame import PacmanGame

TILE_SIZE = 32

def main():
    window = arcade.Window(800, 600, "Pacman")
    game = PacmanGame()
    game.setup()
    window.show_view(game)
    arcade.run()

if __name__ == "__main__":
    main()